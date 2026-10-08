#!/usr/bin/env python3
"""Shortlist internal-link candidates for a draft from cached site inventories.

Outbound (default): which existing pages the draft should link to, the draft
paragraphs where each fits best, and anchor phrases that already exist in
those paragraphs.

  candidates.py --draft draft.json --sites example.com sister.com [--home example.com]
                [--top 30] [--exclude-url URL ...]

Inbound (--inbound): which existing pages should link TO the draft, with the
sentences on those pages that mention the draft's topic.

  candidates.py --draft draft.json --sites example.com --inbound
                [--phrase "inventory turnover" --phrase "stock turns"] [--top 15]

--draft accepts the JSON from `docx_links.py extract --json`, or a .md/.txt
file (paragraphs split on blank lines; markdown headings detected).
--sites takes domains (read from the inventory cache) or paths to cache files.
This is a shortlist for judgment, not a decision: scores are lexical
similarity, nothing more. Standard library only.
"""
import argparse
import json
import math
import os
import re
import sys
import urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import host_of, linkable, site_rules, view  # noqa: E402

CACHE_DIR = os.path.expanduser(os.environ.get("INTERNAL_LINKING_CACHE", "~/.cache/internal-linking"))

STOP = set("""a about above after again against all also am an and any are aren't as at be because been before being
below between both but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each
few for from further get gets getting got had hadn't has hasn't have haven't having he her here hers herself him
himself his how however i if in into is isn't it it's its itself just let's like make makes making many may me
might more most much must my myself need needs no nor not now of off often on once one only or other our ours
ourselves out over own per same she should shouldn't so some such than that that's the their theirs them
themselves then there there's these they this those through to too under until up upon us use used using very
via want was wasn't way ways we well were weren't what what's when where which while who whom why will with
within without won't would wouldn't you your yours yourself yourselves new also every even get help helps
key best top guide blog read learn learning step steps today 2023 2024 2025 2026 2027 etc e.g i.e""".split())

TOKEN = re.compile(r"[a-z0-9][a-z0-9+#]*(?:[.'-][a-z0-9+#]+)*")


def stem(t):
    if len(t) > 4 and t.endswith("ies"):
        return t[:-3] + "y"
    if len(t) > 4 and t.endswith("s") and not t.endswith(("ss", "us", "is")):
        return t[:-1]
    return t


def tokens(text):
    return [stem(t) for t in TOKEN.findall((text or "").lower())]


def features(text):
    toks = tokens(text)
    feats = [t for t in toks if t not in STOP and len(t) > 1]
    for a, b in zip(toks, toks[1:]):
        if a not in STOP and b not in STOP and len(a) > 1 and len(b) > 1:
            feats.append(a + " " + b)
    return feats


def load_draft(path):
    if path.endswith(".json"):
        d = json.load(open(path))
        return d["paragraphs"]
    raw = open(path, encoding="utf-8").read()
    paras = []
    for i, block in enumerate(re.split(r"\n\s*\n", raw)):
        block = block.strip()
        if not block:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", block)
        links = [{"text": t, "url": u} for t, u in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", block)]
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(2) if m else block)
        paras.append({"i": i, "heading": len(m.group(1)) if m else None, "text": text,
                      "words": len(text.split()), "links": links})
    return paras


def load_sites(specs):
    pages = []
    for s in specs:
        path = s if s.endswith(".json") else os.path.join(CACHE_DIR, host_of(s) + ".json")
        if not os.path.exists(path):
            sys.exit("no inventory for %s (expected %s). Run inventory.py first." % (s, path))
        data = json.load(open(path))
        host = host_of(data["site"])
        excl, money = site_rules(host)
        for p in data["pages"]:
            p = view(p, excl, money)
            if linkable(p):
                p["site"] = host
                pages.append(p)
    return pages


def norm_url(u):
    p = urllib.parse.urlparse(u)
    return (re.sub(r"^www\.", "", p.netloc.lower()) + p.path.rstrip("/")).lower()


def page_fields(p):
    focus = " ".join([p.get("title", "")] * 3 + p.get("h1", []) * 2 + p.get("h2", []) + [p.get("description", "")])
    body = " ".join((p.get("text") or "").split()[:2000])
    return focus, body


def tfidf(counter, idf):
    v = {t: (1 + math.log(c)) * idf.get(t, 0) for t, c in counter.items()}
    n = math.sqrt(sum(x * x for x in v.values())) or 1
    return {t: x / n for t, x in v.items()}


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0) for t, x in a.items())


