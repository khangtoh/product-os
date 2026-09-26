# Get started with ProductOS

ProductOS keeps product intent, requirements, priorities, and learning available to people and agents. Onboarding establishes a complete initial brief through a conversation, then offers the first useful loop.

If the ProductOS skill is installed, invoke `$product-os init`. Otherwise, after copying this folder into a target project, paste:

```text
Read product/ONBOARDING.md and guide me through ProductOS onboarding.
Inspect this project, ask me for the missing product vision and requirements,
help me make unresolved decisions, and save the initial brief and roadmap.
```

Adjust the path if the folder lives elsewhere. Both entry points use this guide. The canonical coverage, completion, and location rules live in [MODEL.md](MODEL.md).

## 1. Inspect and establish the target

Follow the target project's existing instructions. Read its product contract, README, supplied briefs, and any [current state](STATE.md), including the onboarding checkpoint. Inspect relevant code and existing specifications enough to distinguish implemented behavior from intended behavior. Read [MODEL.md](MODEL.md) before writing context or records.

The installed skill's asset folder is a blank source, never the target product. Establish the actual project root, product folder, and canonical contract. If several products or contracts could govern the work, ask the user to resolve the scope or conflict before writing. Do not assume that all apps in a monorepo share one product vision.

Choose the appropriate path from the user's request and the project context:

| Situation | Approach |
| --- | --- |
| New idea or project | Interview for the full initial brief; use explicit hypotheses where evidence does not exist |
| Existing product adopting ProductOS | Reuse reliable briefs, requirements, priorities, and evidence; interview for missing or conflicting information |
| Interrupted setup | Resume the checkpoint and saved answers, asking the next unresolved questions |
| New contributor to an initialized project | Explain the product, priorities, current work, and contribution path; ask their focus only when needed |

An orientation does not reset the product brief, change ownership, or create a fresh roadmap. A bare request to explain ProductOS does not authorize setup. Existing optional unknowns do not force another interview during ordinary work.

## 2. Interview for the complete initial brief

Start with a concise summary of what the project establishes and what remains uncertain. Ask two or three related questions per round, then wait for the answers. Use a structured question tool when available; otherwise use ordinary chat. Reuse the original request and previous answers. There is no fixed number of rounds and no need to ask questions already settled by reliable sources.

