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

### Adding guided onboarding to a 0.1.0 instance

The unreleased onboarding addition leaves typed-record metadata and lifecycle unchanged. Merge the model's canonical-home and completion guidance, then add ONBOARDING and REQUIREMENTS where absent. Link them from README and agent instructions, and add STATE's onboarding checkpoint without erasing current work. If requirements already live in a PRD or tracker, make the new entry point link to them. Preserve local adaptations and record IDs.

New-project onboarding defaults to a root PRODUCT.md. Applied 0.1.0 instances retain their current canonical contract. If the owner chooses to consolidate at the root, first check for an existing contract, move or merge the real content without overwriting another source, rewrite its relative links, replace the local entry with a navigation pointer, and update root instructions together. If the product folder is already the project root, no move is needed. Verify both entry points resolve to the same facts.

Do not label an older brief complete merely because its files exist. During a requested revisit, reuse known answers and check coverage against MODEL; otherwise leave ordinary work uninterrupted. Keep the recorded release version at 0.1.0 until adopting a released upgrade and note the onboarding addition as a local change.

### Update the installed skill

The installer refuses an existing `.agents/skills/product-os/` destination, including an empty directory or symlink. To replace it deliberately, preserve local skill edits, move only that skill folder to a backup outside the skill-discovery directory, and rerun the installer from the desired framework checkout. Compare and reapply intentional local skill changes; start a new Codex session if needed.

Skill assets are bundled blank templates. Updating them does not update project-owned PRODUCT, requirements, roadmap, state, or agent instructions. Merge improvements into applied context using the migration guidance above, never by recopying the blank asset folder. No automatic updater or project migration is included.

## Improve the framework

When repeated project friction suggests a reusable improvement, describe the problem and proposed convention here, without copying private product history. Keep fictional examples separate from the template. A proposed framework improvement does not automatically change every applied project.

For installer changes, run `python3 -m unittest discover -s scripts -p 'test_*.py' -v`. For onboarding changes, exercise the installed skill in temporary projects covering new and existing products, explicit deferrals, interrupted setup, contributor orientation, ambiguous scope, and read-only access. Inspect the resulting context and handoff; prose matching alone does not validate an interview. Check repository links and an isolated template copy before publishing.
