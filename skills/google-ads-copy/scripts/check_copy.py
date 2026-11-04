#!/usr/bin/env python3
"""Check Google Ads copy before it goes into the template.

Covers the template's own limits and Check rules, Google editorial-policy patterns, the
competitor-name rule, and the product skill's claim guardrails (passed in the payload).
Policy rules drift, so the policy checks are a safety net, not a ruling from Google.

Usage:
    check_copy.py payload.json [--template Google_Ads_Copy_Template.xlsx] [--verify-urls] [--json]

Exit status is 1 when any ERROR is left, 0 otherwise. Schema: references/template-map.md.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LIMITS = {"headline": 30, "description": 90, "path": 15, "sitelink_text": 25,
          "sitelink_desc": 35, "callout": 25, "snippet_value": 25}

DEFAULT_LISTS = {
    "status": ["Draft", "In Review", "Approved", "Live", "Paused"],
    "match_type": ["Broad", "Phrase", "Exact"],
    "intent": ["Informational", "Commercial", "Transactional", "Navigational"],
    "priority": ["High", "Medium", "Low"],
    "snippet_header": ["Amenities", "Brands", "Courses", "Degree programs", "Destinations",
                       "Featured hotels", "Insurance coverage", "Models", "Neighborhoods",
                       "Service catalog", "Shows", "Styles", "Types"],
}

# All-caps words Google accepts as acronyms. Payload "acronyms" extends this.
ACRONYMS = {"SOC", "ISO", "GDPR", "CCPA", "FERPA", "COPPA", "SSPA", "AWS", "GCP", "AI", "API",
            "POC", "SE", "LMS", "VM", "IT", "CRM", "SSO", "ISV", "CEO", "CTO", "HR",
            "B2B", "B2C", "ROI", "KPI", "SDK", "PDF", "FAQ", "USA", "UK", "EU", "SaaS", "SMB",
            "CI", "CD", "UI", "UX", "SLA", "ERP", "VPN", "ML", "II"}

# Unverifiable-superlative group: ERROR unless the ad lists the term in claims_substantiated.
SUPERLATIVES = re.compile(
    r"(#\s?1\b|\bno\.?\s?1\b|\bnumber[- ]one\b|\bbest\b|\btop[- ]rated\b|\bleading\b|"
    r"\bworld[- ]class\b|\bfastest\b|\bcheapest\b|\blowest[- ]price\b|\bunbeatable\b|"
    r"\bguarantee[ds]?\b)", re.I)
SOFT_CLAIMS = re.compile(r"\b(only|perfect|ultimate|revolutionary|unmatched|unrivaled)\b", re.I)
SLOP = re.compile(
    r"\b(unlock|elevate|seamless(ly)?|streamline[sd]?|supercharge[sd]?|revolutioni[sz]e[sd]?|"
    r"leverag(e|es|ing)|game[- ]chang\w*|cutting[- ]edge|empower\w*|robust|next[- ]gen\w*|"
    r"turnkey|synerg\w+|holistic|delve|best[- ]in[- ]class|take your \w+ to the next level)\b", re.I)
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\s().-]?){9,}\d(?!\d)")
CLICK_HERE = re.compile(r"\bclick (here|now)\b", re.I)
SYMBOLS = re.compile(r"[★☆✓✔✅❌→►•©®™✦❤]")
REPEATED_PUNCT = re.compile(r"([!?$%*.,;:])\1+|\.\.\.")


# --- the template's own Check column, ported so cached values match what Excel computes ---

def _n(s):
    return len(s or "")


def rsa_stats(rec):
    hs = [h for h in rec["headlines"] if h]
    ds = [d for d in rec["descriptions"] if d]
    over = sum(_n(h) > 30 for h in hs) + sum(_n(d) > 90 for d in ds) \
        + (_n(rec["path1"]) > 15) + (_n(rec["path2"]) > 15)
    low = [h.lower() for h in hs]
    dup = sum(low.count(h) > 1 for h in low)
    if over:
        check = "Over limit"
    elif dup:
        check = "Duplicate headline"
    elif len(hs) < 3:
        check = "Need 3+ headlines"
    elif len(ds) < 2:
        check = "Need 2+ descriptions"
    elif not rec["final_url"]:
        check = "Add final URL"
    elif len(hs) < 8:
        check = "OK - add more headlines"
    else:
        check = "Ready"
    return {"F": len(hs), "G": len(ds), "H": over, "I": dup, "J": check}


def sitelink_check(rec):
    if _n(rec["text"]) > 25 or _n(rec["desc1"]) > 35 or _n(rec["desc2"]) > 35:
        return "Over limit"
    if not rec["text"]:
        return "Add link text"
    if not rec["final_url"]:
        return "Add final URL"
    if not rec["desc1"] or not rec["desc2"]:
        return "OK - add both descriptions"
    return "Ready"


def callout_check(rec):
    if _n(rec["text"]) > 25:
        return "Over limit"
    return "Add callout text" if not rec["text"] else "Ready"


def snippet_check(rec):
    vals = [v for v in rec["values"] if v]
    if any(_n(v) > 25 for v in vals):
        return "Over limit"
    if not rec["header"]:
        return "Pick a header"
    return "Need 3+ values" if len(vals) < 3 else "Ready"


def keyword_in_headline(kw, ads):
    """Template rule: the phrase appears in a headline of an ad whose ad group matches (or any)."""
    if not kw["keyword"]:
        return ""
    k = kw["keyword"].lower()
    for ad in ads:
        if kw["ad_group"] and ad["ad_group"] != kw["ad_group"]:
            continue
        if any(k in h.lower() for h in ad["headlines"] if h):
            return "Yes"
    return "No"


# --- payload validation ---

class Checker:
    def __init__(self, payload, lists):
        self.p, self.lists, self.findings = payload, lists, []
        self.competitors = payload.get("competitors", [])
        self.blocked = payload.get("blocked_claims", [])
        self.hedged = payload.get("hedged_claims", [])
        self.customers = payload.get("customers", [])
        self.acronyms = ACRONYMS | set(payload.get("acronyms", []))

    def add(self, sev, where, msg):
        self.findings.append({"severity": sev, "where": where, "message": msg})

    def text(self, value, where, field, ad=None):
        """Policy and style checks shared by every line of copy."""
        if not value:
            return
        limit = LIMITS[field]
        if len(value) > limit:
            self.add("ERROR", where, "%d chars, limit %d: %r" % (len(value), limit, value))
        if value != value.strip() or "  " in value:
            self.add("WARN", where, "stray whitespace: %r" % value)
        bangs = value.count("!")
        if bangs and field in ("headline", "sitelink_text", "callout"):
            self.add("ERROR", where, "exclamation mark; Google disapproves it here: %r" % value)
        elif bangs > 1:
            self.add("ERROR", where, "more than one exclamation mark: %r" % value)
        if REPEATED_PUNCT.search(value):
            self.add("WARN", where, "repeated punctuation: %r" % value)
        if SYMBOLS.search(value):
            self.add("WARN", where, "symbol or emoji may be disapproved: %r" % value)
        if "—" in value or "–" in value:
            self.add("WARN", where, "dash character; use a comma, period or plain hyphen: %r" % value)
        if field == "headline" and value.rstrip().endswith("."):
            self.add("WARN", where, "headline ends with a period; Google often rejects it: %r" % value)
        for w in re.findall(r"\b[A-Z]{2,}\b", value):
            if w not in self.acronyms:
                self.add("WARN", where, "all-caps word %r reads as excessive capitalisation" % w)
        okay = [s.lower() for s in (ad or {}).get("claims_substantiated", [])]
        for m in SUPERLATIVES.finditer(value):
            hit = m.group(0).lower()
            if any(hit in s or s in hit for s in okay):
                self.add("INFO", where, "superlative %r allowed via claims_substantiated; keep the proof on the landing page" % hit)
            else:
                self.add("ERROR", where, "unverifiable claim %r needs proof; cut it or list it in claims_substantiated: %r" % (hit, value))
        for m in SOFT_CLAIMS.finditer(value):
            self.add("WARN", where, "absolute word %r invites a claims review: %r" % (m.group(0), value))
        for m in SLOP.finditer(value):
            self.add("WARN", where, "filler word %r: %r" % (m.group(0), value))
        if PHONE.search(value):
            self.add("ERROR", where, "phone number in ad text; use a call asset: %r" % value)
        if CLICK_HERE.search(value):
            self.add("ERROR", where, "'click here' style call to action is disapproved: %r" % value)
        for b in self.blocked:
            if re.search(b, value, re.I):
                self.add("ERROR", where, "blocked by product claim guardrails (%s): %r" % (b, value))
        for h in self.hedged:
            if re.search(h, value, re.I):
                self.add("WARN", where, "medium-risk claim (%s); confirm the landing page repeats it: %r" % (h, value))
        allowed = {c.lower() for c in (ad or {}).get("competes_with", [])}
        for c in self.competitors:
            if re.search(r"\b%s\b" % re.escape(c), value, re.I):
                if c.lower() in allowed:
                    self.add("INFO", where, "competitor name %r used where competes_with allows it; trademark complaint risk, keep it factual" % c)
                else:
                    self.add("ERROR", where, "competitor name %r but competes_with does not list it (generic ad groups and extensions stay name-free): %r" % (c, value))
        for c in self.customers:
            if re.search(r"\b%s\b" % re.escape(c), value, re.I):
                self.add("INFO", where, "named customer %r; needs the customer's sign-off: %r" % (c, value))

    def enum(self, value, key, where):
        if value and value not in self.lists[key]:
            self.add("ERROR", where, "%r is not in the template's %s list %s" % (value, key, self.lists[key]))

    def url(self, value, where):
        if not value:
            self.add("ERROR", where, "final URL missing")
        elif value.startswith("http://"):
            self.add("WARN", where, "http URL; use https: %s" % value)
        elif not value.startswith("https://"):
            self.add("ERROR", where, "URL must start with https://: %s" % value)

    def ad(self, i, ad):
        where = "ad %s (%s)" % (ad.get("id") or "#%d" % (i + 1), ad.get("ad_group", "?"))
        for key in ("campaign", "ad_group"):
            if not ad.get(key):
                self.add("ERROR", where, "%s missing" % key)
        self.enum(ad.get("status", "Draft"), "status", where)
        self.url(ad.get("final_url"), where)
        hs, ds = ad.get("headlines", []), ad.get("descriptions", [])
        if len(hs) > 15:
            self.add("ERROR", where, "%d headlines, maximum 15" % len(hs))
        if len(ds) > 4:
            self.add("ERROR", where, "%d descriptions, maximum 4" % len(ds))
        rec = {"headlines": hs, "descriptions": ds, "path1": ad.get("path1", ""),
               "path2": ad.get("path2", ""), "final_url": ad.get("final_url", "")}
        st = rsa_stats(rec)
        if st["J"] not in ("Ready", "OK - add more headlines"):
            self.add("ERROR", where, "template Check column would show %r" % st["J"])
        if st["F"] < 8:
            self.add("WARN", where, "%d headlines; Google rates fewer than 8 weak, aim for 15" % st["F"])
        if st["G"] < 4:
            self.add("INFO", where, "%d descriptions; 4 gives Google the most to combine" % st["G"])
        if st["F"] >= 10:
            short = sum(0 < len(h) <= 20 for h in hs)
            long_ = sum(len(h) >= 24 for h in hs)
            if short < 3:
                self.add("WARN", where, "%d headlines of 20 characters or fewer; short lines let three headlines share a row" % short)
            if long_ < 3:
                self.add("WARN", where, "%d headlines of 24 characters or more; long lines carry the specifics" % long_)
        norm = {}
        for n, h in enumerate(hs):
            self.text(h, "%s H%d" % (where, n + 1), "headline", ad)
            norm.setdefault(re.sub(r"[^a-z0-9]", "", h.lower()), []).append(n + 1)
        for n, d in enumerate(ds):
            self.text(d, "%s D%d" % (where, n + 1), "description", ad)
            if d and len(d) < 50:
                self.add("WARN", "%s D%d" % (where, n + 1), "only %d chars; description space is going unused" % len(d))
        for label, items in (("headlines", hs), ("descriptions", ds)):
            seen = {}
            for n, v in enumerate(items):
                if v:
                    seen.setdefault(v.lower(), []).append(n + 1)
            for ns in (x for x in seen.values() if len(x) > 1):
                self.add("ERROR", where, "%s %s are identical; Google rejects duplicate %s" % (label, ns, label))
        for key, ns in norm.items():
            if key and len(ns) > 1 and len({hs[x - 1].lower() for x in ns}) > 1:
                self.add("WARN", where, "headlines %s differ only by case or punctuation" % ns)
        for k in ("path1", "path2"):
            v = ad.get(k, "")
            if v:
                self.text(v, "%s %s" % (where, k), "path", ad)
                if not re.fullmatch(r"[A-Za-z0-9_-]+", v):
                    self.add("ERROR", "%s %s" % (where, k), "paths take letters, digits, hyphens and underscores only: %r" % v)
        if ad.get("path2") and not ad.get("path1"):
            self.add("ERROR", where, "path2 set without path1")
        # keyword coverage and landing-page agreement
        group = [k for k in self.p.get("keywords", [])
                 if k.get("ad_group") in ("", None, ad.get("ad_group"))
                 and k.get("campaign") in ("", None, ad.get("campaign"))]
        low = [h.lower() for h in hs if h]
        for k in group:
            kw = k["keyword"]
            if any(kw.lower() in h for h in low):
                continue
            if len(kw) > LIMITS["headline"]:
                self.add("INFO", where, "keyword %r is over 30 chars so no headline can hold it verbatim" % kw)
            elif k.get("priority", "Medium") == "High":
                self.add("WARN", where, "High priority keyword %r is in no headline" % kw)
            else:
                self.add("INFO", where, "keyword %r is in no headline" % kw)
        lps = {k.get("landing_page", "").rstrip("/") for k in group if k.get("landing_page")}
        if lps and ad.get("final_url", "").rstrip("/") not in lps:
            self.add("WARN", where, "final URL differs from the keyword landing pages %s" % sorted(lps))

    def sitelink(self, i, s):
        where = "sitelink #%d (%s)" % (i + 1, s.get("text", "?"))
        self.enum(s.get("status", "Draft"), "status", where)
        self.text(s.get("text"), where + " text", "sitelink_text", s)
        self.text(s.get("desc1"), where + " desc1", "sitelink_desc", s)
        self.text(s.get("desc2"), where + " desc2", "sitelink_desc", s)
        self.url(s.get("final_url"), where)
        if not s.get("desc1") or not s.get("desc2"):
            self.add("WARN", where, "both description lines should be filled")

    def callout(self, i, c):
        self.enum(c.get("status", "Draft"), "status", "callout #%d" % (i + 1))
        self.text(c.get("text"), "callout #%d" % (i + 1), "callout", c)
        if not c.get("text"):
            self.add("ERROR", "callout #%d" % (i + 1), "callout text missing")

    def snippet(self, i, s):
        where = "snippet #%d (%s)" % (i + 1, s.get("header", "?"))
        self.enum(s.get("status", "Draft"), "status", where)
        if s.get("header") not in self.lists["snippet_header"]:
            self.add("ERROR", where, "header %r is not in the template's list %s" % (s.get("header"), self.lists["snippet_header"]))
        vals = s.get("values", [])
        if not 3 <= len(vals) <= 10:
            self.add("ERROR", where, "%d values; a snippet needs 3 to 10" % len(vals))
        if len({v.lower() for v in vals}) != len(vals):
            self.add("ERROR", where, "duplicate values")
        for n, v in enumerate(vals):
            self.text(v, "%s value %d" % (where, n + 1), "snippet_value", s)

    def keywords(self):
        for i, k in enumerate(self.p.get("keywords", [])):
            where = "keyword #%d (%s)" % (i + 1, k.get("keyword", "?"))
            if not k.get("keyword"):
                self.add("ERROR", where, "keyword text missing")
            for key, lk in (("match_type", "match_type"), ("intent", "intent"), ("priority", "priority")):
                self.enum(k.get(key), lk, where)

    def campaign_totals(self):
        for kind, label, need in (("sitelinks", "sitelinks", 4), ("callouts", "callouts", 4)):
            items = self.p.get(kind, [])
            if not items:
                continue
            per, seen = {}, set()
            for it in items:
                camp, text = it.get("campaign", ""), it.get("text", "").lower()
                per[camp] = per.get(camp, 0) + 1
                if text and (camp, text) in seen:
                    self.add("ERROR", "%s for %r" % (label, camp), "duplicate text %r" % it.get("text"))
                seen.add((camp, text))
            for camp, n in per.items():
                if n < need:
                    self.add("WARN", "%s for %r" % (label, camp), "%d in this run; aim for %d+ per campaign (existing ones in the account may count)" % (n, need))
        heads = {(a.get("campaign", ""), h.lower()) for a in self.p.get("ads", []) for h in a.get("headlines", []) if h}
        for c in self.p.get("callouts", []):
            if (c.get("campaign", ""), c.get("text", "").lower()) in heads:
                self.add("WARN", "callout %r" % c.get("text"), "repeats a headline; a callout should add a fact the ad body lacks")
        if self.p.get("sitelinks") or self.p.get("callouts") or self.p.get("snippets"):
            with_snip = {s.get("campaign", "") for s in self.p.get("snippets", [])}
            for camp in sorted({a.get("campaign", "") for a in self.p.get("ads", [])} - with_snip):
                self.add("INFO", "campaign %r" % camp, "no structured snippet in this run")

    def run(self):
        for i, ad in enumerate(self.p.get("ads", [])):
            self.ad(i, ad)
        for i, s in enumerate(self.p.get("sitelinks", [])):
            self.sitelink(i, s)
        for i, c in enumerate(self.p.get("callouts", [])):
            self.callout(i, c)
        for i, s in enumerate(self.p.get("snippets", [])):
            self.snippet(i, s)
        self.keywords()
        self.campaign_totals()
        return self.findings


def validate(payload, lists=None):
    return Checker(payload, {**DEFAULT_LISTS, **(lists or {})}).run()


def verify_urls(payload):
    """Fetch every distinct URL once. Catches invented sitelink and landing-page URLs."""
    urls = {a.get("final_url") for a in payload.get("ads", [])}
    urls |= {s.get("final_url") for s in payload.get("sitelinks", [])}
    urls |= {k.get("landing_page") for k in payload.get("keywords", [])}
    out, checked = [], sorted(x for x in urls if x)
    for u in checked:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (ads-copy-url-check)"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status >= 400:
                    out.append({"severity": "ERROR", "where": u, "message": "HTTP %d" % r.status})
        except urllib.error.HTTPError as e:
            sev = "WARN" if e.code in (401, 403, 429) else "ERROR"
            out.append({"severity": sev, "where": u, "message": "HTTP %d%s" % (e.code, " (may be bot protection; open it yourself)" if sev == "WARN" else "")})
        except Exception as e:  # DNS failure, timeout, TLS
            out.append({"severity": "ERROR", "where": u, "message": "unreachable: %s" % e})
    print("verify-urls: %d URL(s) checked, %d problem(s)" % (len(checked), len(out)), file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload")
    ap.add_argument("--template", help="read the dropdown lists from this workbook's Lists tab")
    ap.add_argument("--verify-urls", action="store_true", help="GET every final URL and sitelink URL")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.payload, encoding="utf-8") as fh:
        payload = json.load(fh)
    lists = None
    if a.template:
        from xlsx_io import Workbook, read_lists
        lists = read_lists(Workbook(a.template))
    findings = validate(payload, lists)
    if a.verify_urls:
        findings += verify_urls(payload)
    counts = {s: sum(f["severity"] == s for f in findings) for s in ("ERROR", "WARN", "INFO")}
    if a.json:
        print(json.dumps({"counts": counts, "findings": findings}, indent=2))
    else:
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for f in sorted(findings, key=lambda f: order[f["severity"]]):
            print("%-5s  %s: %s" % (f["severity"], f["where"], f["message"]))
        print("\n%d error(s), %d warning(s), %d info" % (counts["ERROR"], counts["WARN"], counts["INFO"]))
    sys.exit(1 if counts["ERROR"] else 0)


if __name__ == "__main__":
    main()
