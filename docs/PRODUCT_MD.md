# PRODUCT.md: the shared product contract

PRODUCT.md is ProductOS's portable contract for product intent: what the product is, who it serves, why it matters, how it speaks, and how its evolution is governed.

ProductOS 0.2 makes this contract a superset of the [open PRODUCT.md standard](https://product.md/). Tools that understand the standard can consume the canonical core. Humans and ProductOS agents can also follow its linked outcomes, operating principles, and learning loop.

## Responsibilities

| File or artifact | Responsibility |
| --- | --- |
| PRODUCT.md | Product identity, users, problem, purpose, voice, boundaries, outcomes, operating principles, and navigation |
| AGENTS.md | How an agent should work in the repository or scoped folder |
| DESIGN.md or established brand system | Visual tokens, components, interaction rules, and detailed visual guidance |
| REQUIREMENTS.md | Initial workflows, functional and quality requirements, acceptance criteria, and open decisions |
| Feature specification or PRD | Detailed behavior and acceptance criteria for a scoped change |
| STATE.md | Current truth, active work, dependencies, and next action |
| ROADMAP.md | Canonical priority order of outcomes |

Keep one authoritative home for each fact. PRODUCT.md links to detailed records rather than copying a backlog, metric history, visual system, or operational procedure.

## Compatibility layers

A ProductOS contract uses the open convention as its core and appends ProductOS operating context.

| Layer | ProductOS requirement |
| --- | --- |
| CommonMark | Exactly one H1 containing the product name, followed by a concise promise |
| Metadata | `productmd: 1`, `productos: 1`, `$type: Product`, and `$context: https://schema.org.ai` |
| Canonical core | Register, Users, Problem, Product Purpose, Brand Personality, Anti-references, Design Principles, Accessibility & Inclusion, optional Offer, Boundaries, and Stack |
| ProductOS extension | Platform, Core Experience and Requirements, Desired Outcomes, Operating Principles, Human and Agent Control, and Evolution Loop |

The bare blueprint is intentionally unresolved. It becomes conformant during onboarding, when the product name, promise, Register, Users, and Product Purpose are established. Unknowns remain explicit elsewhere.

### Register compatibility

The open convention treats `## Register` as the canonical product-wide default. Use exactly `brand` or `product`. When frontmatter includes `register:`, it must match the heading.

Current design tools may choose a mode per page or surface. That task-level choice overrides the default for the surface without rewriting the product register.

### Offer and linked data

Offer is optional. Omit it until the commercial offer is real. A pricing machine island must be valid JSON and contain approved values.

Add `$id` only when a canonical URL exists for the same contract. ProductOS does not require publishing an internal product contract. A project may use the build-time repository binding without serving `/product.md`.

## Contract placement

For a normal new project, onboarding creates the canonical PRODUCT.md at the project root, beside root agent instructions. Supporting context remains under `product/`; its local PRODUCT.md becomes a navigation pointer to the root contract, STATE, and ROADMAP.

The bare template keeps the complete blueprint inside `template/product/` so the copy boundary and installed skill assets remain self-contained. During promotion, rewrite its relative links to `product/...`.

If the product folder is itself a standalone context repository's root, keep the contract there. If a project already has an established product contract, preserve its canonical location and merge only supported additions. Never maintain two populated definitions of the same facts.

## Required questions

A useful first contract answers:

1. What is the product's promise and purpose?
2. Who is it for, in what context, and what problem or job brings them here?
3. What alternatives do they use now?
4. What voice, constraints, and accessibility requirements must hold?
5. What observable outcome would represent successful use?
6. How do humans, users, and agents influence product decisions?
7. Where are requirements, current priorities, measurements, and operating context maintained?

Use [guided onboarding](../template/product/ONBOARDING.md) to answer these through a conversation. Supported facts, user-selected hypotheses, and explicit deferrals remain distinguishable.

## Preservation rules

Tools that update PRODUCT.md must preserve frontmatter, valid machine islands, and sections they do not understand. Do not rewrite historical hypotheses to match later results. Link steering, evidence, or decisions behind material changes.

Changing PRODUCT.md cannot grant tool access, release permission, spending authority, or a new approval policy.

## First version versus mature version

A first version may contain a clearly labeled audience hypothesis, explicit measurement gaps, and one learning outcome. A mature version should point to evidence-backed users, a demonstrated promise, active outcome definitions, and actual operating constraints.

Both should remain brief enough to read before consequential product work.
