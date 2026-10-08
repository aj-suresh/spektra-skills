# Site config: Spektra Systems

The skill reads this at the start of every run. **Always show the writer this site list and ask which sites to include or remove for this draft**, and which one it publishes on. The sites change from post to post.

## Sites

**Default home site:** cloudlabs.ai. The other three are searched too by default.

| Site | In scope by default | Search Console property | Covers |
|---|---|---|---|
| https://cloudlabs.ai | yes (home) | sc-domain:cloudlabs.ai | Hands-on lab platform: virtual labs, cloud sandboxes, POCs, sales demos, self-service trials, immersion workshops and hackathons for ISVs, GSIs and Microsoft/AWS partners; employee and customer training; Azure Lab Services migration (VM Labs); higher-ed and K-12 labs, LMS integration, lab-based skill assessments |
| https://saasify.ai | yes | https://saasify.ai/ | Cloud marketplace GTM for ISVs: Azure/AWS/Google Cloud Marketplace listings, private offers, co-sell, marketplace funding (MDF, POC funding), marketplace analytics and RevOps |
| https://cspcontrolcenter.com | yes | sc-domain:cspcontrolcenter.com | Microsoft CSP partners: NCE billing and invoicing automation, margins and pricing, subscription/license management, Partner Center sync, PSA and accounting integrations (ConnectWise, Autotask, QuickBooks, Xero, Stripe), customer self-service marketplace |
| https://www.spektrasystems.com | yes | sc-domain:spektrasystems.com | Parent company: Microsoft partner services for ISVs and system integrators, company news, trust center, careers. Rarely the best target from a product blog. Use it for company-level claims. |

Note that the sitemap for spektrasystems.com lists `www.` URLs, so pass `https://www.spektrasystems.com` to `inventory.py`.

## Money pages and exclusions

These live in `config/patterns.json` and are applied automatically. Each site has commercial pages at the top level (e.g. cloudlabs.ai `/virtual-labs`, `/cloud-sandbox`; cspcontrolcenter.com `/billing-and-invoicing`), and patterns.json lists them. New product pages show up as type `page` until they're added there, so read titles and treat an obvious product page as commercial anyway.

## House rules

- Sister-site links are welcome when the topic belongs to that site (see "Covers" above), usually 0–2 per post.
- CloudLabs has a large cluster of Azure Lab Services retirement posts. For the retirement or migration concept itself, link **one** page: the migration hub (`/azure-labs-migration-hub`) or `/azure-lab-services-alternative`, whichever Search Console shows is stronger. Supporting posts that cover a *distinct* subtopic (the alternatives comparison, the custom-image transition guide, the pricing calculator) can each earn their own link. Several "ALS is retiring" announcement posts in one draft is the thing to avoid. *(Suggested rule. Edit it to match the team's view.)*
