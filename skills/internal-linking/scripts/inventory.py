#!/usr/bin/env python3
"""Build a cached inventory of a site's linkable pages from its sitemap.

For every URL in the sitemap (minus translations, thank-you pages, tag
archives, etc.) it fetches the page and records title, H1, H2s, meta
description, canonical, noindex, language and body text. The result is
cached per domain so repeat runs are instant.

Usage:
  inventory.py https://example.com [https://other.com ...]
      [--refresh] [--max-age-days 7] [--lang en] [--workers 16]

Site-specific "money page" and exclusion patterns come from
config/patterns.json in the skill folder (see patterns.example.json). They
are applied when the cache is read, by this script and by candidates.py, so
editing them takes effect without a re-crawl.

Prints the path of each cache file plus a one-line summary per site.
Standard library only.
"""
import argparse
import concurrent.futures as cf
import gzip
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

CACHE_DIR = os.path.expanduser(os.environ.get("INTERNAL_LINKING_CACHE", "~/.cache/internal-linking"))
UA = "Mozilla/5.0 (compatible; internal-linking-skill/1.0; +https://agentskills.io)"

LOCALES = ("ar bg cs da de el es et fi fr he hi hu id it ja ko lt lv nb nl no pl pt ro ru sk sl sr sv th tr "
           "uk vi zh zh-cn zh-tw zh-hans zh-hant pt-br pt-pt es-es es-mx fr-ca fr-fr de-de de-at en-gb en-au en-in").split()

DEFAULT_EXCLUDES = [
    r"^/(?:%s)(?:/|$)" % "|".join(re.escape(l) for l in LOCALES),  # translated copies
    r"thank-?you",
    r"/(?:tag|tags|category|categories|author|authors)/",
    r"/page/\d+",
    r"/(?:legal|privacy|privacy-policy|terms|terms-of-use|terms-of-service|cookie|cookies|cookie-policy|gdpr)(?:/|$)",
    r"privacy-notice|-notice/?$|signup/?$|sign-up/?$",
    r"/(?:login|signin|sign-in|signup|sign-up|register|cart|checkout|account|search|contact|contact-us)(?:/|$)",
    r"^/(?:blog|blogs|article|articles|news|insights|resources)/?$",  # listing pages
    r"/(?:landing|lp|template\d*)(?:/|$)",
    r"/feed/?$",
    r"\.(?:pdf|jpg|jpeg|png|gif|svg|webp|zip|xml)$",
]

# Path patterns that usually mean "commercial page" (product, solution, pricing...).
DEFAULT_MONEY = [
    r"^/(?:platform|product|products|solutions|solution|services|service|features|pricing|integrations|"
    r"use-cases|industries|why-[^/]+|demo|compare|[^/]+-alternative[s]?)(?:/|$)",
]

TYPE_RULES = [
    ("blog", r"^/(?:blog|blogs|articles|insights|news|resources/blog)/."),
    ("case-study", r"^/(?:case-studies|case-study|customers|success-stories)(?:/|$)"),
    ("glossary", r"^/(?:glossary|terms|wiki)/."),
    ("faq", r"^/faqs?(?:/|$)"),
    ("guide", r"^/(?:guides?|e-?books?|whitepapers?|resources|learn|docs)(?:/|$)"),
    ("event", r"^/(?:webinars?|events?|virtual-trainings?)(?:/|$)"),
    ("press", r"^/(?:press|press-releases|newsroom)(?:/|$)"),
]


SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS_FILE = os.path.join(SKILL_DIR, "config", "patterns.json")


def host_of(url):
    netloc = urllib.parse.urlparse(url if "//" in url else "https://" + url).netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


def site_rules(host):
    """(exclude, money) compiled regexes for a host: built-ins + config/patterns.json."""
    cfg = {}
    if os.path.exists(PATTERNS_FILE):
        with open(PATTERNS_FILE) as f:
            cfg = json.load(f)
    general, own = cfg.get("*", {}), cfg.get(host, {})
    excl = DEFAULT_EXCLUDES + general.get("exclude", []) + own.get("exclude", [])
    money = own.get("money") or general.get("money") or DEFAULT_MONEY
    return [re.compile(x, re.I) for x in excl], [re.compile(x, re.I) for x in money]


def view(page, excl, money):
    """A cached page record with the current config applied (cache untouched)."""
    pth = urllib.parse.urlparse(page["url"]).path or "/"
    p = dict(page)
    if "type" in p:
        p["type"] = classify(pth, money)
    if not p.get("skip") and any(r.search(pth) for r in excl):
        p["skip"] = "excluded by config"
    return p


