# Run the next product action

Execution carries one bounded action from the current product context through verification to a saved handoff. It applies the canonical protocol in [LOOP.md](LOOP.md) and the record rules in [MODEL.md](MODEL.md); it does not define a second lifecycle. Use it for ordinary product work, not for initial setup — that is [ONBOARDING.md](ONBOARDING.md).

If the ProductOS skill is installed, invoke `$product-os run` in Codex or `/product-os run` in Claude Code, or simply ask for the next action in your own words. Otherwise paste:

```text
Read product/EXECUTION.md and carry out the next eligible bounded action.
Load the product context and current state, resume existing work or select
the next action, execute within established scope, verify the result, and
save a handoff.
```

Adjust the path if the folder lives elsewhere. Both entry points use this guide. One invocation produces either a completed bounded action or an accurate blocked or waiting handoff. Neither outcome is a validated product result.

## 1. Orient

Follow the target project's existing instructions first. Read [PRODUCT.md](PRODUCT.md) for intent, [STATE.md](STATE.md) for current truth and active work, [ROADMAP.md](ROADMAP.md) for priority order, and the most recent steering. Read [operations](operations/README.md) for actual capabilities and operating scope, and [LEARNINGS.md](LEARNINGS.md) where a prior lesson applies. Load the linked records the selected work needs; do not read the entire history.

Establish what is actually true before acting. A handoff describes the state at the time it was written, so inspect reality where the action depends on it: current code, branch and pull request state, deployment target, experiment exposure, and service health. Treat a stale or contradicted handoff as a reason to inspect, not as permission to proceed on its assumptions.

If the product context is missing or the initial brief is incomplete, say so and offer onboarding instead of improvising direction. If several products or contracts could govern the request, resolve the scope with the user before writing. An installed skill's asset folder is a blank source and never the target.

## 2. Resume or select one action

Prefer continuing existing work to opening new work. Check STATE's active cycle and active work table first.

| Situation | Approach |
| --- | --- |
| An active cycle covers this request | Resume it; update its record rather than creating a parallel cycle |
| An active cycle exists for other work | Leave it intact; note it and select within remaining priority |
| A cycle is waiting on a trigger that has now occurred | Resume from its recorded next action after confirming the trigger really fired |
| A cycle is blocked | Check whether the blocker still holds before re-attempting; otherwise select independent authorized work |
| No active cycle | Select the next eligible action, then create a cycle from [the template](templates/cycle.md) if the work is substantive |

