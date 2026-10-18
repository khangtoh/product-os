# Measurement contract

Updated: 2026-09-27.

No metric is defined for PocketGarden yet, and none can be collected by the current product: the prototype has no instrumentation, and analytics, telemetry, and third-party scripts are not permitted (root `AGENTS.md`, Boundaries in [../PRODUCT.md](../PRODUCT.md)). Any evaluation will therefore have to be direct observation of researchers using it, or the owner's own use, rather than product telemetry. How success is evaluated is an open onboarding question.

## Metric registry

| ID | Name | Definition and population | Source | Baseline / window | Target / window | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Metric-01 | Unassisted retrieval success | Share of observed retrieval attempts in which the participant finds and opens the intended article without help, across observed sessions | Observation notes from sessions for [Outcome-01](outcomes/Outcome-01_retrieve_an_old_article.md) | unknown — no session has been held | Deferred by the owner until the study is scoped | Product owner | proposed |

Use `Metric-01`, `Metric-02`, and so on. These IDs identify definitions in this file. Add one subsection per adopted metric with the fields below.

### Metric-01 — Unassisted retrieval success

Defined on 2026-09-27 from the observation method the owner specified. It is a qualitative measure recorded as a proportion, not a statistical estimate: sample sizes will be small enough that it describes the sessions held and nothing more.

- **Purpose:** represents [Outcome-01](outcomes/Outcome-01_retrieve_an_old_article.md) — whether a researcher can recover something they saved, without organizing and without help.
- **Calculation:** attempts where the participant finds *and* opens the intended article unaided, divided by all observed attempts. An attempt where the observer intervenes counts as a failure of that attempt, and the intervention is noted.
- **Population:** researchers with a collection they saved earlier. A participant with an empty or freshly created collection is excluded; they cannot exercise the outcome.
- **Time:** recorded at session time. Observation window is part of the deferred study timing.
- **Source:** session notes. There is no telemetry and there will be none — analytics are forbidden (root `AGENTS.md`).
- **Quality:** observer judgment, unblinded, with no second rater. Expect observer effects: people search differently when watched. Small samples.
- **Baseline:** unknown. No session has been held.
- **Target:** **deferred by the owner** along with participant count and threshold. Without a threshold this metric describes results; it cannot decide them.
- **Owner:** the product owner, who arranges and runs the sessions.

Status is `proposed`: the definition was written by the agent under the owner's 2026-09-27 authorization and has not been used to record anything.

## Required definition

- **Purpose:** which user or business outcome this metric represents.
- **Calculation:** numerator, denominator, unit, and aggregation; for a count or direct measure, state the event or measurement rule.
- **Population:** eligibility, cohort, exclusions, deduplication, and relevant segmentation.
- **Time:** event time, observation window, reporting timezone, and handling of late events.
- **Source:** verified event names, dashboard or query location, query version, and access requirements.
- **Quality:** instrumentation checks, sample coverage, known missing data, and freshness limit.
- **Baseline:** value, sample size, interval, and collection method; use `unknown` until measured.
- **Target:** desired change and evaluation window, including whether it is proposed or accepted.
- **Owner:** who or which agent is responsible for checking it and when.

Changing a definition requires a dated revision. Preserve the definition used by a completed experiment; do not compare incompatible historical numbers as if they were the same metric.

## What to measure

Choose a small set appropriate to the product:

| Layer | Question |
| --- | --- |
| User value | Did the user accomplish the intended job successfully? |
| Continued value | Do users return when the need recurs? |
| AI quality | Are outputs useful and correct for representative tasks? |
| Reliability | Are completion, errors, and latency within defined limits? |
| Economics | What does a successful user outcome cost to deliver? |
| Learning loop | Do completed changes produce evidence and a subsequent decision? |

The AI quality and economics layers are currently not applicable: the product contains no AI behavior and incurs no delivery cost.

For AI behavior changes, record the model, prompt, tool, and evaluation set versions. Use representative cases and product-specific failure cases. Automated judges need a stated rubric and checks against trustworthy labels; passing an evaluation alone does not prove real-user value.

## Evaluation discipline

Define success, failure, guardrails, exposure, and stop criteria before starting an experiment. Select a comparison and sample plan appropriate to the evidence available. Small qualitative studies can guide a decision but do not establish statistical significance. Report an inconclusive result when the data cannot support the claim.

If telemetry is absent, delayed, or broken, report the measurement as unavailable and repair or substitute a stated method. Do not infer success from silence.
