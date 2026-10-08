# Spektra Skills

Claude Code skills that are only relevant to CloudLabs.ai or Spektra Systems, kept here so they follow me across machines (not synced automatically by Claude Code).

## What's here

- `skills/cloudlabs-isv` — CloudLabs GTM context for the ISV (software / SaaS vendor) segment. Invoke with `/cloudlabs-isv`.
- `skills/cloudlabs-edu` — CloudLabs GTM context for the Higher Education segment. Invoke with `/cloudlabs-edu`.
- `skills/internal-linking` — Adds internal links to a blog draft (Word or Google Doc). It crawls the sitemaps of cloudlabs.ai, saasify.ai, cspcontrolcenter.com and spektrasystems.com, checks Search Console, inserts links into a copy of the draft, and lists existing pages that should link back. It runs automatically when you ask for internal links, or you can type `/internal-linking`.

The two cloudlabs skills are manual-invoke only (`disable-model-invocation: true`). Claude never loads them on its own, only when you type the slash command.

### internal-linking: team notes

- **Site list and rules:** `skills/internal-linking/config/sites.md` (which sites, which topics belong where, house rules) and `config/patterns.json` (money-page and exclusion regexes per site). Edit and push these to change behaviour for everyone.
- **Needs:** Python 3 (the first run creates a small venv with python-docx in `~/.cache/internal-linking/`). On Windows, run Claude Code from WSL or Git Bash, because `scripts/run.sh` is a bash script.
- **Search Console:** used when the Google Search Console connector is enabled in Claude. Without it the skill still works and says so in its report.
- **Google Docs:** download the doc as .docx (File → Download → Microsoft Word), run the skill on it, then upload the `– linked.docx` copy back to Drive. Links survive the conversion.
- A generic version (no Spektra config) is public at [aj-suresh/aeo-content-skills](https://github.com/aj-suresh/aeo-content-skills).

## Install via plugin marketplace (recommended for the team)

This repo is public, so no GitHub login or access request is needed.

```bash
claude plugin marketplace add aj-suresh/spektra-skills
claude plugin install spektra@spektra-skills
```

Restart Claude Code (or the desktop app) afterwards. Skills are namespaced by plugin, so the manual ones are `/spektra:cloudlabs-isv` and `/spektra:cloudlabs-edu`. `internal-linking` triggers on its own when you ask for internal links.

**Updating:** `claude plugin marketplace update spektra-skills`, then `claude plugin update spektra@spektra-skills`. Updates only arrive when the `version` in `.claude-plugin/plugin.json` changes, so bump it with every push.

**Maintainers:** don't use the symlink setup below on the same machine as the plugin install, or each skill appears twice.

## Setup on a new machine (symlinks, for maintainers)

Clone this repo, then symlink each skill folder into `~/.claude/skills/` so edits here are picked up automatically without a copy step.

**macOS / Linux:**
```bash
git clone https://github.com/aj-suresh/spektra-skills.git ~/spektra-skills
mkdir -p ~/.claude/skills
ln -s ~/spektra-skills/skills/cloudlabs-isv ~/.claude/skills/cloudlabs-isv
ln -s ~/spektra-skills/skills/cloudlabs-edu ~/.claude/skills/cloudlabs-edu
ln -s ~/spektra-skills/skills/internal-linking ~/.claude/skills/internal-linking
```

**Windows (PowerShell, run as the user — no admin needed for a directory symlink you own):**
```powershell
git clone https://github.com/aj-suresh/spektra-skills.git $HOME\spektra-skills
New-Item -ItemType Junction -Path "$HOME\.claude\skills\cloudlabs-isv" -Target "$HOME\spektra-skills\skills\cloudlabs-isv"
New-Item -ItemType Junction -Path "$HOME\.claude\skills\cloudlabs-edu" -Target "$HOME\spektra-skills\skills\cloudlabs-edu"
New-Item -ItemType Junction -Path "$HOME\.claude\skills\internal-linking" -Target "$HOME\spektra-skills\skills\internal-linking"
```

If you'd rather not symlink, a plain copy of `skills/<name>` into `~/.claude/skills/<name>` also works — you'll just need to re-copy after future edits.

## Adding a new skill later

Create it under `~/.claude/skills/<name>/`, then move (or symlink) it into `skills/` here and push.
