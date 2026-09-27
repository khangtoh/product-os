# PRODUCT.md

> The shared product contract for humans and AI: what we are building, for whom, why it matters, how we choose, and how we learn.

Updated: 2026-09-27 — established during ProductOS adoption. Initial brief complete; see [product/STATE.md](product/STATE.md).

## Purpose and identity

PocketGarden helps a researcher get back to an article they saved while reading, without requiring them to organize their saves first.

The target audience and the problem are the owner's **stated initial hypothesis**, recorded on 2026-09-27 and **not tested against users**. Treat them as direction to work from, not as validated evidence.

| Field | Current definition |
| --- | --- |
| Product name | PocketGarden |
| Purpose and one-sentence promise | Retrieve an article you saved while reading, without having to organize everything. |
| Target users and context | Researchers who save articles while reading and later lose track of them. *Hypothesis, untested.* The moment of saving and the moment of retrieval have not yet been described in detail. |
| Core user job and recurring need | Save an article encountered mid-reading, then find it again later from memory of what it was. |
| Current alternatives | Browser bookmarks and notes. *Owner-stated.* The specific failure of those tools has not yet been articulated beyond "lose track of them". |
| Distinctive value and role of AI, if any | Distinctive value: retrieval without an upfront organizing step (no folders, tags, or filing required). No AI role is established. Project instructions forbid third-party scripts, which would constrain any hosted model; that tradeoff has not been decided. |
| Current experience and maturity | Early prototype. Save by URL and title, case-insensitive title substring search, open at original URL; all data in browser `localStorage`. No accounts, server, deployment, or tests. See [product/REQUIREMENTS.md](product/REQUIREMENTS.md). |
| Business model, if applicable | unknown — not yet discussed. |
| Constraints and non-goals | **Privacy is an owner requirement:** each user's collection stays private, verified before exposing any change. Engineering constraints from [AGENTS.md](AGENTS.md): `src/` stays dependency-free; no build step, bundler, or framework; plain ES modules and vanilla DOM; **no analytics, telemetry, or third-party scripts**. Non-goals for now: team or shared libraries, automated summaries. No release date is committed. See [product/REQUIREMENTS.md](product/REQUIREMENTS.md#exclusions-and-tradeoffs). |
| Source of product direction | The product owner, recorded as `product-owner` — a role identifier, since no name or handle was supplied. They own the first study session and the deferred speed target. |

Use [product/VISION.md](product/VISION.md) for longer-term ambition and [product/STRATEGY.md](product/STRATEGY.md) for current bets.

## Platform

Web app.

Confirmed by the owner on 2026-09-27: it stays a web app, not a native application.

Today it runs as a local file opened directly in a browser (`src/index.html`), with no server and no build step.

Device reach and hosting are an **explicit deferral** with a recommended position: stay single-browser and local for now, because hosting or sync would turn privacy (R7) from free-by-construction into real engineering and pull against the no-dependency constraints. The risk being carried is that saving while reading plausibly happens on a phone, and `localStorage` crosses neither browsers nor devices. Owner `product-owner`; discovery action is to note participants' devices during the first study sessions. See [product/REQUIREMENTS.md](product/REQUIREMENTS.md#explicit-deferrals).

## Core experience and requirements

The essential workflows, initial acceptance criteria, and open decisions live in [product/REQUIREMENTS.md](product/REQUIREMENTS.md). Behavior implemented today is recorded there and distinguished from intended behavior.

## Desired outcomes

- **Active:** [OUT-001](product/outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) — know whether researchers can find and open an article from their collection without help. Evaluated by direct observation (MET-001); no baseline, and the decision threshold is deferred to scoping.
- **Proposed:** [OUT-002](product/outcomes/OUT-002-retrieval-succeeds-more-often.md) — researchers retrieve what they saved more often. Deliberately unspecified until the study reports.

Measurement is genuinely constrained here: the no-analytics instruction rules out usage instrumentation, so evaluation is by watching real people, not by data the app reports. See [product/METRICS.md](product/METRICS.md).

The canonical priority order is [product/ROADMAP.md](product/ROADMAP.md); measurement definitions live in [product/METRICS.md](product/METRICS.md). A shipped feature is not proof that an outcome was achieved.

## Decision principles

These are starting conventions to adapt to the project:

- Follow explicit product direction within its scope.
- Use user feedback, behavior, research, and operating evidence to discover opportunities.
- Prefer the smallest useful intervention or informative experiment.
- Consider user value, confidence, effort, urgency, reliability, and cost together.
- Preserve uncertain claims as hypotheses and retain contrary evidence.
- Let results change product choices and operating practice.

## Shared control

Humans and agents can research, design, build, operate, and evaluate. Active work has an owner, criteria, and a handoff. Owner direction sets intent; user input provides evidence. Actual authority is recorded in [product/operations/README.md](product/operations/README.md) and comes from applicable project/session instructions.

This file does not grant external access, spending, or release permission. Existing authorization carries forward without repeated approval requests for work within scope.

## Evolution

**Steer → observe → prioritize → design → build → verify → release → operate → measure → learn → update the product model.**

Every material change should connect a reason to an observed result and a subsequent decision. Update the app, priorities, evaluation, or operating practice when learning warrants it. An explicit decision to retain an approach is also valid.

Read [product/STATE.md](product/STATE.md) to resume work, [product/AGENTS.md](product/AGENTS.md) for agent instructions, [product/WORKING_TOGETHER.md](product/WORKING_TOGETHER.md) for collaboration, and [product/LOOP.md](product/LOOP.md) for execution. Use [product/MODEL.md](product/MODEL.md) for records and [product/LEARNINGS.md](product/LEARNINGS.md) for durable knowledge.

Keep this contract brief and current. Link the direction or decision behind material changes; detailed specifications and results belong in their own records.
