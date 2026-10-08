---
name: internal-linking
description: "Adds internal links to a blog draft before it's published: finds the right existing pages from the site's live sitemap and Google Search Console, inserts real hyperlinks into a copy of the Google Doc or Word draft, and lists which existing posts should link back to the new one. Use this whenever the user wants internal links added, suggested, or checked on a draft, article, or blog post, or mentions 'internal linking,' 'interlinking,' 'link to our other posts,' 'add links to this draft,' 'which pages should link to this,' 'inbound links for the new post,' 'orphan page,' 'anchor text,' or 'link suggestions,' even when they just hand over a .docx or Google Doc and say 'prep this for publishing.' For writing a brief, see content-brief. For auditing a finished draft's structure and citations, see pre-publish-check."
metadata:
  version: 1.0.0
---

# Internal Linking for Blog Drafts

You take a draft and hand back three things:

1. **A linked copy of the draft** (`<name> – linked.docx`) with real hyperlinks inserted. The original is never touched.
2. **A link report** (`<name> – internal links.md`) listing every link, its anchor, its target, why it was chosen, and what you considered and rejected.
3. **An inbound plan**: the existing pages that should link *to* the new post, each with the exact sentence to edit and an anchor to use. Inbound is the half everyone forgets, and it's what gets a new post crawled and ranked.

The aim is links a good editor would add: each one helps a reader who wants to go deeper at that moment, and together they tell search engines how the new post fits with the rest of the site. Hitting a quota of links is not the goal. Three well-placed links beat ten forced ones.

Read [references/linking-rules.md](references/linking-rules.md) before choosing links. It holds the default rules, the anchor-text guidance, and worked examples. They are **defaults, not laws**. Precedence: **writer instructions > house rules in `config/sites.md` > the defaults and examples in linking-rules.md**. Your judgment applies everywhere.

---

## Step 0 — Load the site config

Read `config/sites.md` in this skill's folder. It lists the sites in scope, the default "home" site (the one the draft will publish on), each site's Search Console property, which topics belong to which site, and house rules. `config/patterns.json` holds each site's money-page and exclusion regexes. The scripts load it automatically, so you don't pass any flags.

If there's no `config/sites.md`, ask for the site URL(s) in Step 1. After the run, offer to save the answers to `config/sites.md` and `config/patterns.json` (copy the formats from the `.example` files) so the next run doesn't have to ask.

## Step 1 — Ask the writer (one message)

Always confirm which sites are in scope, because the right set changes from post to post. Show the default list from the config and ask what to add or remove, and which site the draft publishes on.

In the same message, ask for anything else the writer already knows. All of it is optional:

- **Primary keyword / topic**: what the post is trying to rank for. If skipped, infer it from the title and H2s and say what you inferred.
- **Planned URL or slug**: needed for the inbound plan. If unknown, use `{new-post-url}` as a placeholder.
- **Must-link pages**: e.g. a campaign landing page or the product page this post supports.
- **Pages to avoid**: e.g. a page being retired or rewritten.
- **Audience and funnel stage**: top-of-funnel explainers carry fewer product links than comparison or buying-guide posts.
- **House rules**: link count, sister-site links yes/no, any anchor conventions.

Keep it short and give them an easy way to skip: "or just say go and I'll use the defaults." If they say go, proceed and list your assumptions at the top of the report.

## Step 2 — Get the draft

| Draft arrives as | What to do |
|---|---|
| **Word (.docx)** | `scripts/run.sh docx_links.py extract DRAFT.docx --json "$WORK/draft.json"`. Read the printed `[P12]` paragraph list. Those numbers are how you'll place links. |
| **Google Doc** | If a Google Drive/Docs connector is available, export the doc as .docx (or follow the `google-workspace` skill to work on a copy). If not, ask the writer to use **File → Download → Microsoft Word (.docx)** and give you the path. Process it like a .docx. At the end, tell them to upload `– linked.docx` to Drive and open it as a Google Doc; hyperlinks survive the conversion. |
| **Markdown / pasted text** | Save it to a temp `.md` file. `candidates.py` reads it directly. Return the draft with `[anchor](url)` links instead of a .docx. |

Start by creating a private working folder, `WORK=$(mktemp -d)`, and keep every intermediate file there (`draft.json`, `links.json`). Other runs may be going at the same time, and a shared path like `/tmp/draft.json` gets overwritten silently. `candidates.py` prints the draft file it read on its first line, so check it.

`scripts/run.sh` creates a small private Python environment with python-docx the first time it runs (about 20 seconds), then reuses it.

Note the existing links the extract shows. They count toward density, and their targets are excluded from the candidates automatically.

## Step 3 — Build the site inventory

```bash
python3 scripts/inventory.py https://site-one.com https://site-two.com
```

Pass every site in scope in one call. It reads the sitemap, drops translations, thank-you pages, tag archives, noindex and canonicalised pages, fetches each page's title, H1, H2s, description and text, and caches the result for 7 days in `~/.cache/internal-linking/`. A fresh crawl of a few hundred pages takes a minute or two. Later runs are instant.

Add `--refresh` if the writer mentions a page published in the last few days, or if a target you want isn't in the inventory.

## Step 4 — Shortlist candidates

```bash
python3 scripts/candidates.py --draft "$WORK/draft.json" --sites site-one.com site-two.com --home site-one.com --top 30
```

For each candidate you get: a similarity score, home or SISTER site, page type (`money`, `page`, `blog`, `glossary`, `faq`, `case-study`...), the title and H2s, and the two draft paragraphs it fits best with phrases from those paragraphs that could serve as anchors. A final section lists commercial pages just outside the top 30, so product pages aren't buried by a dozen blog posts.

