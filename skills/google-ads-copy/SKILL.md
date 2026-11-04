---
name: google-ads-copy
description: "Writes Google Ads Search copy (responsive search ad headlines, descriptions and display paths, plus sitelinks, callouts and structured snippets) for one or more ad groups. It uses the campaign and ad group, the keywords, the live landing page, the product context skill and competitor context, then fills the user's Google Ads Copy Template workbook. Use this whenever the user asks for Google Ads copy, RSA headlines or descriptions, search ad copy for a set of keywords, sitelinks, callouts or snippets, or to rewrite or refresh existing Google ads, or when they hand over the Google Ads Copy Template .xlsx or a Keywords & Intent sheet, even if they never say 'RSA'. Not for LinkedIn or Meta ads, for creating or launching campaigns, or for auditing account health."
metadata:
  version: 1.0.0
---

# Google Ads Copy

You write Search ad copy that agrees with three things at once: what the person typed, what the
landing page says, and what the product can honestly claim. Then you put it in the user's Google Ads
Copy Template. You hand back two things:

1. **A filled copy of the workbook.** The original is never touched.
2. **A short chat brief per ad group:** the angle, what the ad tests, and every flag the user needs
   to see before it goes live.

Most of the quality comes from Steps 0 to 3. Headlines written without that context are
interchangeable with every competitor's. Headlines written with it are specific enough to earn the
click and to survive a claims review.

**Defaults the user already chose. Don't re-ask them.**
- Product facts come from a product skill's file, read at run time. Never from memory.
- Brief inputs can come from the template's Keywords & Intent tab, the Google Ads connector, or chat. Combine them.
- Output is the filled `.xlsx`.
- Competitor names go in ad copy only for ad groups built around that competitor (alternative, vs, pricing, reviews). Everywhere else the copy stays name-free.

Read `references/template-map.md` before the first fill. It has the workbook layout, the payload
schema and the script usage.

---

## Step 0: Load the product context

Product facts come from the user's own product context, never from memory. Work down this list and
stop at the first source that yields the context pack:

1. **Already in the conversation?** The user ran a product skill, pasted a brief, or attached a
   positioning document. Use it.
2. **Config.** If `config/product-context.md` exists in this skill's folder, it maps segments to product
   skills or files and says where to find them. Use the segment the user named. Otherwise infer it from
   the ad group, keywords and landing page. If it is ambiguous or the ad group mixes segments, ask once.
   Never blend two segments into one ad.
3. **Project files.** Look for `.agents/product-marketing.md`, `.claude/product-marketing.md` or
   `product-marketing-context.md` in the project (the files the `product-marketing` skill writes).
4. **Ask.** Ask the user to point at a product skill, a file or a URL, or to paste a brief: what the
   product does, for whom, proof points, claims that are off limits, who the competitors are. Say plainly
   that the copy rests on that brief alone.

Read a product skill's `SKILL.md` by path. Don't rely on the Skill tool: product skills are often
manual-invoke only (`disable-model-invocation: true`), and the tool refuses those.

Then **extract the context pack** (`references/context-pack.md`): the job to be done for this ad group,
the persona, safe proof points, claim guardrails with their grades, the competitive frame, messaging
pillars. Note which proof points you plan to use. The notes cell cites them later.

Apply any qualifying test or disqualifiers the product context states. If an ad group targets a buyer it
rules out, say so and ask before writing for it.

## Step 1: Gather the ad group brief

Per ad group you need: **campaign name, ad group name, keywords (with match type, intent, priority),
final URL.** Useful extras: offer, CTA, geography, audience, existing ads, competitor in play.

Sources, combined:

- **Template.** If the user gave a workbook, run `scripts/read_template.py <xlsx>`. The Keywords &
  Intent rows are the brief. The same dump shows copy that already exists, so you don't repeat it. A
  blank copy ships in `assets/Google_Ads_Copy_Template.xlsx`; use it when the user has no workbook.
