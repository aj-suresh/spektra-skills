# Reading the account through the Google Ads connector

The connector exposes `ads_list_accessible_customers`, `ads_get_resource_metadata` and `ads_search`
(GAQL). Use them to learn what the account already runs. **Read only. Never create, edit or pause
anything.** The connector's tool names carry a long server prefix that differs per install; match on the
suffix.

**Status of these queries.** Field names for `ad_group_ad`, `ad_group_ad_asset_view`, `ad_group_criterion`
and `search_term_view` were checked against the connector's own resource metadata. The queries
themselves have not been run against a live account. If one is rejected, call `ads_get_resource_metadata`
for the resource and fix the field name rather than guessing.

## Setup

- `customer_id` is digits only. Strip hyphens from `123-456-7890`.
- If the user hasn't given one, call `ads_list_accessible_customers` and ask which account.
- Money is in micros: divide `metrics.cost_micros` by 1,000,000.
- Dates are `YYYY-MM-DD`, or a named range such as `segments.date DURING LAST_30_DAYS`.
- Set `limit` on every query. Narrow with `conditions` (campaign or ad group name) before pulling more.

## Queries

Each is one `ads_search` call: `resource`, `fields`, `conditions`, `orderings`, `limit`.

**1. Search campaigns and ad groups**

- resource `ad_group`
- fields `campaign.name`, `campaign.status`, `ad_group.id`, `ad_group.name`, `ad_group.status`
- conditions `campaign.advertising_channel_type = 'SEARCH'`, `ad_group.status != 'REMOVED'`, `campaign.status != 'REMOVED'`

**2. Keywords in an ad group**

- resource `ad_group_criterion`
- fields `campaign.name`, `ad_group.name`, `ad_group_criterion.keyword.text`,
  `ad_group_criterion.keyword.match_type`, `ad_group_criterion.status`,
  `ad_group_criterion.quality_info.quality_score`, `ad_group_criterion.final_urls`
- conditions `ad_group_criterion.type = 'KEYWORD'`, `ad_group_criterion.negative = FALSE`,
  `ad_group_criterion.status != 'REMOVED'`, and `ad_group.name = '<name>'`

Map match types to the template's list: `BROAD` to Broad, `PHRASE` to Phrase, `EXACT` to Exact.
The account has no intent or priority. Propose them and say you did.

**3. Live responsive search ads**

- resource `ad_group_ad`
- fields `campaign.name`, `ad_group.name`, `ad_group_ad.ad.id`, `ad_group_ad.status`,
  `ad_group_ad.ad_strength`, `ad_group_ad.ad.final_urls`,
  `ad_group_ad.ad.responsive_search_ad.headlines`, `ad_group_ad.ad.responsive_search_ad.descriptions`,
  `ad_group_ad.ad.responsive_search_ad.path1`, `ad_group_ad.ad.responsive_search_ad.path2`
- conditions `ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'`, `ad_group_ad.status != 'REMOVED'`

The headlines and descriptions fields return the text and any pin position for each asset.

**4. Asset performance labels** (what to keep and what to replace)

- resource `ad_group_ad_asset_view`
- fields `ad_group.name`, `ad_group_ad_asset_view.field_type`,
  `ad_group_ad_asset_view.performance_label`, `ad_group_ad_asset_view.pinned_field`,
  `ad_group_ad_asset_view.asset`, `metrics.impressions`
- conditions `ad_group_ad_asset_view.field_type IN ('HEADLINE','DESCRIPTION')`,
  `ad_group_ad_asset_view.enabled = TRUE`, `segments.date DURING LAST_30_DAYS`

`asset` comes back as a resource name. To get its text, run a second query on the `asset` resource
(`asset.resource_name`, `asset.text_asset.text`) and match on the resource name. Labels: BEST and GOOD
keep, LOW replace, LEARNING and PENDING leave alone.

**5. Search terms** (the searcher's real wording, and where the wording drifts from the keywords)

- resource `search_term_view`
- fields `search_term_view.search_term`, `campaign.name`, `ad_group.name`, `metrics.impressions`,
  `metrics.clicks`, `metrics.ctr`, `metrics.conversions`, `metrics.cost_micros`
- conditions `segments.date DURING LAST_30_DAYS`, `metrics.impressions > 0`
- orderings `metrics.impressions DESC`, limit 100

Use converting terms' wording in headlines. Report terms that show a mismatch between keyword and intent
(an informational query on a transactional ad group) as an INFO in the brief. Don't add negatives yourself.

**6. Existing sitelinks, callouts and snippets** (optional, to avoid duplicates)

- resource `campaign_asset`
- fields `campaign.name`, `campaign_asset.field_type`, `campaign_asset.status`,
  `asset.sitelink_asset.link_text`, `asset.callout_asset.callout_text`,
  `asset.structured_snippet_asset.header`, `asset.structured_snippet_asset.values`
- conditions `campaign_asset.field_type IN ('SITELINK','CALLOUT','STRUCTURED_SNIPPET')`,
  `campaign_asset.status != 'REMOVED'`

These `asset.*` fields are the least verified of the six. If the connector rejects them, skip this query
and say duplicates weren't checked.

## What to do with the results

- **Brief:** ad groups, keywords and match types become the Keywords & Intent rows.
- **Copy:** converting search terms inform the keyword-echo headlines. Live RSA text is the baseline for
  a refresh. Don't repeat a live headline unless it is labelled BEST.
- **Refresh:** follow "Refreshing live ads" in SKILL.md. Record what you replaced in the notes cell.
- **Privacy:** the account data is the user's. Summarise it for the task. Don't paste raw rows into the
  workbook beyond keywords and the copy itself.
