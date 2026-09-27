# Current strategy

Updated: 2026-09-27.

## Thesis

Researchers who save articles while reading lose them because staying findable currently costs organizing work they will not do mid-task. PocketGarden's bet is that search over a saved collection, with no filing required, is enough to make those articles retrievable.

Confirmed direction: retrieval must not depend on organizing ([VISION.md](VISION.md)); the product stays a web app; collections stay private.

Hypothesis, not confirmed: that the audience is researchers of this kind, that they experience this loss as a problem worth changing tools for, and that title search is sufficient retrieval. Nothing here has been observed with a user. There is no sustainability or business model direction, and none has been asked for.

## Bets and choices

| Choice | Evidence / rationale | Uncertainty | Revisit condition |
| --- | --- | --- | --- |
| Retrieval by search rather than by folders or tags | Owner direction, 2026-09-27; the organizing cost is the stated reason alternatives fail | High — no observation of whether search alone succeeds weeks later | First study of whether researchers can retrieve an old article |
| Search matches titles only | Existing implementation (`src/search.js`), retained by the owner's round 2 workflow description | High — a save made without typing a title is findable only by URL text, which is the same failure the product exists to fix | Same study; see [open decision 1](REQUIREMENTS.md#open-decisions) |
| Keep the collection in the user's own browser, no accounts or sync | Follows the privacy requirement (QR-3) and the no-dependency, no-analytics constraints | Medium — clearing browser data destroys the collection, and multi-device use is impossible | Evidence that loss of collection or single-device use blocks retrieval |
| Learn before improving retrieval | Owner direction, 2026-09-27: find out first, improve second | Low as direction; the cost is that known unmet requirements (FR-4, QR-1, QR-2) wait | Study findings, or owner reprioritization |
| Keep the collection durable enough as-is, with no export or backup | Agent recommendation adopted under the owner's 2026-09-27 authorization; adding export would be the largest change in the product and rests on no evidence | High — a researcher losing months of saved work would discredit the product with its target audience | Any participant reporting they have lost a saved collection |

## Constraints and discovery

Constraints: no dependencies in `src/`, no build step, no analytics or telemetry, no third-party scripts, no accounts, no deployment, no tests. Product maturity is prototype. Resource limits and available time are unknown and were not asked about. No product ownership is assigned, which is the binding constraint on starting anything.

The most consequential uncertainty is whether a researcher can retrieve an article they saved weeks ago at all. The small next step to resolve it is the Now item: a first study of real retrieval attempts. Every other uncertainty here is cheaper to resolve after that one.

Link material changes to decisions and evidence. Keep ordering in [ROADMAP.md](ROADMAP.md) and immediate next actions in [STATE.md](STATE.md).