- **Google Ads connector** (when the `ads_search` tool is available). Read-only. Pull the ad groups,
  keywords, search terms, and live RSAs with their asset performance labels. Queries and caveats are in
  `references/google-ads-connector.md`. Ask for the customer ID if you don't have it. Never write to the account.
- **Chat.** Whatever the user pasted or described.

Use names exactly as they appear in the account or sheet. Don't invent campaign or ad group names. If
something blocking is missing, ask once, in one message, and list everything you need.

Keyword intent and priority: if the user didn't set them, propose them from the keyword wording and
say which you inferred. Intent decides the angle (see `references/rsa-playbook.md`).

## Step 2: Read the landing page and the site

Fetch each final URL live. WebFetch returns a small-model summary, and its "not found" answers are
unreliable, so use it to read the page, then confirm every claim the copy will rely on against the raw
HTML (`curl -sL <url> | grep -i -o '.\{40\}<claim>.\{40\}'`). Use the browser for pages that need
JavaScript. If a page can't be fetched, ask the user to paste its copy. Never write from memory of a page.

Capture the H1, subhead, primary CTA label, the offer and its terms, pricing visibility, proof on the
page, the form or booking flow, and every claim the page makes. Then read the site's navigation or
sitemap to find sitelink destinations and the pages that back each callout and snippet value. Record
the page for each in that row's notes cell.

What the page can and can't change:

- **Message match.** The ad's promise, CTA and key terms must appear on the page. A headline the page
  doesn't back up costs quality score and trust.
- **Claim ceiling.** Don't claim more in an ad than the page does. When the product skill allows a claim
  the page lacks, use it only if you flag the gap ("add this to the page before launch").
- **Offers come from the page.** Product skills rarely list offers. Use a free trial, demo length or
  price only when the page states it. If its terms or audience aren't on the page, flag that instead of guessing.
- **Blocked claims on the page.** If the page carries a claim the product skill's guardrails block, don't
  repeat it, and tell the user. Their site contradicts their own rules.
- **A weaker page than they could use.** If the user's URL doesn't carry the keywords and a better page
  exists, keep their URL, flag the gap, and name the better page. If they agree, change `final_url` and
  each keyword's `landing_page` together.

List landing-page gaps for the brief: offer in the ad but not on the page, CTA mismatch, thin proof.

## Step 3: Competitor context

Start from the product skill's competitive frame: who the rivals are, where to fight, where to
concede. For ad groups built on a competitor's name, also fetch that competitor's own pricing or
landing page (one or two pages) so the copy answers what they claim today. Don't scrape Google results pages.

