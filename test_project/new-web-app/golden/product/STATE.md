# Current state

Updated: 2026-09-27 — ProductOS adoption complete. **Initial brief complete.** Setup only; no product work was executed.

## Snapshot

- Product stage: **early prototype**, confirmed by the owner. Save by URL and title, case-insensitive title substring search, open at original URL; all data in browser `localStorage`.
- Product owner: recorded as `product-owner`. A role identifier — the owner self-identified but supplied no name or handle, and none was invented. Replace it at any time.
- Other active work: **none**, confirmed by the owner.
- Current app and service health: **not inspected** (owner statement). No deployment, server, or tests are known to exist. Verify by opening `src/index.html`. See [operations](operations/README.md).
- Measurement: MET-001 only, by direct observation. Analytics are forbidden, so no instrumentation exists or will ([METRICS.md](METRICS.md)).
- Code shows the implemented behavior exists; it does not show users need it. The audience remains the owner's untested hypothesis.

## Active work

| Work | Owner | State | Record |
| --- | --- | --- | --- |
| Know whether researchers can find and open a saved article unaided | `product-owner` | `active` | [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) |
| Improve retrieval from what the study finds | unassigned | `proposed` | [OUT-002](outcomes/OUT-002-retrieval-succeeds-more-often.md) |

Active cycle: none. No cycle record was created — the owner asked to record the next action and stop after setup, so no execution run was opened.

## Onboarding checkpoint

Session 2026-09-27, six interview rounds. **Complete** per [MODEL.md](MODEL.md#onboarding-completion): all eight required areas are covered and saved, links resolve, the roadmap agrees with the first action, and a linked summary was presented for correction.

In the final round the owner closed the interview and authorized the agent's recommendation on every remaining open question, to be labeled as a hypothesis or an explicit deferral. Those positions are recorded as such and are weaker than individually reasoned direction — see below.

| Required area | Saved where |
| --- | --- |
| Identity and vision | [VISION.md](VISION.md), [../PRODUCT.md](../PRODUCT.md) |
| Users and problem | [../PRODUCT.md](../PRODUCT.md) — owner-stated hypothesis, untested |
| Core experience | [REQUIREMENTS.md](REQUIREMENTS.md#core-workflows) |
| Initial requirements | [REQUIREMENTS.md](REQUIREMENTS.md) — R1–R7 with acceptance criteria |
| Boundaries | [REQUIREMENTS.md](REQUIREMENTS.md#exclusions-and-tradeoffs), [../PRODUCT.md](../PRODUCT.md#platform) |
| Success | [METRICS.md](METRICS.md), [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) |
| Priorities | [ROADMAP.md](ROADMAP.md) |
| Starting point | this file, [operations](operations/README.md) |

**A complete brief is not a validated product.** Nothing here has been tested with a user.

### Deferred, with owners

| Deferred | Owner | Discovery action | Blocks |
| --- | --- | --- | --- |
| Participant count | `product-owner` | Scope the study | Interpreting a result, not running the first session |
| Decision threshold for "can retrieve" | `product-owner` | Scope the study — fix before observing | Interpreting a result |
| Session timing and how old a save must be | `product-owner` | Scope the study | Interpreting a result |
| Numeric speed target | `product-owner` | Inspect current save/search behavior first | A later performance decision only |
| Device reach and hosting — recommendation: stay single-browser and local | `product-owner` | Note each participant's device and cross-device expectations during the first sessions | Hosting, sync, or mobile work; nothing currently planned |
| Whether R5 (keyboard operation) is actually met — assumed likely, unverified | `product-owner`, delegable to an agent run | Complete all three workflows in a browser using only the keyboard. Cheap; needs no participants. | Any claim that R5 is verified |

Study deferrals are detailed in [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md); the rest in [REQUIREMENTS.md](REQUIREMENTS.md#explicit-deferrals).

### Selected hypotheses

On 2026-09-27 the owner authorized the agent's recommendation on the remaining open questions. Recorded in [REQUIREMENTS.md](REQUIREMENTS.md#selected-hypotheses):

- **H1** — researchers recall a topic or phrase rather than an exact title. If true, title search is the wrong handle and OUT-002 becomes a redesign.
- **H2** — silent data loss is the failure that matters most, ranked by irreversibility; then unsearchable saves, link rot, duplicates.

Both are working positions taken on an agent recommendation under a blanket authorization, not findings. H1's discovery action is built into [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md). H2 carries a standing caveat: data loss is possible today, needs no study to confirm, and nothing on the roadmap addresses it.

### Unmet requirements, not prioritized

**R4** (explain zero search matches) and **R6** (visible labels on collection controls) are owner-stated and unmet by the current build. The owner placed discovery first, so neither is on the roadmap. They are not lost — see [ROADMAP.md](ROADMAP.md#not-on-the-roadmap).

## Next action

**The product owner arranges the first observation session**: watch researchers try to retrieve an article from their collection and record whether they can find and open it without help. Scope participant count, decision threshold, and timing as part of arranging it.

This is owner-executed work. An agent session can help scope the protocol or work on R4/R6 if the owner asks, via `/product-os run` in Claude Code or `$product-os run` in Codex.

## Dependencies

- **A participant may have no genuinely old save.** `localStorage` is per-browser and the app is a local file, so scoping must establish how an aged collection exists to retrieve from. This may force a waiting period, and it interacts with the timing deferral.
- **Privacy during research (R7).** A session looks at someone's real collection. Do not copy, retain, or transmit participants' saved articles.
- **No version control.** The project is not a git repository, so there is no history to recover from. Prefer small, reversible edits.

## Next review

Trigger: the first observation session taking place. **No schedule is registered** — ProductOS installs no runner and none is configured here ([operations](operations/README.md)). Continuation depends on someone invoking the next session.
