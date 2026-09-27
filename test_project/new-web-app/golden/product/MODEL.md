# Product model

ProductOS uses Markdown for readability and YAML front matter for predictable record metadata. The established document history preserves changes. A future runner can index the model; no indexer is installed by these files.

## Canonical homes

PRODUCT.md holds product identity and the product contract. VISION.md holds durable product ambition and relevant company direction; REQUIREMENTS.md holds initial workflows, functional and quality requirements, acceptance criteria, and open decisions; STRATEGY.md holds current bets; ROADMAP.md holds priority order; STATE.md holds the current handoff. METRICS.md defines measurements and LEARNINGS.md stores reusable conclusions. Operations holds actual service context and operating scope. Typed records hold the detail behind these summaries.

Link to the canonical fact instead of maintaining parallel copies.

New project onboarding creates the canonical contract at the target project root, beside its root agent instructions. The product folder's PRODUCT.md becomes a navigation pointer to that contract. The bare template keeps its full contract inside the folder so it remains independently copyable; onboarding promotes it only in the target project, rewriting the root contract's relative links to the product folder.

If the product folder is itself a standalone context repository's root, keep its contract in place. Do not create a self-referencing pointer or move the contract outside that project.

### PRODUCT.md compatibility

The ProductOS 0.2 contract is a superset of the open PRODUCT.md convention. A newly adopted contract must have one product-name H1 and preserve its `productmd: 1`, `productos: 1`, `$type: Product`, and `$context` metadata.

Use the canonical headings in the blueprint. Resolve `## Register` to exactly `brand` or `product` during onboarding, then mirror the value in frontmatter. Page-level design modes may override that default for one surface. Retain `## Platform` as a separate ProductOS and design-tool field.

When promoting the blueprint, rewrite its local Stack and ProductOS links to `product/...`. Replace the local file with a navigation pointer only after the root contract is complete and its links resolve. Preserve frontmatter, valid machine islands, and sections a tool does not understand when modifying an established contract.

Offer, pricing islands, and `$id` are optional. Omit them until the underlying values and any public binding are established. A bare blueprint with unresolved identity and Register is intentionally incomplete; do not claim conformance until onboarding resolves the required product context.

When adopting into a project with an established product contract, preserve its canonical location. The local PRODUCT.md can link to that source or its sections. Do not promote a populated local contract or replace a root file without direction to consolidate. Keep one authoritative home for each fact and update affected links and agent instructions together. For multiple products, the target app root is the project root; establish the target before writing.

REQUIREMENTS.md is a summary document, not a new typed record or parallel task backlog. Link existing specifications and issue trackers instead of copying their maintained details. Feature records add scoped implementation and verification detail and link to the relevant requirements. ROADMAP remains the only canonical priority order.

## Onboarding completion

A complete initial brief addresses each area below using supported facts, explicit owner direction, user-selected hypotheses, or explicit user deferrals. A field containing `unknown` alone is not evidence that its required area was discussed. Use only applicable detail; no mandatory business model, numerical target, aesthetic choices, or release dates are implied.

| Required area | Coverage | Canonical destination |
| --- | --- | --- |
| Identity and vision | Promise, reason to exist, lasting change, source of direction | PRODUCT, VISION |
| Users and problem | Primary users, usage situation, problem, current alternatives | PRODUCT |
| Core experience | Essential user workflows and what users must accomplish | REQUIREMENTS |
| Initial requirements | Must-have behavior, relevant failure cases, observable acceptance criteria | REQUIREMENTS |
| Boundaries | Non-goals, tradeoffs, platform, applicable resource and delivery constraints | PRODUCT, REQUIREMENTS |
| Success | Desired outcomes, evaluation approach, evidence available, measurement gaps | Outcome records, METRICS when defined |
| Priorities | Now / Next / Later outcomes, rationale, dependencies, actual commitments | ROADMAP, STRATEGY |
| Starting point | Maturity, ongoing work, ownership, concrete first action | STATE, operations |

During the interview, STATE's onboarding checkpoint records coverage with links to the canonical answers, remaining questions, and the next interview topic. Save answers in their canonical homes as they arrive. For a material inference, retain its source and distinguish it from confirmed direction; an agent proposal becomes a selected hypothesis only after the user's answer. Record an explicit deferral's question, consequence, owner if known, and next discovery action in the relevant document, linking it from STATE. Silence is not deferral.

Mark the initial brief complete only after all required areas are addressed, context is saved, canonical and agent-context links resolve, the roadmap agrees with the first action, and the user is shown a linked summary with an opportunity to correct it. There is no additional mandatory approval round to save already supplied answers. If answers or writes are missing, preserve an incomplete checkpoint and explain what remains. A new contributor's orientation does not reset this checkpoint or require a new interview.

Report readiness for the proposed next action separately from brief completion. A complete brief can require discovery before implementation. Unknown scope, ownership, access, or success criteria must remain visible as dependencies; follow the existing lifecycle rules before marking work active or ready. Summarize this in STATE without adding new typed-record states. Onboarding itself proves neither a product outcome nor a running schedule.

