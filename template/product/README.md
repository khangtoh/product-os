# ProductOS instance

The shared product memory where humans and AI steer, build, operate, and evolve this product together.

Template version: 0.2.0. Adoption date: unknown. Project owner: unknown. Set those values when adopting this folder.

This is a bare instance. No project facts, live records, measurements, or operating authority are supplied by the template.

## Start here

- Read [PRODUCT.md](PRODUCT.md) for product intent and [STATE.md](STATE.md) for current work.
- Agents also read [AGENTS.md](AGENTS.md). Humans can use [WORKING_TOGETHER.md](WORKING_TOGETHER.md).
- Use [guided onboarding](ONBOARDING.md) to establish an initial product brief, requirements, and roadmap, or follow the same guide manually. Keep uncertainty explicit.
- Connect the project root's existing agent instructions to this folder; a nested context file may not be automatically loaded when working elsewhere.

## Map

| Location | Purpose |
| --- | --- |
| [ONBOARDING.md](ONBOARDING.md) | Guided setup or orientation for a new contributor |
| [PRODUCT.md](PRODUCT.md) | Contract blueprint; after onboarding, entry point to the canonical contract |
| [VISION.md](VISION.md) | Durable ambition and boundaries |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Core workflows, initial requirements, acceptance criteria, and open decisions |
| [STRATEGY.md](STRATEGY.md) | Current thesis, bets, and uncertainties |
| [ROADMAP.md](ROADMAP.md) | Outcome priority order |
| [STATE.md](STATE.md) | Current truth and resumable handoff |
| [MODEL.md](MODEL.md) | Record types, metadata, relationships, and lifecycle |
| [LOOP.md](LOOP.md) | Development, operation, and learning protocol |
| [METRICS.md](METRICS.md) | Measurement definitions |
| [LEARNINGS.md](LEARNINGS.md) | Evidence-backed reusable knowledge |
| [operations/](operations/README.md) | Actual capabilities, authority, runbooks, and incidents |
| [templates/](templates/README.md) | Blank templates for typed records |
| `steering/`, `outcomes/`, `opportunities/` | Direction, desired changes, and problems worth solving |
| `features/`, `experiments/` | Behavior specifications and hypothesis tests |
| `evidence/`, `decisions/`, `cycles/` | Observations, choices, and execution history |

Create record directories with their first real record. Use only the types needed for the work. Keep one canonical home for each fact and link existing tools where appropriate.

New-project onboarding places the canonical PRODUCT.md at the target project root and replaces the local contract with a relative navigation pointer. Existing established contracts stay in place. Before adoption, this folder remains self-contained; see [MODEL.md](MODEL.md) for the boundary and completion rules.

This folder supplies memory and protocol. Record actual execution, observation, and scheduling capabilities in operations; documentation alone does not run a product loop.
