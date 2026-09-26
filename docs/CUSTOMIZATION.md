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

## Improve the framework

When repeated project friction suggests a reusable improvement, describe the problem and proposed convention here, without copying private product history. Keep fictional examples separate from the template. A proposed framework improvement does not automatically change every applied project.
