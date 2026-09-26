# Migrate a ProductOS 0.1 instance to 0.2

ProductOS 0.2 combines the guided-onboarding addition with an open-standard-compatible PRODUCT.md contract. Applied instances own their history; migrate them deliberately rather than copying the blank template over them.

## 1. Establish the canonical contract

Identify the populated PRODUCT.md that currently owns product identity. Check for another root contract before moving anything.

For a normal application repository:

1. Move or merge the populated contract to root `PRODUCT.md`.
2. Rewrite links to supporting records under `product/`.
3. Replace `product/PRODUCT.md` with a short navigation pointer to the root contract, STATE, and ROADMAP.
4. Update root and nested agent instructions together.

If the product folder is itself the repository root, leave its contract in place. If another established contract already exists, preserve it and reconcile meanings before consolidation.

## 2. Merge onboarding support

Add ONBOARDING.md and REQUIREMENTS.md when absent. Merge the 0.2 MODEL, STATE checkpoint, AGENTS, README, and roadmap guidance without erasing applied records, active work, local lifecycle adaptations, or priorities.

An installed ProductOS skill is separate from project context. Reinstalling the skill updates its blank assets; it does not migrate the project's records.

## 3. Reshape the contract

Preserve supported product facts and their status while mapping them into the canonical core:

| Earlier ProductOS content | ProductOS 0.2 destination |
| --- | --- |
| Product name and promise | H1 and opening sentence |
| Target users and context | Users |
| Core job, need, and alternatives | Problem |
| Purpose and role of AI | Product Purpose |
| Voice and durable personality | Brand Personality and Tone |
| Constraints and non-goals | Boundaries |
| Existing design commitments | Design Principles, Accessibility & Inclusion, or a linked design system |
| Decision principles | Operating Principles |
| Shared control | Human and Agent Control |
| Evolution | Evolution Loop |

Add the ProductOS metadata block. Establish Register as `brand` or `product` and mirror it in frontmatter. Retain Platform as its own heading.

Omit Offer, pricing islands, and `$id` until their values and public binding are established. Preserve other useful sections and machine islands verbatim.

## 4. Connect and verify

Update all affected links and root agent instructions. Confirm the roadmap and STATE still identify the same actual work.

Validate:

- Exactly one product-name H1.
- Register is resolved and matches frontmatter.
- Users and Product Purpose contain supported content or labeled hypotheses.
- Relative links and anchors resolve from both root PRODUCT.md and the local pointer.
- No canonical fact is maintained in two populated files.
- Existing record IDs and lifecycle states are unchanged.
- The application build remains unaffected.

Run `npx productmd check` when the checker is available. A bare unresolved blueprint is not expected to pass; a completed adopted contract should.
