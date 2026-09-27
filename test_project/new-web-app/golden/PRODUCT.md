---
productmd: 1
productos: 1
register: product
$type: Product
$context: https://schema.org.ai
---

# PocketGarden

Save an article while you are reading, and find it again later without having to organize anything.

Updated: 2026-09-27.

This is the canonical product contract. It follows the open PRODUCT.md convention and adds ProductOS operating context. Sections still marked unknown have not been established; onboarding is in progress and the checkpoint lives in [product/STATE.md](product/STATE.md). Replace unknowns only with supplied direction, supported evidence, a user-selected hypothesis, or an explicit deferral.

## Register

product

Design serves a task here rather than being the product itself: PocketGarden is a personal utility built around save and retrieve, and every requirement the owner stated is functional or accessibility-related, not expressive.

**Provenance:** the agent recommended `product` in onboarding rounds 1 to 3; the owner did not answer those rounds and then authorized the agent's recommendations wholesale on 2026-09-27. So this is owner-authorized, but it was never a considered per-field choice. Revisit if the product ever becomes something whose presentation is the point. Page-specific design modes may override this default without changing the product register.

## Users

**Hypothesis — stated by the owner on 2026-09-27 and explicitly untested.** Researchers who save articles while they are reading and later lose track of them. They are mid-task when they save: reading something, following a thread, not filing an archive.

