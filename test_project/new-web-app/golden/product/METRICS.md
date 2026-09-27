# Metrics

Updated: 2026-09-27 — established during ProductOS adoption.

## Measurement is constrained here

PocketGarden forbids analytics, telemetry, and third-party scripts ([AGENTS.md](../AGENTS.md)), and the owner treats privacy as a product requirement (R7 in [REQUIREMENTS.md](REQUIREMENTS.md#quality-requirements-and-constraints)). **No usage instrumentation is available or permitted.** Do not propose event tracking, funnels, or session analytics as a way to measure this product.

Measurement therefore has to come from direct observation of people using the app, not from data the app reports.

## Defined measurements

| ID | Definition | Method | Baseline | Target |
| --- | --- | --- | --- | --- |
| MET-001 | Whether a researcher can **find and open** an article from their collection **without help**. | Qualitative observation, owner-defined 2026-09-27. Watch a participant attempt retrieval of a real earlier save. Both halves must succeed unaided: finding without opening is not success, and neither is success after a prompt or hint. Record any assistance given and mark that attempt assisted. Also record what they recalled and what they tried. Separate observation from interpretation. | **Unknown — no observations exist** (owner statement, 2026-09-27). | None set. The decision threshold is **deferred** until the study is scoped. |

MET-001 serves [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md), which is `active`. Participant count, decision threshold, and session timing are deferred to scoping — recorded in that outcome. Fix the threshold before observing; a bar chosen afterwards can be made to fit whatever happened.

## Undefined and deferred

- **Retrieval success rate over time.** Would serve [OUT-002](outcomes/OUT-002-retrieval-succeeds-more-often.md). Not definable until MET-001 produces a baseline and the study reveals what actually fails.
- **Save and search speed.** A numeric target is an **explicit owner deferral** — see [REQUIREMENTS.md](REQUIREMENTS.md#explicit-deferrals). The owner owns the follow-up; the discovery action is to inspect current behavior before choosing a target. No performance baseline has been measured.

Unknown baselines stay unknown. An unmeasured value is not zero, and a shipped change is not evidence that an outcome moved.
