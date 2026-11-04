# Template map and payload schema

How the Google Ads Copy Template is laid out, what `scripts/` write into it, and the JSON the
scripts take. Read this before writing a payload or when a script complains.

## The workbook

A blank copy ships in `assets/Google_Ads_Copy_Template.xlsx`. Fill a copy of it; never save into the
skill folder.

| Tab | Rows | You write (input columns) | Template calculates |
|---|---|---|---|
| Keywords & Intent | 6 to 155 | A Keyword, B Match type, C Intent, D Campaign, E Ad Group, F Landing page URL, G Priority, I Ad angle / notes | H "In a headline?" (Yes when the keyword text sits inside any headline of that ad group) |
| RSA Ads | 6 to 105 | A Ad ID, B Campaign, C Ad Group, D Status, E Owner, K Final URL, L Path 1, M Path 2, N to AB Headline 1 to 15, AC to AF Description 1 to 4, AG Pinning / test hypothesis, AH Notes | F headlines filled, G descriptions filled, H over-limit fields, I duplicate headlines, J Check |
| Sitelinks | 6 to 105 | A ID, B Campaign, C Ad Group (blank = campaign level), D Status, E Owner, G Link text, H Description 1, I Description 2, J Final URL, K Notes | F Check |
| Callouts | 6 to 105 | A ID, B to E as above, G Callout text, H Notes | F Check |
| Snippets | 6 to 105 | A ID, B to E as above, G Header, H to Q Value 1 to 10, R Notes | F Check |
| Ad Generator | n/a | C4 Ad ID to preview | Search-result preview, five random combinations, character counters |
| Lists | n/a | n/a | Dropdown values: Status, Match type, Intent, Priority, Snippet header |
| Instructions | n/a | n/a | Workflow, colour legend, limits |

Row 6 on every tab is a fictional sample (TaskFlow). The filler overwrites it and clears any other
sample rows on a tab it writes to. It recognises a sample row by the text `taskflow.example.com` or
`Sample row: replace me`, so don't use either in real data.

Limits as the template states them: headline 30, description 90, display paths 15 each, sitelink
text 25, sitelink descriptions 35 each, callout 25, snippet value 25 (3 to 10 values).

The Check column on RSA Ads reads, in order: Over limit, Duplicate headline, Need 3+ headlines,
Need 2+ descriptions, Add final URL, OK - add more headlines (fewer than 8), Ready.

## Payload schema (`payload.json`)

A complete, passing example lives in `example-payload.json` next to this file. Every top-level key
except the lists you are writing is optional.

```jsonc
{
  "defaults":  {"status": "Draft", "owner": ""},          // applied when a row omits them
  "meta": {},                                             // ignored by the scripts; free-form provenance
  "competitors":   ["RivalApp", "OtherCo"],               // names that need competes_with to appear
  "customers":     ["Contoso", "Fabrikam"],               // named customers; each use is logged for sign-off
  "blocked_claims": ["80\\s?%", "2\\s?-\\s?3\\s?x"],       // regex; any hit is an ERROR
  "hedged_claims":  ["under (60|a) (seconds?|minute)"],   // regex; any hit is a WARN
  "acronyms": ["MFA"],                                    // extra all-caps words that are fine

  "keywords": [{"keyword", "match_type", "intent", "campaign", "ad_group", "landing_page", "priority", "notes"}],
  "ads": [{
    "id": "AD-004",                 // optional; the next free AD-nnn is assigned when omitted
    "campaign", "ad_group", "status", "owner",
    "final_url", "path1", "path2",
    "headlines": ["... up to 15"], "descriptions": ["... up to 4"],
    "hypothesis": "pinning and what this ad tests",
    "notes": "claims used and their source, landing page gaps, review flags",
    "competes_with": ["RivalApp"],          // competitor names this ad group is built around
    "claims_substantiated": ["best"]        // superlatives the user confirmed they can prove
  }],
  "sitelinks": [{"campaign", "ad_group"?, "text", "desc1", "desc2", "final_url", "notes"}],
  "callouts":  [{"campaign", "ad_group"?, "text", "notes"}],
  "snippets":  [{"campaign", "ad_group"?, "header", "values": ["3 to 10"], "notes"}]
}
```

`blocked_claims` and `hedged_claims` come from the product skill's claim guardrails: grade D or HIGH
risk goes in blocked, medium risk goes in hedged. Write one regex per guardrail row, and cover each
phrasing the claim could take. `customers` comes from the proof points. `competes_with` and
`claims_substantiated` can also sit on a sitelink, callout or snippet.

Dropdown fields (status, match_type, intent, priority, snippet header) must match the Lists tab
exactly. `check_copy.py --template` reads the real lists from the workbook.

## Scripts

Stdlib-only Python (3.9 or newer; tested on 3.14). Run them as `python3 <skill>/scripts/<name>.py`.
`openpyxl` is not needed.

| Script | Does |
|---|---|
| `read_template.py T.xlsx [--only keywords,ads,...]` | Dumps real (non-sample) rows as JSON in payload shape, plus the Lists values. Use it to read the Keywords & Intent tab as the brief and to see copy that already exists. |
| `check_copy.py payload.json --template T.xlsx [--verify-urls] [--json]` | Limits, duplicates, the template's Check rules, policy patterns, competitor rule, claim guardrails, keyword coverage. Exit 1 on any ERROR. `--verify-urls` fetches each URL once to catch invented pages. |
| `fill_template.py --template T.xlsx --payload p.json --out O.xlsx [--dry-run] [--force] [--overwrite]` | Validates, writes into the first free rows, refreshes cached Check values, saves a new file, then verifies the result. Refuses to write over the template or to fill with ERRORs unless `--force`. |

How the filler stays safe: it edits cell XML in place and copies every other part's content
unchanged (the zip is recompressed, so the file size differs slightly). After saving it confirms that dropdown blocks, data validations, conditional formats, row
counts and every formula are unchanged, that untouched parts are identical, and that each row it wrote
reads back. A failed check exits non-zero and says not to hand the file over.

## Gotchas

- **Do not round-trip the workbook through openpyxl.** The Status, Match type, Intent, Priority and
  Snippet header dropdowns live in x14 extension blocks that openpyxl drops on save.
- Excel recalculates every formula when it opens the file (`fullCalcOnLoad`). The cached values the
  filler writes only matter for viewers that do not recalculate, such as previews.
- Capacity is 100 rows per asset tab and 150 keywords. Past that, copy the last row down in Excel
  first. The filler stops with a clear message instead of overflowing.
- The "In a headline?" column uses Excel's `SEARCH`, where `?` and `*` are wildcards. The script and
  the cached values use a plain substring test, so a keyword containing `?` or `*` can differ.
- The Ad Generator tab ignores pinning and picks combinations at random. It is a preview.
- The RSA Ads headers follow Google Ads Editor's column names, so the block can be pasted into
  Editor's paste tool. Try one or two rows first.
- The workbook has no pin columns. Pinning intent goes in the "Pinning / test hypothesis" cell.
