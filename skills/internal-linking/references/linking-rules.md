# Linking Rules

Defaults for choosing outbound links and anchors. Each rule comes with its reason so you can tell when breaking it is right. Precedence: writer instructions > house rules in `config/sites.md` > this file. A writer's "max N links" is a cap, not a target.

## Contents
1. Density and placement
2. Choosing the target
3. Commercial (money) pages
4. Anchor text
5. Sister sites
6. Cannibalization
7. Inbound links
8. Worked examples

---

## 1. Density and placement

| Default | Why | When to bend it |
|---|---|---|
| ~1 internal link per 150–250 body words (1,500 words → 6–10). Existing internal links count. External citations don't. | Enough to connect the post to its cluster without turning every sentence blue | Thin site coverage → fewer. Dense reference posts (glossaries, roundups) can take more. Short drafts (under ~400 words): one link per body section is fine, typically 3–4. |
| Max 1 link per paragraph | Two links side by side compete for the click and look spammy | A long paragraph that names two distinct, relevant things |
| Each URL once, at its first meaningful mention | Repeat links add nothing for readers. Search engines mostly count the first anchor. | Never for body copy. A closing CTA link to the same page is the writer's call. |
| No links in the title or headings | Headings are navigation, and linked headings read badly in most templates | — |
| No link in the intro's first sentence | The opening answer is what AI Overviews and LLMs quote, and it should keep the reader on the page | Later sentences in the intro are fine |
| Be sparing in tables, lists and image captions | They're scanned, not read, so links there get few clicks | A list item that names a capability the product page explains is a fine anchor |
| Prefer links early in the body | Readers drop off, so early links get more clicks and more weight | — |

## 2. Choosing the target

When several pages could take a link, prefer the one that:

1. **Answers what the reader wants at that moment.** Someone reading "compare pricing across vendors" wants pricing or a comparison, not the company history.
2. **Google already associates with the concept**, judging by Search Console queries and impressions.
3. **Is the hub, not a spoke.** Link the migration hub over the fourth blog post about the same deadline.
4. **Is current.** Prefer a 2026 update over a 2022 post on the same topic, and check the year in titles.
5. **Has room to climb.** Positions 5–20 for a valuable query gain the most from a new contextual link.

Skip: press releases (rarely useful mid-article), past-dated event or webinar pages unless the recording is the resource, thin pages (under ~150 words) other than glossary entries, and anything the writer said to avoid.

## 3. Commercial (money) pages

Product, solution, platform, integration and pricing pages convert. Most blog traffic never reaches them unless the post links there.

- **1–3 per post**, scaled by funnel stage. Top-of-funnel explainer: one, where the problem is discussed. Comparison, migration or buying guide: two or three.
- **Link where the problem is described**, not where the product is name-dropped. "Grade pass-back into Canvas" → the LMS integration page. That's a reader following their need.
- **Prefer specific over generic.** `/solutions/isv/pocs` beats the home page, and the home page beats nothing only rarely.
- **Pricing and demo pages** only when the text is about cost, evaluation or next steps.
- Pages the inventory types as `page` (top-level, non-blog) are often product or landing pages too. Read the title to decide.

## 4. Anchor text

Anchor text tells the reader where the link goes and tells search engines what the target is about.

**Do**
- Use words **already in the draft**. 2–6 words is the sweet spot.
- Make it **predictive**: a reader should be able to guess the destination.
- **Vary** anchors across links. Use partial-match and descriptive phrases ("grade pass-back into Canvas or Moodle"), not the same head term every time.
- Keep the anchor to the meaningful noun phrase. Leave trailing words like "and compare" outside the link.

**Don't**
- "click here", "this article", "read more", "learn more", bare URLs.
- Exact-match keyword stuffing (every anchor = the target's head keyword).
- Use **the draft's own primary keyword** as an anchor to another page. That tells Google the other page is the answer for this post's query.
- Rewrite the writer's sentence to manufacture an anchor. If a link matters and no phrase fits, propose a short bridging phrase in the report as **optional — needs writer OK** and leave the draft alone.

**Good / bad**

| Draft sentence | Weak anchor | Better anchor |
|---|---|---|
| "…browser access, LTI grade pass-back into Canvas or Moodle, cost controls…" | "Canvas" | "LTI grade pass-back into Canvas or Moodle" |
| "Shortlist two or three Azure Lab Services alternatives and compare them…" | "two or three Azure Lab Services alternatives and compare" | "Azure Lab Services alternatives" |
| "A free POC with Azure credits can cover the cost of the pilot." | "cover the cost" | "free POC with Azure credits" |

## 5. Sister sites

When the config lists several sites from one company, a link to a sister site is an **external** link technically. It passes less weight than an internal one, but it serves the reader and connects the brands.

- Link to a sister site **only when the draft really discusses that site's topic** (the config says which site owns what) and the sister page is the best resource for it.
- **0–2 per post**, and never as a stand-in for a home-site page on the same subject.
- Label them **SISTER** in the report so the writer sees them.

## 6. Cannibalization

If Search Console shows an existing page already ranking for the draft's primary keyword, or the candidate list has a page whose title is almost the draft's title, put it at the top of the report:

- name the page, its position and impressions for the keyword
- say what the risk is: two pages splitting one query, and both ranking worse
- recommend one option: give the new post a distinct angle and link to the existing page as the authority on the overlap; merge into the existing page; or proceed knowingly. The writer decides.

## 7. Inbound links

- **3–6 sources.** More is fine for a pillar post.
- Rank sources by: impressions for the topic (relevance plus authority), then topical closeness, then how easy they are to edit (blog, glossary, FAQ and guide pages before product pages).
- Quote the **exact sentence** to edit. Pick an anchor inside it that describes the new post, not "here".
- If no sentence works, write **one** new sentence that fits the section. Label it so.
- Pages with very few internal links pointing to them are orphan risks. The new post becomes one too if nobody links to it, so say so if the inbound list is thin.

## 8. Worked examples

**Example A — migration checklist, ~1,200 words, home = product site**
- Pick 6–8 links: the migration hub (hub page, in the intro's second paragraph), the LMS integration page (where faculty requirements mention grade pass-back), the alternatives comparison post (where the draft says "shortlist alternatives"), the pricing calculator (in the cost section), one case study if there's an ungated, substantive one (in the pilot section), the custom-images step of the transition guide (in the "migrate in waves" section). The comparison post and the transition guide cover *different subtopics* from the hub, so all three can earn a link. What you avoid is several pages saying the same thing.
- Reject: four more retirement-announcement posts (same concept as the hub), the webinar recording from 2024 (dated), a sister site's billing page (off-topic).
- Inbound: the "alternatives" post, the hub's resources section, the glossary entry for the product category.

**Example B — explainer on a sister company's topic**
- The draft is published on site A but has one section on cloud-marketplace private offers, site B's core topic. One SISTER link to site B's private-offer page is right. Five would turn the post into an ad for site B.

**Example C — writer override**
- Writer: "max 4 links, and the webinar page must be in." Honour both. If the webinar is weakly relevant, place it where it fits best and say so in the report rather than leaving it out.
