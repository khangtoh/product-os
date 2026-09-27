# Outcome roadmap

Updated: 2026-09-27 — established during ProductOS adoption, interview round 4.

This is the canonical priority order. Priorities carry **no dates**: the owner committed no release date. A priority slot does not itself authorize spending or release.

## Now

| Rank | Outcome / record | State | Next step |
| --- | --- | --- | --- |
| 1 | [OUT-001 — We know whether researchers can retrieve an article they saved weeks ago](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) | `active` | The product owner arranges the first observation session, scoping participant count, decision threshold, and timing with it. |

Rationale — owner direction, 2026-09-27: "First find out whether researchers can retrieve an old article. We have no observations." Discovery leads because the product's whole retrieval design rests on title search and nobody has checked whether title recall matches how researchers remember what they saved.

Owner: the product owner, who will arrange the first session. Participant access is no longer a blocker. Remaining dependency: a participant may have no genuinely old save to retrieve, since `localStorage` is per-browser — scoping must solve this ([STATE.md](STATE.md)).

## Next

| Outcome / record | State | Depends on |
| --- | --- | --- |
| [OUT-002 — Researchers retrieve what they saved more often](outcomes/OUT-002-retrieval-succeeds-more-often.md) | `proposed` | [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) |

Owner direction, 2026-09-27: "improve retrieval using what we learn; treat that as proposed." Deliberately left unspecified — what to improve depends on what the study finds, so no features are attached.

## Later

**Undecided, by owner direction.** The owner will revisit Later after the first study rather than fill it now: "I don't want an invented backlog."

This horizon is empty on purpose. It is not an oversight, and it should not be populated with speculative items.

## Not on the roadmap

Two owner-stated requirements are unmet by the current build and are **not prioritized**, because the owner placed discovery first:

- **R4** — a search with no matches must say so and let the query be changed. Currently indistinguishable from an empty collection.
- **R6** — collection controls need visible labels. Currently placeholder-only.

Both are specified in [REQUIREMENTS.md](REQUIREMENTS.md#functional-requirements) and remain available if the owner pulls them forward. They are recorded here so they are not silently lost.

## Selection rules

Address active incidents and breached constraints; apply current owner direction; finish due verification/evaluation before opening competing work. Rank eligible opportunities by impact, evidence strength, urgency, effort, reversibility, and value of resolving uncertainty.

Keep blocked work visible with its dependency and select the next eligible action. Explain material priority changes with evidence or steering; do not invent precise scores from unknown inputs.

## Changes

| Date | Change | Evidence / steering / decision |
| --- | --- | --- |
| 2026-09-27 | Roadmap established. Now: OUT-001 discovery. Next: OUT-002, proposed. Later: deliberately undecided. | Owner direction during ProductOS onboarding, round 4. |
| 2026-09-27 | Agent proposed R4 + R6 as Now; owner overrode in favour of discovery first. R4 and R6 left unprioritized. | Owner direction, round 4. |
| 2026-09-27 | OUT-001 moved `proposed` → `active`. Owner named and committed to arranging the first session; observation method defined as find-and-open without help. | Owner direction, round 5. |
