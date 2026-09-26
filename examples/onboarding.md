# A guided first session

**Fictional example.** All people, product details, conversations, records, and results below are invented for teaching. They are not live product evidence or proof that ProductOS improves outcomes.

## Start with what exists

Suppose Mira owns PocketGarden, a small reading-list web app. Its README describes saving articles and its code implements saving and search. It has no established product contract, research records, or usage measurements. Mira installed the ProductOS skill into the app project.

**Mira:** $product-os init

**Assistant, after inspecting the project:** The README describes a reading-list app, and the code includes saving and search. I haven't found evidence about who uses it or whether it meets their needs. Who is it for, what do they use today, and what lasting change do you want to make possible?

**Mira:** Researchers who save articles while reading and later lose track of them. They use browser bookmarks or notes. I want them to retrieve what they found without having to organize everything. Treat that audience as my initial hypothesis; we haven't tested it.

The assistant saves the audience hypothesis and promise in the new root PRODUCT.md, records the ambition in VISION, and updates STATE's coverage checkpoint. The local product/PRODUCT.md becomes a navigation pointer. No visual design changes are made.

## Establish requirements and boundaries

**Assistant:** What must the initial experience let researchers do? How would we check those behaviors work, and what should we preserve or exclude?

**Mira:** Save an article link, search my saved collection by title, and open the original article. A saved article must appear in the collection; a title search must return its matching article; opening the result must use its saved URL. If there are no matches, explain that and let me change the query. Preserve the existing saving flow. No team libraries or automated summaries for now.

**Assistant:** Which platform and quality requirements matter, and what constraints should shape the first work?

**Mira:** Keep it a web app. Saving, search, and opening a result must work by keyboard, and collection controls need visible labels. My requirement is to keep each user's collection private; verify that before exposing changes. We haven't inspected production health or analytics. No release date is committed. Defer a numeric speed target until we can inspect current behavior; I'll own that follow-up.

The assistant records requirements and observable checks in REQUIREMENTS. Privacy is recorded as a requirement, not a verified property of the implementation. The speed target remains unknown with an explicit owner and discovery action.

## Decide what matters next

**Assistant:** What result should we evaluate first, and do you have evidence already? Which outcomes should come next or later?

**Mira:** First find out whether researchers can retrieve an old article. We have no observations. Next, improve retrieval using what we learn; treat that as proposed. Leave Later undecided until the first study, and I'll revisit it then. I don't want an invented backlog.

**Assistant:** How should we evaluate the first outcome, and who owns the initial action? What other work is already underway?

**Mira:** Observe researchers trying to retrieve an article from their collection and record whether they can find and open it without help. Defer the participant count, decision threshold, and timing until the study is scoped. I'm the product owner and will arrange the first session. This is an early prototype; there's no other active work. Record that next action and stop after setup.

The assistant records the evaluation approach and the explicitly deferred protocol choices. The outcome remains proposed; no experiment is running. STRATEGY explains the owner-selected approach of observing existing retrieval before deciding what to change.

## Saved context and handoff

| Place | Illustrative content |
| --- | --- |
| Root PRODUCT | Promise, intended users as a hypothesis, current alternatives, web platform, boundaries, source of direction, and links |
| VISION | Retrieval without mandatory manual organization as the lasting ambition |
| REQUIREMENTS | Save, title search, and opening behavior; no-match handling; keyboard and privacy requirements; observable checks and exclusions |
| STRATEGY | Observe retrieval first; revise the approach based on evidence |
| Outcome | Proposed retrieval outcome with an evaluation approach and explicitly unresolved study criteria |
| ROADMAP | Now: understand retrieval success; Next: proposed retrieval improvement; Later: explicitly deferred until study findings |
| STATE | Coverage links, first action owned by Mira, unresolved study scope, and readiness for discovery rather than implementation |
| Operations | Inspected code references; production health, observation access, release scope, and scheduling remain unverified |

These are illustrative summaries, not complete typed records. A real outcome uses MODEL's metadata, unique ID, actual dates, and relative links. The assistant preserves existing root agent instructions while adding the product-context pointer.

**Assistant:** I've saved the initial brief and linked it from the project instructions. The vision, requirements, and roadmap are captured; the audience is still a hypothesis, and study criteria remain explicitly deferred. The next action is for Mira to arrange and scope the observation session. Setup is complete, but implementation and product success are not established. Review the linked summary and correct anything I misunderstood. When ready, ask: “Read the product context and help prepare the retrieval observation session.” Scheduling can be configured separately; none has been registered.

Preparing and conducting the study is a subsequent loop with a cycle and an evaluation protocol established before collecting results. Completing onboarding does not activate or achieve the proposed outcome.

## Other paths

- **Interrupted setup:** if Mira stopped after requirements, STATE would show saved coverage and the next questions about success, priorities, and starting work. A fresh session resumes there; unanswered fields do not count as deferrals.
- **New contributor:** a collaborator joining this initialized project gets an explanation of the product, retrieval priority, and next action. Their arrival does not reset the brief or change ownership.
- **Established contract:** an existing root or local PRODUCT.md stays canonical. The agent preserves its facts and useful structure, and links the new supporting context without creating a competing contract.
- **Conflicting scope:** if two apps have different product briefs and the target is unclear, the agent asks which app the request concerns before writing.
- **Read-only project:** the assistant can propose the brief and a checkpoint, but reports that saving and agent-context wiring remain incomplete.

Continue with [a fictional learning loop](first-learning-loop.md) to see how a later experiment connects observations to a decision.