Treat the score as a shortlist. It measures word overlap, not usefulness. Read the titles and H2s and decide for yourself.

## Step 5 — Check Search Console

If a Search Console connector is available, use it. If it isn't, or a call fails, continue without it and say so in the report. Keep this to roughly 10–20 calls. Search Console sometimes reports a URL with a trailing slash, or a translated `/ja/...` version, that the sitemap lists differently. Treat those as the same page, and always link the URL exactly as the inventory lists it.

**a. Which pages already rank for the draft's topic.** One call per site in scope:
`gsc_get_advanced_search_analytics(site_url=<property>, dimensions="page,query", filter_dimension="query", filter_operator="contains", filter_expression="<core topic term>", start_date=<90 days ago>, sort_by="impressions", row_limit=200)`

Pick a filter term that can't match inside other words. `contains "nce"` also matches "experience" and "compliance". For short acronyms use a full phrase ("new commerce") or add a trailing space ("nce "). If the result is huge, narrow the term rather than paging through it.

Use this for two things:
- **Cannibalization**: if an existing page already ranks (roughly top 20) for the draft's *primary* keyword, flag it at the top of the report. The new post may compete with it. Recommend a distinct angle, linking to that page as the authority, or consolidating, and don't use the primary keyword as anchor text to any other page.
- **Inbound sources**: pages with impressions for the topic are the ones whose links carry the most relevance (Step 7).

**b. What each shortlisted target is known for.** For your top 10–15 outbound picks:
`gsc_get_advanced_search_analytics(site_url=<property>, dimensions="query", filter_dimension="page", filter_operator="contains", filter_expression="<path without trailing slash, e.g. /blog/azure-lab-services-alternatives-in-2026>", start_date=<90 days ago>, sort_by="impressions", row_limit=10)`
Filtering on the path with `contains` catches both the slash and no-slash versions. `gsc_get_search_by_page_query` needs the exact URL and often comes back empty for the version without the slash.

- When several pages cover the same concept, link the one Google already associates with it (most impressions and best position for that concept's queries).
- Pages sitting at **positions 5–20** for a valuable query benefit most from a new, well-anchored internal link. Prefer them when relevance is otherwise equal.
- Let the queries guide the anchor's meaning, but take the anchor wording from the draft. Don't paste the query in.

## Step 6 — Choose outbound links

Apply [references/linking-rules.md](references/linking-rules.md). In short, these are the defaults:

- About **1 link per 150–250 body words**. Fewer is fine when the site has nothing relevant, and you never pad to reach the number.
- **At most one link per paragraph**, and **each URL once**.
- **No links in the title, headings, or the intro's first sentence.**
- **Commercial pages first** where the draft discusses the problem the product solves. Usually 1–3 per post, scaled to funnel stage.
- **Anchors come from the draft's own words**: 2–6 words that tell the reader what they'll get, varied, and not exact-match keyword stuffing. Don't rewrite the writer's sentences to fit a link. If an important link has no natural anchor, propose wording in the report as *optional* and don't insert it.
- **Sister-site links** only when the draft really covers that site's topic. Usually 0–2, and never in place of a home-site page on the same subject.

Writer instructions from Step 1 override any of these. When you deliberately break a default (a second link in one long paragraph, say), note why in the report.

## Step 7 — Plan inbound links

```bash
python3 scripts/candidates.py --draft "$WORK/draft.json" --sites <same> --home <home> --inbound --phrase "core topic" --phrase "close variant" --top 15
```

Combine this with the Search Console pages from Step 5a. Pick **3–6 source pages**. Prefer, in order: pages with impressions for the topic, then closely related posts that mention the topic in a sentence, then the most relevant solution page (many have a resources or FAQ section). For each one:

- quote the **exact existing sentence** where the link should go, and the anchor inside it. The cached text can contain extraction glitches, so fetch the live page and confirm the sentence reads exactly as you quote it
- if no sentence fits, write one short new sentence and label it **new sentence**
- point at the planned URL, or `{new-post-url}` if it isn't known yet

You're only recommending these. Live pages are edited by whoever owns the CMS.

## Step 8 — Insert and verify

Write the chosen links to `$WORK/links.json`:

```json
[{"paragraph": 7, "anchor": "LTI grade pass-back", "url": "https://example.com/platform/lms-integration"}]
```

`anchor` must be copied exactly from the paragraph text, matching case and punctuation. Add `"occurrence": 2` if the phrase appears twice and you want the second one.

```bash
scripts/run.sh docx_links.py apply DRAFT.docx "$WORK/links.json" "<dir>/<name> – linked.docx"
scripts/run.sh docx_links.py verify "<dir>/<name> – linked.docx" "$WORK/links.json"
```

`apply` reports any link it couldn't place, for example an anchor that spans a line break or overlaps an existing link. Fix the anchor and re-run, or list it in the report as "insert manually". `verify` must show every planned link as `OK` before you report success. Save outputs next to the original draft unless the writer asked otherwise.

## Step 9 — Write the report

Use [references/report-template.md](references/report-template.md). Save it as `<name> – internal links.md` next to the linked copy. In chat, keep it short: the link count (outbound and inbound), any cannibalization or must-fix flags, links that need the writer's approval, and the two file paths.

---

## What not to do

- **Don't invent URLs.** Every target comes from the inventory (live, 200, indexable) or from the writer. If the right page doesn't exist, list it as a **content gap** in the report. That's useful in itself.
- **Don't link to translated versions, thank-you pages, gated-form pages, or noindex pages.** The inventory filters most of these. Watch for any that slip through.
- **Don't edit the original draft** or rewrite the writer's prose to fit a link.
- **Don't link the same concept to several near-identical pages.** When a site has five posts on one topic, pick the strongest and mention the others in "considered" only if it helps the writer.
