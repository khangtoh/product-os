---
name: product-os
description: Onboard a new or existing project to ProductOS through a product interview, save its vision, requirements, and roadmap, resume incomplete setup, or orient a new contributor. Use for ProductOS setup and orientation, not ordinary implementation requests.
---

# ProductOS onboarding

Help the user establish a complete initial product brief and a resumable starting point for product work. This skill currently provides onboarding and orientation; it does not implement dedicated run, review, or scheduling commands.

## Choose the entry

- `init`, a request to set up ProductOS, or a request to complete its onboarding: follow the onboarding guide below.
- A person joining an initialized project: use the guide's orientation path, preserving established direction.
- Bare invocation with no task: inspect the target's existing contract and current state, briefly describe setup readiness, and offer `init`, resuming the interview, or orientation. Do not start writing or interviewing until the intent is clear.
- Advice about the method: answer from the bundled guide and model without starting setup.
- An execution or scheduling request: explain that this skill supplies setup, and point to the target's loop and operations context for the requested next workflow. Do not claim another skill subcommand exists.

## Load and apply the guide

Resolve resources relative to this SKILL.md's directory, not the project's working directory. The installed package contains `assets/product/ONBOARDING.md` and `assets/product/MODEL.md`. Read those for the interview procedure and canonical completion rules. Other files in `assets/product/` are blank project templates; load only those needed for the work. The source checkout is packaged by the installer; if assets are missing, report an incomplete installation rather than improvising templates.

Keep the target project separate from the skill directory and its bundled assets. Follow the target's existing root instructions. Locate any existing ProductOS instance, product contract, and onboarding checkpoint before creating files. If several products could be the target, establish which one the user means before writing.

For an explicitly requested initialization with no instance, copy the bundled product folder into the target as `product/` without overwriting an existing path. If the path already exists, inspect and merge only missing ProductOS documents needed for onboarding; never replace project records with bundled blanks. Resolve conflicting meanings of the directory with the user. Do not copy the entire framework repository, the skill's own files, or fictional examples into product context.

Then follow the guide in the target project. Respect established local model adaptations; an installation update is not authorization to migrate product records. For older instances missing onboarding guidance, use the bundled procedure with their existing model and preserve their lifecycle conventions.

When creating or promoting a PRODUCT.md, follow the bundled MODEL and ONBOARDING compatibility rules. Preserve open-standard metadata, canonical headings, valid machine islands, and unknown sections; resolve Register during onboarding rather than inventing it.

Interview through the available structured question tool or ordinary conversation. Wait for answers to questions that determine product direction. Save supported answers and progress in project-owned files, never in the installed skill assets. Do not infer user approval from silence.

Finish with links to saved context, unresolved decisions, and the first proposed loop. An onboarding-only request ends there. Do not implement the product, register schedules, or suggest that setup proves a user outcome was achieved.