No user research, interview, or usage evidence exists for this audience. See [Desired Outcomes](#desired-outcomes) for the discovery action that would test it.

## Problem

Articles saved while reading get lost. Retrieval today depends on having organized the material at save time, which is exactly the work a reader in the middle of something will not do.

### Current alternatives

Browser bookmarks and notes apps (owner, 2026-09-27). Why they are insufficient is part of the same untested hypothesis: they stay findable only if the user maintains folders, tags, or note structure, so saved items accumulate unorganized and become unretrievable.

Not established: which of these the target researchers actually use, in what proportion, or whether they experience the loss as a problem worth changing tools for.

## Product Purpose

PocketGarden lets someone save an article in one step while reading, and get it back later by searching rather than by filing. Successful use means a researcher recovers something they saved weeks ago without ever having organized it.

The durable commitment is **retrieval without organizing**: the product must not make findability depend on user-maintained structure. Recorded in [product/VISION.md](product/VISION.md).

### Role of AI

Not applicable at present. The product contains no AI behavior, and no direction has established any. Recorded as a fact about the current product, not a decision against future use.

## Brand Personality

**Hypothesis — agent recommendation, authorized wholesale by the owner on 2026-09-27, never discussed directly.** Quiet and unfussy. The product is a place things are put down and picked up again; it should not ask for attention, enthusiasm, or maintenance. Revisit condition: any observation that users want the product to feel like a library or a workspace rather than a pocket.

### Tone

**Hypothesis, same provenance.** Plain and literal. In ordinary use it says almost nothing. In failure it states what happened and what the person can do next — the empty-result message in [FR-4](product/REQUIREMENTS.md#fr-4--explain-an-empty-result-and-allow-a-new-query) is the first and currently only instance of this tone, and is a good test of it.

## Anti-references

**Hypothesis, same provenance.** The product must not resemble tools whose usefulness depends on the user maintaining structure — folder trees, tag taxonomies, curated collections. This follows directly from the established retrieval-without-organizing principle, so it is the most durable of the hypotheses in this section. A feature that asks the user to file, tag, or tidy is suspect by default.

## Design Principles

**Hypotheses, same provenance.** Derived from the established purpose and the owner's stated requirements, not from any design discussion:

1. Saving costs one action and no decisions. A person mid-reading should never be asked to categorize.
2. Retrieval degrades gracefully. When search finds nothing, say so and keep the person's query — never show a blank space.
3. Controls are labeled, not guessed. Visible labels over placeholder-only fields (QR-2), for everyone, not only assistive-technology users.

Visual tokens and component rules belong in project design guidance; this repository has none, and the prototype has no stylesheet at all.

## Accessibility & Inclusion

Established by the owner on 2026-09-27:

- **Keyboard operability.** Saving an article, searching, and opening a result must all work by keyboard.
- **Visible labels.** Collection controls need visible labels, not placeholder text alone.

**Proposed floor — agent recommendation under the owner's 2026-09-27 authorization, not verified and not a conformance claim:** WCAG 2.2 Level AA. It is the ordinary baseline for a public web app and is consistent with the two requirements the owner did state. Adopting it as a target costs nothing today; claiming to meet it would be false.

Observed gap: the inputs in `src/index.html` have placeholders and no labels, so the visible-label requirement is unmet. Nothing has been audited against any standard, and the page has no stylesheet, so contrast and focus styling are browser defaults. Discovery action, owner the product owner: audit the prototype against the proposed floor once the first study is done, and either accept the floor or replace it with a smaller one. Verification criteria are in [product/REQUIREMENTS.md](product/REQUIREMENTS.md).

## Platform

web

A web app. Confirmed as owner direction on 2026-09-27 ("keep it a web app"), consistent with the repository: `src/index.html` is opened directly in a browser, there is no build step and no server, and saved data lives in that browser's `localStorage`. Whether it is eventually hosted, installable, or multi-device is not established; native platforms are excluded by this direction.

## Boundaries

Owner requirements and commitments, 2026-09-27:

- **Each user's collection stays private.** This is an owner requirement, not an inference from the current storage choice. Any change that would expose a collection must have its privacy verified before that exposure.
- **No release date is committed.** Priorities are not deadlines.
- **Not yet inspected:** production health and analytics. Nothing is known about how the product behaves in real use; absence of reports is not evidence of health.

Established constraints, from the repository's root `AGENTS.md` and `README.md`:

- `src/` stays dependency-free. No build step, no bundler, no framework.
- No analytics, telemetry, or third-party scripts.
- Plain ES modules and vanilla DOM APIs; two-space indentation.
- No accounts, no deployment pipeline, no tests at present.

Product non-goals and unacceptable tradeoffs are unknown and scheduled for a later round. Detailed requirement exclusions belong in [product/REQUIREMENTS.md](product/REQUIREMENTS.md).

No commercial offer is established, so this contract has no `## Offer` section, no pricing island, and no `$id`.

## Stack

- [Agent instructions](product/AGENTS.md)
- [Current state](product/STATE.md)
- [Vision](product/VISION.md)
- [Requirements](product/REQUIREMENTS.md)
- [Strategy](product/STRATEGY.md)
- [Roadmap](product/ROADMAP.md)
- [Metrics](product/METRICS.md)
- [Learning](product/LEARNINGS.md)
- [Operations](product/operations/README.md)

This repository has no DESIGN.md or other established contract to link.

## Core Experience and Requirements

Essential workflows, initial functional and quality requirements, acceptance criteria, and open decisions live in [product/REQUIREMENTS.md](product/REQUIREMENTS.md). That document currently holds only behavior observed in the source; intended behavior is being established.

## Desired Outcomes

[Outcome-01 — a researcher retrieves an article they saved weeks earlier](product/outcomes/Outcome-01_retrieve_an_old_article.md). Status `active`, owned by the product owner. Evaluation is direct observation — whether a researcher finds and opens an article from their own collection without help — since analytics are forbidden and the prototype has no instrumentation. It has no baseline (nobody has been observed using this product) and no threshold or sample plan yet; those are deferred until the study is scoped, so the first session can produce observations but not a verdict.

The canonical priority order is [product/ROADMAP.md](product/ROADMAP.md); measurement definitions belong in [product/METRICS.md](product/METRICS.md), which currently defines none. The owner's Now priority is discovery — finding out whether researchers can retrieve an old article — before changing retrieval. A shipped feature is not proof that this outcome was achieved.

## Operating Principles

These are starting conventions to adapt to the project:

- Follow explicit product direction within its scope.
- Use user feedback, behavior, research, and operating evidence to discover opportunities.
- Prefer the smallest useful intervention or informative experiment.
- Consider user value, confidence, effort, urgency, reliability, and cost together.
- Preserve uncertain claims as hypotheses and retain contrary evidence.
- Let results change product choices and operating practice.

## Human and Agent Control

Humans and agents can research, design, build, operate, and evaluate. Active work has an owner, criteria, and a handoff. Owner direction sets intent; user input provides evidence. Actual authority is recorded in [product/operations/README.md](product/operations/README.md) and comes from applicable project or session instructions.

This file does not grant external access, spending, or release permission. Existing authorization carries forward without repeated approval requests for work within scope.

## Evolution Loop

**Steer → observe → prioritize → design → build → verify → release → operate → measure → learn → update the product model.**

Every material change should connect a reason to an observed result and a subsequent decision. Update the app, priorities, evaluation, or operating practice when learning warrants it. An explicit decision to retain an approach is also valid.

Keep this contract brief and current. Preserve frontmatter, valid machine islands, and sections a tool does not understand. Link the direction or decision behind material changes; detailed specifications and results belong in their canonical records.
