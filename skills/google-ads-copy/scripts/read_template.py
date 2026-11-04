#!/usr/bin/env python3
"""Dump what a filled-in Google Ads Copy Template already contains, as JSON.

Usage:
    read_template.py Google_Ads_Copy_Template.xlsx [--only keywords,ads,sitelinks,callouts,snippets,lists]

Output keys match the payload schema (references/template-map.md): keywords, ads, sitelinks,
callouts, snippets, plus lists (the dropdown values) and samples_skipped. The fictional sample rows
that ship in the template are skipped. Use it to read the Keywords & Intent tab as the brief, and to
see which copy already exists so new copy does not repeat it.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xlsx_io import KEY_TO_SHEET, SHEETS, Workbook, read_lists, read_records


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template")
    ap.add_argument("--only", help="comma-separated subset of keys")
    a = ap.parse_args()
    wb = Workbook(a.template)
    want = set(a.only.split(",")) if a.only else set(KEY_TO_SHEET) | {"lists"}
    out, skipped = {}, {}
    for key, sheet in KEY_TO_SHEET.items():
        if key in want:
            rows, samples = read_records(wb, sheet)
            out[key] = [dict(rec, _row=row) for row, rec in rows]
            skipped[sheet] = samples
    if "lists" in want:
        out["lists"] = read_lists(wb)
    out["samples_skipped"] = skipped
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
