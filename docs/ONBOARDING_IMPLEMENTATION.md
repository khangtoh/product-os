# Onboarding: decisions and implementation

This record explains the onboarding addition to the ProductOS framework. It records the implemented design and its rationale; the [development plan](DEVELOPMENT_PLAN.md) tracks the remaining operating workflows.

Status snapshot: **2026-09-26**. Onboarding is merged and released as part of ProductOS 0.2.0 together with the open-standard-compatible product contract. This is not a claim of validation on an actual customer product or of a running autonomous loop.

Update **2026-09-27** (unreleased): named `resume` and `orient` entries, an inline argument hint, and a Claude Code installation target. See [entry hints and Claude Code](#entry-hints-and-claude-code).

## Intent and decisions

The requested inspiration was Impeccable's conversational context-onboarding approach: help a user establish context by asking for what is missing and save it for later agent work. ProductOS applies that approach to product intent, requirements, priorities, and a resumable starting point.

| Decision | Rationale and resulting behavior |
| --- | --- |
| Offer a Codex skill, a Claude Code skill, and a portable prompt | Provide a discoverable entry point while retaining a workflow usable without a particular runtime. Both use the same onboarding procedure. |
| Establish a complete initial brief | Cover the product's vision, users, experience, requirements, boundaries, success, priorities, and starting point, rather than collecting only enough detail for one immediate task. Applicable detail and explicit deferrals keep this practical. |
| Inspect first and ask two or three related questions per round | Reuse reliable project context and previous answers. Adapt the conversation instead of repeating settled questions or presenting one large questionnaire. |
| Help users make unresolved decisions | Present options and tradeoffs. A user-selected hypothesis is direction, not validated evidence. Explicit deferrals retain consequences and a discovery action; silence is not agreement. |
| Save between answered rounds | Store supported answers in their canonical homes and coverage in STATE so interrupted setup can resume without reconstructing the chat. |
| Use a root product contract for new projects | Give contributors a shared entry point, with supporting context under `product/` and a local PRODUCT pointer. Preserve established contracts and the standalone-context exception. |
| Keep requirements separate from durable vision | Save initial workflows and acceptance criteria in REQUIREMENTS; keep the product contract concise and link detailed specifications instead of duplicating them. |
| Use Now / Next / Later outcome priorities | Connect the brief to a proposed first action without inventing deadlines, commitments, or a feature backlog. |
| Distinguish onboarding from contributor orientation | A person joining an initialized project needs current context and a contribution path, not a reset of ownership, priorities, or the interview. |
| Offer the first loop after setup | Make the handoff useful while keeping onboarding completion separate from implementation, release, scheduling, and evidence of an achieved outcome. |

These decisions are implemented through the canonical [onboarding coverage and completion rules](../template/product/MODEL.md#onboarding-completion) and [onboarding procedure](../template/product/ONBOARDING.md). Those sources govern behavior; this record explains it rather than introducing additional rules.

## Implementation

### Entry points and installation

The [skill](../skills/product-os/SKILL.md) handles `$product-os init` (`/product-os init` in Claude Code), `resume`, `orient`, and the equivalent natural-language requests. A bare invocation reports readiness and offers the appropriate next step. Advice requests remain advice. Execution later gained its own `run` entry, recorded in the [execution implementation record](EXECUTION_IMPLEMENTATION.md); review, steering, and scheduling requests are still directed to the existing loop and operations guidance without claiming unsupported subcommands.

The [installer](../scripts/install_skill.py) accepts an existing target directory through `--project` and creates `.agents/skills/product-os/` for Codex, `.claude/skills/product-os/` with `--agent claude`, or both with `--agent both`. It bundles the skill entry point and the canonical blank template under `assets/product/`, using only Python's standard library. The source skill alone is not a complete installed package.

Installation does not initialize product context or edit root agent instructions. It rejects a target inside the framework checkout, refuses an existing skill destination or unsafe symlinked parents, and removes its newly created partial package if copying fails. Replacement is deliberate; it does not migrate applied product records. [Quickstart](QUICKSTART.md) documents installation, manual packaging, and the portable prompt.

### Saved context and session continuity

For a new default-layout project, onboarding creates the canonical root `PRODUCT.md` and uses `product/PRODUCT.md` as a navigation pointer. Existing canonical contracts keep their established locations. If the product context folder is itself the repository root, its contract stays there instead of moving to a parent or becoming a self-link. Placement is defined in [MODEL](../template/product/MODEL.md#canonical-homes).

Supporting documents hold vision, requirements, strategy, roadmap, current state, and relevant operating context. STATE records interview coverage, remaining questions, explicit deferrals, and the next topic. Existing facts, record IDs, history, active work, design guidance, and local conventions are preserved when adding missing context.

Onboarding merges a product-context pointer into the target's root agent instructions, preserving unrelated instructions. New contracts retain a standalone `Platform` heading, with constraints separate. The template remains self-contained before adoption; root contract links are rewritten for the target layout when onboarding creates it.

A read-only target receives proposed content and an explicitly unsaved checkpoint. Ambiguous product scope is resolved before writing. A contributor orientation does not restart setup. These paths share the same procedure and completion model.

### Completion and compatibility

Completion requires saved coverage of the required areas, working references and agent pointers, an aligned roadmap and first action, and a linked summary presented to the user for correction. An additional approval round is not required for answers already supplied. Readiness for the next action is reported separately: a complete brief may still need discovery, access, or another dependency resolved before implementation.

The addition introduces REQUIREMENTS and onboarding guidance, plus checkpoint and navigation changes. ProductOS 0.2 also makes the promoted contract a superset of the open PRODUCT.md convention while retaining ProductOS operating sections. Typed-record metadata and lifecycle remain unchanged. The [upgrade guidance](CUSTOMIZATION.md#adding-guided-onboarding-to-a-010-instance) explains how to merge these additions while preserving applied context; installed skill updates are separate from product-context upgrades. The [fictional walkthrough](../examples/onboarding.md) illustrates the experience without placing example facts in the template.

### Entry hints and Claude Code

Impeccable also showed that an inline hint helps users find a skill's entries: Claude Code displays a skill's `argument-hint` after the typed command. The skill declares `[init|resume|orient] [target or question]`. `resume` and `orient` name paths the guide already defined, so no new workflow was added, and run, review, and scheduling remain unsupported.

The Agent Skills specification that Codex follows has no top-level `argument-hint`, so the source and Codex copy keep it under `metadata:` and still pass the skill validator. The installer hoists it to the top level only in the Claude Code copy. Codex shows no inline hint. `--agent` defaults to `codex`, so existing installation commands behave as before.

## Validation record

The following checks were completed during implementation on 2026-09-26. They are evidence of local behavior and simulated onboarding coverage, not a real-product pilot or proof of improved user outcomes.

| Check | Observed result |
| --- | --- |
| Six automated [installer tests](../scripts/test_install_skill.py) | Passed: self-contained packaging without initialization, preservation of context and other skills, refusal of reinstallation, rejection of missing/framework targets, symlink refusal, and cleanup after copy failure |
| CLI and skill validation | Installation succeeded in a temporary project; repeat installation was refused. Source and freshly installed skill entry points passed the skill validator. |
| New-project interview simulations | Saved a root contract, supporting context, explicit hypotheses/deferrals, priorities, and a first action without executing product work or registering schedules |
| Interrupted setup and continuation | Saved partial coverage, incorporated subsequent answers, and preserved a paused incomplete checkpoint without repeating settled questions |
| Existing-product adoption | Preserved original contract content, roadmap, design guidance, active work, and unrelated agent instructions while adding needed onboarding context |
| Contributor, ambiguous-target, and read-only scenarios | Oriented without rewriting context, requested target clarification before writing, and reported unsaved proposals honestly |
| Platform heading follow-up | An initial simulation combined platform with boundaries; the guide was clarified and a fresh installed-skill simulation retained a standalone Platform section |
| Documentation and template checks | Repository and isolated-template relative links and anchors resolved; generic-template leakage checks and whitespace checks passed; record templates were unchanged |
| Offline onboarding regression checks ([checker](../scripts/check_instance.py), [tests](../scripts/test_check_instance.py)), added 2026-09-27 | Passed. A captured completed instance satisfies the canonical-home, required-area, front-matter, lifecycle, measurement, and link rules; a bare installation fails those checks; 28 mutations of the captured instance are each rejected by their named check. The checker parses record types, id forms, and lifecycle states from MODEL.md rather than restating them. Deterministic, offline, no agent involved. |
| Scripted live onboarding run ([runner](../scripts/run_onboarding_e2e.py), opt-in), 2026-09-27 | A scripted seven-turn headless interview plus two catch-all nudges, in a temporary project outside the checkout, produced an instance passing every check above and left the installed skill assets byte-identical. One sample, one model, one CLI version, one runtime. |

The 2026-09-27 update added these checks:

| Check | Observed result |
| --- | --- |
| Thirteen automated installer tests | Passed: the six above plus hint placement in the source, Claude hoisting with an unchanged body and bundled assets, preservation of other metadata, both-runtime installation, refusal without writes when either destination exists, and rejection of an unknown runtime |
| CLI and skill validation | `--agent both` installed both copies, and a repeat `--agent claude` was refused. The source and Codex copy passed the skill validator; the Claude copy fails it only on its top-level `argument-hint`, as intended |
| Claude Code 2.1.283 | Typing `/product-os ` rendered `[init|resume|orient] [target or question]` inline. No turn was submitted, so interview behavior of the new entries was not exercised |

Installer tests can be rerun with:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

The first two checks are now an automated regression suite committed to the repository; [the fixtures](../demo_project/README.md) hold the mock product, the scripted turns, the expectation spec, and the captured instance. The remaining scenarios — contributor orientation, ambiguous target scope, and read-only access — stay manual, as described in [framework maintenance guidance](CUSTOMIZATION.md#improve-the-framework).

These are regression checks over one captured run, not validation of onboarding. They cannot show that the interview asks good questions, that unscripted users reach the same coverage, that the Codex entry point behaves the same way, or that any product outcome improved. A captured instance goes stale when the template changes; a provenance digest fails the suite when it does, and the only sanctioned fix is a recapture.

The first complete live run exposed seven defects, all in the checker, the expectation spec, or the test harness, and no gap in the procedure itself. They are recorded with their classifications in [the fixture README](../demo_project/README.md).

## Limits and follow-up

The current skill supplies setup and orientation. It does not provide dedicated run, review, or scheduling commands, install a runner, or register wake-ups. Users can request product work through the existing documented loop, but packaged operating workflows and a complete real-project pilot remain on the [development plan](DEVELOPMENT_PLAN.md#remaining-work).

Update this record when the implemented decisions materially change, and update its status snapshot when the onboarding addition is merged or released. Keep runtime success, product outcome evidence, and delivery status distinct.
