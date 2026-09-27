# Execution: decisions and implementation

This record explains the packaged execution procedure added to the ProductOS framework. It records the implemented design and its rationale; the [development plan](DEVELOPMENT_PLAN.md) tracks the remaining operating workflows.

Status snapshot: **2026-09-27**. The procedure and its skill entry are implemented and structurally checked locally. The changes are uncommitted and unreleased at this snapshot, and the recorded framework release remains 0.2.0. No behavioral trial and no real-product run have been performed; see [limits](#limits-and-follow-up).

## Intent and decisions

Before this addition, the skill supplied setup and orientation and explicitly declined execution requests, pointing users at [LOOP.md](../template/product/LOOP.md) instead. The protocol was documented but nothing packaged it into a repeatable session. This addition closes that gap for the user-triggered case only.

| Decision | Rationale and resulting behavior |
| --- | --- |
| Hybrid interface: `run` plus natural-language routing | `run` gives a deliberate, documentable entry; equivalent requests in ordinary language reach the same procedure. Matches how `init` already worked, so the skill gains no interface style of its own. This resolves the plan's open interface question for execution; review and steering should follow the same pattern unless a trial argues otherwise. |
| Procedure in the portable template, not the skill | [EXECUTION.md](../template/product/EXECUTION.md) ships in `template/product/` beside ONBOARDING.md, so the method works from a prompt or by hand without the skill installed. The installer already copies the whole template, so it is bundled as an asset with no packaging change. |
| Apply LOOP and MODEL rather than restate them | LOOP remains the canonical protocol and MODEL the canonical record rules. EXECUTION is the session-level procedure that applies them and links to their sections. This mirrors the existing ONBOARDING/MODEL split and avoids the competing lifecycle that [framework maintenance guidance](../AGENTS.md) prohibits. |
| One action per invocation | A run selects exactly one action, states why it is next, and bounds it before acting. This keeps a run reviewable and makes the handoff meaningful, instead of producing an open-ended work session. |
| Resume before selecting | The procedure checks STATE's active cycle first and prefers continuing existing work, including resuming waiting cycles whose trigger actually fired. This is the main defense against two sessions duplicating the same work. |
| Treat a handoff as a claim to verify | A handoff describes the state when it was written, so the procedure requires inspecting actual code, branch, deployment, and exposure where the action depends on them, rather than proceeding on the handoff's assumptions. |
| Grant no authority | The guide cannot expand tool permissions, approve a release, or invent operating scope. Missing access blocks only the action needing it. Authorization comes from the session and the project's operations context, as before. |
| Make a blocked or waiting run a first-class result | A run ends either with a completed bounded action or with a specific blocked, waiting, or stopped-at-limit handoff, and must report which. This prevents both false completion and silent scope expansion. |
| Keep verification separate from outcome evaluation | Verification establishes that a change behaves as specified. Whether it produced the intended product change is a later evaluation with its own observation window. A successful build never marks an outcome achieved. |

## Implementation

### Entry points

The [skill](../skills/product-os/SKILL.md) now routes by entry: onboarding for `init` and setup requests, orientation for someone joining, and execution for `run` or a request to do the next product work, continue, or resume. A bare invocation reports setup readiness and the current next action, then offers the applicable entry. Review, steering, and scheduling requests are still directed to the target's loop, model, and operations context without claiming a workflow that does not exist.

Onboarding and execution stay separate. An uninitialized or incomplete project is reported and offered `init` rather than having product intent improvised for it; a setup request does not authorize implementation, and an execution request does not reopen the interview. [ONBOARDING.md](../template/product/ONBOARDING.md)'s closing offer now hands off to the execution procedure instead of proposing an ad-hoc prompt.

### The procedure

[EXECUTION.md](../template/product/EXECUTION.md) runs in seven steps: orient in actual current state; resume or select one action; bound the run; execute at whichever loop step the work needs; verify against the criteria that were set; record results and hand off; and stop, block, or wait accurately. Research, verification, evaluation, and incident recovery are ordinary runs — not every run builds or releases.

Safety rules carried from LOOP are stated where a running session meets them: confirm an uncertain external action's real result before repeating it, since a duplicate release or payment can be worse than a delay; stop at the recorded limit and propose a split instead of quietly widening scope; capture mid-run direction as steering and reconcile it before continuing; and for a read-only target, present proposals and say plainly that nothing was saved.

The procedure writes to the canonical homes MODEL already defines and adds no record type, state, or metadata field. ROADMAP remains the only canonical priority order, and STATE stays the short handoff.

### Wiring

The template's [README](../template/product/README.md), [AGENTS.md](../template/product/AGENTS.md), and [STATE.md](../template/product/STATE.md) point to the procedure; the [operating guide](OPERATING_GUIDE.md) names it as the packaged path through the protocol; and [quickstart](QUICKSTART.md) documents the `run` entry and the equivalent portable prompt. The installer now requires EXECUTION.md and LOOP.md in the source checkout alongside ONBOARDING.md and MODEL.md, so an incomplete checkout fails at install time rather than at use. [Upgrade guidance](CUSTOMIZATION.md#adding-the-execution-procedure-to-an-earlier-instance) covers adding the procedure to an earlier instance.

## Validation record

The following checks were completed on 2026-09-27. They establish structural correctness and packaging only. They are not evidence that the procedure produces good execution behavior.

| Check | Observed result |
| --- | --- |
| Six automated [installer tests](../scripts/test_install_skill.py) | Passed. The asset assertion compares a full template snapshot, so it covers the new file without modification. |
| Fresh installation into a temporary project | Succeeded. All four asset paths the skill names — ONBOARDING, EXECUTION, MODEL, LOOP — resolve in the installed package. |
| Relative-link and heading-anchor check, repository-wide and in an isolated copy of the template | Passed after one fix. The first pass found an invented anchor, `LOOP.md#release-and-observation-end`; the real heading is `## Release and observation`. Corrected and rechecked. |
| Whitespace and template-leakage checks | Passed. No trailing whitespace, no missing final newlines, and no dates, names, URLs, or project-specific references in the template. |

Installer tests can be rerun with:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

No behavioral scenario was exercised. Unlike the [onboarding addition](ONBOARDING_IMPLEMENTATION.md#validation-record), which was validated through agent-driven interview trials in temporary fixtures, this procedure has not been run against an initialized product. Prose review is not validation of a procedure.

## Limits and follow-up

The skill supplies setup, orientation, and execution. It provides no review, steering, or scheduling workflow, installs no runner, and registers no wake-ups. Every run still depends on a person or a separate runner invoking it.

The following remain to be exercised before this capability should be called validated, and are tracked as the plan's [validate user-triggered execution](DEVELOPMENT_PLAN.md#remaining-work) row:

- A real bounded action, carried from selection through verification to a saved handoff.
- A fresh-session resume that continues the saved handoff without duplicating the work.
- A blocked run, a waiting run whose trigger has not fired, and a run stopped at its limit.
- An execution request against an uninitialized or incomplete brief.
- An execution request whose highest-priority action is not authorized.
- A read-only target.

Expect the trials to change the procedure. Update this record when they do, keep its status snapshot accurate through merge and release, and keep run success, verification, and product outcome evidence distinct.
