# Policy and claims checklist

Two separate concerns. Google's editorial policy decides whether an ad runs. The product skill's claim
guardrails decide whether the ad is honest. `scripts/check_copy.py` enforces both as far as patterns
allow. It is a safety net, not a ruling.

Policy patterns here are the ones understood when this skill was written. Google changes them. If the
script flags something you believe is allowed now, check Google's editorial policy pages before
overriding, and record the reason in the notes cell.

## Google editorial patterns

| Rule | In practice | Script |
|---|---|---|
| Exclamation marks | None in headlines, sitelink text or callouts. At most one in a description | ERROR |
| Repeated punctuation | No `!!`, `??`, `...` | WARN |
| Symbols and emoji | Avoid stars, ticks, arrows, bullets, trademark glyphs | WARN |
| Capitalisation | No ALL CAPS words except real acronyms (SOC, ISO, AWS, POC). Extend with `acronyms` | WARN |
| Unverifiable claims | "Best", "#1", "leading", "fastest", "cheapest", "guaranteed" need third-party proof Google can see. Cut them, or list them in `claims_substantiated` once the user confirms the proof | ERROR |
| Absolute words | "Only", "perfect", "ultimate" invite a claims review | WARN |
| Phone numbers | Not in ad text. Use a call asset | ERROR |
| Gimmicky calls to action | "Click here", "Click now" | ERROR |
| Trailing full stop in a headline | Often rejected | WARN |
| Duplicates | Identical headlines or descriptions in one ad | ERROR |
| Destination | Final URL loads, uses https, matches what the ad promises | ERROR if not https; `--verify-urls` for reachability |
| Trademarks | A competitor's name in ad text can be restricted if its owner complains. Fine in keywords | See below |

## Competitor names

Allowed only in ads whose ad group is built around that competitor, listed in `competes_with` on the
ad. Generic ad groups and every extension stay name-free unless the item itself lists the competitor.
Keep the claim factual and checkable on the landing page. Each named use is logged as INFO. Put it in
the notes cell ("Competitor name in H1, D1: trademark complaint risk") and in the chat brief, so
whoever approves the ad knows.

Never write "#1 alternative to X", "cheaper than X", or anything that compares price or performance
without a sourced figure on the landing page.

## Claim handling

1. **Read the product skill's guardrail table.** It grades each claim. If the product skill contradicts
   itself (a claim graded Medium in the table but offered as plain proof in a job card), the table wins.
2. **Map grades to the payload.**
   - Grade D, HIGH risk, "never state as fact": add a regex to `blocked_claims`. These never appear.
     Write one per row, and allow for rewordings ("in hours, not weeks", "weeks to hours").
   - Medium risk (vendor claim, per-unit figure, not peak-load): add to `hedged_claims`. They appear
     only when the landing page repeats them. Flag in notes.
   - Safe, named, specific proof points: usable. Cite the source in the notes cell ("Proof points:
     SOC 2 Type II report").
3. **Check the landing page** for each claim used, against the raw HTML. A claim the page lacks is a
   landing-page gap. List it. If the page itself states a blocked claim, don't repeat it and tell the user.
   Offers (trial, demo length, price) come from the page, not the product skill. Use one only when the
   page states it, and flag missing terms.
4. **Numbers need context.** A customer figure with no period or unit ("1,700+ deployments") misleads.
   Use only the framing the product skill allows, or leave the number out.
5. **Named customers** in ad text usually need the customer's approval. List them in `customers`; the
   script logs each use as INFO. Flag them for sign-off even if the product skill lists them as safe for
   use elsewhere. That includes sitelink descriptions.
6. **A question to ask the prospect is not an ad.** The product skill sometimes says "ask, don't assert".
   An ad can't ask for the prospect's number. Omit the claim.

## When the script and your judgment disagree

An ERROR you want to keep means either the rule needs an override the schema allows
(`claims_substantiated`, `competes_with`) or the line should change. Don't edit the checker to pass.
If a rule is wrong for the account, tell the user and let them decide.
