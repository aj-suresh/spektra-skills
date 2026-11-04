#!/usr/bin/env python3
"""Write ads, sitelinks, callouts, snippets and keywords into a copy of the Google Ads Copy Template.

Usage:
    fill_template.py --template Google_Ads_Copy_Template.xlsx --payload payload.json --out filled.xlsx
                     [--dry-run] [--force] [--overwrite]

Rows go into the first free rows from row 6. The fictional sample rows are cleared on every tab
that gets new content. Dropdowns, conditional formatting and formulas are left untouched, and the
cached Check values are refreshed so previews show the right status. The template file itself is
never modified. Payload schema: references/template-map.md.
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_copy
from xlsx_io import (FIRST_ROW, KEY_TO_SHEET, SHEETS, Workbook, input_cols, is_empty, is_sample,
                     read_lists, read_records, row_record, set_formula_cache, set_text)

SHEET_ORDER = ["keywords", "ads", "sitelinks", "callouts", "snippets"]


def plan_sheet(wb, sheet, recs):
    """Pick target rows and fill in ids. Returns (rows, sample_rows_to_clear, recs)."""
    spec, cells, last = SHEETS[sheet], wb.cells(sheet), wb.last_row(sheet)
    free, samples, ids = [], [], []
    for row in range(FIRST_ROW, last + 1):
        rec = row_record(cells, spec, row)
        if is_empty(rec):
            free.append(row)
        elif is_sample(rec):
            free.append(row)
            samples.append(row)
        else:
            ids.append(rec.get("id", ""))
    if len(recs) > len(free):
        sys.exit("%s has room for %d more rows but the payload has %d. Copy the last row down in "
                 "the template first, or split the run." % (sheet, len(free), len(recs)))
    prefix = spec["id_prefix"]
    recs = [dict(r) for r in recs]
    if prefix:
        taken = {i for i in ids if i}
        top = max([int(m.group(1)) for i in taken if (m := re.fullmatch(prefix + r"-(\d+)", i))] or [0])
        for r in recs:
            if not r.get("id"):
                top += 1
                r["id"] = "%s-%03d" % (prefix, top)
            if r["id"] in taken:
                sys.exit("%s id %s already exists in the template" % (sheet, r["id"]))
            taken.add(r["id"])
    rows = free[:len(recs)]
    return rows, [r for r in samples if r not in rows], recs


def write_sheet(wb, sheet, rows, clear_rows, recs, defaults):
    spec, last = SHEETS[sheet], wb.last_row(sheet)
    clean = {c: wb.style_of(sheet, c, last) for c in input_cols(spec)}
    xml = wb.xml(sheet)
    for row, rec in zip(rows, recs):
        for key, col in spec["scalars"].items():
            val = rec.get(key, defaults.get(key, "Draft" if key == "status" else ""))
            xml = set_text(xml, "%s%d" % (col, row), val, clean[col])
        for key, cs in spec["lists"].items():
            vals = rec.get(key, [])
            for i, col in enumerate(cs):
                xml = set_text(xml, "%s%d" % (col, row), vals[i] if i < len(vals) else "", clean[col])
    for row in clear_rows:
        for col in input_cols(spec):
            xml = set_text(xml, "%s%d" % (col, row), "", clean[col])
    wb.set_xml(sheet, xml)


def refresh_caches(wb, sheets):
    ads = [rec for _, rec in read_records(wb, "RSA Ads")[0]]
    for sheet in sheets:
        spec, xml = SHEETS[sheet], wb.xml(sheet)
        for row, rec in read_records(wb, sheet)[0]:
            if sheet == "RSA Ads":
                st = check_copy.rsa_stats(rec)
                vals = [st[c] for c in spec["formulas"]]
            elif sheet == "Sitelinks":
                vals = [check_copy.sitelink_check(rec)]
            elif sheet == "Callouts":
                vals = [check_copy.callout_check(rec)]
            elif sheet == "Snippets":
                vals = [check_copy.snippet_check(rec)]
            else:
                vals = [check_copy.keyword_in_headline(rec, ads)]
            for col, v in zip(spec["formulas"], vals):
                xml = set_formula_cache(xml, "%s%d" % (col, row), v)
        wb.set_xml(sheet, xml)


def _formulas(xml):
    return sorted(re.findall(r"<f[^>]*?(?:/>|>.*?</f>)", xml, re.S))


def verify(template, out, written, touched):
    """Structural checks on the saved file. Returns a list of problems (empty means clean)."""
    problems, a, b = [], Workbook(template), Workbook(out)
    expected = {a.sheet_parts[s] for s in touched}
    for name, data in a.parts.items():
        if name not in b.parts:
            problems.append("part missing from output: %s" % name)
        elif name not in expected and data != b.parts[name]:
            problems.append("untouched part changed: %s" % name)
    for name, data in b.parts.items():
        if name.endswith((".xml", ".rels")):
            try:
                ET.fromstring(data)
            except ET.ParseError as e:
                problems.append("%s is not well-formed XML: %s" % (name, e))
    for sheet in sorted(touched):
        ax, bx = a.xml(sheet), b.xml(sheet)
        for label, pat in (("x14 dropdowns", "<x14:dataValidation "), ("data validations", "<dataValidation "),
                           ("conditional formats", "<conditionalFormatting"), ("rows", "<row ")):
            if ax.count(pat) != bx.count(pat):
                problems.append("%s: %s count changed %d -> %d" % (sheet, label, ax.count(pat), bx.count(pat)))
        if _formulas(ax) != _formulas(bx):
            problems.append("%s: formulas changed" % sheet)
        have = [rec for _, rec in read_records(b, sheet)[0]]
        spec = SHEETS[sheet]
        for rec in written.get(sheet, []):
            probe = {k: rec.get(k, "") for k in spec["scalars"] if k in ("id", "text", "keyword", "header")}
            if not any(all(h.get(k) == v for k, v in probe.items()) for h in have):
                problems.append("%s: row %s not found after save" % (sheet, probe))
    try:
        import openpyxl  # optional extra check; the fill itself never needs it
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            openpyxl.load_workbook(out)
    except ImportError:
        pass
    except Exception as e:
        problems.append("openpyxl could not open the output: %s" % e)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True)
    ap.add_argument("--payload", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true", help="plan and validate, write nothing")
    ap.add_argument("--force", action="store_true", help="write even when check_copy reports ERRORs")
    ap.add_argument("--overwrite", action="store_true", help="replace --out if it exists")
    a = ap.parse_args()
    if os.path.abspath(a.out) == os.path.abspath(a.template):
        sys.exit("--out must differ from --template; the template is never overwritten")
    if os.path.exists(a.out) and not (a.overwrite or a.dry_run):
        sys.exit("%s exists; pass --overwrite to replace it" % a.out)
    with open(a.payload, encoding="utf-8") as fh:
        payload = json.load(fh)
    wb = Workbook(a.template)
    findings = check_copy.validate(payload, read_lists(wb))
    errors = [f for f in findings if f["severity"] == "ERROR"]
    for f in errors:
        print("ERROR  %s: %s" % (f["where"], f["message"]), file=sys.stderr)
    warns = [f for f in findings if f["severity"] == "WARN"]
    for f in warns:
        print("WARN   %s: %s" % (f["where"], f["message"]), file=sys.stderr)
    if warns or any(f["severity"] == "INFO" for f in findings):
        print("%d warning(s), %d info; run check_copy.py for the INFO lines"
              % (len(warns), sum(f["severity"] == "INFO" for f in findings)), file=sys.stderr)
    if errors and not a.force:
        sys.exit("%d error(s) in the payload; fix them (or pass --force) before filling" % len(errors))
    defaults = payload.get("defaults", {})
    plans, written = {}, {}
    for key in SHEET_ORDER:
        recs = payload.get(key) or []
        if recs:
            sheet = KEY_TO_SHEET[key]
            plans[sheet] = plan_sheet(wb, sheet, recs)
    for sheet, (rows, clear_rows, recs) in plans.items():
        print("%-18s rows %s%s" % (sheet, ", ".join(map(str, rows)),
                                   "  (cleared sample rows %s)" % clear_rows if clear_rows else ""))
        if sheet == "RSA Ads":
            for row, rec in zip(rows, recs):
                print("    %s  %s" % (rec["id"], rec.get("ad_group", "")))
    if a.dry_run:
        return
    for sheet, (rows, clear_rows, recs) in plans.items():
        write_sheet(wb, sheet, rows, clear_rows, recs, defaults)
        written[sheet] = recs
    touched = set(written) | ({"Keywords & Intent"} if "RSA Ads" in written else set())
    refresh_caches(wb, sorted(touched))
    wb.save(a.out)
    problems = verify(a.template, a.out, written, touched)
    for p in problems:
        print("VERIFY  " + p, file=sys.stderr)
    if problems:
        sys.exit("saved %s but verification found %d problem(s); do not hand it over" % (a.out, len(problems)))
    ads = [rec for _, rec in read_records(Workbook(a.out), "RSA Ads")[0]]
    for rec in ads:
        if rec["id"] in {r["id"] for r in written.get("RSA Ads", [])}:
            st = check_copy.rsa_stats(rec)
            print("    %s check: %s (%d headlines, %d descriptions)" % (rec["id"], st["J"], st["F"], st["G"]))
    print("saved %s" % a.out)


if __name__ == "__main__":
    main()