Apply [LOOP.md's eligibility rules](LOOP.md#choose-eligible-work): address active incidents and breached constraints first, then explicit owner direction, then due evaluations and unfinished verification, then roadmap priority. Within an outcome, choose the smallest step that delivers value or removes a consequential uncertainty. An inexpensive research step can outrank implementation when a key assumption is untested.

Select exactly one action and state it concretely, with the record it belongs to and why it is next. If the highest-priority work is not authorized or not ready, say which dependency stops it instead of silently substituting easier work. Reading, answering a question, and small standalone corrections do not need a new cycle.

## 3. Bound the run

Before acting, record the actor, the action, its deliverable, the environment, the applicable effort or cost limit, the exposure limit where a release is involved, and the stop conditions. Use the project's actual limits or the explicit scope of this session; never invent a budget. A research action may be bounded by its deliverable instead of a spend amount.

Existing authorization persists across sessions. This guide cannot expand tool permissions, approve a release, or create operating authority that operations does not record. Missing access blocks the action that needs it and nothing else: continue authorized preparation or other eligible work.

For a change that will reach users, establish the release target, the applicable authority, the observation method, and the recovery path before building, per [LOOP.md](LOOP.md#release-and-observation). If any of those is absent, keep the action inside a safe scope and record what remains before exposure.

## 4. Execute

Enter the loop at the step the work actually needs. Not every run builds or releases; research, verification, evaluation, and incident recovery are ordinary runs.

- **Design**, when scope or criteria are unsettled: define the smallest scope, the observable acceptance criteria, and how the result will be observed. Fix an experiment's measure, comparison, population, duration or sample plan, guardrails, and stopping rules before any exposure.
- **Build**, within the authorized scope: implement the change and keep the artifact reference. Follow the project's own engineering conventions; ProductOS does not override them.
- **Release**, only under established authority: use the recorded rollout path, then confirm the deployment rather than assuming it.
- **Operate or recover**, for an incident: mitigate using verified steps and actual authority, and record the actions taken.
- **Evaluate**, for a due result: compare observations with the original criteria without revising them.

Stay inside the bound from step 3. If the work turns out to be larger than its scope, stop at the limit, record what was completed, and propose the split rather than expanding the run silently. If new direction arrives mid-run, capture it as steering and reconcile it before continuing.

Before repeating any uncertain external action, confirm its actual result. A timeout, a lost connection, or an unread response does not prove failure, and a duplicate release, message, or payment can be worse than a delay. Record external action IDs or idempotency keys where available.

## 5. Verify

Check the result against the criteria that were set, not against the intention. Run the project's actual tests, checks, or evaluations where they exist, and report what they returned. State plainly when a check was unavailable, skipped, or inconclusive.

| Work | Verification that closes the run |
| --- | --- |
| Behavior change | Acceptance criteria met, regression risk considered, instrumentation confirmed working |
| Release | Deployment confirmed live, exposure as intended, recovery path available, observation time recorded |
| Research | Question addressed, sources and method recorded, limits stated |
| Incident recovery | Recovery verified against the symptom, prevention follow-up assigned |
| Evaluation | Result compared with original criteria, confidence and uncertainty explained |

Delivery is not an outcome. Verification establishes that the change behaves as specified; whether it produced the intended product change is a separate evaluation with its own observation window. Do not mark an outcome achieved, or an experiment supported, from a successful build. Preserve negative and inconclusive results as they are.

## 6. Record results and hand off

Save what actually happened in its canonical home, per [MODEL.md](MODEL.md#canonical-homes). Scale the writing to the decision; a small correction needs a change note, not a record chain.

| Result | Record it in |
| --- | --- |
| Work performed, artifacts, and how it resumes | The cycle record |
| Delivered or changed behavior | The feature record and REQUIREMENTS where criteria changed |
| Observation, measurement, or user report | An evidence record with its source and freshness |
| Material choice with alternatives | A decision record, with a revisit condition |
| Reusable conclusion | [LEARNINGS.md](LEARNINGS.md), with its evidence and scope |
| Changed priority | [ROADMAP.md](ROADMAP.md), which remains the only canonical priority order |

Then update [STATE.md](STATE.md) so another session can continue without repeating the work: current truth, active work and owner, blockers, the concrete next action, and an exact next observation time or event trigger. Keep it brief, preferably under 100 lines, with the detail in the cycle. Include actual branches, pull requests, deployment references, and external action IDs where they apply.

Set the cycle's final state honestly — `completed`, `waiting`, `blocked`, or `cancelled` — and make sure the records agree with the actual result. Do not mark work complete to clear a queue, and do not leave a finished action recorded as active.

## 7. Stop, block, or wait

Ending a run without finishing the action is a valid result when it is reported accurately.

- **Blocked:** name the specific dependency, the responsible actor if known, what was completed, and the next action once it clears. Keep the record's lifecycle state and continue other independent authorized work if any exists.
- **Waiting:** record the exact event or time that should resume the work, and what to inspect on return. Avoid repeat checks scheduled before evidence could change.
- **Stopped at a limit:** record the limit reached, the verified partial result, and the remaining scope.

A scheduling field is a written intention, not a registered wake-up. If a runner is available, register the trigger and record whether that registration actually succeeded; if none is available, say the continuation depends on someone invoking it. See the project's [operations](operations/README.md) context for what is genuinely configured.

For a read-only target, present the proposed changes and the handoff in the response and state clearly that nothing was saved. Do not describe unsaved work as recorded.

Finish by telling the user what was done, what it was verified against, what changed in the context, and what happens next. Report an unfinished action as unfinished. One completed run is progress, not proof that the product improved.
