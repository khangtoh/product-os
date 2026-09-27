---
schema_version: 1
id: OUT-002
type: outcome
title: Researchers retrieve what they saved more often
status: proposed
owner: unassigned
created: 2026-09-27
updated: 2026-09-27
related: [OUT-001]
---

# Researchers retrieve what they saved more often

Owner direction, 2026-09-27: "Next, improve retrieval using what we learn; treat that as proposed." Recorded as `proposed` at the owner's explicit instruction.

## Intent

- **Desired change and affected users:** researchers succeed more often at finding an article they saved, without having had to organize it. Same audience as [OUT-001](OUT-001-know-whether-researchers-can-retrieve-an-old-article.md), still an untested hypothesis.
- **Link to product purpose, steering, or strategy:** direct expression of the [VISION.md](../VISION.md) ambition.
- **Why it matters now:** it does not yet. This outcome intentionally waits on [OUT-001](OUT-001-know-whether-researchers-can-retrieve-an-old-article.md). What "improve retrieval" means is **not decidable in advance** — the study determines whether the problem is title recall, save quality, durability, or something unanticipated.

## Success contract

- **Metric definition or qualitative evaluation method:** undefined. It should be derived from what OUT-001 observes, using the same no-instrumentation constraint. Defining it now would fix a measure to an unknown problem.
- **Baseline, source, and observation window:** none. OUT-001 is intended to produce the baseline.
- **Target, timeframe, and whether proposed or accepted:** none. Proposed only. No release date is committed.
- **Guardrails and unacceptable tradeoffs:**
  - Preserve the existing saving flow (owner direction, 2026-09-27) — retrieval improvements must not push organizing work onto the user at save time, which would contradict [VISION.md](../VISION.md).
  - Privacy (R7) holds.
  - Stay inside the project's engineering constraints: no dependencies, no build step, no third-party scripts ([../../AGENTS.md](../../AGENTS.md)).
- **Evidence required to mark achieved:** comparison against whatever baseline OUT-001 establishes. Not markable until then.

## Execution and evaluation

- **Linked opportunities, features, or experiments:** none. No features have been selected for this outcome, and none should be until OUT-001 reports.
- **Dependencies, owner, and next action:** depends entirely on [OUT-001](OUT-001-know-whether-researchers-can-retrieve-an-old-article.md), which is `active` but has produced no observation yet. Owner unassigned. No next action until the first session reports.
- **Observed result and evidence:** none.
- **Decision, learning, and next review time/trigger:** trigger is the conclusion of the OUT-001 study. Not scheduled; no runner exists.

## Note on unmet requirements

Two owner-stated requirements are unmet by the current build — R4 (explain zero search matches) and R6 (visible labels on collection controls), in [REQUIREMENTS.md](../REQUIREMENTS.md). They are **not** part of this outcome and are not on the roadmap: the owner placed the study first instead. They remain real gaps, tracked in REQUIREMENTS, available if the owner chooses to pull them forward.
