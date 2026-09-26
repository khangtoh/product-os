# What is ProductOS?

ProductOS is a shared product operating model for humans and AI. It gives a product durable intent, a current work state, and an evidence trail so it can evolve coherently across contributors, tools, and sessions.

It is expressed in portable Markdown files. A team can use it manually, with a coding assistant, or with an autonomous runner. The same product memory serves all three.

## The problem it addresses

Product context often lives across conversations, ticket queues, dashboards, and individual memory. An agent may implement a request correctly while missing why it matters. A human may see a release without knowing whether it improved the product. Repeated sessions can repeat research or revive an idea without knowing why it failed.

ProductOS connects the reason for work, the work itself, its observed result, and the decision that follows. It gives the next contributor a short path back into the current state.

## Five connected layers

| Layer | Question | Main records |
| --- | --- | --- |
| Intent | What should this product become, for whom, and why? | PRODUCT, VISION, STRATEGY |
| Priority | What outcome matters next? | ROADMAP, outcomes, opportunities |
| Execution | What are we doing, and how will we verify it? | STATE, features, experiments, cycles |
| Operation and evidence | What is happening in use, and what do we actually know? | operations, METRICS, evidence |
| Learning | What decision changes because of the result? | decisions, LEARNINGS, updated intent and priority |

The canonical [record model](../template/product/MODEL.md) defines the relationships and states.

## One product, shared agency

Humans and agents can both research, design, build, operate, evaluate, and review. Each active work item has an owner and a next action. Either actor can resume the other's work from shared records.

Owner direction sets or changes intent within its scope. Users influence the product through expressed needs and observed behavior. User feedback is evidence to evaluate, not authority to change operating permissions. Existing authorization lets routine work continue without repeated approval requests.

The method does not require a human checkpoint at every step or assume that every decision should be automated. It makes direction, evidence, ownership, and authority explicit enough to support the chosen operating model.

## The loop is the unit of progress

**Steer → observe → prioritize → design → build → verify → release → operate → measure → learn → update the system.**

A completed change should produce an observed result and a decision. That decision can expand an approach, revise it, stop it, recover from a failure, or retain it with a reason. Learning becomes useful when it changes future behavior or explicitly confirms the current approach.

A release can be complete while its outcome is still unknown. An inconclusive experiment is a legitimate result. An operational incident can teach the system as much as a new feature.

## Start small

Start with a product contract, one outcome, one action, and a handoff. Create supporting records when the decision needs them. The template offers a full vocabulary so the model can grow; it does not require every record type for every change.

Unknown facts remain unknown. The template supplies structure, not a product strategy, customer evidence, targets, or permissions.

## Origin and scope

This method was extracted from an applied ProductOS layer for GetIntro, following the owner's stated 0ptr.ai vision of products that evolve through AI execution, observation, and human/user steering. The reusable template does not inherit that app's context or company mission.

It can support consumer products, B2B software, internal tools, or AI native apps. Use AI-specific evaluation fields where AI behavior affects the product. Adapt the rest to the actual project.

## What makes an instance useful

- A newcomer can understand the product and resume work without reconstructing chats.
- Priorities connect to intended outcomes and evidence.
- Active work has an owner, criteria, and a next observation.
- Results preserve uncertainty and contrary evidence.
- Decisions update the product, roadmap, or operating practice.

These are qualities to assess in use, not results already proven by installing the files.
