"""Minimal .xlsx reader/writer for the Google Ads Copy Template. Stdlib only.

The template keeps its Status/Match type/Intent/Priority/Snippet header dropdowns in
x14 extension blocks, which openpyxl silently drops on save. This module therefore
edits cells in the raw sheet XML and copies every other part of the zip byte for byte.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
M = "{%s}" % NS["m"]
FIRST_ROW = 6
SAMPLE_MARKERS = ("taskflow.example.com", "Sample row: replace me")


def col_index(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


def col_letter(i):
    out = ""
    while i:
        i, rem = divmod(i - 1, 26)
        out = chr(65 + rem) + out
    return out


def cols(first, last):
    return [col_letter(i) for i in range(col_index(first), col_index(last) + 1)]


# Input columns per tab. Formula columns (Check, counts, "In a headline?") are never written
# by hand; their cached values are refreshed after a fill so previews show the right status.
SHEETS = {
    "RSA Ads": dict(
        key="ads",
        scalars={"id": "A", "campaign": "B", "ad_group": "C", "status": "D", "owner": "E",
                 "final_url": "K", "path1": "L", "path2": "M", "hypothesis": "AG", "notes": "AH"},
        lists={"headlines": cols("N", "AB"), "descriptions": cols("AC", "AF")},
        formulas=cols("F", "J"), id_prefix="AD"),
    "Sitelinks": dict(
        key="sitelinks",
        scalars={"id": "A", "campaign": "B", "ad_group": "C", "status": "D", "owner": "E",
                 "text": "G", "desc1": "H", "desc2": "I", "final_url": "J", "notes": "K"},
        lists={}, formulas=["F"], id_prefix="SL"),
    "Callouts": dict(
        key="callouts",
        scalars={"id": "A", "campaign": "B", "ad_group": "C", "status": "D", "owner": "E",
                 "text": "G", "notes": "H"},
        lists={}, formulas=["F"], id_prefix="CO"),
    "Snippets": dict(
        key="snippets",
        scalars={"id": "A", "campaign": "B", "ad_group": "C", "status": "D", "owner": "E",
                 "header": "G", "notes": "R"},
        lists={"values": cols("H", "Q")}, formulas=["F"], id_prefix="SN"),
    "Keywords & Intent": dict(
        key="keywords",
        scalars={"keyword": "A", "match_type": "B", "intent": "C", "campaign": "D",
                 "ad_group": "E", "landing_page": "F", "priority": "G", "notes": "I"},
        lists={}, formulas=["H"], id_prefix=None),
}
KEY_TO_SHEET = {spec["key"]: name for name, spec in SHEETS.items()}


def input_cols(spec):
    out = list(spec["scalars"].values())
    for cs in spec["lists"].values():
        out += cs
    return out


class Workbook:
    def __init__(self, path):
        with zipfile.ZipFile(path) as z:
            self.infos = z.infolist()
            self.parts = {i.filename: z.read(i.filename) for i in self.infos}
        self.sheet_parts = self._sheet_parts()
        self.shared = self._shared_strings()
        self.modified = set()

    def _sheet_parts(self):
        wb = ET.fromstring(self.parts["xl/workbook.xml"])
        rels = ET.fromstring(self.parts["xl/_rels/workbook.xml.rels"])
        target = {r.get("Id"): r.get("Target") for r in rels}
        out = {}
        for s in wb.find(M + "sheets"):
            rid = s.get("{%s}id" % NS["r"])
            out[s.get("name")] = "xl/" + target[rid].lstrip("/").removeprefix("xl/")
        return out

    def _shared_strings(self):
        if "xl/sharedStrings.xml" not in self.parts:
            return []
        root = ET.fromstring(self.parts["xl/sharedStrings.xml"])
        out = []
        for si in root.findall(M + "si"):
            # plain <t>, or rich-text <r><t> runs; phonetic <rPh> text is skipped
            runs = si.findall(M + "t") + [t for r in si.findall(M + "r") for t in r.findall(M + "t")]
            out.append("".join(t.text or "" for t in runs))
        return out

    def xml(self, sheet):
        return self.parts[self.sheet_parts[sheet]].decode("utf-8")

    def set_xml(self, sheet, text):
        self.parts[self.sheet_parts[sheet]] = text.encode("utf-8")
        self.modified.add(self.sheet_parts[sheet])

    def last_row(self, sheet):
        ref = re.search(r'<dimension ref="[A-Z]+\d+:[A-Z]+(\d+)"', self.xml(sheet)).group(1)
        return int(ref)

    def cells(self, sheet):
        """{(col, row): text} for every non-empty cell, formula cells included (cached value)."""
        root = ET.fromstring(self.parts[self.sheet_parts[sheet]])
        out = {}
        for c in root.iter(M + "c"):
            m = re.match(r"([A-Z]+)(\d+)$", c.get("r"))
            t = c.get("t")
            v = c.find(M + "v")
            if t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(M + "t"))
            elif t == "s" and v is not None:
                val = self.shared[int(v.text)]
            elif v is not None and v.text is not None:
                val = v.text
            else:
                continue
            if val != "":
                out[(m.group(1), int(m.group(2)))] = val
        return out

    def style_of(self, sheet, col, row):
        m = re.search(r'<c r="%s%d"[^>]*?\bs="(\d+)"' % (col, row), self.xml(sheet))
        return m.group(1) if m else None

    def save(self, out):
        with zipfile.ZipFile(out, "w") as z:
            for info in self.infos:
                z.writestr(info, self.parts[info.filename], compress_type=zipfile.ZIP_DEFLATED)


def _cell_re(ref):
    return re.compile(r'<c r="%s"([^>]*?)(?:/>|>(.*?)</c>)' % ref, re.S)


_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def set_text(xml, ref, text, style):
    """Replace one cell with an inline string (or an empty styled cell when text is blank)."""
    s = ' s="%s"' % style if style else ""
    if text in (None, ""):
        new = '<c r="%s"%s/>' % (ref, s)
    else:
        body = escape(_CTRL.sub("", str(text)))
        new = '<c r="%s"%s t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, s, body)
    out, n = _cell_re(ref).subn(lambda _m: new, xml, count=1)
    if n != 1:
        raise KeyError("cell %s not found in sheet XML" % ref)
    return out


def set_formula_cache(xml, ref, value):
    """Refresh the cached result of a formula cell without touching the formula itself."""
    m = _cell_re(ref).search(xml)
    if not m or not m.group(2):
        raise KeyError("formula cell %s not found" % ref)
    f = re.search(r"<f[^>]*?(?:/>|>.*?</f>)", m.group(2), re.S)
    if not f:
        raise KeyError("cell %s has no formula" % ref)
    s = re.search(r'\bs="(\d+)"', m.group(1))
    s = ' s="%s"' % s.group(1) if s else ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        new = '<c r="%s"%s>%s<v>%s</v></c>' % (ref, s, f.group(0), value)
    else:
        new = '<c r="%s"%s t="str">%s<v>%s</v></c>' % (ref, s, f.group(0), escape(str(value)))
    return xml[:m.start()] + new + xml[m.end():]


def row_record(cells, spec, row):
    rec = {k: cells.get((c, row), "") for k, c in spec["scalars"].items()}
    for k, cs in spec["lists"].items():
        rec[k] = [cells.get((c, row), "") for c in cs]
    return rec


def is_empty(rec):
    return not any((v if isinstance(v, str) else any(v)) for v in rec.values())


def is_sample(rec):
    flat = [v for x in rec.values() for v in (x if isinstance(x, list) else [x])]
    return any(any(mk in v for mk in SAMPLE_MARKERS) for v in flat if v)


def read_records(wb, sheet):
    """Real (non-sample) rows as [(row, record)], plus the number of sample rows skipped."""
    spec, cells = SHEETS[sheet], wb.cells(sheet)
    rows, samples = [], 0
    for row in range(FIRST_ROW, wb.last_row(sheet) + 1):
        rec = row_record(cells, spec, row)
        if is_empty(rec):
            continue
        if is_sample(rec):
            samples += 1
            continue
        rows.append((row, rec))
    return rows, samples


def read_lists(wb):
    cells = wb.cells("Lists")
    keys = {"A": "status", "B": "match_type", "C": "intent", "D": "priority", "E": "snippet_header"}
    out = {k: [] for k in keys.values()}
    for (c, r), v in sorted(cells.items(), key=lambda kv: kv[0][1]):
        if r >= 2 and c in keys:
            out[keys[c]].append(v)
    return out
