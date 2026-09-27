---
name: product-os
description: Run shared product work with ProductOS. Onboard a new or existing project through a product interview, resume incomplete setup, orient a new contributor, or carry out the next eligible bounded product action from established context and save a resumable handoff. Use for ProductOS setup, orientation, and product execution; not for ordinary code edits unrelated to product direction.
metadata:
  argument-hint: "[init|resume|orient|run] [target or question]"
---

# ProductOS

Help humans and agents share product context and act on it. This skill provides onboarding, contributor orientation, and execution of one bounded action from established product context. It does not provide dedicated review, steering, or scheduling workflows, and it installs no runner.

## Choose the entry

Recognize the explicit verb or the equivalent request in ordinary language; both route to the same procedure.

- `init`, a request to set up ProductOS, or a request to complete its onboarding: follow the onboarding guide below.
- `resume`, or a request to continue an interrupted setup: follow the guide from the saved onboarding checkpoint, asking only the next unresolved questions. With no checkpoint, say so and offer `init`.
- `orient`, or a person joining an initialized project: use the guide's orientation path, preserving established direction.
- `run`, or a request to do the next product work, continue established work, or pick up where the last session stopped: follow the execution guide.
- A specific product action named by the user that the established context and authority already cover: follow the execution guide, selecting that action.
- Bare invocation with no task: inspect the target's existing contract and current state, briefly describe setup readiness and the current next action, and offer `init`, `resume`, `orient`, or `run`. Do not start writing, interviewing, or executing until the intent is clear.
- Advice about the method: answer from the bundled guide and model without starting setup or work.
- A review, steering, or scheduling request: point to the target's loop, model, and operations context for the requested workflow. Do not claim a skill subcommand that does not exist.

`resume` and `run` are different: `resume` continues an unfinished interview, `run` carries out product work once a brief exists. Onboarding and execution stay separate. An uninitialized or incomplete project needs setup before execution has direction; report that and offer `init` rather than inventing product intent. A setup request does not authorize implementation, and an execution request does not reopen the interview.

## Load and apply the guides

Resolve resources relative to this SKILL.md's directory, not the project's working directory. The installed package contains `assets/product/ONBOARDING.md`, `assets/product/EXECUTION.md`, `assets/product/MODEL.md`, and `assets/product/LOOP.md`. Read the guide for the selected entry plus the canonical rules it applies: MODEL for record and completion rules, LOOP for the operating protocol. Other files in `assets/product/` are blank project templates; load only those needed for the work. The source checkout is packaged by the installer; if assets are missing, report an incomplete installation rather than improvising templates.

Keep the target project separate from the skill directory and its bundled assets. Follow the target's existing root instructions. Locate any existing ProductOS instance, product contract, and onboarding checkpoint before creating files. If several products could be the target, establish which one the user means before writing.

For an explicitly requested initialization with no instance, copy the bundled product folder into the target as `product/` without overwriting an existing path. If the path already exists, inspect and merge only missing ProductOS documents needed for onboarding; never replace project records with bundled blanks. Resolve conflicting meanings of the directory with the user. Do not copy the entire framework repository, the skill's own files, or fictional examples into product context.

Then follow the guide in the target project. Respect established local model adaptations; an installation update is not authorization to migrate product records. For older instances missing a guide, use the bundled procedure with their existing model and preserve their lifecycle conventions.

## Onboarding

When creating or promoting a PRODUCT.md, follow the bundled MODEL and ONBOARDING compatibility rules. Preserve open-standard metadata, canonical headings, valid machine islands, and unknown sections; resolve Register during onboarding rather than inventing it.

Interview through the available structured question tool or ordinary conversation. Wait for answers to questions that determine product direction. Save supported answers and progress in project-owned files, never in the installed skill assets. Do not infer user approval from silence.

Finish with links to saved context, unresolved decisions, and the first proposed loop. An onboarding-only request ends there. Do not implement the product, register schedules, or suggest that setup proves a user outcome was achieved.

## Execution

Orient in the project's actual current state before acting, and inspect reality where the action depends on it rather than trusting a stale handoff. Resume existing work in preference to opening new work. Select one eligible action, bound it, execute within established authority, verify against the criteria that were set, and save results and a handoff in project-owned files.

This skill grants no permissions. Use only the tools and authority the session and the target's operations context already provide. Missing access blocks the action that needs it, not other authorized work. Confirm the result of an uncertain external action before repeating it.

End with a completed bounded action or an accurate blocked, waiting, or stopped-at-limit handoff, and report which it was. Keep delivery distinct from a validated product outcome: a verified change is not evidence that the intended outcome was achieved. Do not mark work complete to clear a queue, expand scope past its bound without saying so, or claim a registered schedule the runner did not accept.