Use [MODEL.md's required areas](MODEL.md#onboarding-completion) as a coverage checklist, not a questionnaire to dump on the user. A useful progression is:

- **Purpose and people:** What lasting change should this product make possible? Who needs it, in what situation, and what do they use today? Establish whether the product-wide Register is `brand` or `product`; if the repository does not make that clear, explain the distinction and ask.
- **Experience and requirements:** What must users be able to do? Walk through the essential workflow. What behavior must the first version include, and how would we check it works? Which failures matter?
- **Boundaries and success:** What must remain intact, and what is out of scope? What platform and constraints apply? What result would tell us the product is helping, and what evidence do we already have?
- **Direction and starting work:** Which outcomes belong Now, Next, and Later, and why? What is already underway? Who owns direction and the first action, and what needs resolving before it can start?

Adapt the order to the conversation. Ask about business model, technical choices, accessibility, resource limits, or delivery dates when they materially shape the product; do not demand an answer to every possible field. Product vision belongs in the brief; detailed visual styling stays in the project's design guidance.

### Help the user decide

When the user is unsure, offer a small set of plausible options with tradeoffs and a grounded recommendation. Ask for their selection or an explicit decision to defer. Their chosen hypothesis is valid product direction but is not validated user evidence.

A deferral retains the unanswered question, its consequence, an owner if known, and a concrete discovery action. Record whether it blocks implementation or only a later decision. Unanswered questions remain unanswered; do not infer agreement, invent evidence, or keep asking the same question indefinitely when the user wants to pause.

Treat repository evidence according to what it can establish. Code can show that a feature exists, but not that users need it or that it improves an outcome. Confirm material inferences before promoting them to owner direction. Preserve sources and conflicting evidence.

### Save progress between rounds

After each answered round, save supported content in its canonical document and update the onboarding checkpoint in STATE with coverage links, outstanding questions, and the next interview topic. Do not copy the whole transcript into the brief. Clearly label proposals, hypotheses, and explicit deferrals. Preserve original answers when later direction changes them through the normal decision history.

For a read-only project, show the proposed edits and unsaved checkpoint in the response. Do not claim saved context or completed setup. When answers stop arriving, leave an incomplete checkpoint and a clear resume prompt.

## 3. Establish the product context

For a writable new instance, use the provided blank documents. If an instance already exists, merge only needed additions and preserve project facts, IDs, history, local adaptations, and existing priorities. Missing supporting documents can be created as needed; never copy blank records over applied ones.

Follow [MODEL.md's canonical homes](MODEL.md#canonical-homes):

- **No established contract:** create `PRODUCT.md` at the target project root from the local contract blueprint. Rewrite its relative links to the actual product-folder paths. Replace the blank local PRODUCT.md with a short relative link to the canonical root contract and links to STATE and ROADMAP. Other product-folder links continue to use this local entry point.
- **Existing established contract:** keep its current location and useful structure. Add a local navigation pointer if necessary, with supported additions in the canonical document. Preserve a populated local PRODUCT.md as canonical unless the user directs consolidation. A freshly copied, untouched blueprint is not an established contract.
- **Standalone product-context repository:** if the product folder is itself the target root, retain its PRODUCT.md in place; do not create a self-link or move it to the parent directory.

Do not overwrite an unrelated root file. If two populated contracts disagree, resolve authority with the user. Do not invent a second canonical definition or claim compatibility with another tool solely because a link exists. Keep DESIGN.md and other existing design artifacts in place.

When creating a new contract, retain the blueprint's open PRODUCT.md metadata and canonical headings. Replace the H1 with the product name and the opening line with its promise. Resolve `## Register` to `brand` or `product` and add the identical `register:` value to frontmatter. Keep the standalone `## Platform` heading and put the established platform beneath it. Keep boundaries separate. Omit Offer, pricing islands, and `$id` unless their values and any public binding are established.

When updating an existing contract, preserve frontmatter, valid machine islands, and sections not owned by ProductOS. Map supported facts into canonical headings without erasing useful local sections. Current page-level design modes may differ from the product Register.

This lets standard-aware tools consume the contract while ProductOS follows its extension sections and linked records. Preserve useful existing contract structure when updating an established file.

| Destination | Saved context |
| --- | --- |
| Canonical PRODUCT | Product-name H1 and promise; Register; users, problem and alternatives; purpose; voice and design commitments; accessibility; platform; boundaries; ProductOS operating sections; sources and navigation |
| [VISION.md](VISION.md) | Lasting product ambition and durable principles |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Core workflows, initial functional and quality requirements, acceptance criteria, exclusions, and open decisions |
| [STRATEGY.md](STRATEGY.md) | Initial approach, rationale, assumptions, and what would change the approach |
| [ROADMAP.md](ROADMAP.md) | Now / Next / Later outcome priorities, rationale, dependencies, and links to requirements and outcome records |
| [STATE.md](STATE.md) | Current work, onboarding checkpoint, first action, ownership, and readiness dependencies |
| [operations/](operations/README.md) | Relevant verified systems, capabilities, existing operating scope, and unknowns |
| [README.md](README.md) | Actual adoption date and owner when established; retain an existing adoption date |

Keep one canonical home for each fact. Link established specifications and external tools instead of duplicating their maintained details. Create scoped feature records only when they add useful implementation detail. Outcome records use the existing templates and lifecycle from MODEL; metrics belong in [METRICS.md](METRICS.md) when defined. Unknown baselines remain unknown.

Reuse current outcomes and work. For a new roadmap, select a meaningful Now outcome and discuss Next and Later; leave a horizon empty when the user has no established priority. Record an explicit deferral where needed instead of manufacturing a backlog. Priorities are not deadlines, and setup does not make an outcome active or achieved.

## 4. Connect future agent sessions

Merge a pointer into the target project's existing root agent instructions, avoiding duplicate entries and preserving unrelated content. For a new project with the default layout:

```markdown
## Product context

For product work, read PRODUCT.md, product/AGENTS.md, and product/STATE.md
before making changes. Follow linked vision, requirements, roadmap, and
work records as needed. Update the affected context after material
product decisions or results.
```

Adapt the contract and folder paths for an existing instance or standalone context repository. Use the project's equivalent agent configuration when applicable, and report exactly what was changed. A nested AGENTS.md alone may not load during work elsewhere.

## 5. Check completion and offer the first loop

Apply the completion rules in [MODEL.md](MODEL.md#onboarding-completion). Verify saved coverage, references and agent pointers, explicit hypotheses and deferrals, and agreement between roadmap, requirements, records, and STATE. A complete brief may still need discovery before implementation; report the dependency instead of claiming build readiness. Do not expand tool permissions or invent an owner to clear the check.

Show a short linked summary of the product vision, core requirements, Now / Next / Later priorities, unresolved decisions, and the first proposed action. Invite corrections. Record completion only once the required coverage has been saved and presented; do not require another approval round for answers already given.

Offer the next action using a working prompt such as:

```text
Read the product context and current state. Carry out the next eligible
bounded action using the ProductOS loop, verify the result, and save a handoff.
```

Also offer scheduling setup as a separate next step when the user wants recurring work. A proposed cadence or next-review field is not a registered schedule. Do not present run or scheduling skill commands that have not been implemented.

An onboarding-only request ends with this offer. Do not start implementation, release anything, or register a schedule. If a broader request already authorizes subsequent work, hand back to that task's workflow using [LOOP.md](LOOP.md) and existing operating scope. On a later onboarding visit, continue from the saved checkpoint rather than repeating settled questions.
