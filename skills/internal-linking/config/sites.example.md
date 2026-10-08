# Site config (example)

Copy this file to `config/sites.md` and fill it in. The skill reads it at the start of every run, shows the writer the default site list, and asks what to add or remove. Without it, the skill asks for the sites each time.

## Sites

**Default home site:** example.com (where drafts publish unless the writer says otherwise)

| Site | In scope by default | Search Console property | Covers |
|---|---|---|---|
| https://example.com | yes (home) | sc-domain:example.com | Core product: what it is, who it's for, the problems it solves |
| https://sister-brand.com | yes | https://sister-brand.com/ | Sister product's topic. Link here only when the draft covers it. |

Use the property string exactly as Search Console lists it (`sc-domain:` for domain properties, the full URL with trailing slash for URL-prefix properties).

## Money pages and exclusions

Put regexes in `config/patterns.json` (copy `config/patterns.example.json`). `"money"` lists the paths that count as commercial pages for that host. It replaces the built-in defaults, which cover `/platform`, `/product(s)`, `/solutions`, `/features`, `/pricing`, `/integrations`, `/use-cases`, `/industries`, `/why-*`, `/demo`, `/compare` and `*-alternative(s)`. `"exclude"` adds paths to drop on top of the built-in ones (translations, thank-you, tag/category/author archives, legal, signup/login, contact, listing pages). The `"*"` key applies to every site. The scripts apply the file automatically whenever they read the cache.

## House rules (optional)

Anything writers have agreed on that should override the defaults in `references/linking-rules.md`, e.g. "no more than 8 links per post", "always link the product page once", "never link the pricing page from blog posts".
