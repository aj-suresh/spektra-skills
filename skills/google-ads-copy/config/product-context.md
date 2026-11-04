# Product context map (CloudLabs)

The skill never stores product facts. It reads them from a product skill at run time, so a change to
the product skill reaches the next ad group with no edit here. This file says which product skill
covers which ad groups and where to find the file.

Edit the table when a product skill is added or renamed.

## Segments

| Segment | Product skill | Pick it when the ad group, keywords or landing page are about |
|---|---|---|
| ISV | `cloudlabs-isv` | Software and SaaS vendors. POCs, demo environments, solutions-engineer capacity, trials, partner enablement, events, cloud cost of labs. Competitor and alternative terms for CloudShare, Instruqt, Skillable, Qwiklabs. Pages under cloudlabs.ai aimed at ISVs. |
| Higher Ed | `cloudlabs-edu` | Colleges, polytechnics, universities. Azure Lab Services retirement and migration, course labs, LMS integration, instructors and students. Pages under cloudlabs.ai aimed at education. |

If one ad group mixes both segments, ask which it is for. Do not blend the two contexts into one ad.

## Where to find a product skill's SKILL.md

These skills are manual-invoke (`disable-model-invocation: true`), so the Skill tool refuses to load
them. Read the file directly. Check in this order and stop at the first hit:

1. `../<name>/SKILL.md`, relative to this skill's folder. In the spektra plugin and in a symlinked
   `~/.claude/skills/`, the product skills sit next to this one.
2. `~/.claude/skills/<name>/SKILL.md`
3. `./.claude/skills/<name>/SKILL.md`
4. `~/.claude/plugins/cache/*/*/*/skills/<name>/SKILL.md` (plugin install; take the highest version)
5. `~/.claude/plugins/marketplaces/*/skills/<name>/SKILL.md`

Fallback: `find ~/.claude -path "*/skills/<name>/SKILL.md" 2>/dev/null`. If nothing turns up, ask the
user for the path or for a product brief, and say what you are missing.

What to pull from the product skill is in `references/context-pack.md`. For these two skills, the
claim guardrails are the "Claim guardrails" table, the safe proof points are under "Proof points", and
the competitive frame is under "Competitive frame".