## Record types

| Type | ID | Directory | Answers |
| --- | --- | --- | --- |
| `steering` | `Steering-01` | `steering/` | What direction was given, by whom, within what scope? |
| `outcome` | `Outcome-01` | `outcomes/` | What observable change matters? |
| `opportunity` | `Opportunity-01` | `opportunities/` | What user problem could produce that change? |
| `feature` | `Feature-01` | `features/` | What behavior will we deliver and verify? |
| `experiment` | `Experiment-01` | `experiments/` | What uncertain claim are we testing? |
| `evidence` | `Evidence-01` | `evidence/` | What was observed, where, when, and how? |
| `decision` | `Decision-01` | `decisions/` | What did we choose and why? |
| `cycle` | `Cycle-01` | `cycles/` | What happened, and how does the work resume? |
| `incident` | `Incident-01` | `operations/incidents/` | What failed and how was it resolved? |
| `runbook` | `Runbook-01` | `operations/runbooks/` | How do we carry out or recover an operation? |

`Metric-01` and `Learning-01` style IDs identify entries in METRICS.md and LEARNINGS.md. Create a directory with its first real record; do not manufacture work to populate folders.

## Metadata

Copy the relevant template. Every typed record has these fields:

```yaml
---
schema_version: 1
id: Opportunity-01
type: opportunity
title: A concise description of the user problem
status: proposed
owner: unassigned
created: YYYY-MM-DD
updated: YYYY-MM-DD
related: []
---
```

IDs use the full record type as a single-word prefix, a hyphen, and a two-digit sequence number, such as `Opportunity-01`; never abbreviate the type. Name the file `<ID>_short_text_description.md`, for example `Opportunity-01_first_save_confusion.md`, using lowercase words joined by underscores. Continue with three digits after `99`. Use a stable unique ID. Select the next unused ID after checking records; coordinate allocation if several actors write. Never reuse IDs. Keep IDs when retiring or moving records and repair affected links. Instances with older abbreviated IDs such as `OPP-001` keep them; use the full-word form for new records.

Dates use ISO `YYYY-MM-DD`; observations and execution use UTC ISO timestamps when precision matters. Active work must have a named human or agent owner. Proposed work may be `unassigned`. `related` lists existing record, metric, or learning IDs. Use relative Markdown links in the body for human navigation.

Replace template blanks before creating a real record. Use `unknown`, `not_applicable` with a reason, or an explicit proposal where appropriate. Root summary documents do not require front matter.

## Relationships

- Outcome → vision/steering, metric or evaluation definition, and success criteria.
- Opportunity → outcome and evidence, or an explicit untested hypothesis.
- Feature → outcome plus opportunity or incident; implementation and verification artifacts when available.
- Experiment → outcome, intervention or feature, evaluation method, result evidence, and decision.
- Evidence → original source and relevant records; separate observation from interpretation.
- Decision → evidence/steering, affected records, and superseded decision when applicable.
- Cycle → work records, actual execution artifacts, and next action or review trigger.
- Incident → affected service, evidence, recovery work, and prevention/runbook changes.

Research need not create a feature. A fix need not create an experiment. User feedback need not become owner steering. The requirements are traceable purpose and an honest result.

## Lifecycle

| Type | Allowed states | Transition evidence |
| --- | --- | --- |
| Steering | `captured`, `applied`, `superseded`, `withdrawn` | Applied direction links to affected documents/decisions |
| Outcome | `proposed`, `active`, `achieved`, `missed`, `retired` | Achievement needs evidence against its criteria |
| Opportunity | `proposed`, `investigating`, `selected`, `deferred`, `rejected`, `resolved` | Selection needs rationale; resolution needs a disposition |
| Feature | `proposed`, `ready`, `building`, `verifying`, `released`, `evaluated`, `retired` | Ready needs scope/validation; released needs an artifact; evaluated needs a result |
| Experiment | `draft`, `ready`, `running`, `analyzing`, `concluded`, `cancelled` | Running needs fixed criteria and working observation; concluded needs results/decision |
| Evidence | `recorded`, `superseded`, `invalidated` | Preserve sources and reasons for invalidation |
| Decision | `proposed`, `accepted`, `superseded`, `reversed` | Acceptance identifies decider, rationale, and authority |
| Cycle | `planned`, `active`, `waiting`, `blocked`, `completed`, `cancelled` | Final or waiting state has an accurate handoff |
| Incident | `open`, `mitigating`, `monitoring`, `resolved` | Resolution needs verified recovery and assigned follow-up |
| Runbook | `draft`, `active`, `retired` | Active needs verified steps, authority, recovery, and verification date |

Explain reversals or skipped stages. Blocked work keeps its lifecycle state and records the blocker, responsible actor, and next check in the body and cycle. A blocked feature must not be marked ready or complete simply to clear a queue.

## Integrity

Check unique IDs, resolving links, valid metadata/states, and agreement between records and summary files. Active work needs ownership and a next action. Running experiments need an observation window and stop criteria. Conclusions link to evidence; material learning states its implications. Preserve original hypotheses and historical results.
