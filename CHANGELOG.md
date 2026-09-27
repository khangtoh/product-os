# Changelog

## Unreleased

- Replaced abbreviated record IDs such as `OPP-001` with full-word IDs such as `Opportunity-01`, and record filenames with `<ID>_short_text_description.md`. Existing abbreviated IDs remain valid and are not renamed.

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