Use competitor research to choose the angle (switching reason, cost transparency, what you do that
they can't) and to avoid claims you can't prove. It is never a source of lines to copy.

Competitor names:
- Allowed in headlines, descriptions and display paths of ads whose ad group is built on that competitor. Set `competes_with` on the ad in the payload.
- Not allowed in generic ad groups or in sitelinks, callouts and snippets.
- Never "#1", "best", or "cheaper than X" without proof. Never disparage.
- Every named use is a trademark-complaint risk. The check script logs each one; carry that into the notes cell and the chat brief.

## Step 4: Plan before you write

Per ad group, write a short plan: primary intent, the one job it speaks to, three or four angles
(keyword echo, outcome, proof, differentiator, offer, risk reducer), and which keywords must appear
verbatim. Why: an RSA is recombined by Google, so what matters is coverage across angles with each
line standing alone, not one tidy sentence split into 15 pieces.

Plan the assets too: four or more sitelink destinations (real pages from Step 2), four or more callout
facts with the page that backs each, and a snippet header whose values you can fill honestly.

Note who else the keywords attract (learners, students, hobbyists, the wrong segment). Add a qualifier
headline where it helps, and recommend negatives in the brief. Don't add negatives yourself.

Decide one ad or two. Run a second RSA in an ad group only when it tests a different angle. A mixed-intent
ad group still gets one lead ad: its CTA mix follows the highest priority keyword, and a soft
description CTA beside direct headline CTAs is fine.

## Step 5: Write

Follow `references/rsa-playbook.md` for headline and description recipes, intent-to-angle mapping, paths,
pinning and the hypothesis cell. Follow `references/assets-playbook.md` for sitelinks, callouts and
snippets. Follow `references/policy-checklist.md` for what Google disapproves and how to handle claims.

The short version:
- 15 headlines and 4 descriptions for the lead ad. Each headline reads correctly beside any other.
- Echo the High priority keywords in a headline. Choose the longest variant so shorter sibling keywords
  sit inside it. Echo headlines are exempt from the "don't open on the same words" rule. Readability
  beats the template's "In a headline?" check: if a keyword reads like a typo ("multi cloud"), write the
  natural form ("Multi-Cloud") and say in the notes that the check will show No.
- Claims come only from the product skill's safe list, within its guardrails. Grade D or HIGH risk claims never appear. Medium-risk claims appear only when the landing page repeats them.
- Sitelink URLs are real pages you fetched. Never invent a path.
- Write it in the product skill's voice. Plain words, specific nouns, no "unlock", "seamless", "streamline".

Before you move on, run the copy through the `stop-slop` skill if it is available. Use its filler and
structure rules on every line, and its scoring on the descriptions read as one draft; revise below 35/50.
In 30-character headlines, limits, policy and message match outrank its adverb and passive-voice rules.
Keep "Trusted by" if the alternative is a worse headline, but prefer the active form when it costs nothing.

## Step 6: Check, then fill

Write the payload JSON to a scratch location (not the skill folder, not the user's repo). Schema in
`references/template-map.md`; a passing example is `references/example-payload.json`. Build the
guardrail lists from the product skill's table: one regex per row in `blocked_claims` or `hedged_claims`.
Where the product skill contradicts itself, the guardrail table wins. Put every named customer from the
proof points in `customers`.

```bash
python3 <skill>/scripts/check_copy.py payload.json --template <template.xlsx> --verify-urls
```

Fix every ERROR. Read every WARN and either fix it or keep it for a reason you can state. INFO lines
(competitor-name use, named customers, keywords not in a headline) go into the brief. Then:

```bash
python3 <skill>/scripts/fill_template.py --template <template.xlsx> --payload payload.json \
    --out "<template stem> - filled.xlsx"
```

Save the output next to the user's workbook, or in the working directory when you used the bundled
template. Never save into the skill folder. The script validates again, writes into the first free rows,
clears the fictional sample rows, and verifies the saved file. If it exits non-zero, don't hand the file
over; fix the cause. If Python isn't available, offer the same rows as tab-separated blocks in template
column order.

## Step 7: Hand back

Give the path to the filled file, one block per ad group, and one block for the campaign's assets. Keep
it short; the copy is in the file.

```
**AD-001 · rivalapp alternative**  Ready, 15 headlines, 4 descriptions
Angle: switching and migration, cost as the test arm.
Tests: H3, H4, D2 against H8, H14, D4. Read asset labels once they leave Learning.
Flags: competitor name in H1, D1, path2 (complaint risk). H11 names customers (needs sign-off).
Landing page gaps: free import is not on the page yet.

**Assets · Search | Project Mgmt | Competitor Alternatives**  4 sitelinks, 5 callouts, 1 snippet (Types)
Pages: every sitelink fetched and loads. Callouts backed by the homepage and /import.
Flags: sitelink "Customer Stories" names Fabrikam (sign-off).
```

Then a short **Needs your decision** list: a better landing page, offers whose terms the page omits,
unapproved claims you left out, customers to clear, negatives to add, keywords too long for any
headline, ad groups you'd split, anything you assumed. Say what you verified (check script, URL
fetches, claims grepped in raw HTML) and what you didn't (the workbook has not been opened in Excel;
connector queries not run unless you ran them).

## Refreshing live ads

If the connector shows existing RSAs for the ad group, treat the job as a refresh. Keep assets labelled
BEST or GOOD, replace LOW, leave LEARNING alone, preserve pins unless they're wrong, and list what you
replaced in the notes cell and the brief. Don't rewrite a working ad from scratch.
