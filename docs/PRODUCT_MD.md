# PRODUCT.md: the shared product contract

PRODUCT.md is ProductOS's proposed portable convention for product intent. It describes what a product should become, for whom, why it matters, and how humans and agents will make decisions about its evolution.

Keep it understandable without execution history. It is the starting point for product decisions; linked records supply detail.

## Responsibilities

| File or artifact | Responsibility |
| --- | --- |
| PRODUCT.md | Purpose, users, core job, desired outcomes, constraints, decision principles, and navigation |
| AGENTS.md | How an agent should work in the repository or scoped folder |
| Design guidance, such as DESIGN.md if a project uses it | Visual and interaction principles and design conventions |
| Feature specification or PRD | Detailed behavior and acceptance criteria for a particular change |
| STATE.md | Current truth, active work, dependencies, and next action |
| ROADMAP.md | Canonical priority order of outcomes |

These files complement one another. Avoid copying a detailed backlog or metric history into PRODUCT.md.

## Required questions

1. What is the product's promise and purpose?
2. Who is it for, in what context, and what job does it help them do?
3. What would an observable improvement look like?
4. What constraints, non-goals, and tradeoffs shape choices?
5. How do direction and evidence become product decisions?
6. Where are the current priorities, work, measurements, and operating context?

The [bare PRODUCT.md](../template/product/PRODUCT.md) provides a starting structure. Unknown answers can remain explicit; do not invent facts to fill sections.

## Loading it into agent context

PRODUCT.md is a documentation convention in this repository. Naming a file does not guarantee that an agent tool loads it automatically. Add an explicit instruction to the project's existing root AGENTS.md or equivalent agent configuration to read `product/PRODUCT.md`, `product/AGENTS.md`, and `product/STATE.md` before product work.

A nested AGENTS.md may only apply when an agent works in that directory. The root pointer makes the context relevant when it edits app code elsewhere. Preserve existing root instructions and tool-specific configuration. See [quickstart](QUICKSTART.md).

## Updating the contract

Change PRODUCT.md when identity, intended outcomes, boundaries, or decision principles change. Link the steering, evidence, or decision that prompted the change. Keep historical rationale in records and version control.

Owner direction can change purpose. Evidence can refine strategy and product choices within established intent. Changing PRODUCT.md cannot grant tool access, release permission, spending authority, or a new approval policy.

## First version versus mature version

A first version may contain a user/job hypothesis and one learning outcome. A mature version should point to an evidence-backed audience, product promise, active outcome framework, and actual operating constraints. Both should stay brief enough to read before important work.
