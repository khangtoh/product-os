# Strategy

Updated: 2026-09-27 — established during ProductOS adoption.

## Current approach

**Find out before building.** The owner's direction on 2026-09-27 was to establish whether researchers can retrieve an old article before improving retrieval. Discovery comes first; retrieval work is proposed and waits on what the study finds.

The product keeps its current shape while that happens: a dependency-free local web app, personal collection, existing saving flow preserved.

## Rationale

The product's retrieval design has a single handle — substring match on a user-typed title ([REQUIREMENTS.md](REQUIREMENTS.md#functional-requirements), R2). Whether that matches how researchers actually recall a save is unknown and untested. Building more retrieval capability first would risk refining the wrong mechanism, so the cheaper move is to look.

## Assumptions

All of these are unvalidated. They are what the current approach rests on.

- **The audience is researchers who lose track of what they saved.** The owner's explicit hypothesis, stated as untested ([../PRODUCT.md](../PRODUCT.md), [VISION.md](VISION.md)).
- **Retrieval is the binding problem**, rather than saving, durability, or the app simply not being used. The study should be designed to notice if this is wrong.
- **H1: recall is topical or phrase-based rather than title-exact.** Agent recommendation, owner-authorized 2026-09-27 ([REQUIREMENTS.md](REQUIREMENTS.md#selected-hypotheses)). If this holds, title search is the wrong handle and OUT-002 becomes a redesign rather than a refinement — which is a larger bet than the current approach implies.
- **H2: silent data loss is the failure that matters most**, ranked by irreversibility. Authorized on the same basis. It is not on the roadmap, which is a deliberate risk the owner is carrying.
- **Researchers can be observed.** Participant access is unverified ([operations](operations/README.md)).
- **A meaningful "old save" can be produced for a study.** Uncertain: `localStorage` is per-browser and the app is a local file, so participants may have no existing collection at all. This may force a waiting period into the study design.
- **Retrieval without organizing is achievable** under the current constraints — no dependencies, no build step, no third-party scripts.

## What would change the approach

- The study finds retrieval is **not** where researchers fail — then OUT-002 is the wrong Next, and priorities should follow the observed failure instead.
- The researcher audience does not hold up — then [VISION.md](VISION.md) needs revising with the evidence and a recorded decision, not a quiet rewrite.
- Participants cannot be recruited or observed — then discovery-by-study is blocked, and the owner should choose between self-observation, a different evidence source, or pulling the unmet requirements (R4, R6) forward instead of sitting idle.
- Durability becomes urgent — one `localStorage` key holds everything, with no export and no version control on the project. A real data loss would outrank discovery.

## Bets not being made

- No team or shared libraries, and no automated summaries — owner non-goals "for now".
- No hosting or sync decision. Device reach remains an open question ([REQUIREMENTS.md](REQUIREMENTS.md#open-decisions)).
- No redesign of the saving flow, by owner direction, despite its tension with the vision.

Priority order is canonical in [ROADMAP.md](ROADMAP.md).
