---
schema_version: 1
id: Outcome-01
type: outcome
title: A researcher retrieves an article they saved weeks earlier
status: active
owner: product-owner
created: 2026-09-27
updated: 2026-09-27
related: [Metric-01]
---

# A researcher retrieves an article they saved weeks earlier

Status is `active`: the product owner took ownership on 2026-09-27 and will arrange the first observation session. `owner: product-owner` denotes the person who ran onboarding that day and self-identified as product owner; no personal name or handle was recorded. Substitute one if more than one person works on this product.

## Intent

- **Desired change and affected users:** a researcher who saved an article while reading can get it back weeks later without having organized it. Affected users are the owner's stated primary audience — researchers who save while reading and lose track — which is an explicit untested hypothesis.
- **Link to product purpose, steering, or strategy:** Product Purpose in [../../PRODUCT.md](../../PRODUCT.md) and the retrieval-without-organizing principle in [../VISION.md](../VISION.md). Prioritized by the owner on 2026-09-27.
- **Why it matters now:** it is the product's whole promise, and there is no evidence for or against it. The owner's Now priority is to find out whether retrieval actually works for researchers, before changing retrieval.

## Success contract

- **Metric definition or qualitative evaluation method:** qualitative, by direct observation, specified by the owner on 2026-09-27. Observe researchers trying to retrieve an article from their own collection, and record **whether they can find and open it without help**. Unassisted success is the observation; helping the participant ends that observation. No telemetry is possible: analytics, telemetry, and third-party scripts are forbidden (root `AGENTS.md`) and the prototype has no instrumentation. Written up as [Metric-01](../METRICS.md#metric-01--unassisted-retrieval-success), status `proposed`.
- **Baseline, source, and observation window:** **none. No observations of anyone using this product exist**, confirmed by the owner on 2026-09-27. The baseline is unknown, not zero. The observation window is part of the deferred timing below.
- **Proposed starting scope — agent recommendation, NOT accepted, and it does not lift the deferral below.** Something to react to when scoping: five participants, each with a collection they have been adding to for at least a few weeks; one retrieval attempt each for an article they remember saving but have not opened recently; stop after five sessions or earlier if the same failure repeats three times. No success threshold is proposed — with five qualitative observations, a threshold would imply precision that is not there. Judge the pattern, not the fraction.
- **Target, timeframe, and whether proposed or accepted:** **deferred by the owner on 2026-09-27** until the study is scoped — participant count, decision threshold, and timing all remain open. The proposal above is the agent's; the owner has accepted none of it. Consequence: the study can be run and its observations recorded, but it **cannot be concluded as a pass or a fail**, because no threshold separates success from failure and no sample plan says when observation stops. Owner: the product owner. Next discovery action: scope the study, then fix these three before drawing conclusions from the results. A numeric speed target is separately deferred (see [../REQUIREMENTS.md](../REQUIREMENTS.md#open-decisions)).
- **Guardrails and unacceptable tradeoffs:** each participant's collection stays private (QR-3); the existing saving flow is preserved; no analytics or third-party scripts; no new dependencies in `src/`.
- **Evidence required to mark achieved:** observations of researchers actually retrieving articles they saved earlier, against criteria fixed before the study. Shipping a retrieval improvement is not evidence. This outcome cannot be marked achieved from the current state of knowledge.

## Execution and evaluation

- **Linked opportunities, features, or experiments:** none. No feature or experiment record has been created: the owner's Now step is discovery, the study's criteria are deferred, and the owner asked for no invented backlog. An experiment record becomes appropriate once the study is scoped and its criteria are fixed. [FR-4](../REQUIREMENTS.md#fr-4--explain-an-empty-result-and-allow-a-new-query) and QR-1/QR-2 are known unmet requirements, not currently prioritized.
- **Dependencies, owner, and next action:** owner is the product owner. **Next action: the owner arranges the first observation session.** Scoping the study — participant count, decision threshold, timing — follows and must be settled before any result is interpreted. Participants must be researchers with a collection they saved earlier; a participant with an empty or freshly created collection cannot exercise this outcome. Guardrail: observing a participant's own collection means seeing what they saved, so QR-3 privacy applies to the session itself, not only to the software.

Three cheap observations to collect in the same session, each attached to an open decision in [../REQUIREMENTS.md](../REQUIREMENTS.md#open-decisions): whether failed retrievals cluster on items saved without a typed title (decision 1); whether the participant has ever lost a saved collection (decision 3); whether duplicate rows appear and confuse anyone (decision 4).
- **Observed result and evidence:** none. No session has been held.
- **Decision, learning, and next review time/trigger:** none yet. Trigger: the owner completing or scheduling the first session. No date is set, no schedule is registered, and no runner exists — continuation depends on someone starting a session.
