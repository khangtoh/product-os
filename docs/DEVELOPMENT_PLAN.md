# ProductOS development plan

This is the framework's development roadmap, not the roadmap of a product adopting ProductOS. Keep applied product direction and work in the target project's own context.

## Current state

Status snapshot: **2026-09-26**.

| Capability | Status |
| --- | --- |
| Portable product memory, record model, and loop protocol | Available in the 0.1.0 framework |
| Guided onboarding and contributor orientation | Implemented and validated locally; changes are uncommitted and unreleased at this snapshot |
| User-triggered product work | Can follow the documented loop through an ordinary prompt; no dedicated operating workflow is packaged in the skill |
| Review, learning, and handling new direction | Described in the operating model; dedicated skill workflows remain to be implemented |
| Recurring execution | Runtime contract documented; no runner or registered scheduler is bundled |
| Complete experience on an actual product | Not yet validated as part of this work |

The [onboarding implementation record](ONBOARDING_IMPLEMENTATION.md) captures the completed decisions, implementation, and validation. [Quickstart](QUICKSTART.md) is the adoption interface; this roadmap does not introduce additional commands.

## Remaining work

The sequence below is a proposed development roadmap reconstructed from the available discussion and current implementation. It is not a verbatim record of the earlier full plan or a commitment to delivery dates. Workflow names describe capabilities, not supported skill subcommands.

| Piece | Intended behavior | Dependencies | Completion criteria |
| --- | --- | --- | --- |
| Ship onboarding | Make the reviewed onboarding implementation available through the repository's delivery process | Review the local implementation, documentation, and validation evidence | Changes are committed, reviewed, and merged; the changelog and release status accurately describe what is available |
| User-triggered execution | Load context, resume existing work or select the next eligible action, execute within scope, verify, and save a handoff | Established product context, the existing loop protocol, and actual tools and authorization for the selected action | An invocation completes a bounded action or leaves a specific blocked/waiting handoff; another session resumes without duplicating work; affected records match actual results |
| Review and learning | Evaluate results against the original requirements and outcome criteria, then update decisions, learning, and priorities | Execution artifacts, observation sources, and an evaluation question; basic verification and handoff must already work in the first execution workflow | A supported or inconclusive result leads to a recorded decision and appropriate context updates; delivery is not mistaken for outcome validation |
| New direction and feedback | Capture owner direction as steering and user feedback as evidence; reconcile each with priorities and active work | Existing record model and current product state; execution must already respect established direction | Representative direction changes and feedback update or retain priorities with a reason, preserve history, and leave a clear next action without changing operating authority |
| Recurring execution | Wake on a useful schedule or event, resume eligible work, persist results, and arrange the next check | A proven user-triggered loop, an actual runner and scheduler, observation, resource limits, and coordination where needed | A registered trigger causes a real run, persists verified results, and resumes correctly on a later run; interruption, uncertain side effects, and observation failure are handled |
| Complete-experience pilot | Exercise onboarding through work, verification, learning, and continuation on an actual product | User-triggered execution and review; recurring execution for the scheduled portion | Real artifacts demonstrate the full path, including a fresh-session handoff; limitations and follow-up improvements are recorded without claiming an unmeasured product outcome |

Start with user-triggered execution, including its basic verification and handoff. Develop richer review and steering workflows around that working path. Begin the product pilot as soon as execution and review are usable, then extend it to recurring execution once a runner is connected.

The operating behavior already has a foundation: follow the [operating guide](OPERATING_GUIDE.md), canonical [loop protocol](../template/product/LOOP.md), and [record model](../template/product/MODEL.md). Future skill work should package and apply those rules rather than create a competing lifecycle. Recurring work must satisfy the [automation runtime contract](AUTOMATION.md).

## Decisions still open

- The skill interface for execution, review, and steering, including whether these use named commands or natural-language routing.
- The runner, scheduling integration, and observation sources for recurring execution. No vendor or mandatory service has been chosen.
- The pilot product, its owner, operating scope, and measures of whether ProductOS helps contributors work and resume effectively.
- Release version and timing for the onboarding addition and subsequent capabilities.

Resolve these when designing the corresponding implementation. They do not prevent documenting or using the current onboarding workflow. Keep documentation adoption portable; optional automation must not become a prerequisite for using the model.

## Maintaining this plan

Update a piece's status with links to implementation and validation when it changes. Distinguish documented behavior, locally implemented behavior, merged changes, released capabilities, and demonstrated operation. Keep the dated snapshot accurate when shipping onboarding; a written roadmap or scheduled-check field is not evidence that a runtime is running.

This plan and the onboarding record stay in the framework's guides. They are not copied into the blank product template or installed skill assets as a customer's product history.
