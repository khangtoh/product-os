# ProductOS development plan

This is the framework's development roadmap, not the roadmap of a product adopting ProductOS. Keep applied product direction and work in the target project's own context.

## Current state

Status snapshot: **2026-10-18**. The new event-journal work below is specified only; existing capability validation has not been reclassified as demonstrated operation.

| Capability | Status |
| --- | --- |
| Portable product memory, record model, and loop protocol | Available in the 0.2.0 framework |
| Open-standard-compatible product contract | Available in 0.2.0 with ProductOS operating extensions |
| Guided onboarding and contributor orientation | Available in 0.2.0 through the packaged ProductOS skill and portable prompt. Covered by an offline regression suite and one scripted live run against a fixture project; not exercised on an actual product |
| User-triggered product work | Procedure packaged as [EXECUTION.md](../template/product/EXECUTION.md) and reachable through `run` or natural language; structurally checked but not behaviorally trialled |
| Review, learning, and handling new direction | Described in the operating model; dedicated skill workflows remain to be implemented |
| Recurring execution | Runtime contract documented; no runner or registered scheduler is bundled |
| Structured event journal and version-aware evolution | [Requirements specified](EVENT_LOGGING_REQUIREMENTS.md): committed `.product-os/` events, command/interview/artifact provenance, version detection and compatible migrations; no emitter, capture hooks or migration runner implemented |
| Automated demo validation | [Demo checks workflow](../.github/workflows/demo-checks.yml) runs the offline suite, captured-demo validation and link checks on PRs and pushes to `main`; a manual live interview requires its configured API credential |
| New executable runtime and broader harness support | [TypeScript/Node.js selected](../plans/product-os-metrics-experiments-plan.md#implementation-language-and-harness-portability) for new CLI, events, migrations, MCP and metrics capabilities; thin adapters target Claude Code, Codex, Cursor, OpenCode, Gemini CLI and Pi. Existing Python tools remain; the new runtime and additional integrations are not yet implemented |
| Complete experience on an actual product | Not yet validated as part of this work |

The [onboarding implementation record](ONBOARDING_IMPLEMENTATION.md) captures the completed decisions, implementation, and validation. [Quickstart](QUICKSTART.md) is the adoption interface; this roadmap does not introduce additional commands.

## Remaining work

The sequence below is a proposed development roadmap reconstructed from the available discussion and current implementation. It is not a verbatim record of the earlier full plan or a commitment to delivery dates. Workflow names describe capabilities, not supported skill subcommands.

| Piece | Intended behavior | Dependencies | Completion criteria |
| --- | --- | --- | --- |
| Event journal and version-aware evolution | Record all ProductOS invocations and dispatched commands, interview checkpoints and artifact changes as parseable events in committed `.product-os/`; retain exact producer/artifact versions; apply known compatible structural upgrades or propose unresolved migrations | [Event requirements](EVENT_LOGGING_REQUIREMENTS.md), schema/writer, actual host capture, version metadata, Git integration and versioned migration definitions | Correlated events survive interruption/merge; steps and artifact hashes match reality; effective Git tracking is verified; old content/events survive a validated idempotent migration; capture and compatibility gaps remain explicit |
| Validate user-triggered execution | Exercise the packaged procedure on real work, including a fresh-session resume, and correct what the trials expose | The procedure and `run` entry, an initialized product, and actual tools and authorization for the selected action | Real invocations complete a bounded action or leave a specific blocked/waiting handoff; another session resumes without duplicating work; affected records match actual results |
| Second onboarding seed | Cover the established-contract path, where the rule whose violation destroys user data is "do not promote a populated local contract or replace a root file without direction to consolidate" | The existing fixture layout and checker; a seed with a populated contract, and a preservation check that allows extension while forbidding replacement | A seed whose captured run preserves the original contract's facts and structure; a mutation that overwrites it with the blueprint is rejected |
| Review and learning | Evaluate results against the original requirements and outcome criteria, then update decisions, learning, and priorities | Execution artifacts, observation sources, and an evaluation question; basic verification and handoff must already work in the first execution workflow | A supported or inconclusive result leads to a recorded decision and appropriate context updates; delivery is not mistaken for outcome validation |
| New direction and feedback | Capture owner direction as steering and user feedback as evidence; reconcile each with priorities and active work | Existing record model and current product state; execution must already respect established direction | Representative direction changes and feedback update or retain priorities with a reason, preserve history, and leave a clear next action without changing operating authority |
| Recurring execution | Wake on a useful schedule or event, resume eligible work, persist results, and arrange the next check | A proven user-triggered loop, an actual runner and scheduler, observation, resource limits, and coordination where needed | A registered trigger causes a real run, persists verified results, and resumes correctly on a later run; interruption, uncertain side effects, and observation failure are handled |
| Complete-experience pilot | Exercise onboarding through work, verification, learning, and continuation on an actual product | User-triggered execution and review; recurring execution for the scheduled portion | Real artifacts demonstrate the full path, including a fresh-session handoff; limitations and follow-up improvements are recorded without claiming an unmeasured product outcome |

Start with user-triggered execution, including its basic verification and handoff. Develop richer review and steering workflows around that working path. Begin the product pilot as soon as execution and review are usable, then extend it to recurring execution once a runner is connected.

The operating behavior already has a foundation: follow the [operating guide](OPERATING_GUIDE.md), canonical [loop protocol](../template/product/LOOP.md), and [record model](../template/product/MODEL.md). Future skill work should package and apply those rules rather than create a competing lifecycle. Recurring work must satisfy the [automation runtime contract](AUTOMATION.md).

## Decisions still open

- The skill interface for execution, review, and steering, including whether these use named commands or natural-language routing.
- The runner, scheduling integration, and observation sources for recurring execution. No vendor or mandatory service has been chosen.
- The pilot product, its owner, operating scope, and measures of whether ProductOS helps contributors work and resume effectively. The [fixture project](../demo_project/README.md) is a test harness, not a pilot: its product is fictional and its answers are scripted.
- Release version and timing for subsequent operating capabilities.

Resolve these when designing the corresponding implementation. They do not prevent documenting or using the current onboarding workflow. Keep documentation adoption portable; optional automation must not become a prerequisite for using the model.

## Maintaining this plan

Update a piece's status with links to implementation and validation when it changes. Distinguish documented behavior, locally implemented behavior, merged changes, released capabilities, and demonstrated operation. Keep the dated snapshot accurate when shipping onboarding; a written roadmap or scheduled-check field is not evidence that a runtime is running.

This plan and the onboarding record stay in the framework's guides. They are not copied into the blank product template or installed skill assets as a customer's product history.
