# Operating with ProductOS

The full protocol lives in [LOOP.md](../template/product/LOOP.md), and [EXECUTION.md](../template/product/EXECUTION.md) is the step-by-step procedure for carrying one action through it. This guide explains how to use both without turning every small action into a documentation exercise.

## Start a work session

With the skill installed, `$product-os run` follows [EXECUTION.md](../template/product/EXECUTION.md) for you; the same procedure works from a prompt or by hand.

Read PRODUCT, STATE, and current steering. Check the roadmap and relevant records. Resume existing work if it covers the same task; do not open a duplicate because another conversation started.

Check actual service and deployment state where the action depends on them. A stale handoff is a reason to inspect reality. Choose the highest-priority eligible action, identify its owner, and set a concrete deliverable or run limit.

## Turn input into the right kind of record

| Input | Capture it as | Then |
| --- | --- | --- |
| Owner changes direction | Steering | Apply its scope to priorities and active work |
| User reports friction | Evidence | Assess the affected cohort, severity, and related opportunity |
| Team proposes a solution | Feature or experiment proposal | Link it to a problem/outcome and identify uncertainty |
| Dashboard changes | Evidence | Verify the definition, population, freshness, and significance |
| Service fails | Incident | Mitigate using actual authority and verified recovery steps |
| Work produces a result | Evidence plus a decision | Update product behavior, priorities, or operating practice |

People can provide input in ordinary language. The contributor or agent can structure it afterward. Capture the source and distinguish observation, interpretation, hypothesis, and direction.

## Prioritize outcomes

An outcome is a change we want, an opportunity is a problem worth solving, and a feature is one possible intervention. A roadmap of features alone can hide whether the product is improving.

Respond to active incidents and breached constraints, apply explicit owner direction, and complete due evaluations before opening competing bets. Rank other work by expected impact, evidence, urgency, effort, and reversibility. Avoid numerical precision when the inputs are guesses.

When a key assumption is uncertain, an inexpensive research step may be more valuable than implementation.

## Use enough documentation for the decision

| Work | Usually sufficient |
| --- | --- |
| Small correction | Existing record or a brief change note; no new cycle needed |
| Scoped bug fix | Linked feature/incident, acceptance evidence, and handoff if substantive |
| Product bet | Outcome, relevant evidence, intervention, evaluation protocol, result, and decision |
| Research | Question, source/method, observations, limits, and next decision |
| Operational recovery | Incident, actual actions, recovery evidence, and prevention follow-up |

Create directories and records only as needed. Links may point to existing tools: keep the canonical fact in one home and summarize its meaning here.

## Deliver and observe

Before implementation, define observable behavior and acceptance criteria. Before an experiment, define its primary measure, comparison, population, duration/sample rationale, guardrails, and stopping rules. Before a release, establish the target, applicable authority, observation, and recovery path.

After release, record the actual artifact and observation time. For AI behavior changes, preserve model, prompt, tool, and evaluation versions. Use qualitative evidence honestly when a quantitative comparison is not justified.

## Decide from results

State what happened, how confident the conclusion is, and what changes because of it. An experiment can support a hypothesis, fail to support it, or remain inconclusive. A negative result is useful if it changes the next decision.

Preserve the original hypothesis and criteria. Do not quietly revise them to match results. Record material choices with alternatives, rationale, affected records, and conditions for revisiting.

Add reusable lessons to LEARNINGS with evidence and scope. Then update the roadmap, product contract, design, evaluation, or runbook as warranted. Recording a lesson without applying it leaves the loop incomplete.

## Collaborate and hand off

Humans and agents use the same ownership and handoff fields. One actor may research while another implements or reviews, but concurrency is optional. Use real coordination when available; a Markdown owner field is not a lock.

Keep STATE small: current truth, active work, blockers, next action, and next check. Put detail in the cycle. Include actual branches, PRs, deployment references, and external action IDs when applicable. Check uncertain external results before retrying.

If work is waiting, name the dependency and event/time that should resume it. If blocked, continue independent authorized work. If nothing useful is eligible, leave an accurate handoff rather than producing another empty plan.

## Review the system itself

At useful intervals, ask whether contributors can resume work, experiments lead to decisions, and repeated failures lead to better operation. Improve the model when friction is observed. Changes to the method should have a reason; they do not create new operating authority.
