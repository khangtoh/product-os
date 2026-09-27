# Initial product requirements

Updated: 2026-09-27 — established during ProductOS adoption, interview rounds 2 and 3.

Product identity lives in [../PRODUCT.md](../PRODUCT.md), outcome priority in [ROADMAP.md](ROADMAP.md), record rules in [MODEL.md](MODEL.md). No separate specification document exists for this project; this is the canonical requirements summary.

## Core workflows

Owner-stated on 2026-09-27. Three workflows, all performed by a single researcher on their own collection:

1. **Save an article link.** The researcher is reading, encounters an article worth keeping, and saves it to their collection. The existing saving flow is to be preserved (see the constraint below).
2. **Search the saved collection by title.** Later, the researcher looks for something they saved, using words from its title.
3. **Open the original article.** From a search result, the researcher opens the article at the URL that was saved.

The detailed situation at each moment — what the researcher is doing when they save, and what they actually remember when they return — was **not established**. See [Open decisions](#open-decisions); this is the most consequential gap in the brief.

## Functional requirements

Source for all four: owner direction, 2026-09-27. Related outcome: none defined yet ([ROADMAP.md](ROADMAP.md) is not yet populated).

| ID | Requirement | Observable acceptance criteria | Status in current build |
| --- | --- | --- | --- |
| R1 | A saved article appears in the collection. | After saving an article, it is present in the collection and visible in the unfiltered list. | Implemented — `src/store.js` appends to `localStorage`; `src/search.js` returns all items for an empty query. |
| R2 | A title search returns its matching article. | Given a saved article, searching text contained in its title returns that article among the results. | Implemented — case-insensitive substring match on title (`src/search.js`). |
| R3 | Opening a result uses the article's saved URL. | Activating a result navigates to exactly the URL stored with that article. | Implemented — result anchors use `item.url` (`src/index.html:26`). |
| R4 | When a search has no matches, the app explains that and lets the researcher change the query. | With a query matching no saved article, the interface states that nothing matched, and the query remains editable so a new search can be run without losing the collection or reloading. | **Not implemented.** `render()` clears the list and appends nothing, so zero matches is indistinguishable from an empty collection (`src/index.html:22-32`). |

R4 is the only functional gap between owner-stated requirements and the current build.

## Quality requirements and constraints

Owner-stated on 2026-09-27, round 3:

| ID | Requirement | Observable acceptance criteria | Status in current build |
| --- | --- | --- | --- |
| R5 | Saving, searching, and opening a result must work by keyboard. | Each of the three core workflows can be completed using only the keyboard: reach every control in a sensible tab order, submit a save, enter a query, and activate a result. | **Likely met, unverified.** The markup uses a native `form` with a submit button, native inputs, and anchor elements, all keyboard-operable by default (`src/index.html`). Nothing has been checked in a browser, and there is no test suite, so this is an inference from the markup, not a verified result. |
| R6 | Collection controls need visible labels. | Each control for saving and searching has a persistently visible text label, not a placeholder that disappears once the field has content. | **Not implemented.** All three inputs carry only `placeholder` attributes and no `label` elements (`src/index.html:10-14`). |
| R7 | Each user's collection stays private. Verify privacy before exposing changes. | No saved article, URL, title, or collection content leaves the user's own browser or becomes reachable by another user. Any change that could expose collection data is checked against this before release. | **Met by construction today.** Data lives only in `localStorage`; there is no server, no network request, and no third-party script (`src/store.js`, project [AGENTS.md](../AGENTS.md)). This holds only while the app stays local — hosting or sync would make it a live risk. |

R7 is a release gate, not just a property: the owner's direction is to verify it *before* exposing changes.

- **Preserve the existing saving flow.** Owner direction, 2026-09-27: the save interaction is not to be redesigned. This was stated after the tension below was raised, so it is a decision, not an oversight.
- **Platform: web app.** Owner direction, 2026-09-27 — "keep it a web app". No native application. See [../PRODUCT.md](../PRODUCT.md#platform).
- **No release date is committed.** Owner direction, 2026-09-27. Priorities in [ROADMAP.md](ROADMAP.md) carry no delivery dates.
- **No analytics, telemetry, or third-party scripts;** `src/` dependency-free, no build step, bundler, or framework; plain ES modules and vanilla DOM; two-space indentation. Established in the project's [AGENTS.md](../AGENTS.md) and treated as a product boundary in [VISION.md](VISION.md).
- **Verification method:** no test suite exists. The project instruction is to verify by opening `src/index.html` in a browser. Any acceptance check above is therefore a manual browser check unless testing is introduced by a later decision.
- Reliability requirements beyond R7: **not established.** See the unruled failure cases in [Open decisions](#open-decisions).
- Accessibility beyond R5 and R6 (contrast, screen-reader semantics, focus visibility): **not established.** Not discussed.

## Exclusions and tradeoffs

Owner-stated non-goals, 2026-09-27, both qualified as "for now" — these are current exclusions, not permanent ones:

- **Team or shared libraries.** The collection is personal and single-user.
- **Automated summaries.** No generated descriptions or digests of saved articles.

Tradeoff accepted by preserving the saving flow: the researcher types the title by hand at save time, and a blank title falls back to the raw URL (`src/store.js:18`). This is in tension with the [VISION.md](VISION.md) principle that saving should cost nothing and retrieval should work from partial memory — a save with no typed title is effectively unsearchable by title. The owner chose to keep the flow; the consequence is recorded here rather than treated as resolved.

## Open decisions

On 2026-09-27 the owner authorized the agent's recommendation for every remaining open question, to be labeled as a hypothesis or an explicit deferral. Recorded below on that basis.

**These are working positions, not findings.** A hypothesis selected on an agent's recommendation and a blanket authorization is weaker evidence than one the owner reasoned about individually. Treat each as the thing to check first, not as settled.

### Selected hypotheses

| # | Hypothesis | Basis | Consequence if wrong | Discovery action |
| --- | --- | --- | --- | --- |
| H1 | Researchers recall a **topic or a phrase from inside the article** more reliably than its exact title. | Agent recommendation, owner-authorized 2026-09-27. Common pattern for read-later collections. No observation of PocketGarden users exists. | Title search (R2) is aimed at the wrong handle, and the entire core retrieval workflow needs rethinking rather than refining. This is the most consequential open question in the brief. | [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md): record what each participant recalls before they start searching. Owner: `product-owner`. |
| H2 | Of the four failure cases, **silent data loss ranks first**, then unsearchable saves, then link rot, then duplicates. | Agent recommendation, owner-authorized 2026-09-27. Ranked by reversibility, not frequency: the others degrade retrieval, data loss destroys the collection outright and cannot be undone. | Durability work is over- or under-prioritized relative to retrieval. | Ask participants during [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md) whether they have lost saves before, and note blank-title saves in their collections. Owner: `product-owner`. |

The four failure cases, unchanged:

- *Silent data loss* — the whole collection is one `localStorage` key, wiped by clearing browser data, with no export or backup, and absent on every other browser and device.
- *Unsearchable saves* — a blank title stores the URL as the title (`src/store.js:18`), leaving the entry effectively unfindable.
- *Link rot* — only the URL is stored, so a moved or dead page makes the save worthless.
- *Duplicates* — saving the same URL twice appends a second entry.

H2 carries a standing caveat: **data loss is the one failure that is irreversible**, and it needs no study to establish that it is possible — the code makes it plain. If a real collection is lost before the study concludes, that outranks discovery.

### Explicit deferrals

Recorded per [MODEL.md](MODEL.md#onboarding-completion).

| Question | Recommended position | Consequence of deferring | Owner | Next discovery action | Blocks? |
| --- | --- | --- | --- | --- | --- |
| What numeric speed target should saving and search meet? | None set. | No performance requirement exists, so no change can be judged too slow and no regression threshold can be set. | `product-owner` (owner's own statement, 2026-09-27) | Inspect actual current save and search behavior, then set a target from observed behavior rather than a guess. | A later performance decision only. |
| Device reach and hosting — are mobile browsers, multiple devices, or a hosted deployment in scope? | **Stay single-browser and local for now.** Hosting or sync would turn R7 (privacy) from free-by-construction into real engineering, and pull against the no-dependencies, no-build constraints. Not worth committing before the study. | Saving while reading plausibly happens on a phone, and `localStorage` crosses neither browsers nor devices — so a real user need may be going unmet and unnoticed. | `product-owner` | During [OUT-001](outcomes/OUT-001-know-whether-researchers-can-retrieve-an-old-article.md), note which device each participant saves from and whether they expect their collection elsewhere. | Any hosting, sync, or mobile work. Blocks nothing currently planned. |
| Is R5 (keyboard operation of save, search, open) actually met? | Assume likely met, treat as unverified. | A stated requirement is recorded as satisfied on an inference from markup rather than a check, so a regression would go unnoticed. | `product-owner`, delegable to an agent run | Open `src/index.html` and complete all three workflows using only the keyboard. Cheap, and needs no participants. | Any claim that R5 is verified. |

Accessibility beyond R5 and R6, and reliability beyond R7, remain undiscussed rather than deferred — no position has been formed and none was requested.

Unresolved dependencies are linked from [STATE.md](STATE.md).
