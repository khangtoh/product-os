# A first learning loop

**Fictional example.** The app, records, sample, observations, and decisions below are invented to illustrate the method. Do not copy them into a project's real evidence or roadmap.

## Intent

Imagine a reading-list app called PocketGarden. Its proposed promise is to help people save an article and retrieve it when needed. The product owner wants to investigate confusion when someone first saves a link.

PRODUCT.md would define that user job. STATE.md would name the current research action and owner. ROADMAP.md would prioritize a first-use outcome before unrelated features.

## Connected records

| Illustrative ID | Meaning | Links |
| --- | --- | --- |
| STR-001 | Investigate first-save confusion | OUT-001 |
| OUT-001 | Improve successful first-save behavior | MET-001, EXP-001 |
| EV-001 | Fictional usability notes suggest uncertainty about whether a link was saved | OPP-001 |
| OPP-001 | New users cannot confidently tell whether saving succeeded | OUT-001, EV-001 |
| FEAT-001 | Prototype a visible saved-item confirmation | OPP-001, OUT-001 |
| EXP-001 | Evaluate whether the confirmation is understandable | FEAT-001, MET-001 |
| EV-002 | Fictional observations from the prototype sessions | EXP-001 |
| DEC-001 | Revise duplicate-save feedback before live exposure | EV-002, FEAT-001 |
| LRN-001 | Distinguish first-save and already-saved feedback in future designs | EV-002, DEC-001 |

MET-001 would be defined in METRICS.md and LRN-001 in LEARNINGS.md. The other IDs would have typed records if this were a real project.

## Protocol before observation

The hypothetical team chooses a small qualitative study, not a claim of population-level lift. Five invited participants will try a prototype. The primary observation is whether each participant can tell, without prompting, that a save succeeded and retrieve the saved item.

The illustrative decision rule is: proceed to a bounded live evaluation only if at least four of five complete the task and no data-loss failure occurs. A duplicate-save attempt is included as a failure-mode check. This criterion guides the next design decision; it does not establish statistical significance.

The intervention is a prototype with a visible confirmation and direct access to the saved item. The study uses test data, a fixed task script, and a defined session limit. No production release is implied or authorized by this fictional scenario.

## Fictional result

Suppose all five participants recognize the first successful save, but two become confused when saving the same link again. There is no data loss. These are invented teaching observations, not real measurements.

The primary task criterion was met in this small sample, while a relevant failure case remains unresolved. The evidence would preserve both findings and the limited population. The team would not declare a durable product outcome achieved from five prototype sessions.

## Decision and resulting changes

The illustrative decision is to revise already-saved feedback before exposing the change to real users. The feature acceptance criteria gain an explicit duplicate-save case. The next experiment tests that case and later defines a suitable live evaluation. LEARNINGS records the scoped design lesson with its evidence and revisit condition.

STATE points to the next action, and the roadmap keeps the user-value outcome active. The research cycle can be `completed`, EXP-001 can be `concluded`, and the feature can remain `building`. The outcome is not `achieved` because its live user-value criteria have not been demonstrated.

That distinction lets the system learn honestly while continuing useful work.
