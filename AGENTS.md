# Maintaining ProductOS

This repository defines the reusable ProductOS method, guides, and bare template. It is not the applied memory of a customer product. Read [README.md](README.md), [the overview](docs/WHAT_IS_PRODUCTOS.md), and [the product contract guide](docs/PRODUCT_MD.md) before changing the conventions.

- Keep `template/product/` self-contained. Its relative links must resolve after that directory is copied into another repository.
- Keep template instructions generic: no project name, company mission, operating permissions, dated history, claimed integrations, live record IDs, or fabricated results.
- Use `unknown` for facts a new project must supply. Keep record templates blank; show completed examples only in `examples/`, explicitly labeled fictional.
- Separate framework maintenance instructions here from the target-project instructions in `template/product/AGENTS.md`. Do not activate or run the target template while maintaining this repository.
- Keep canonical lifecycle and metadata rules in `template/product/MODEL.md`; guides should explain or link to them rather than invent conflicting variants.
- Preserve the distinction between delivery and validated outcomes, owner direction and user evidence, and written scheduling intent and actual runtime execution.
- Do not add a mandatory service, framework, SDK, or agent runtime just to adopt the documentation model.
- When changing file paths, metadata, or states, update guides, templates, examples, version notes, and migration instructions together.
- Before publishing, check relative links across the repository and in an isolated copy of the template (`python3 scripts/check_links.py` and `--template`). Check for project-specific leakage and consistency of the example with the declared model.
- Release by bumping [VERSION](VERSION) with `node scripts/release-kit/release.mjs bump`; CI tags and packages it. See [releasing](docs/RELEASING.md). Change the shared release kit in specloop first, then copy it here unchanged.
- Do not change visibility, add a license, or make external product commitments without applicable owner direction. Existing task authorization still applies to routine repository work.

There is no application build or dependency installation step. Validate the documentation at the level affected by a change; do not create an implementation-shaped test suite for prose edits.

The checks under `scripts/` are the exception that proves the rule: they validate the observable result of a procedure, not its wording. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` for any change to the installer, the checker, or `template/product/`; it is stdlib-only, offline, and adds no dependency. Changing the onboarding procedure additionally warrants the scripted live run described in [framework maintenance guidance](docs/CUSTOMIZATION.md#improve-the-framework). A check that can only be expressed as "the prose says X" does not belong in that suite.