def linkable(p):
    return p.get("status") == 200 and not p.get("skip") and not p.get("error")


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
            try:
                data = gzip.decompress(data)
            except OSError:
                pass
        return r.status, r.geturl(), r.headers.get("Content-Type", ""), data


def sitemap_urls(base):
    """Return {url: lastmod} from robots.txt sitemaps or common fallbacks."""
    roots = []
    try:
        _, _, _, body = fetch(urllib.parse.urljoin(base, "/robots.txt"))
        for line in body.decode("utf-8", "replace").splitlines():
            if line.lower().startswith("sitemap:"):
                roots.append(line.split(":", 1)[1].strip())
    except Exception:
        pass
    if not roots:
        roots = [urllib.parse.urljoin(base, p) for p in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml")]

    seen, out, queue = set(), {}, list(roots)
    while queue:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            status, _, _, body = fetch(sm)
            root = ET.fromstring(body)
        except Exception:
            continue
        tag = root.tag.split("}")[-1]
        for node in root:
            loc = lastmod = None
            for child in node:
                name = child.tag.split("}")[-1]
                if name == "loc":
                    loc = (child.text or "").strip()
                elif name == "lastmod":
                    lastmod = (child.text or "").strip()
            if not loc:
                continue
            if tag == "sitemapindex":
                queue.append(loc)
            else:
                out[loc] = lastmod
    return out


class PageParser(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer", "form", "template", "aside"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "blockquote", "dd", "dt", "figcaption"}
    SPACER = {"div", "br", "section", "article", "header", "main", "button", "label"}  # layout tags: avoid "ofsales"

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.desc = ""
        self.canonical = ""
        self.robots = ""
        self.lang = ""
        self.h1, self.h2 = [], []
        self.links = []
        self._skip = 0
        self._cur = None  # heading being captured
        self._buf = []
        self._in_title = False
        self._block = []
        self.blocks = []
        self._href = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = (a.get("lang") or "").lower()
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n == "description" and not self.desc:
                self.desc = a.get("content") or ""
            elif n == "robots":
                self.robots = (a.get("content") or "").lower()
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href") or ""
        elif tag == "title" and not self._skip and not self.title:
            self._in_title = True  # first <title> only; SVG icons carry their own
        if tag in self.SKIP:
            self._skip += 1
        if self._skip:
            return
        if tag == "a" and a.get("href"):
            self._href = a["href"]
        if tag in ("h1", "h2"):
            self._cur = tag
            self._buf = []
        if tag in self.BLOCK:
            self._flush()
        elif tag in self.SPACER:
            self._block.append(" ")
            if self._cur:
                self._buf.append(" ")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self.SKIP and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if tag == "a":
            if self._href:
                self.links.append(self._href)
            self._href = None
        if tag == self._cur:
            text = " ".join(html.unescape("".join(self._buf)).split())
            if text:
                (self.h1 if tag == "h1" else self.h2).append(text)
            self._cur = None
        if tag in self.BLOCK:
            self._flush()

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip:
            return
        if self._cur:
            self._buf.append(data)
        self._block.append(data)

    def _flush(self):
        t = " ".join(html.unescape("".join(self._block)).split())
        if t:
            self.blocks.append(t)
        self._block = []

    def close(self):
        super().close()
        self._flush()


STOP_HEADINGS = re.compile(
    r"^(?:related (?:articles|posts|reads|questions|resources|blogs?)|you (?:may|might) also like|"
    r"more (?:from|articles|posts)|recommended (?:reading|articles)|read next|keep reading|latest (?:posts|articles))$",
    re.I)


def strip_boilerplate(pages):
    """Drop H2s/text blocks repeated across many pages (cookie banners, CTAs,
    footers) and cut each page at its 'Related articles' style trailer."""
    live = [p for p in pages if p.get("_blocks") is not None]
    n = len(live) or 1
    h2_count, block_count = {}, {}
    for p in live:
        for h in set(p.get("h2", [])):
            h2_count[h] = h2_count.get(h, 0) + 1
        for b in set(p["_blocks"]):
            block_count[b] = block_count.get(b, 0) + 1
    limit = max(3, n * 0.2)
    for p in live:
        blocks = []
        for b in p.pop("_blocks"):
            if STOP_HEADINGS.match(b.strip(" :")):
                break
            if block_count.get(b, 0) < limit:
                blocks.append(b)
        h2 = []
        for h in p.get("h2", []):
            if STOP_HEADINGS.match(h.strip(" :")):
                break
            if h2_count.get(h, 0) < limit:
                h2.append(h)
        p["h2"] = h2
        words = " ".join(blocks).split()
        p["words"] = len(words)
        p["text"] = "\n".join(blocks) if len(words) <= 5000 else " ".join(words[:5000])


def classify(path, money_res):
    if any(r.search(path) for r in money_res):
        return "money"
    for name, pat in TYPE_RULES:
        if re.search(pat, path):
            return name
    if path in ("", "/"):
        return "home"
    return "page"


def scrape(url, money_res, lang):
    rec = {"url": url}
    try:
        status, final, ctype, body = fetch(url)
    except urllib.error.HTTPError as e:
        rec.update(status=e.code, error=str(e))
        return rec
    except Exception as e:
        rec.update(status=0, error=str(e)[:200])
        return rec
    rec["status"] = status
    if final.rstrip("/") != url.rstrip("/"):
        rec["redirects_to"] = final
    if "html" not in ctype:
        rec["error"] = "not html"
        return rec
    p = PageParser()
    try:
        p.feed(body.decode("utf-8", "replace"))
        p.close()
    except Exception as e:
        rec["error"] = "parse: %s" % e
        return rec
    path = urllib.parse.urlparse(url).path
    rec.update(
        title=html.unescape(" ".join(p.title.split())),
        description=p.desc.strip(),
        h1=p.h1[:2],
        h2=p.h2[:25],
        canonical=p.canonical,
        noindex="noindex" in p.robots,
        lang=p.lang,
        type=classify(path, money_res),
        _blocks=p.blocks,
        internal_links=len([h for h in p.links if h.startswith("/") or urllib.parse.urlparse(h).netloc == urllib.parse.urlparse(url).netloc]),
    )
    if lang and p.lang and not p.lang.startswith(lang):
        rec["skip"] = "lang=%s" % p.lang
    elif rec["noindex"]:
        rec["skip"] = "noindex"
    elif rec["canonical"] and urllib.parse.urljoin(url, rec["canonical"]).rstrip("/") != url.rstrip("/"):
        rec["skip"] = "canonicalised to %s" % rec["canonical"]
    return rec


def build(base, args):
    host = host_of(base)
    path = os.path.join(CACHE_DIR, host + ".json")
    excl, money = site_rules(host)
    if os.path.exists(path) and not args.refresh:
        age = (time.time() - os.path.getmtime(path)) / 86400
        if age < args.max_age_days:
            with open(path) as f:
                data = json.load(f)
            return path, data, "cached %.1fd old" % age

    urls = sitemap_urls(base)
    keep, dropped = [], 0
    for u in urls:
        pth = urllib.parse.urlparse(u).path or "/"
        if any(r.search(pth) for r in excl):
            dropped += 1
            continue
        keep.append(u)

    pages = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for rec in ex.map(lambda u: scrape(u, money, args.lang), keep):
            rec["lastmod"] = urls.get(rec["url"])
            pages.append(rec)
    strip_boilerplate(pages)
    pages.sort(key=lambda r: r["url"])
    data = {
        "site": base,
        "built": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "sitemap_urls": len(urls),
        "excluded_by_pattern": dropped,
        "pages": pages,
    }
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)
    return path, data, "fresh"



def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sites", nargs="+")
    ap.add_argument("--refresh", action="store_true", help="ignore cache")
    ap.add_argument("--max-age-days", type=float, default=7)
    ap.add_argument("--lang", default="en", help="keep pages whose <html lang> starts with this ('' = any)")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()

    for s in args.sites:
        if not s.startswith("http"):
            s = "https://" + s
        path, data, how = build(s, args)
        excl, money = site_rules(host_of(s))
        pages = [view(p, excl, money) for p in data["pages"]]
        live = [p for p in pages if linkable(p)]
        types = {}
        for p in live:
            types[p["type"]] = types.get(p["type"], 0) + 1
        broken = [p["url"] for p in pages if p.get("status") not in (200,)]
        print("%s  [%s]  %d linkable of %d in sitemap (%d excluded by pattern, %d skipped, %d not 200)  %s"
              % (path, how + (", config/patterns.json applied" if os.path.exists(PATTERNS_FILE) else ", default patterns"),
                 len(live), data["sitemap_urls"], data["excluded_by_pattern"],
                 len([p for p in pages if p.get("skip")]), len(broken),
                 " ".join("%s=%d" % kv for kv in sorted(types.items()))))
        for b in broken[:10]:
            print("   %s: listed in sitemap but not 200: %s" % (host_of(s), b))


if __name__ == "__main__":
    main()
