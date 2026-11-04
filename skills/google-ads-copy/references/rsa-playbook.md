# RSA playbook

How to build the responsive search ad for one ad group. Limits are the template's: headline 30
characters, description 90, display paths 15 each.

## Shape

- **15 headlines and 4 descriptions** for the lead ad. Google builds each impression from up to three
  headlines and two descriptions out of your pool, so a bigger, more varied pool gives it more to try
  and gives you more to learn from. The template marks fewer than 8 headlines amber.
- **One RSA per ad group by default.** Add a second only when it tests a different angle. Google
  allows three, but splitting a small ad group's traffic slows every test.
- **Every line stands alone.** You don't control order unless you pin, so each headline must read
  correctly beside any other. No "Step 1", no sentence split across two headlines, no pronoun that
  points at a headline you can't guarantee is shown.

## Headlines

| Slot | Count | Job | What goes in it |
|---|---|---|---|
| Keyword echo | 2 to 3 | Show the searcher their own words | The top keywords, verbatim, as a natural phrase |
| Outcome | 3 to 4 | What changes for the persona | The job-to-be-done result in the buyer's terms |
| Proof | 2 to 3 | A reason to believe | Named customers (if cleared), certifications, scale figures the product skill marks safe |
| Differentiator | 2 | Why this over the alternative | From the competitive frame. Competitor name only when `competes_with` is set |
| Offer or CTA | 2 | The next step | What the landing page's primary CTA actually says |
| Risk reducer or qualifier | 1 to 2 | Remove doubt, or filter bad clicks | "Built for Agencies", "Free Setup Help", a plain price or plan fact |

**Keyword echo and the template's check.** The "In a headline?" column tests whether the keyword text
sits inside some headline of that ad group. When two keywords are siblings ("rivalapp alternative",
"rivalapp alternatives"), write the longer one as the headline. It contains the shorter, so one
headline satisfies both. A keyword longer than 30 characters can't fit; use its closest natural phrase
and expect a "No".

**Length.** Mix them. Aim for at least three short headlines (20 characters or fewer) and three long
ones (24 to 30). Short lines let three headlines share a row. The script warns when either group runs
short. Count with the script; don't eyeball it.

**Form.** Pick Title Case or sentence case and hold it across the ad. Digits for numbers. "&" is fine
and saves characters. No full stop at the end, no exclamation mark, no emoji.

**Variety.** No two headlines that open on the same words or restate the same fact. "Free Trial" and
"Free 14-Day Trial" count as one idea. Each headline should add something a different one doesn't.
Keyword-echo headlines are exempt: two keywords that start "Project Management" can both open that way.

**When the keyword reads badly.** A keyword like "e commerce platform" has no hyphen. Echoed
verbatim it looks like a typo; written "E-Commerce Platform" it fails the template's substring check.
Readability wins. Write the natural form, note in the notes cell that "In a headline?" will show No, and
let the keyword still earn its place through the description and a close headline.

| Weak | Why it fails | Stronger |
|---|---|---|
| Best Project Tool | Superlative with no proof, tells the reader nothing | Boards, Gantt & Timelines |
| Unlock Seamless Workflows | Filler verbs, no concrete noun | Replace Your Spreadsheets |
| Learn More | No reason to click | Compare Plans Side by Side |
| We Lead in Project Management | Brand first, reader second | Project Management Software |

## Descriptions

Four lines, four jobs. Each one stands alone, ends with a full stop, and uses 70 to 90 characters
(the script only warns under 50).

1. **Query, benefit, CTA.** Echo the keyword, state the core outcome, give the next step.
2. **Differentiator or proof,** with one specific fact.
3. **How it works, or the main objection answered.** Use the objections in the product skill.
4. **Offer and CTA,** matched to what the landing page asks for.

Don't end all four on the same CTA verb. Don't repeat a headline's words as a description's opening.

**Mixed intent.** One ad group can hold Commercial and Transactional keywords. Write one lead ad whose
CTA temperature follows the highest priority keyword. A soft description CTA ("See how it works") beside
direct headline CTAs ("Book a 30-Minute Demo") is fine. Split into two ad groups only if the keywords
need different landing pages.

## Intent to angle

| Keyword intent | Angle | CTA temperature |
|---|---|---|
| Transactional | Offer, speed, proof. The searcher is ready | Direct: "Book a Demo", "Start Free" |
| Commercial | Differentiators, comparison, proof against the alternative | Soft: "See How", "Compare" |
| Informational | Usually not a paid priority. If it runs, teach first and offer something low-friction | Soft, no hard sell |
| Navigational | Confirm the brand, send them to the right page; sitelinks do the work | Direct |

**Competitor and alternative ad groups.** The searcher is mid-decision and often at a renewal. Lead
with the switching reason, remove the fear of migration, and be open about cost. Compete on the axis the
product skill names (for example, running the customer's own SaaS inside the lab), not on price claims
you can't source. Don't attack the rival.

## Display paths

Two paths, 15 characters each, hyphens instead of spaces, letters and digits only. They should describe
the page's theme or the searcher's term and need not exist as real URLs. They follow the same
competitor-name rule as headlines.

## Pinning

Default to no pins. Pinning shrinks the pool Google can combine and usually lowers ad strength. Pin only
for a legal line that must show, a brand requirement, or to hold a High priority exact keyword in
position 1. The workbook has no pin columns, so write the intent in the "Pinning / test hypothesis"
cell: "Pin H1 to position 1: exact-match keyword must show."

## The hypothesis cell

Every ad says what it tests. Name the arms by line number so someone can read the result later.

> No pins. Test the switching angle (H3, H4, D2) against the cost angle (H8, H14, D4). Read asset
> performance labels once they leave Learning.

Don't invent traffic thresholds. You don't know the account's volume. Point at the asset labels: BEST
and GOOD keep, LOW gets replaced, LEARNING waits.

## Ad strength

Google rates RSAs Poor to Excellent from asset count, variety, keyword use and pinning. The template
doesn't show it. Treat it as a diagnostic. Don't pad with filler to reach Excellent; a relevant ad rated
Good beats a vague one rated Excellent.

## Message match

The ad promises what the landing page delivers. Headline and CTA vocabulary should appear on the page.
If a good line depends on a page change ("Migration Help Included" when the page doesn't say so), keep it
only if you list the gap in the notes cell and the brief.

A complete, passing example is in `example-payload.json`.
