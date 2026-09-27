---
schema_version: 1
id: OUT-001
type: outcome
title: We know whether researchers can retrieve an article they saved weeks ago
status: active
owner: product-owner
created: 2026-09-27
updated: 2026-09-27
related: [OUT-002]
---

# We know whether researchers can retrieve an article they saved weeks ago

This is a knowledge outcome. Its purpose is to replace an untested assumption with an observation, not to ship a change.

`active` since 2026-09-27: the product owner self-identified during onboarding and committed to arranging the first session. `owner: product-owner` is a role identifier — the human owner did not supply a name or handle to record, and none was invented. Replace it with a preferred identifier at any time.

## Intent

- **Desired change and affected users:** the team can state, from observation, whether a researcher can find an article they saved weeks earlier using the current app. Affects the researchers described in [../../PRODUCT.md](../../PRODUCT.md) — an audience that is itself the owner's untested hypothesis.
- **Link to product purpose, steering, or strategy:** serves the [VISION.md](../VISION.md) ambition of retrieval without organizing. Owner direction, 2026-09-27: "First find out whether researchers can retrieve an old article." See [STRATEGY.md](../STRATEGY.md).
- **Why it matters now:** the product's entire retrieval design rests on title search, and nobody knows whether title recall is how researchers actually remember what they saved ([REQUIREMENTS.md](../REQUIREMENTS.md#open-decisions), open decision 1). Building more retrieval features before answering this risks improving the wrong handle.

## Success contract

- **Metric definition or qualitative evaluation method:** qualitative, observational. Owner-defined on 2026-09-27: **observe researchers trying to retrieve an article from their collection, and record whether they can find and open it without help.**
  - Both halves count. Finding the article but failing to open it is not a success, and neither is succeeding only after a prompt or hint from the observer.
  - "Without help" needs holding to: the observer does not point, suggest search terms, or explain the interface. Record any assistance given and treat that attempt as assisted.
  - Also record what the participant recalled and what they tried — a failure is only useful if it says *why*.
  - **Capture these too**, since they are the discovery actions for open positions in [REQUIREMENTS.md](../REQUIREMENTS.md#open-decisions): what the participant recalled *before* searching (H1); whether they have lost saves before, and whether their collection contains blank-title entries (H2); which device they save from and whether they expect the collection elsewhere (device-reach deferral).
  - No instrumentation. Analytics and telemetry are forbidden ([../AGENTS.md](../AGENTS.md)); see [METRICS.md](../METRICS.md) (MET-001).
- **Baseline, source, and observation window:** **no baseline. No observations exist** — owner statement, 2026-09-27. Any retrieval success rate quoted before this study would be invented. **Timing and observation window are deferred** until the study is scoped (see below).
- **Target, timeframe, and whether proposed or accepted:** no target. A discovery outcome succeeds by producing a trustworthy observation, not by hitting a number. The **decision threshold — what result would count as "researchers can retrieve" — is deferred** until scoping. Fix it before observing, not after, or the result becomes unfalsifiable. No release date is committed.
- **Guardrails and unacceptable tradeoffs:**
  - **Privacy (R7).** A study necessarily looks at someone's real collection. Do not copy, retain, or transmit participants' saved articles. Verify privacy before exposing anything.
  - Do not change the app to make the study look better. Observe the build as it is.
  - Preserve negative and inconclusive results. "Researchers could not retrieve their article" is a valid, useful finding.
- **Evidence required to mark achieved:** recorded evidence from real participants attempting real retrieval, using the [evidence template](../templates/evidence.md), with the observation separated from interpretation. A study that was designed but not run does not achieve this outcome.

## Execution and evaluation

- **Linked opportunities, features, or experiments:** none. No experiment record exists, deliberately — the owner asked for no invented backlog. Create one if the study grows a fixed protocol worth versioning.

- **Deferred scoping decisions.** Owner direction, 2026-09-27: defer these until the study is scoped. Owner: the product owner. Discovery action: scope the study. None blocks arranging the first session; all three block *interpreting* a result.

  | Deferred | Consequence of leaving it open |
  | --- | --- |
  | Participant count | No idea whether one session is indicative or an anecdote. Affects how much weight any finding carries. |
  | Decision threshold | Without a pre-set bar, any outcome can be read as confirming the hypothesis. Fix before observing. |
  | Timing — when sessions happen and how "old" a save must be | "Retrieve an old article" is undefined without an age. A save from ten minutes ago tests nothing about memory. |

- **Dependencies, owner, and next action:**
  - Owner: the product owner, who **will arrange the first session** (owner statement, 2026-09-27). Participant access is no longer an open blocker.
  - Next action: **the owner arranges the first observation session.** Scoping the three deferred decisions comes with it.
  - Unsolved practical obstacle, carried forward: `localStorage` is per-browser and the app is a local file, so a participant may have **no existing collection to retrieve from**. Scoping has to address how a genuinely old save is established — this may force a waiting period between setup and observation, and it interacts with the timing deferral above.
- **Observed result and evidence:** none. No session has happened.
- **Decision, learning, and next review time/trigger:** trigger is the first session taking place. **Nothing is scheduled** — no runner exists ([../operations/README.md](../operations/README.md)), so this depends on the owner.
