# Initial product requirements

Updated: 2026-09-27.

The initial brief's workflows and requirements, following [MODEL.md](MODEL.md). Product identity stays in [../PRODUCT.md](../PRODUCT.md), outcome priority in [ROADMAP.md](ROADMAP.md), and scoped implementation detail in feature records. This repository has no separate specification document to link.

Source for everything below unless stated otherwise: the project owner, onboarding round 2 on 2026-09-27. Implementation status is observed from the source, which shows what exists — not that it works well or that anyone needs it.

## Core workflows

1. **Save an article link.** A researcher, in the middle of reading, saves the article they are looking at. Expected result: the article appears in their saved collection.
2. **Find a saved article by title.** Later, the researcher searches their saved collection by title. Expected result: the matching article is returned.
3. **Open the original.** The researcher opens a result. Expected result: it opens at the URL that was saved.

Failure and recovery path stated by the owner: when a search matches nothing, the product explains that and lets the researcher change the query.

## Functional requirements

Labels below (`FR-1`…) are local references within this summary document, not typed record IDs.

### FR-1 — Save an article link

- **Behavior:** a researcher saves an article by URL, with a title.
- **Acceptance criteria:** after saving, the article appears in the saved collection.
- **Status:** implemented. `src/store.js:15` appends `{url, title, savedAt}` to `localStorage` key `pocketgarden.saved`; `src/index.html:34` re-renders the list after submit.
- **Constraint:** the existing saving flow must be preserved (owner). Any change must keep the current path — one form, URL plus optional title, one submit — working as it does now.
- **Observed gaps, not owner requirements:** the title is optional and defaults to the raw URL (`src/store.js:18`); a submit with an empty URL throws from `save()` and is not caught by the submit handler; the same URL can be saved repeatedly. See [Open decisions](#open-decisions).

### FR-2 — Search the saved collection by title

- **Behavior:** the researcher searches saved articles by title.
- **Acceptance criteria:** a title search returns its matching article.
- **Status:** implemented. `src/search.js:3` matches a case-insensitive substring of the title; an empty query returns the whole collection.

### FR-3 — Open a result at its saved URL

- **Behavior:** opening a search result reaches the original article.
- **Acceptance criteria:** opening the result uses the URL saved with it.
- **Status:** implemented. `src/index.html:26` sets the link target to `item.url`.

### FR-4 — Explain an empty result and allow a new query

- **Behavior:** when no saved article matches the query, the product says so and the researcher can change the query without losing their place.
- **Acceptance criteria:** with a query that matches nothing, the interface displays a message stating that no saved article matches; the query input retains its value and remains editable so the query can be revised.
- **Status:** **not implemented.** `src/index.html:22` clears the results list and renders nothing, so an empty result is indistinguishable from an empty collection or a broken search. This is the one stated requirement the prototype does not meet.
- **Dependencies:** none beyond the existing files. No new dependency is permitted (root `AGENTS.md`).
- **Interacts with QR-1 and QR-2:** the message must be reachable and understandable by a keyboard user, and adding labels touches the same markup.

## Quality requirements and constraints

The durable product and repository constraints are canonical under Boundaries, Platform, and Accessibility & Inclusion in [../PRODUCT.md](../PRODUCT.md); they are not repeated here. Source for QR-1 to QR-3: the owner, onboarding round 3 on 2026-09-27.

### QR-1 — Keyboard operability

- **Requirement:** saving an article, searching, and opening a result must all work by keyboard.
- **Acceptance criteria:** using only the keyboard, a researcher can reach the save fields, save an article, enter a query, reach a result, and open it.
- **Status:** **unverified.** Reading `src/index.html` suggests the paths exist by default — a submit button inside a form, a text input, and real `<a href>` results — but nobody has operated it by keyboard, and the page has no styles, so focus visibility is whatever the browser supplies. Treat this as untested, not as met.

### QR-2 — Visible labels on collection controls

- **Requirement:** collection controls need visible labels, not placeholder text alone.
- **Acceptance criteria:** each collection control has a visible, persistent label that remains readable while the field contains text, and the label is programmatically associated with its control.
- **Status:** **not met.** `src/index.html:10`–`14` uses placeholders only for the URL, title, and query inputs.

### QR-3 — Each user's collection stays private

- **Requirement:** each user's collection stays private. Verify privacy before exposing any change.
- **Acceptance criteria:** no change is exposed to users until it has been checked not to transmit, share, or otherwise expose one user's saved collection. A change that adds hosting, sync, sharing, or any network call needs that verification explicitly recorded before exposure.
- **Status:** currently satisfied by construction — data stays in the browser's `localStorage`, the app makes no network requests, and analytics and third-party scripts are forbidden. This is an owner requirement in its own right, so it constrains future changes rather than merely describing today's storage choice.

### Other quality areas

- **Performance:** no numeric speed target. **Explicitly deferred** — see [Open decisions](#open-decisions).
- **Reliability and operations:** unknown. Production health and analytics have not been inspected; the owner confirmed this on 2026-09-27. Nothing is measured and no evaluation approach exists. Verification today is manual: open `src/index.html` in a browser (root `AGENTS.md`). Baselines are unknown, not zero.
- **Delivery:** no release date is committed.

## Exclusions and tradeoffs

Owner-stated non-goals, 2026-09-27, scoped "for now" rather than permanently:

- No team or shared libraries.
- No automated summaries.

The trade recorded by the owner: preserving the existing saving flow takes precedence over improving it.

## Open decisions

Unresolved dependencies are linked from [STATE.md](STATE.md).

**Explicit owner deferral, 2026-09-27 — numeric speed target.** The owner deferred setting a numeric performance target until current behavior can be inspected. Consequence: there is no performance acceptance criterion, so no change can be accepted or rejected on speed, and no performance regression can be detected. Owner: the project owner, who took the follow-up. Next discovery action: inspect the prototype's current behavior — search and render latency against a realistic collection size — then set a target from what is measured. Does not block FR-4 or any current work.

Items 1 to 4 were raised or observed by the agent, not by the owner. On 2026-09-27 the owner authorized the agent's recommendation on each. Every resolution below is therefore an agent judgment the owner adopted wholesale, not a considered choice — treat them as the weakest direction in this brief and overturn them cheaply.

1. **Untitled saves versus title-only retrieval.** Title is optional and defaults to the raw URL (`src/store.js:18`), while retrieval is by title, so an article saved mid-reading without a typed title is findable only by its URL text. This directly limits the retrieval-without-organizing principle in [VISION.md](VISION.md), and "preserve the existing saving flow" rules out the cheapest fix.

   **Recommendation: explicit deferral, do not decide now.** Deciding it before the first study would preempt exactly the question the study asks. Consequence of deferring: the product's core promise may not hold for its primary use, and that stays unresolved until observations exist. Owner: the product owner. Discovery action: during the first session, record for each retrieval attempt whether the saved item had a typed title, and whether attempts on untitled items fail more often. Blocks nothing currently prioritized.

2. **Register.** Resolved as `product` in [../PRODUCT.md](../PRODUCT.md) under the same authorization. See the provenance note there.

3. **Durability of the collection.** Clearing browser data destroys the collection; there is no export or backup.

   **Recommendation: hypothesis that this is acceptable at prototype stage, with a cheap check attached.** Adding export or sync now would be the largest change in the product and rests on no evidence. Consequence if the hypothesis is wrong: a researcher loses months of saved work, which would discredit the product with the very audience it targets. Owner: the product owner. Discovery action: ask each participant in the first session whether they have ever lost a saved collection and what it cost them. Revisit immediately if any participant has.

4. **Duplicate saves.** Saving the same URL twice appends a second entry (`src/store.js:18`), so search returns both.

   **Recommendation: proposed behavior, unbuilt and unprioritized** — re-saving a known URL should update the existing entry rather than add a second, keeping the newest title and the original `savedAt`. This preserves the saving flow the owner protected (same form, same submit) and removes duplicate rows from results. It is a proposal only: no work is authorized, it is not on the roadmap, and it should be reconsidered if the first study shows duplicates are not a real nuisance. Owner: the product owner. Discovery action: note in the first session whether duplicate rows appear and whether they confuse anyone.
