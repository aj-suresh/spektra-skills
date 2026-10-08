---
name: cloudlabs-isv
description: CloudLabs go-to-market context for the ISV segment (software / SaaS vendors) - ICP, buying committee, buying centres, jobs-to-be-done, messaging, competitors, proof points and claim guardrails. Manual-invoke only; load when writing or reviewing ISV-facing marketing, sales or strategy work.
argument-hint: "[task, e.g. 'write a LinkedIn ad for SE leaders']"
disable-model-invocation: true
metadata:
  version: 1.0.0
  sources: "CloudLabs Assignment (Ajay Suresh).pptx; ICP Summary | CloudLabs.xlsx; ICP Value Prop Canvas | CloudLabs.xlsx; JTBD Matrix | CloudLabs.xlsx"
---

# CloudLabs: ISV Segment Context

Everything below is CloudLabs' working context for the **ISV (software / SaaS vendor)** segment. Use it as the ground truth for any task that follows: ad copy, emails, landing pages, content briefs, ABM lists, sales enablement, positioning, channel plans.

## How to use this context

1. **Do the task the user asked for.** If they invoked with arguments, that is the task. If not, confirm the context is loaded and ask what they want to work on.
2. **Pick the job first.** Map the task to a job ID in [Jobs, ranked](#jobs-ranked-isv). The job decides the pain, angle, proof, trigger and discovery question to use.
3. **Pick the persona.** Use the [buying committee](#buying-committee) and [buying centres](#buying-centres-land-and-expand) to decide who you're talking to. Each buying centre has its own budget holder and success metric.
4. **Respect the [claim guardrails](#claim-guardrails).** Never state a HIGH-risk claim as fact. When in doubt, ask the question rather than asserting the number.
5. **Lead with peers, not features.** A named security or data vendor (Check Point, Databricks, Wiz, Sophos) beats a feature list for this audience.
6. Scores, SE-hour figures and size bands marked *hypothesis* are unvalidated. Don't present them as research findings.

---

## CloudLabs at a glance

CloudLabs (cloudlabs.ai) is a **managed hands-on lab platform**. It provisions real, pre-built cloud environments across **Azure, AWS, GCP and Oracle**, with the customer's own SaaS integrated into the same lab, for demos, POCs, trials, training, partner enablement and events.

**Positioning statement (draft):** For ISVs, colleges and enterprise training teams whose product or curriculum cannot be shown without real infrastructure, CloudLabs is the managed hands-on lab platform that puts a working environment in front of a prospect, a student or an engineer in under a minute, on any cloud, under your own brand. Unlike lab tools retrofitted from a learning management system, CloudLabs runs the customer's own SaaS and real multi-cloud infrastructure inside the same environment, and operates it for you.

**Qualifying test (more important than vertical or headcount):** *Can the product be shown honestly without real infrastructure?* If yes, CloudLabs is the wrong tool.

### Product capabilities relevant to ISVs

| ID | Capability | Role |
|---|---|---|
| PS-02 | Multi-cloud environments (Azure, AWS, GCP, Oracle) with a custom integration to the ISV's own SaaS in a single lab. Shipped for Check Point, Databricks, Wiz, Sophos. | Core, **most differentiated** |
| PS-03 | Pre-provisioned environments live in under 60 seconds, browser-based, no install. | Core |
| PS-04 | **Validation Center**: trial engagement, feature coverage and drop-off pushed into CRM as MQL signals. | Core |
| PS-05 | Embeddable, ungated demos by iframe or share link, on a marketing page or marketplace listing ("Zero Gated Forms"). | Core |
| PS-06 | White-label end-user portal on the customer's own domain (registration pages, labs, post-event surveys). | Core |
| PS-07 | Instructor VM Shadow: real-time over-the-shoulder view with annotation and live intervention. | Core |
| PS-09 | **Cosmos AI Lab Builder**: generates infrastructure, lab guide and validation logic from a prompt. | Supporting |
| PS-10 | Cloud cost governance: automated provisioning, idle detection, scheduled shutdown, lifecycle mgmt, per-user / per-lab reporting, fixed-price managed option. | Supporting |
| PS-11 | Managed delivery: 24x7 support, pre-allocated multi-region capacity, expert instructors and proctors, end-to-end event operations. | Enabling, gates everything |
| PS-12 | Compliance: SOC 2 Type II, ISO 27001:2022, GDPR, CCPA, FERPA, COPPA, Microsoft SSPA. | Enabling |

**Pricing model for ISVs:** custom (cloud hosting fee + platform fee), based on VMs and users.

---

## ICP definition

| Item | ISV definition |
|---|---|
| **Stage / size** | Series B through public, **200-5,000 employees** (broad ICP). The focused target in the assignment deck narrows this to **501-5,000** (501-1,000; 1,001-2,000; 2,001-5,000). Size band is a *hypothesis*. |
| **Profile** | Infrastructure-complex product that cannot be shown in a click-through demo. Enterprise deals require a POC, an SE team exists, and **it is over capacity**. |
| **Sub-industries** | 1. Cybersecurity  2. Data / AI / Analytics  3. Cloud and DevOps infrastructure |
| **Region** | US and Canada; UK&I; ANZ; India (delivery hub, GSI accounts); EMEA focus on DACH and Nordics. |
| **Departments** | Sales / Solutions Engineering / Pre-Sales / Technical Sales & Support; Product Marketing / GTM Enablement / Training & Delivery; Customer Success / Onboarding / Professional Services; Partner / Channel Sales; DevRel and Technical Evangelism. |
| **Persons of interest** | VP Solutions; VP Technical Sales; VP Product Marketing; Head of Training & Delivery; VP Professional Services; VP Customer Success; VP Partnerships. |
| **Day-to-day owner** | Solutions Engineer, Technical Sales / Support Exec, Systems Engineer, Cloud Architect, Technical Marketing Engineer (TME), Demo Engineer. |
| **Cloud posture** | Azure-first or genuinely multi-cloud. Microsoft partner ecosystem membership, or committed cloud spend (MACC / EDP), is a strong positive signal because it unlocks marketplace purchase and shortens procurement. |
| **Decisive variable** | Whether the ISV has an in-house platform engineering team. If it does, it will build the labs itself. |
| **Addressable universe** | ~800-1,500 infrastructure-complex ISVs (*hypothesis*). |

### Why ISVs are the priority segment (economics)

1. **Multiple buying centres:** Marketing, Partnerships, Presales, Customer Enablement / Training and Technical Support each have a different need and an independent budget.
2. **Higher deal size:** custom pricing on VMs and users; ISVs are assumed to have higher lab usage than universities.
3. **Higher expansion revenue:** land in sales demos, then expand into POCs, trials, customer training, partner enablement and hackathons in the same logo.
4. **Wider sales window:** technical, solution-aware buyers; procurement across teams happens independently throughout the year, driven by triggers (hackathons, enablement, POCs, trials).

> The narrowing is the point: target ISVs whose product *physically cannot* be shown in a click-through demo. That is where CloudLabs is undisputed.

### Disqualify (rule out)

| Exclude | Why |
|---|---|
| **Simple UI-only SaaS** | A click-through demo tool (Storylane, Navattic, Supademo, Arcade, Reprise, Walnut) does the job at a fraction of the price. They cannot fake a firewall, a Spark cluster or a Kubernetes posture scan. Where the product doesn't need a real environment, CloudLabs loses on cost and should never bid. |
| **ISVs under ~200 employees** | No dedicated product marketing or SE function, no budget line for enablement infrastructure, demo volume too low to justify managed delivery. |
| **On-prem / legacy infrastructure, no cloud footprint** | The hosting and integration layer is the limiting factor. A platform decision comes before a lab decision. |
| **Content-only e-learning providers** | Need an LMS and courseware, not live infrastructure. Low ACV, high support burden. |

---

## Triggers and buying signals

**Triggers (why now):**
1. A GTM motion that needs hands-on proof: a launch, a marketplace listing, a user conference, a POC programme.
2. **Sales-engineering capacity crunch:** demo and POC demand has outgrown the team, and headcount is frozen.
3. A partner or channel programme launching and needing scalable enablement.
4. A large technical event (summit, hackathon) with no in-house capacity to run environments.

**Buying signals in the wild:**
- Job postings for Technical Marketing Engineer, Demo Engineer, Sales Engineer or Lab Content Developer, especially with "building demo environments" in the JD.
- New VP of Technical Sales, Solutions, or Training & Enablement; a first Head of Customer Education or Enablement being hired (the function is being formalised and budgeted).
- An announced user conference, summit or hackathon with hands-on workshop tracks on the agenda.
- A new AWS / Azure / GCP Marketplace listing, a new co-sell or ISV partner badge, or joining Microsoft ISV Success / AWS ISV Accelerate.
- A new certification programme, workshop series or partner sales motion.
- A trial or POC programme that is still form-gated and sales-led (no self-service environment exists).
- A Microsoft immersion workshop or GTM event already on their calendar (in the motion, not on our platform).
- Public complaints (G2, forums, Reddit) about the trial or demo being hard to get working.

**Qualification shorthand: "3 in, 2 out"**
- IN: (1) active hiring signal; (2) new certification, hackathon or partner motion; (3) a competitor labs platform already embedded (budget exists, so it's a displacement play).
- OUT: (1) on-prem / legacy infrastructure; (2) simple UI-only SaaS.

---

## Buying committee

Budget sits in **GTM or Customer Success, never in IT**, which speeds things up.

| Role | Titles | What they do | Decision power |
|---|---|---|---|
| **Champion** | Director / VP Sales Engineering; Sr. Manager Technical Sales / Support; Technical Marketing Engineer; Head of Technical Product Marketing; Head of Customer Onboarding; Partner Enablement Manager | Personally absorbs the cost of hand-built environments. The title depends on the entry motion, so **qualify the motion first**. Usually the operator rather than the VP, because they do the rebuild. | Drives the evaluation and builds the shortlist. High influence, rarely final sign-off. Must sell internally. |
| **Economic buyer** | VP / Head of Product Marketing; VP Sales Engineering or CRO; CCO / VP Customer Success; VP Channel Sales / Head of Alliances; CFO above threshold | One per motion, not one per account. The line is judged against pipeline, NRR or partner-sourced revenue depending on who is buying. Cares about price predictability, cloud-cost control and defensibility, not features. | Signs within threshold; Finance co-signs above it. |
| **Technical buyer** | Principal SE; Platform / DevOps lead; Director of Cloud Infrastructure; Product or Infrastructure Architect | Checks whether the lab can carry the real product: APIs, identity, dependencies, multi-cloud. Owns cloud cost controls and tenant isolation at volume. Judges depth of integration, not breadth of features. | **Genuine veto** on integration coverage and cloud-spend controls. |
| **End user** | SEs running demos and POCs; customer education and onboarding teams; reseller and SI partners in training; prospects in self-service trials | Lives in the tool daily. Their verdict after two weeks decides renewal. | Low influence on price, consulted on selection, **decisive at renewal**. |
| **Legal / procurement** | Vendor Security Review; General Counsel; Procurement Manager; privacy counsel if GDPR / HIPAA in scope | Standard SaaS review: SOC 2 report, DPA, pen-test summary. Usually paperwork, not a contest. | Cannot approve; can delay. A timeline risk, not a selection risk. |
| **Executive sponsor** | CMO; CRO; CPO; CCO; CTO | Engages when pipeline, deal velocity or time-to-value is visibly suffering, **never because of lab features**. CPO engages only when sandboxes are embedded in the product itself. | Unblocks budget and overrides stalls between GTM, CS and Finance. |

**Big Hire vs Little Hire**
- *Big Hire (the purchase):* sold on "your product running in a real environment, delivered and managed for you": speed to a working environment, white-label, multi-cloud plus your own SaaS, compliance-ready. Decided by a GTM leader on a demo, a pilot and peer references (Check Point, Databricks, Microsoft).
- *Little Hire (daily use):* the TME / SE who keeps lab content current as the product ships, fixes environments that won't start, watches cloud spend, and answers "why did the lab break in front of the customer". Common complaints: content drifting from the shipping product, slow starts at peak concurrency, unclear cost attribution, support latency across time zones.
- *Risk:* a platform sold as "fully managed" that still leaves the customer chasing broken environments will churn regardless of how good the Big Hire pitch was.

---

## Buying centres: land and expand

ISVs are the only segment where several budget holders can each buy independently. There is no single committee to work. **Land in one motion, then expand by name into the others.**

| Motion | Entry champion | Budget holder | What they're actually buying |
|---|---|---|---|
| **Pre-sales POC and demo** (usual landing zone) | Director / VP Sales Engineering; TME; Head of Field Engineering | VP Sales Engineering, or CRO / VP Global Sales | Environments in minutes instead of SE days. Measured on cycle length and POCs per SE. Pain is sharpest and budget sits closest to revenue. |
| **Product-led growth and trials** | Head of Growth / VP PLG; Technical PMM | VP / Head of Product Marketing (VP RevOps co-signs routing; name them early) | Ungated self-service sandboxes on their own domain, with trial usage routed to CRM as intent. |
| **Launches, events and hackathons** | Director of Field Marketing; Events Marketing Manager; Head of DevRel | VP / Head of Product Marketing | Hundreds to thousands of environments live on one date. Budgeted per event: short, spiky cycle. Fastest way in when a conference is already on their agenda. |
| **Customer onboarding and education** | Head of Customer Onboarding; CS Enablement Manager; Director of Implementation | CCO / VP Customer Success, or VP Professional Services | Time-to-value and adoption. Judged on churn and NRR, budgeted on a different cycle from GTM. **Expansion territory, rarely the first deal.** |
| **Partner and channel enablement** | Partner Enablement Manager; Director of Partner Training; Channel Marketing Manager | VP Channel Sales / Head of Global Alliances | Training and certifying thousands of resellers and SIs. Highest seat volume, least contested internally (no in-house team wants to own partner environments). |

---

## Core job-to-be-done (ISV)

> **When** an enterprise prospect needs to see our product working in conditions that resemble their own, **I want to** hand them a real, pre-provisioned environment in minutes instead of burning SE days rebuilding one, **so** the product experience closes the deal instead of the SE calendar throttling it.

**Jobs in 3D**
- *Functional:* deliver repeatable, pre-provisioned multi-cloud environments with our own product wired in, across demos, POCs, trials, customer training, partner enablement and events, from one platform.
- *Emotional:* stop being the team that answers every demo request with "give me three days to build the environment", and stop bracing for the demo to break live in front of the prospect.
- *Social:* be the vendor in the category whose product is genuinely easy to evaluate, and look like a company whose engineering is solid enough to let prospects touch the real thing.

**Pains today**
- SEs rebuild environments by hand for every POC, then tear them down when the deal moves (6-10 hours per POC is an *unvalidated assumption*; don't state it).
- Demo tenants drift out of sync with the shipping product and break without warning.
- Trials produce no usage data, so marketing has no intent signal and sales follows up blind.
- Cloud spend on demo and trial tenants is untracked; orphaned resources linger.
- Six GTM motions run on five different tools with no shared reporting.

**Gains sought**
- Environments live in under 60 seconds, pre-provisioned and consistent.
- Fully white-labelled on their own domain; the prospect never sees a third party.
- Trial engagement piped into CRM as MQL signals.
- One platform across demos, POCs, trials, training, partner enablement and hackathons.
- Lower lab delivery cost than managing environments in-house.
- SOC 2 Type II and ISO 27001:2022, so procurement isn't a fresh fight each time.

**Four forces**
- **Push:** an enterprise deal stalls waiting on a POC environment. A launch or new marketplace listing needs a trial motion that doesn't exist. SE capacity is the bottleneck and headcount is frozen.
- **Pull:** multi-cloud plus their own SaaS inside one lab, which no LMS-derived platform does. Embeddable, ungated, live demos. Trial intent routed to CRM. Managed delivery, so no internal platform team is needed.
- **Anxiety:** "Will it actually integrate with our product and our stack?" "Will our brand show through anywhere?" "What happens to cloud spend at volume?" "Can lab content keep pace with a weekly release cycle?"
- **Habit:** hand-built demo tenants that individual SEs own and guard. A Terraform repo maintained by whoever wrote it. Recorded videos and screenshots standing in for a live product.

---

## Jobs, ranked (ISV)

Opportunity score = Importance + (Importance - Satisfaction). Tiers: Critical 15+, High 12-14.9, Moderate 9-11.9, Low <9. Scores are a *working hypothesis*, not survey-derived. **Fund Critical and High first; Moderate jobs are expansion and retention material, not acquisition messaging.**

### DP-01 · Demo and POC delivery · Score 15 · Critical · Fit: Strong · Confidence: High
- **Job:** when an enterprise prospect asks to see our product running against something like their own stack, hand them a working environment the same day, so evaluation moves at the pace of their interest, not the SE calendar.
- **Executor:** Director / VP Sales Engineering, built by an SE. Frequency: per opportunity, several times a week.
- **Pain, in their words:** "Every POC starts with an engineer building a tenant from scratch."
- **Angle:** hand the prospect a working environment on the day they ask, without an engineer building anything.
- **Proof:** Check Point runs 1,700+ hands-on security deployments. Environments live in under 60 seconds.
- **Trigger:** a deal stalls waiting on a POC environment, or SE headcount is frozen while pipeline grows.
- **Discovery Q:** "How many hours went into standing up the environment for your last POC?"
- **Objection:** "Our SEs are fine, they know the setup." → Ask what happens when pipeline doubles and headcount doesn't.
- **Status quo:** hand-built tenants owned by individual SEs, or an internal Terraform repo.
- **What breaks at scale:** demo demand grows with pipeline but SE headcount doesn't. The cost hides inside salaries until deals slip.
- **Success metrics:** SE hours per POC; days from POC request to environment live.
- **Differentiator:** multi-cloud plus the customer's own SaaS in one lab; no LMS-derived competitor offers it.

### DP-02 · Demo and POC delivery · Score 13 · High · Fit: Partial · Confidence: Medium
- **Job:** when the product ships every two weeks but the demo environment was built six months ago, keep the demo matching what we actually sell.
- **Executor:** TME or Demo Engineer. Continuous, pressure at every release.
- **Pain:** "The demo broke on a customer call because the product moved and the environment did not."
- **Angle:** one environment definition, updated once per release, that every seller draws from.
- **Proof:** reusable templates plus managed maintenance.
- **Trigger:** a demo fails on a live call, or a major release changes the product surface.
- **Discovery Q:** "When you ship a release, who updates the demo environment and how long does it take?"
- **Objection:** "We update them when we notice." → Ask how they find out a demo is stale.
- **Gap:** **no named release-versioning capability** was found. Sell it as a managed-service promise, not a product feature.

### TC-01 · Trial and self-serve conversion · Score 13 · High · Fit: Strong · Confidence: High (watch the credibility gap)
- **Job:** when a technical buyer wants to try the product before speaking to anyone, let them run it immediately with no form or call, so we stop losing evaluators who will never book a demo.
- **Executor:** Head of Product Marketing, with Demand Gen.
- **Pain:** "Most people who want to try our product will not book a call to do it."
- **Angle:** let evaluators run the real product straight from your site, with no form and no calendar.
- **Proof:** embeddable demos by iframe or share link; "Zero Gated Forms" positioning.
- **Trigger:** a launch or new marketplace listing needs a trial motion that doesn't exist yet.
- **Discovery Q:** "What can someone actually do on your site today without talking to sales?"
- **Objection:** "Our product is too complex for self-serve." → That's the argument for a real environment rather than a video.
- **Success metrics:** lab starts per 1,000 visitors; ratio of lab starts to demo bookings.
- **Credibility gap:** cloudlabs.ai still gates its own demo behind a Microsoft Bookings widget. A sharp prospect will notice.

### CG-01 · Cloud cost and governance · Score 13 · High · Fit: Strong · Confidence: High (lead with pricing table)
- **Job:** as lab usage grows across teams, know what each programme costs and shut down what nobody uses, so spend stays defensible.
- **Executor:** platform owner on the ISV side.
- **Pain:** "I own a cloud bill I cannot fully explain to finance."
- **Angle:** know what every programme costs, and stop paying for environments nobody is using.
- **Proof:** idle detection, scheduled shutdown, per-user and per-lab reporting, fixed-price managed option.
- **Discovery Q:** "Can you tell me what one campaign cost you in lab spend last quarter?"
- **Objection:** "We watch it in the billing console." → Ask how spend gets attributed once teams share a subscription.

### TC-02 · Trial and self-serve conversion · Score 12 · High · Fit: Strong · Confidence: High if the number is attributed
- **Job:** when someone spends twenty minutes in the trial, know which features they touched and where they stopped, so sales follows up with context.
- **Executor:** PMM and Demand Gen, consumed by Sales.
- **Pain:** "Someone spent twenty minutes in our trial and all sales got was an email address."
- **Angle:** turn what the prospect did inside the trial into a scored signal in your CRM.
- **Proof:** Validation Center pushes feature-level engagement and drop-off to CRM as MQL signals.
- **Discovery Q:** "When someone finishes a trial, what does your sales team actually know about them?"
- **Objection:** "We track signups already." → Ask whether they can tell an evaluator from a tyre-kicker before the call.
- **Success metrics:** trial-to-MQL rate; share of trials with usage data attached.

### LC-01 · Lab content operations · Score 11 · Moderate · Fit: Partial · Confidence: Medium
- **Job:** when building one lab takes weeks, produce a working lab in hours, so content stops capping how many hands-on programmes run.
- **Pain:** "Building one good lab takes us weeks, so we ship a fraction of what we planned."
- **Angle:** generate the lab, then edit, rather than authoring from zero.
- **Proof:** Cosmos AI Lab Builder (infra + guide + validation from a prompt).
- **Discovery Q:** "How long does it take your team to publish one new lab today?"
- **Objection:** "Generated content won't match our standards." → Offer to generate one of *their own* scenarios live and compare.
- **Note:** no published quality or time-saved evidence. **Demo it; don't quote "weeks to hours".** The most demoable capability; one measured customer would move it to Strong.

### EV-01 · Event and hackathon delivery · Score 10 · Moderate · Fit: Strong · Confidence: High
- **Job:** when we commit to a summit or hackathon with thousands of registrants, the environments hold on the day.
- **Executor:** Events / Program Manager, with DevRel. Episodic, very high stakes.
- **Pain:** "We get one shot at this event and quota errors at 9am would be the whole story."
- **Angle:** capacity pre-allocated and environments validated before doors open, with live support on the day.
- **Proof:** **Databricks ran a 7,000-attendee Data + AI Summit** on CloudLabs; **Microsoft delivered 1,200+ GTM events in one year.** The best-evidenced capability; lead with it for any event conversation.
- **Discovery Q:** "What's your fallback if regional capacity runs out on the morning of the event?"
- **Objection:** "Our cloud team can provision it." → Ask whether they've hit a regional quota limit before.
- **Note:** low score because it's episodic, not because it's weak. Rarely starts a buying process on its own, but it closes one.

### TE-02 · Partner enablement · Score 8 · Low · Fit: Strong · Confidence: Medium-High (not a lead motion)
- **Job:** when partners resell or implement our product, train them in the same environments we use, under our brand.
- **Pain:** "Our partners implement our product and we have no idea how well."
- **Angle:** train partners in the same environments your own team uses, under your brand, with certification gated on a scored lab.
- **Proof:** white-label partner portals, scenario labs, gated assessments; channel-scale rollouts for **Wiz and Sophos**.
- **Discovery Q:** "How do you know a partner is ready before you let them implement for a customer?"
- **Objection:** "We send them documentation and a recording." → Ask what their escalation rate by partner looks like.
- **Note:** expansion motion, rarely the way into a new logo.

*Also relevant but secondary for ISVs:* PC-02 (data / network isolation, voucher-based access) and TE-01 (scored lab assessments proving capability, not attendance), which is mainly for customer education.

---

## Messaging

**Message pillars (ISV-relevant)**
- **Pillar 2: Let them use the product, don't describe it.** Jobs DP-01, TC-01, TC-02. Proof: Check Point, embeddable demos, Validation Center.
- **Pillar 3: It runs itself, and someone else runs it.** Jobs CG-01, EV-01. Proof: Databricks at 7,000 attendees, per-user cost reporting, 24x7 managed delivery.
- *(Pillar 1, the Azure Lab Services deadline, belongs to Higher Ed; see `/cloudlabs-edu`.)*

**Headline options**
- "Your engineers did not take the job to rebuild demo environments." Strong for outbound to SE leaders. Weaker for inbound because it assumes the reader has the problem.
- "Let them touch the product. Not a slide about the product." Broadest and brand-led, but proves the least. Pair with a named customer.

**What to lead with, by trigger**

| Situation | Lead with | Discovery question |
|---|---|---|
| POC-blocked enterprise deal | Pillar 2, DP-01 | How many hours went into standing up the environment for your last POC? |
| Launching a product or marketplace listing | Pillar 2, TC-01 | What can someone do on your site today without talking to sales? |
| Large event or hackathon already committed | Pillar 3, EV-01 | What's your fallback if regional capacity runs out on the morning? |
| Cloud bill under review | Pillar 3, CG-01 | What did one campaign cost you in lab spend last quarter? *(Lead with the pricing table, not "80%".)* |

**Framing that works:** SE capacity is a budgeted, measured resource. Framing CloudLabs as *recovering SE hours* makes it a resourcing decision, not a new tool purchase, which is a much easier internal conversation. "You don't have too few SEs. You have a process that requires an SE to hand-build every environment." Executive sponsors respond to pipeline, deal velocity and time-to-value, never to lab features.

**Top objections**
- *"Our cloud / platform team can just build this."* Concede that they can. Ask who maintains it in year two, and what happens when the person who wrote it leaves.
- *"Every vendor claims 60-second labs."* Agree, then offer a live test at their real concurrency rather than arguing about the number.
- *"Will it integrate with our product and stack?"* Invite the technical objection. "Tell me where it breaks for your stack" disqualifies bad fits early and pulls in the technical buyer.

---

## Competitive frame

**Named competitors:** Instruqt, CloudShare, Skillable, Google Cloud Skills Boost (Qwiklabs). Also listed in the assignment: Apporto. **In-house Terraform wins more of these deals than any named vendor.**

- **vs Instruqt / CloudShare / Skillable:** the differentiator is running the customer's own SaaS alongside real multi-cloud infrastructure in one environment. Name Check Point, Databricks, Wiz and Sophos; a peer list beats a feature list.
- **vs in-house build (Terraform, platform team):** it looks free because the headcount already exists. Compete on **maintenance burden** and **time to first environment**, never on licence cost.
- **vs doing nothing:** SEs keep building by hand and the cost stays hidden inside salaries. Make the hidden cost visible (ask, don't assert, the hours).
- **vs click-through demo tools (Storylane, Navattic, Reprise, Walnut, Arcade, Supademo):** cheaper and, for a simple UI, genuinely sufficient. **Don't fight them; qualify out early.** They're dangerous when a buyer hasn't yet worked out that their product isn't simple.
- **vs recorded video demos plus a longer sales cycle:** position live, touchable product against slideware.

---

## Proof points

**Safe to use (named, specific):**
- 500+ organisations; 5M+ labs provisioned.
- **Check Point**: 1,700+ hands-on security deployments. *(State the period and whether it's demos, POCs or both if you can; don't imply an annual run rate.)*
- **Databricks**: 7,000-attendee Data + AI Summit. *(Registrations ≠ concurrency; attribute to Databricks, don't imply it's typical.)*
- **Microsoft**: 1,200+ GTM events in one year.
- **Wiz, Sophos**: channel-scale partner enablement rollouts.
- **JFrog, CLICO**: customers referenced for webinars and testimonials.
- SOC 2 Type II, ISO 27001:2022, GDPR, CCPA, Microsoft SSPA.
- Multi-cloud: Azure, AWS, GCP, Oracle.

### Claim guardrails

| Claim | Grade | Rule |
|---|---|---|
| ~80% reduction in lab delivery cost | D, unsourced | **HIGH risk.** Don't use in outbound. Use the published pricing table instead. |
| 2-3x trial-to-MQL improvement | D, no customer or baseline | **HIGH risk.** Attribute as a CloudLabs claim ("CloudLabs reports...") or leave the number out. |
| SEs spend 6-10 hours per POC | D, internal assumption | **HIGH risk.** Never state as fact. **Ask the prospect for their number** instead. |
| Environments live in under 60 seconds | C, vendor claim | Medium. It's a per-lab number, not a peak-load number. Offer a live concurrency test. |
| Cosmos AI builds labs "in hours instead of weeks" | Vendor claim | Demo it on the prospect's own scenario; don't quote the time saving. |
| Release-versioning for demo environments | Not evidenced | Don't claim as a product feature; frame as managed maintenance. |

Conceding the unproven early makes the strong claims land harder, and the strong claims here are unusually strong.

---

## Channel strategy and prior creative (from Ajay's assignment work)

**Channel mix to invest in**
- **Events and communities** (high upfront cost; builds in-person trust and awareness): DevLearn, KubeCon, DevRelCon, ChannelCon (partners and distributors), EmpowerED, TICE, Learning Technologies, CloudLabs CEd Meets (CEdMA-style), invite-only exec dinners, a CloudLabs hands-on conference (like Instruqt Hands-On).
- **Ads and ABM** (high CAC; captures in-market intent and hits pipeline within a quarter; LinkedIn for precise targeting and awareness):
  - Google Ads keywords: *cloudshare competitors / alternatives / pricing / reviews, cloudshare vs instruqt, virtual it labs, virtual lab software, cloud based virtual labs, cloud sandbox environment, multi cloud lab platform, hands on lab platform, aws / azure / gcp hands on platform, proof of concept environment platform, mct lab*.
  - LinkedIn Ads targeting ISVs by use case, role and content.
- **Content: SEO, AEO, video** (low CAC; compounds; needs 3-4 months to hit pipeline):
  - ToFu: glossaries, AI agents in CEd, KPIs for training managers, AI in IT training.
  - MoFu: ebooks (Cyber CEd, virtual labs for cyber, CEd AI).
  - BoFu: "5 Best DevOps Training Platforms", "5 Best AI Virtual Labs Software", "6 POC Tools for Enterprise".
  - Customer webinars and testimonials: Databricks, JFrog, CLICO.
- **Email nurture:** distributes content at marginal cost; engages leads from other sources through the cycle.
- **Direct gifting:** highest cost per touch; reserved for a small named list of priority accounts; best for prompting a meeting, not creating awareness.
- **Avoid / test only: X (Twitter).** The B2B ISV enterprise-training and DevSec audience isn't active there; low channel fit.

**Google Search ad (CloudShare alternative)**, landing page `cloudlabs.ai/cloudshare-alternative`
- Headlines (sample): "#1 CloudShare Alternative", "Switching Lab Vendors?", "Migration Help Included", "Managed Labs, 24/7 Support", "One Vendor, Every Cloud", "Azure, AWS, GCP & Oracle", "Compare Total Lab Cost", "Launch POCs at Scale", "Build Labs With AI", "Production-Grade Replicas", "No Surprise Cloud Bills", "Pay For Lab Hours Used", "Consolidate Your Lab Stack", "SOC 2 Type II. ISO 27001."
- Descriptions (sample): "See how CloudLabs compares against CloudShare before your renewal date." / "We migrate your existing labs across. Book a 30-minute demo to see the plan." / "1 vendor, 1 contract, 1 admin experience across every cloud your teams use." / "Environments tear themselves down on schedule, so nothing is left running by mistake." / "Describe the scenario & the AI lab builder drafts it. Edit, publish, go live in mins."

**LinkedIn ads (SE-leader persona)**
- *Manual Build / "Game Over" concept:* image copy "Deal stuck waiting on a POC build? That shouldn't feel like GAME OVER." Visual: Mario (the deal) hitting Goombas (manual builds). Headline: "Don't let sales call you a buzzkill." Body: empathises with SEs being blamed when deals stall at POC, then offers the AI lab builder plus auto-teardown and managed multi-cloud labs.
- *Demo Rebuild concept:* image copy "Stop rebuilding the same demo." Visual: side-by-side "old way" (build → demo → tear down → repeat) vs "CloudLabs" (provisioned → demo → reuse). Body: pipeline grows, SE headcount can't; pre-provisioned multi-cloud environments with your product wired in, live the same day.
- Closing line used in both: "Try CloudLabs' managed lab services across Azure, AWS, GCP & Oracle. No more manual builds, no more solution engineers drowning in work."

**Cold email (to Technical Sales / SE leader)**
- Subject: "Is your CRO on your side?" Preview: "The SE orgs that scale without adding headcount look different from the ones that just hired."
- Angle: every POC still starts with an SE building a tenant from scratch; that scales *up* with pipeline. "You don't have too few SEs. You have a process that requires an SE to hand-build every environment. Hiring fixes the symptom."
- CTA: "How many hours did your last POC take to stand up, start to finish?" Low commitment; invites the technical objection.
- Rationale: the subject is a question they know the answer to and don't like; the CRO mention earns the open. Recovering SE hours frames it as resourcing, not a tool purchase. Keep under 150 words; a competitor proof point (e.g. Check Point for a security ISV) persuades better than a feature list.

**Demo page review (cloudlabs.ai):** weak H1 (state the problem and context); logos buried below the form, so move them to the hero and add a named testimonial with face, title and logo; remove the MS Bookings embed and add a multi-select "what are you solving for" qualifier; add privacy / terms / compliance / G2 badges; strip the nav to logo plus CTA; split the hero into left and right halves.

---

## Open hypotheses: validate before they drive spend

- SE hours consumed per POC (assumed 6-10).
- The 200-5,000 employee band and the 800-1,500 addressable-ISV figure.
- Buying-committee composition per motion.
- Which buying signals actually correlate with closed-won.
- All JTBD opportunity scores (currently desk research, not survey-derived).

Validate through win/loss interviews and CRM analysis.
