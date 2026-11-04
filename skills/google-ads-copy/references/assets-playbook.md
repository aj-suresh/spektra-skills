# Sitelinks, callouts and structured snippets

Assets sit under the ad and widen its footprint. Each one is a row on its own tab of the template.
Limits: sitelink text 25, sitelink descriptions 35 each, callout 25, snippet values 25 each (3 to 10).

**Campaign level or ad group level.** Leave `ad_group` blank to apply an asset to the whole campaign.
Set it only when the asset makes sense for that ad group alone. Most assets should be campaign level.

**Competitor names.** Never in an extension unless the item carries `competes_with` for that
competitor. Default is name-free, even in a competitor campaign.

**Source page for every row.** Callouts and snippet values have no URL of their own, so name the page
that backs each one in its notes cell ("/cloud-sandbox: automated cleanup"). A callout the homepage lacks
but a product page states is fine; a callout no page states is not.

**Account context.** If the connector is available, check what the campaign already has before adding
more (`references/google-ads-connector.md`), so you don't create duplicates.

## Sitelinks

Aim for four or more per campaign; the template marks fewer amber.

- **One destination each, all different.** Link text names where the click goes ("Customer Stories"), not
  a slogan ("Discover More").
- **Two description lines that each carry a different fact.** Don't restate the link text.
- **Real pages only.** Pick destinations from the site's navigation or sitemap and fetch each one. Run
  `check_copy.py --verify-urls`. Never guess a path, even a plausible one.
- **Each destination should serve the campaign's intent.** A competitor-alternative campaign wants
  "Compare Plans", import support, a trial sign-up, and customer proof. A generic category
  campaign wants product, use cases, pricing if public, and proof.
- Typical B2B set: how it works or product, pricing or plans (only if the page is public), book a demo,
  customer stories, security and compliance, comparison page.

## Callouts

Short, true attributes. Four or more per campaign.

- Facts the landing page backs: "Managed 24/7 Support", "White-Label Portal", "SOC 2 Type II".
- No punctuation at the end, no exclamation marks, no superlatives, no pricing you can't hold.
- Don't repeat a headline. A callout earns its place by adding a fact the ad body didn't have.
- Keep each under 25 characters; most read best at 12 to 20.

## Structured snippets

A header plus 3 to 10 values. The header must be one of the template's Lists values (Amenities,
Brands, Courses, Degree programs, Destinations, Featured hotels, Insurance coverage, Models,
Neighborhoods, Service catalog, Shows, Styles, Types). Each value must be an instance of the header.

| Header | Values are | Fits |
|---|---|---|
| Service catalog | Services you provide | Setup, data migration, training, support plans |
| Types | Kinds of one thing | Types of lab or environment the product supports |
| Brands | Brand names you carry or work with | Only names cleared for public use |
| Courses | Named courses | Education: courses or lab series offered |
| Degree programs | Named programs | Education: programs the labs support |

If no header fits honestly, skip the snippet. A mismatched header is disapproved.

## Before you fill

- Count per campaign: four or more sitelinks, four or more callouts, at least one snippet.
- No duplicate link text, callout or value inside a campaign.
- Every URL fetched and returns a page.
- Nothing contradicts the landing page.
