# Changelog

## Unreleased

- Specified [event logging and version-aware evolution requirements](docs/EVENT_LOGGING_REQUIREMENTS.md): committed, machine-readable `.product-os/` events for commands, interview progress, artifact provenance, version compatibility, and recoverable migrations. This records requirements only; no logger, command interception, or automatic migration is implemented by this change.
- Added [EXECUTION.md](template/product/EXECUTION.md), a packaged procedure for carrying one bounded action from current product context through verification to a resumable handoff. It applies the existing loop protocol and record model rather than defining a second lifecycle, and adds no record type, state, or metadata field. See the [execution decisions and implementation record](docs/EXECUTION_IMPLEMENTATION.md).
- Added a `run` entry to the skill, alongside `init`, `resume`, and `orient`, with equivalent natural-language requests routing to the same procedure. `resume` continues an unfinished interview; `run` carries out product work once a brief exists.
- Added an end-to-end onboarding test: fixtures under [test_project/](test_project/README.md), a deterministic instance checker (`scripts/check_instance.py`), its regression tests, and an opt-in scripted live runner (`scripts/run_onboarding_e2e.py`). The checker parses record types, id forms, and lifecycle states out of the canonical template MODEL.md rather than restating them, so that file stays the single source of truth.
- Required EXECUTION.md and LOOP.md in the source checkout at install time, so an incomplete checkout fails at install rather than at use.
- Run output from the live runner stays outside the checkout by a guard in the runner, mirroring the installer's refusal of an in-checkout target, rather than by a `.gitignore` rule that would hide in-repo output instead of preventing it.

## 0.3.0 — 2026-09-27

- Replaced abbreviated record IDs such as `OPP-001` with full-word IDs such as `Opportunity-01`, and record filenames with `<ID>_short_text_description.md`. Existing abbreviated IDs remain valid and are not renamed.
- Added an inline argument hint, `[init|resume|orient] [target or question]`, which Claude Code shows while `/product-os` is typed. `resume` and `orient` now name the existing interrupted-setup and contributor-orientation paths.
- Added a VERSION-driven release: changing VERSION on `main` runs a shared release kit (identical to specloop's) that verifies, packages Codex and Claude Code skill archives plus the blank template, and creates a tagged GitHub Release. See [releasing](docs/RELEASING.md).
- Added `scripts/check_links.py` for repository and isolated-template link checks.
- Added `--agent codex|claude|both` to the installer. Claude Code installs go to `.claude/skills/product-os/` with the hint at the top level of the frontmatter; Codex remains the default and keeps the hint under `metadata:`. See the [onboarding record](docs/ONBOARDING_IMPLEMENTATION.md#entry-hints-and-claude-code).

## 0.2.0 — 2026-09-26

- Made the ProductOS contract a superset of the open PRODUCT.md convention with canonical headings, preservation rules, and ProductOS extension sections.
- Standardized root-contract promotion while retaining a self-contained blueprint and local navigation pointer.
- Added 0.1-to-0.2 migration guidance and validation for adopted contracts.
- Added a discoverable Codex onboarding skill and an optional standard-library Python installer that bundles the canonical template without initializing project context. See the [onboarding decisions and implementation record](docs/ONBOARDING_IMPLEMENTATION.md).
- Added a complete initial-brief interview with decision support, explicit deferrals, saved checkpoints, contributor orientation, and a first-loop offer. The portable prompt uses the same procedure.
- Defaulted new-project onboarding to a shared root PRODUCT.md with a local navigation pointer, preserving established contracts and the self-contained bare template.
- Added REQUIREMENTS.md, Now / Next / Later onboarding guidance, and canonical completion rules distinguishing a complete brief from readiness to implement.
- Added a fictional onboarding walkthrough and [upgrade guidance](docs/CUSTOMIZATION.md#adding-guided-onboarding-to-a-010-instance). Record schema and lifecycle are unchanged.

## 0.1.0 — 2026-09-26

- Introduced ProductOS as a reusable method for shared human and agent product work.
- Defined PRODUCT.md as the shared product contract and documented its relationship to AGENTS.md and current-state records.
- Added adoption, operating, customization, and automation guides.
- Added a bare project template with no applied product history or inherited authority, plus ten record templates.
- Added an explicitly fictional example of an experiment and learning loop.

This is the initial standalone release. There is no automated migration or runtime bundled with it.
