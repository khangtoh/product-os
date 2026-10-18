# Customize and maintain an instance

Once copied, a ProductOS instance belongs to its project. The framework supplies starting conventions. Product facts, owners, priorities, decisions, and operating authority come from that project.

## Keep the entry points stable

Prefer PRODUCT.md for the shared product contract, AGENTS.md for agent instructions, and STATE.md for resumable current work. Keep one canonical roadmap, metric registry, and learning index.

You may rename the containing folder or place it in a dedicated repository. Repair root agent pointers and external references when doing so. Internal template links are relative so moving the whole instance preserves them.

If a small project combines documents, update links and agent instructions together. Preserve the questions the documents answer rather than retaining empty bureaucracy.

## Integrate existing tools

Tickets, designs, dashboards, code, and deployment systems can remain where they are. ProductOS links them into intent and learning. Decide where each fact is canonical so a ticket status and a Markdown status do not drift without detection.

For evidence, record the query/source version, observation window, population, and limits. For execution, link actual artifacts. For decisions, capture why the evidence changes the next action. Do not duplicate a large raw dataset or private user payload into the product folder.

## Adapt to the product

- Consumer apps may emphasize first-use success, recurring value, and feedback cohorts.
- B2B products may emphasize role-specific workflows, account-level outcomes, and support context.
- Internal tools may emphasize task completion, time saved, reliability, and stakeholder constraints.
- AI behavior may need representative evaluation sets, model/prompt/tool versions, and quality/cost tradeoffs.

These are possible concerns, not preselected metrics or strategy. Choose actual definitions and evidence for your product.

## Multiple products

Give each product its own PRODUCT, STATE, roadmap, outcomes, and operating context. Shared company intent can live above them with explicit links. Transfer learning only when its scope applies; do not pool unrelated baselines or silently share authority across products.

Avoid placing competing product contracts where agents cannot determine which one governs the task. Root agent instructions should identify the product from the work location or explicit task scope.

## Upgrade deliberately

The framework release is in [VERSION](../VERSION); a copied instance records its template version in README. Record changes in [CHANGELOG](../CHANGELOG.md) and any future migration guidance.

To upgrade an applied instance:

1. Compare the new template with the version originally adopted.
2. Review changes to conventions, field meanings, lifecycles, and agent instructions.
3. Merge useful changes into the applied files while preserving product facts and history.
4. Repair links and verify current-state consistency.
5. Update the recorded template version and note material local deviations.

Do not recopy the blank template over an applied instance. There is no automatic migration in this release. Template release version and per-record `schema_version` are separate: a documentation revision need not change record schema.

The planned [event journal and version-aware evolution](EVENT_LOGGING_REQUIREMENTS.md) will record the loaded framework/package version, instance layout, artifact schema and hashes, and target Git revision under a committed `.product-os/`. It specifies automatic handling of known compatible structural changes and proposed migrations for unresolved changes, preserving local content and historical events. This is a future requirement, not an updater available in the current release; continue using the deliberate upgrade procedure above until an implementation is released.

### Upgrading the product contract to 0.2.0

Follow [the 0.2 migration guide](MIGRATING_0.2.md). Preserve the applied contract and record history, establish one canonical location, map supported facts into the open-standard headings, and retain ProductOS operating sections. Do not copy the blank blueprint over a populated contract.

A normal application repository should use root PRODUCT.md and a local `product/PRODUCT.md` navigation pointer. A standalone context repository keeps its contract at its own root. Omit Offer, pricing data, `$id`, and public publication until separately established.

### Adding guided onboarding to a 0.1.0 instance

The 0.2 onboarding addition leaves typed-record metadata and lifecycle unchanged. Merge the model's canonical-home and completion guidance, then add ONBOARDING and REQUIREMENTS where absent. Link them from README and agent instructions, and add STATE's onboarding checkpoint without erasing current work. If requirements already live in a PRD or tracker, make the new entry point link to them. Preserve local adaptations and record IDs.

New-project onboarding defaults to a root PRODUCT.md. Applied 0.1.0 instances retain their current canonical contract. If the owner chooses to consolidate at the root, first check for an existing contract, move or merge the real content without overwriting another source, rewrite its relative links, replace the local entry with a navigation pointer, and update root instructions together. If the product folder is already the project root, no move is needed. Verify both entry points resolve to the same facts.

Do not label an older brief complete merely because its files exist. During a requested revisit, reuse known answers and check coverage against MODEL; otherwise leave ordinary work uninterrupted. Keep the recorded release version at 0.1.0 until adopting a released upgrade and note the onboarding addition as a local change.

### Adding the execution procedure to an earlier instance

EXECUTION.md is a new procedure document; it changes no record metadata, lifecycle, or canonical home. Copy it into the instance, then link it from the instance README, agent instructions, and STATE's next action. It applies the LOOP and MODEL rules the instance already has, so local adaptations to those stay authoritative — if a local LOOP has diverged, keep the local rules and adjust the procedure's references rather than reintroducing the canonical text.

Instances that added their own run checklist can keep it. Reconcile the two rather than stacking them: one procedure per instance, with the other retired or folded in. Update the installed skill separately, using the guidance below.

### Update the installed skill

The installer refuses an existing `.agents/skills/product-os/` or `.claude/skills/product-os/` destination, including an empty directory or symlink. To replace it deliberately, preserve local skill edits, move only that skill folder to a backup outside the skill-discovery directory, and rerun the installer from the desired framework checkout. Compare and reapply intentional local skill changes; start a new Codex or Claude Code session if needed. Pass the same `--agent` value used originally.

Skill assets are bundled blank templates. Updating them does not update project-owned PRODUCT, requirements, roadmap, state, or agent instructions. Merge improvements into applied context using the migration guidance above, never by recopying the blank asset folder. No automatic updater or project migration is included.

## Improve the framework

When repeated project friction suggests a reusable improvement, describe the problem and proposed convention here, without copying private product history. Keep fictional examples separate from the template. A proposed framework improvement does not automatically change every applied project.

Run the offline suite for any change to the installer, the checker, or the template:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

It needs no network, no agent, and no dependencies. It covers the installer and the release packaging, and it validates a completed instance against the rules MODEL states: a bare installation must fail the checker, a captured good instance must pass, and each named check must reject a specific corruption. Check repository links and an isolated template copy with `python3 scripts/check_links.py`.

For changes to the onboarding procedure itself, run the scripted live interview and read its output:

```sh
PRODUCT_OS_E2E_LIVE=1 python3 scripts/run_onboarding_e2e.py --seed new-web-app --keep
```

It costs tokens, takes minutes, and needs the `claude` CLI, so it stays opt-in and out of the default suite. When it disagrees with the checker, classify the finding before changing anything: a checker bug, an expectation bug, or a genuine gap in the guide. Never loosen a check to make a run pass, and record any relaxation in [the fixture README](../test_project/README.md). The captured good instance is never hand-edited; the only sanctioned change is a fresh capture recorded in its provenance file.

Scenarios the suite does not cover remain manual: contributor orientation, ambiguous target scope, and a read-only project. Exercise those by hand in temporary projects and inspect the resulting context and handoff; prose matching alone does not validate an interview.