def anchor_phrases(text, focus_terms, idf, k=3):
    """n-grams (2-6 words) from text weighted by overlap with the target's focus terms."""
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9+#'’.-]*", text)
    best = {}
    for n in range(2, 7):
        for i in range(len(words) - n + 1):
            gram = words[i:i + n]
            low = [stem(w.lower().strip(".")) for w in gram]
            if low[0] in STOP or low[-1] in STOP:
                continue
            hits = [w for w in low if w in focus_terms]
            bis = [a + " " + b for a, b in zip(low, low[1:]) if a + " " + b in focus_terms]
            if len(hits) < 2 and not bis:
                continue
            score = sum(idf.get(w, 0) for w in set(hits)) + 2 * sum(idf.get(b, 0) for b in set(bis))
            score *= len(set(hits)) / n  # prefer tight phrases
            phrase = " ".join(gram).strip(".,;:")
            if score > best.get(phrase, 0):
                best[phrase] = score
    ranked = sorted(best.items(), key=lambda kv: -kv[1])
    out = []
    for ph, _ in ranked:
        if any(ph in o or o in ph for o in out):
            continue
        out.append(ph)
        if len(out) == k:
            break
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text or "") if 30 < len(s.strip()) < 400]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft", required=True)
    ap.add_argument("--sites", nargs="+", required=True)
    ap.add_argument("--home", help="domain the draft will publish on (others are labelled sister sites)")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--exclude-url", action="append", default=[])
    ap.add_argument("--inbound", action="store_true")
    ap.add_argument("--phrase", action="append", default=[], help="topic phrase for inbound sentence search")
    args = ap.parse_args()

    paras = load_draft(args.draft)
    pages = load_sites(args.sites)
    home = re.sub(r"^www\.", "", args.home or pages[0]["site"])

    existing = {norm_url(l["url"]) for p in paras for l in p.get("links", [])}
    excluded = existing | {norm_url(u) for u in args.exclude_url}
    pages = [p for p in pages if norm_url(p["url"]) not in excluded]

    draft_text = " ".join((p["text"] + " ") * (2 if p.get("heading") is not None else 1) for p in paras)
    page_counts = []
    for p in pages:
        focus, body = page_fields(p)
        page_counts.append((Counter(features(focus)) + Counter(features(body)), Counter(features(focus))))
    df = Counter()
    for full, _ in page_counts:
        df.update(set(full))
    N = len(pages) + 1
    idf = {t: math.log(N / (1 + c)) + 1 for t, c in df.items()}
    dvec = tfidf(Counter(features(draft_text)), idf)

    scored = []
    for p, (full, focus) in zip(pages, page_counts):
        s = 0.6 * cos(dvec, tfidf(full, idf)) + 0.4 * cos(dvec, tfidf(focus, idf))
        scored.append((s, p, focus))
    scored.sort(key=lambda x: -x[0])

    body_paras = [p for p in paras if p.get("heading") is None]
    pvecs = [(p, tfidf(Counter(features(p["text"])), idf)) for p in body_paras]

    print("# Draft file: %s" % os.path.abspath(args.draft))
    print("# Draft: %d paragraphs, ~%d body words, %d existing links (excluded from candidates)" %
          (len(paras), sum(p["words"] for p in body_paras), len(existing)))
    print("# Inventory: %d live pages across %s; home site = %s\n" %
          (len(pages), ", ".join(sorted({p["site"] for p in pages})), home))

    if args.inbound:
        phrases = [ph.lower() for ph in args.phrase]
        if not phrases:
            title = next((p["text"] for p in paras if p.get("heading") is not None), paras[0]["text"])
            toks = [t for t in tokens(title) if t not in STOP]
            phrases = [" ".join(toks[i:i + 2]) for i in range(len(toks) - 1)] or toks
        print("## Inbound candidates (pages that should link to the new post)")
        print("topic phrases searched: %s\n" % ", ".join(repr(p) for p in phrases))
        shown = 0
        for s, p, _ in scored:
            hits = []
            for sent in sentences(p.get("text")):
                low = " %s " % " ".join(tokens(sent))
                for ph in phrases:
                    if " %s " % " ".join(tokens(ph)) in low:  # whole words only: "nce" must not match "experience"
                        hits.append((ph, sent))
                        break
            if not hits and s < scored[min(len(scored) - 1, args.top)][0]:
                continue
            shown += 1
            tag = "home" if p["site"] == home else "SISTER"
            print("%2d. [%.3f] %s · %s · %s\n    %s" % (shown, s, tag, p["type"], p["url"], p.get("title", "")))
            for ph, sent in hits[:3]:
                print("    ↳ mentions %r: \"%s\"" % (ph, sent))
            if not hits:
                print("    ↳ no sentence names the topic phrases; would need a new sentence")
            if shown >= args.top:
                break
        return

    def show(rank, s, p, focus):
        tag = "home" if p["site"] == home else "SISTER"
        print("%2d. [%.3f] %s · %s · %s" % (rank, s, tag, p["type"], p["url"]))
        print("    title: %s" % p.get("title", ""))
        if p.get("h2"):
            print("    h2: %s" % " | ".join(p["h2"][:6]))
        focus_terms = set(focus)
        fvec = tfidf(focus, idf)
        fits = sorted(((cos(v, fvec), para) for para, v in pvecs), key=lambda x: -x[0])[:2]
        for fs, para in fits:
            if fs <= 0:
                continue
            ph = anchor_phrases(para["text"], focus_terms, idf)
            print("    fits P%d (%.2f): %s" % (para["i"], fs, "; ".join(repr(x) for x in ph) if ph else "(no natural phrase)"))

    print("## Outbound candidates (ranked by topical similarity)")
    top = scored[:args.top]
    for n, (s, p, focus) in enumerate(top, 1):
        show(n, s, p, focus)
    shown = {id(p) for _, p, _ in top}
    money = [x for x in scored if x[1]["type"] in ("money", "page", "home") and id(x[1]) not in shown][:8]
    if money:
        print("\n## Commercial pages just outside the shortlist (consider for money-page links)")
        for n, (s, p, focus) in enumerate(money, len(top) + 1):
            show(n, s, p, focus)


if __name__ == "__main__":
    main()
