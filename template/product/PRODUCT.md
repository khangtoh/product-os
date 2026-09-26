---
productmd: 1
productos: 1
$type: Product
$context: https://schema.org.ai
---

# Product name

Unknown — establish the one-sentence product promise during onboarding.

Updated: unknown — set when adopted or changed.

This is the product contract blueprint for a new ProductOS instance. It follows the open PRODUCT.md convention and adds ProductOS operating context. Replace unknowns only with supplied direction, supported evidence, a user-selected hypothesis, or an explicit deferral.

For a normal application repository, onboarding promotes this contract to the project root and replaces this local file with a navigation pointer, following [MODEL.md](MODEL.md). If this folder is itself the context repository root, keep the contract here.

## Register

unknown

Choose exactly one during onboarding:

- `brand`: design is the product, such as a campaign, publication, or portfolio.
- `product`: design serves a task, such as an app, dashboard, or tool.

When established, add the same value as `register:` in the frontmatter. Page-specific design modes may override this default without changing the product register.

## Users

Unknown. Describe who this is for in language they recognize, their situation, and the job they need to complete. Label hypotheses and link their source.

## Problem

Unknown. State what concretely breaks, costs time, creates risk, or remains impossible without the product.

### Current alternatives

Unknown. Record what users do today and why those alternatives are insufficient. Existing behavior is evidence; an assumed competitor set is not.

## Product Purpose

Unknown. State what the product does, why it exists, and how successful use should change the user's situation.

### Role of AI

Unknown or not applicable. Describe AI only when it materially changes the user experience. Name the behavior and its limits rather than using “AI-powered” as an unexplained benefit.

## Brand Personality

Unknown. Record durable personality commitments that should shape downstream writing and design.

### Tone

Unknown. State how the product speaks in ordinary, successful, and failure situations.

## Anti-references

No product-specific anti-references supplied. Record experiences, language, or patterns the product must not resemble. Make normative constraints concrete.

## Design Principles

No product-specific design principles supplied. Add a short numbered list of strategic rules derived from product purpose and user context. Keep visual tokens and component rules in DESIGN.md or the project's established design system.

## Accessibility & Inclusion

Unknown. Record the applicable accessibility floor, known user needs, and platform-specific requirements. Do not claim conformance that has not been checked.

## Platform

unknown

Record the actual usage platform from project context and owner direction. Do not infer a native experience from a framework or assume web when unresolved.

## Boundaries

Unknown. State what the product is not, meaningful non-goals, unacceptable tradeoffs, and durable constraints. Detailed requirement exclusions belong in [REQUIREMENTS.md](REQUIREMENTS.md).

Add an `## Offer` section only when the commercial offer is established. Add a `json product.md#pricing` machine island only when its values are approved and valid. Never manufacture pricing to complete the file.

## Stack

- [Agent instructions](AGENTS.md)
- [Current state](STATE.md)
- [Vision](VISION.md)
- [Requirements](REQUIREMENTS.md)
- [Strategy](STRATEGY.md)
- [Roadmap](ROADMAP.md)
- [Metrics](METRICS.md)
- [Learning](LEARNINGS.md)
- [Operations](operations/README.md)

Link DESIGN.md, AUTH.md, or another established contract when the project uses one. Link rather than duplicate its facts.

## Core Experience and Requirements

Link the essential workflows, initial functional and quality requirements, acceptance criteria, and open decisions in [REQUIREMENTS.md](REQUIREMENTS.md), or in the project's established specification.

## Desired Outcomes

No outcomes are supplied by this template. Define a real desired change and link its outcome record. Specify an evaluation method, baseline, target, and review window appropriate to the decision. Keep proposed targets distinguishable from accepted ones.

The canonical priority order is [ROADMAP.md](ROADMAP.md); measurement definitions live in [METRICS.md](METRICS.md). A shipped feature is not proof that an outcome was achieved.

## Operating Principles

These are starting conventions to adapt to the project:

- Follow explicit product direction within its scope.
- Use user feedback, behavior, research, and operating evidence to discover opportunities.
- Prefer the smallest useful intervention or informative experiment.
- Consider user value, confidence, effort, urgency, reliability, and cost together.
- Preserve uncertain claims as hypotheses and retain contrary evidence.
- Let results change product choices and operating practice.

## Human and Agent Control

Humans and agents can research, design, build, operate, and evaluate. Active work has an owner, criteria, and a handoff. Owner direction sets intent; user input provides evidence. Actual authority is recorded in [operations](operations/README.md) and comes from applicable project or session instructions.

This file does not grant external access, spending, or release permission. Existing authorization carries forward without repeated approval requests for work within scope.

## Evolution Loop

**Steer → observe → prioritize → design → build → verify → release → operate → measure → learn → update the product model.**

Every material change should connect a reason to an observed result and a subsequent decision. Update the app, priorities, evaluation, or operating practice when learning warrants it. An explicit decision to retain an approach is also valid.

Keep this contract brief and current. Preserve frontmatter, valid machine islands, and sections a tool does not understand. Link the direction or decision behind material changes; detailed specifications and results belong in their canonical records.
