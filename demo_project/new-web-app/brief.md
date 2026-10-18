# Seed: new web app with no product contract

**Fictional example.** PocketGarden, Mira, and every answer below are invented for testing. They are not live product evidence.

## The starting state

`seed/` is a small reading-list web app. Its README describes saving and search, its `src/` implements both, and its `AGENTS.md` carries unrelated engineering conventions. It has no product contract, no research records, and no usage measurements.

This is the default-layout path from [MODEL.md](../../template/product/MODEL.md#canonical-homes): onboarding should create the canonical `PRODUCT.md` at the project root, turn `product/PRODUCT.md` into a navigation pointer, and merge a product-context pointer into the existing `AGENTS.md` without losing what is already there.

The seed is deliberately not empty. The walkthrough premises a project with code to inspect, so the procedure's "inspect first" step has something real to find, and the pre-existing `AGENTS.md` gives the preservation assertion something to preserve.

## The scripted answers

Taken verbatim from [the fictional walkthrough](../../examples/onboarding.md), where they appear as Mira's replies. `turns.json` holds the machine-readable copy that the runner feeds one per round, regardless of exactly what the agent asked.

1. **Users and problem.** Researchers who save articles and later lose track of them; they use bookmarks or notes today; the goal is retrieval without mandatory organizing. The audience is an explicit hypothesis, not tested.
2. **Requirements and boundaries.** Save a link, search saved titles, open the original. Observable checks for each. Handle no-match by explaining and letting the query change. Preserve the existing saving flow. No team libraries or automated summaries.
3. **Platform, quality, constraints.** Keep it a web app. Keyboard operation and visible labels. Collection privacy is a requirement to verify, not a verified property. Production health and analytics uninspected. No release date. A numeric speed target is explicitly deferred, with Mira owning the follow-up.
4. **Priorities.** Now: find out whether researchers can retrieve an old article, with no observations yet. Next: improve retrieval, proposed. Later: deliberately undecided. No invented backlog.
5. **Evaluation and first action.** Observe researchers retrieving an article and record whether they succeed unaided. Participant count, decision threshold, and timing deferred until the study is scoped. Mira owns direction and the first session. Early prototype, no other active work. Record the next action and stop after setup.

A sixth harness turn asks the agent to finish saving, wire the agent context, and show the summary, labelling anything still open as a hypothesis or an explicit deferral. It has no counterpart in the walkthrough.

## What a correct run should produce

The specifics live in `expect.json`, derived from [MODEL.md's required areas](../../template/product/MODEL.md#onboarding-completion) and [ONBOARDING.md step 3](../../template/product/ONBOARDING.md). In summary:

- A canonical root `PRODUCT.md` with a standalone `## Platform` section naming the web platform, and a resolved identity table.
- `product/PRODUCT.md` reduced to a short pointer at the root contract.
- Vision, requirements, strategy, roadmap, state, and operating context saved in their canonical homes.
- A roadmap with a populated `## Now`, a proposed `## Next`, and an explicitly deferred `## Later`.
- Explicit deferrals that keep their consequence, owner, and discovery action — the speed target and the study protocol.
- A retrieval outcome that stays proposed, with no fabricated baseline and nothing marked achieved.
- The pre-existing README, sources, and `AGENTS.md` conventions intact.
- The installed skill's blank assets byte-identical to the template.
