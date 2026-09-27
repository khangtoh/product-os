# A first learning loop

**Fictional example.** The app, records, sample, observations, and decisions below are invented to illustrate the method. Do not copy them into a project's real evidence or roadmap.

## Intent

Imagine a reading-list app called PocketGarden. Its proposed promise is to help people save an article and retrieve it when needed. The product owner wants to investigate confusion when someone first saves a link.

PRODUCT.md would define that user job. STATE.md would name the current research action and owner. ROADMAP.md would prioritize a first-use outcome before unrelated features.

## Connected records

| Illustrative ID | Meaning | Links |
| --- | --- | --- |
| Steering-01 | Investigate first-save confusion | Outcome-01 |
| Outcome-01 | Improve successful first-save behavior | Metric-01, Experiment-01 |
| Evidence-01 | Fictional usability notes suggest uncertainty about whether a link was saved | Opportunity-01 |
| Opportunity-01 | New users cannot confidently tell whether saving succeeded | Outcome-01, Evidence-01 |
| Feature-01 | Prototype a visible saved-item confirmation | Opportunity-01, Outcome-01 |
| Experiment-01 | Evaluate whether the confirmation is understandable | Feature-01, Metric-01 |
| Evidence-02 | Fictional observations from the prototype sessions | Experiment-01 |
| Decision-01 | Revise duplicate-save feedback before live exposure | Evidence-02, Feature-01 |
| Learning-01 | Distinguish first-save and already-saved feedback in future designs | Evidence-02, Decision-01 |

Metric-01 would be defined in METRICS.md and Learning-01 in LEARNINGS.md. The other IDs would have typed records if this were a real project.

## Protocol before observation

The hypothetical team chooses a small qualitative study, not a claim of population-level lift. Five invited participants will try a prototype. The primary observation is whether each participant can tell, without prompting, that a save succeeded and retrieve the saved item.

The illustrative decision rule is: proceed to a bounded live evaluation only if at least four of five complete the task and no data-loss failure occurs. A duplicate-save attempt is included as a failure-mode check. This criterion guides the next design decision; it does not establish statistical significance.

The intervention is a prototype with a visible confirmation and direct access to the saved item. The study uses test data, a fixed task script, and a defined session limit. No production release is implied or authorized by this fictional scenario.

## Fictional result

Suppose all five participants recognize the first successful save, but two become confused when saving the same link again. There is no data loss. These are invented teaching observations, not real measurements.

The primary task criterion was met in this small sample, while a relevant failure case remains unresolved. The evidence would preserve both findings and the limited population. The team would not declare a durable product outcome achieved from five prototype sessions.

## Decision and resulting changes

The illustrative decision is to revise already-saved feedback before exposing the change to real users. The feature acceptance criteria gain an explicit duplicate-save case. The next experiment tests that case and later defines a suitable live evaluation. LEARNINGS records the scoped design lesson with its evidence and revisit condition.

STATE points to the next action, and the roadmap keeps the user-value outcome active. The research cycle can be `completed`, Experiment-01 can be `concluded`, and the feature can remain `building`. The outcome is not `achieved` because its live user-value criteria have not been demonstrated.

That distinction lets the system learn honestly while continuing useful work.
