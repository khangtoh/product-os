# End-to-end onboarding test: plan and handoff

This is the working plan for the onboarding end-to-end test, kept with the framework's other
maintenance records so the work can be resumed by someone who was not present for it. The
design sections below are the plan as approved; the status and handoff sections above them
record what actually happened, including where the plan turned out to be wrong.

## Status at handoff

**2026-10-18 update:** fixtures now live under `demo_project/`. The [Demo checks workflow](../.github/workflows/demo-checks.yml) automates offline regression, captured-demo and link validation, with a manual credentialed live interview. The captured seed/golden contents and provenance remain unchanged. The dated snapshot below describes the original onboarding work.

Snapshot: **2026-09-27**. All of it is on the branch `feat/onboarding-e2e-and-execution`, unmerged.

| Piece | State |
| --- | --- |
| Fixture seed, brief, scripted turns, expectation spec | Done — [demo_project/](../demo_project/README.md), seed `new-web-app` |
| Instance checker | Done — `scripts/check_instance.py`, 23 checks, rules parsed from MODEL.md |
| Offline regression tests | Done — 36 tests, green on Python 3.14.7 and 3.9.6, ~1s, no network |
| Mutation suite | Done — 28 rows covering 19 checks; nothing uncovered |
| Live scripted runner | Done — `scripts/run_onboarding_e2e.py`, opt-in via `PRODUCT_OS_E2E_LIVE=1` |
| Captured golden and provenance | Done — from a clean 9-turn run, ~$7.43 |
| Claude Code skill discovery | Fixed — the installer wrote only `.agents/skills/`, which Claude Code does not read |
| Second seed (`existing-contract`) | Not started, deliberately |
| Read-only, ambiguous-scope, contributor-orientation, interrupted-setup scenarios | Manual, by design |

The checker discriminates the three states it needs to: a blank instance reports 45 errors, a
truncated interview reports 2, a complete one reports 0.

## Outstanding decisions

These need a person, and none of them are safe for an agent to settle alone.

1. **The `--agent` default is `codex`.** That preserves prior behavior and keeps the original
   installer tests passing, but it means the install command in the README still leaves a Claude
   Code adopter with a skill that cannot be discovered unless they pass `--agent claude`. That is
   the same failure the flag was added to fix, now one flag away. Changing the default to `both`
   makes the tool work everywhere at the cost of creating a `.claude/` directory a Codex-only user
   did not ask for. One line in `scripts/install_skill.py` plus three documentation files.
2. **Release version and timing** for the `## Unreleased` section, which now holds the execution
   procedure, the installer fix, and this suite.
3. **Whether the 36-file captured golden belongs in version control.** It is 208K of generated
   fixture and the positive control the 28 mutations run against; without it that suite skips. It
   is also the thing most likely to produce noisy diffs, because a recapture rewrites all of it.

## How to resume

Read [the fixture README](../demo_project/README.md) first: it records every finding from the live
runs with its classification, the two relaxations and the risk each accepts, and the rule that the
golden is never hand-edited.

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v      # offline, no agent, no network
python3 scripts/check_links.py                                 # repository link check
python3 scripts/check_links.py --template                      # isolated template copy
PRODUCT_OS_E2E_LIVE=1 python3 scripts/run_onboarding_e2e.py --seed new-web-app --keep
```

Editing `template/product/` will fail `test_provenance_matches_the_current_template` on purpose,
because the captured golden is only meaningful against the template it came from. The fix is
`python3 scripts/run_onboarding_e2e.py --seed new-web-app --capture-golden`, which costs a live
run. That failure is deliberate; do not silence it.

When a live run disagrees with the checker, classify before changing anything: a checker bug, a
bug in `expect.json`, or a real gap in the procedure. Record the classification in the fixture
README. Never loosen a check to make a run pass.

## What the first complete run actually showed

Seven defects, **all in the checker, the expectation spec, or the test harness, and none in the
onboarding procedure**. The procedure produced a conforming instance on its first complete
attempt. The two that matter most as cautionary tales:

- A run truncated two thirds of the way through passed the entire spec, because nothing required a
  fact that only the later scripted answers supply. Three traceability entries now catch it.
- The checkpoint check rejected an instance that was *better* than the template, because it counted
  bullets while the instance used richer tables. Shape, not substance.

Both were found only by running the thing. Neither would have been caught by review.

---

## Note on the plan below

The design sections were written before this branch was rebased onto v0.3.0. Two things changed
underneath them. Main added `scripts/check_links.py`, which is now the repository link-check entry
point and delegates to `check_instance.check_links` so the two cannot disagree; the plan's
`--links-only` invocations still work but are no longer the documented path. Main also replaced
abbreviated record ids such as `OUT-001` with full-word ids such as `Outcome-01`, keeping the old
form valid for existing instances, so the checker accepts both and warns on the legacy form.
Main had independently added `--agent codex|claude|both` to the installer, so this branch's own
installer change was dropped in favour of theirs, which additionally hoists the argument hint for
Claude Code.

## The approved plan

## Context

ProductOS's onboarding is an agent-driven interview that writes product context files. Its correctness is entirely about *what ends up on disk*: did the canonical contract land at the project root, did the required brief areas reach their canonical homes, did the agent avoid writing into the installed skill's blank assets, did explicit deferrals survive as deferrals.

None of that is tested. `docs/ONBOARDING_IMPLEMENTATION.md:73` says the interview scenarios were "agent-driven trials in temporary fixtures, not an automated regression suite committed to the repository," and `docs/EXECUTION_IMPLEMENTATION.md:60` says no behavioral scenario was exercised. The repo's own records name this as the missing piece; the six existing tests cover the installer only.

**Goal:** a committed fixture describing a mock product, a deterministic checker that validates a completed instance against the rules `MODEL.md` already states, negative tests proving the checker catches failures, and an opt-in live runner that drives a real scripted interview. Then run it, and **iterate on ProductOS itself until the test project's `product/` folder contains every required output.**

### On proportionality

`AGENTS.md` warns: "do not create an implementation-shaped test suite for prose edits." This does not violate that, and the CHANGELOG entry should say so explicitly:

> This suite does not test prose. It tests whether an agent following the procedure produces an instance satisfying the rules `MODEL.md` already states normatively. It is stdlib-only, adds no dependency, build step, or CI, and everything requiring an agent is skipped by default.

Budget with teeth: **~400 lines of checker, ~250 of tests, ~150 of runner.** Past that, cut checks rather than add machinery. If a check can only be expressed as "the prose says X," it does not belong.

## Fixed decisions

1. **`demo_project/` is a committed seed fixture, never the run location.** `install_skill.py:20` refuses any target inside the checkout, and that guard stays — it has its own passing test. The runner copies the seed to a temp dir outside the repo, installs there, runs, asserts.
2. **Offline and deterministic by default.** `python3 -m unittest discover -s scripts -p 'test_*.py'` stays fast, network-free, and does not need the `claude` CLI. The live run is opt-in via `PRODUCT_OS_E2E_LIVE=1`.
3. **Scripted input is an ordered list of user turns**, fed one per round regardless of what was asked, ending with a catch-all. Assertions are on saved files, never on dialogue wording.

## Verified facts this plan depends on

Checked directly, because several of my initial assumptions were wrong:

- **`--max-turns` does not exist** in `claude` 2.1.274. `--max-budget-usd <amount>` does (print-mode only) and is the better cap. `--session-id <uuid>`, `--resume`, `--output-format json`, `--permission-mode acceptEdits`, `--permission-prompts none`, `--strict-mcp-config`, `--setting-sources` all confirmed present.
- **`--no-session-persistence` must not be used** — it disables resume, which the whole multi-turn design needs.
- **Do not use `--bare`** — it skips `CLAUDE.md`/`AGENTS.md` auto-discovery, and "follows the target's root instructions" is part of what we're testing.
- **`examples/onboarding.md` has five Mira answer turns**, plus the trigger: users/problem, requirements/boundaries, platform/quality/constraints, Now-Next-Later priorities, and evaluation/owner/first-action. The fifth carries "record that next action and stop after setup," which matters.
- **All nine template docs open with** `Updated: unknown — set when adopted or changed.` — the cheapest blank/filled discriminator.
- **`PRODUCT.md` `## Purpose and identity`** has nine `Unknown` rows plus `Current alternatives | unknown` lowercase. Cell checks must be case-insensitive.
- **`PRODUCT.md` `## Platform`** (line 28) has a body of bare `unknown` (line 30). `ONBOARDING.md` step 3 requires it survive standalone, and `docs/ONBOARDING_IMPLEMENTATION.md` records that an early trial regressed exactly here. This gets its own named check.
- **STATE's checkpoint has five bullets, and the fifth ends `none recorded.`**, not `unknown`. The check is "no bullet retains its template value," not "no bullet says unknown."
- **Only `## Now` is a table in ROADMAP.md** (header + separator, zero data rows when blank). `## Next` is the prose "No items selected." and `## Later` is "No commitments. …". Do not write a table check for all three.
- **`$product-os init` is Codex syntax.** Claude Code discovers `.agents/skills/` and reads `AGENTS.md`, but invokes skills differently. See *Findings to expect* — this is likely the first real ProductOS gap this work exposes.

**Do not hardcode blank-marker counts.** Today's counts (`PRODUCT` 10/3, `operations` 17/1, …) are accurate but are the most brittle thing that could be committed — any template prose edit breaks the test for no behavioral reason. Derive at test time: count markers in the project file and in its `template/product/` counterpart, require strictly fewer. Keep exact structural assertions only where the structure *is* the rule.

## The mock product

`examples/onboarding.md` already holds what's needed: an explicitly-fictional walkthrough of **PocketGarden**, a reading-list web app owned by **Mira**. Reuse that product — one fictional product, two consumers.

Its "Saved context and handoff" table is keyed by *place* ("Root PRODUCT", "VISION", …), not by path, and is hedged as "illustrative summaries, not complete typed records." Good scripted input and a good behavioral checklist; **not a golden output tree.** Expectations derive from `MODEL.md` (`## Canonical homes`, `## Onboarding completion`, `## Metadata`, `## Lifecycle`) and `ONBOARDING.md` step 3.

**Copy the turns into the fixture; do not parse `examples/onboarding.md` at runtime.** Parsing couples the runner to prose formatting, and that document interleaves narration between turns and will be reworded. Duplication risks silent drift, so guard it: one offline test asserts each turn string appears whitespace-normalized in `examples/onboarding.md`. Silent drift becomes a loud one-line failure with an obvious fix, and the coupling is documented in exactly one place.

## File layout

```
demo_project/
  README.md                      **Fictional example.** label; what this is; the recapture rule
  new-web-app/
    seed/                        the ONLY subtree copied to the temp target
      README.md                  PocketGarden — saving and search, as the walkthrough premises
      AGENTS.md                  ~8 lines of unrelated instructions — the preservation subject
      package.json               name/version; makes "a web app" legible
      src/{store.js,search.js,index.html}
    brief.md                     fictional brief + turns in prose, for humans
    turns.json                   {"trigger": "...", "turns": [...]} machine form
    expect.json                  per-seed assertion data
    golden/                      captured completed instance; no .agents/
    golden_provenance.json       digests + capture metadata
  existing-contract/             second seed, same shape
```

**`brief.md` and `turns.json` live outside `seed/`.** The brief is delivered only as chat turns, never as a file in the target. That is what makes a leakage check meaningful: if fictional content appears in `product/`, there was no legitimate file source for it.

The seed is deliberately **not empty** — the walkthrough premises an existing README and code, so the agent's "inspect first" step has something real to find, and a pre-existing `AGENTS.md` gives the preservation assertion.

**Seeds to ship: two.**
- `new-web-app` — mandatory. The default-layout path: root `PRODUCT.md` created, `product/PRODUCT.md` demoted to a pointer, `AGENTS.md` gains a pointer.
- `existing-contract` — second, and worth it: it tests the one rule whose violation *destroys user data* — "Do not promote a populated local contract or replace a root file without direction to consolidate." Cost is a 30-line populated `PRODUCT.md`; the assertion is byte-exact. This is also the path `docs/ONBOARDING_IMPLEMENTATION.md` claims was validated by simulation, so committing it converts a claim into a check.

**Dropped:** a read-only seed. Its only real assertion is "the assistant *said* it could not save," which decision 3 forbids; the file-level part is already covered by the asset and unexpected-path checks, and a chmod fixture risks `TemporaryDirectory.cleanup()` leaving garbage on macOS. It stays a manual scenario in `docs/CUSTOMIZATION.md`.

**Deferred:** `interrupted-setup`. It needs a two-phase live run and its offline golden is just a partially-filled instance the same checker validates. Design `expect.json` so it can be added later with no code change (`filled` / `may_stay_blank` / `skip_checks` already express it).

## Assertion spec: checks in Python, per-seed data in JSON

The *rules* are universal and belong in code — restating them per fixture guarantees they drift and that a new seed silently omits half of them. Expressing "an empty-bodied table," "this anchor resolves to a heading slug," or "`status` is legal *for this record's type*" declaratively means building a matcher language in JSON, i.e. reimplementing unittest in data. What genuinely varies per seed is data: paths, keyword stems, layout mode. Python 3.9.6 is what's installed, so `json`, not `tomllib`.

`demo_project/<seed>/expect.json`:

```json
{
  "schema_version": 1,
  "seed": "new-web-app",
  "layout": "new-root-contract",
  "canonical_contract": "PRODUCT.md",
  "product_dir": "product",
  "agent_files": ["AGENTS.md", "CLAUDE.md"],
  "must_exist": ["PRODUCT.md", "AGENTS.md", "product/PRODUCT.md", "product/VISION.md",
                 "product/REQUIREMENTS.md", "product/STRATEGY.md", "product/ROADMAP.md",
                 "product/STATE.md", "product/operations/README.md"],
  "must_not_exist": ["product/experiments", "product/features", "product/decisions",
                     "product/cycles", "product/evidence", "product/operations/runbooks"],
  "seed_preserved": ["README.md", "package.json", "src/store.js", "src/search.js"],
  "filled": ["PRODUCT.md", "product/VISION.md", "product/REQUIREMENTS.md",
             "product/STRATEGY.md", "product/ROADMAP.md", "product/STATE.md",
             "product/operations/README.md"],
  "may_stay_blank": ["product/METRICS.md", "product/LEARNINGS.md"],
  "pointer": { "path": "product/PRODUCT.md", "target": "../PRODUCT.md", "max_lines": 25 },
  "coverage": {
    "identity-and-vision": ["PRODUCT.md", "product/VISION.md"],
    "users-and-problem":   ["PRODUCT.md"],
    "core-experience":     ["product/REQUIREMENTS.md"],
    "initial-requirements":["product/REQUIREMENTS.md"],
    "boundaries":          ["PRODUCT.md", "product/REQUIREMENTS.md"],
    "success":             ["product/outcomes"],
    "priorities":          ["product/ROADMAP.md", "product/STRATEGY.md"],
    "starting-point":      ["product/STATE.md", "product/operations/README.md"]
  },
  "traceability": [
    { "id": "platform",      "path": "PRODUCT.md", "section": "## Platform", "all_of": ["web"] },
    { "id": "users",         "path": "PRODUCT.md", "all_of": ["research"] },
    { "id": "hypothesis",    "path": "PRODUCT.md", "all_of": ["hypothes"] },
    { "id": "alternatives",  "path": "PRODUCT.md", "any_of": ["bookmark", "notes"] },
    { "id": "non-goals",     "any_of_paths": ["PRODUCT.md", "product/REQUIREMENTS.md"],
                             "all_of": ["team librar", "summar"] },
    { "id": "workflows",     "path": "product/REQUIREMENTS.md", "all_of": ["search", "open"] },
    { "id": "no-match",      "path": "product/REQUIREMENTS.md", "any_of": ["no match", "no matches"] },
    { "id": "accessibility", "path": "product/REQUIREMENTS.md", "all_of": ["keyboard"] },
    { "id": "privacy",       "path": "product/REQUIREMENTS.md", "all_of": ["privat"] },
    { "id": "speed-deferral","any_of_paths": ["product/REQUIREMENTS.md", "product/STATE.md"],
                             "all_of": ["defer"] },
    { "id": "now-priority",  "path": "product/ROADMAP.md", "all_of": ["retriev"] },
    { "id": "first-action",  "path": "product/STATE.md", "any_of": ["mira", "observ"] }
  ],
  "skip_checks": []
}
```

Keyword **stems, matched case-insensitively** (`librar`, `summar`, `privat`, `defer`, `retriev`, `research`, `hypothes`) survive pluralization and rewording. `coverage` makes the mapping to `MODEL.md#onboarding-completion`'s eight areas auditable; `traceability` makes it falsifiable. `skip_checks` must be validated against the real check registry or a typo silently disables a check.

## The checker

`scripts/check_instance.py`, beside `install_skill.py`, no package — so `from check_instance import …` works under `discover -s scripts`, preserving the existing convention. Stdlib only.

```python
Finding = collections.namedtuple("Finding", "check severity path message")  # "error" | "warning"
CHECKS = (...)          # ordered tuple of ids; single source of truth

def load_expect(path): ...
def check_instance(project, expect, template=TEMPLATE, skill_root=None) -> list
def check_links(root, skip_dirs=(".git", ".agents")) -> list
def main()              # --project --expect [--links-only] [--json]; exit 1 on any error
```

`check_instance` returns findings and never raises on content — the same function serves the offline tests, the mutation suite, the live runner, and a maintainer at the shell.

| Check | Asserts | Scope |
| --- | --- | --- |
| `skill_assets_untouched` | `snapshot()` equality both directions vs `template/product/` (catches added, modified, deleted); `SKILL.md` byte-equal | universal |
| `required_paths_exist` | each `must_exist` is a file | seed |
| `seed_preserved` | `seed_preserved` byte-identical to the seed | seed |
| `no_unexpected_paths` | flags stray files (`NOTES.md`, transcripts, `.DS_Store`) as *warning* | universal |
| `no_empty_record_dirs` | every existing record dir holds ≥1 record with front matter; nothing in `must_not_exist` exists | universal |
| `adoption_stamp_set` | every `filled` doc's `Updated:` differs from the template string; any date is ISO and not future | universal |
| `blank_markers_reduced` | strictly fewer case-insensitive `\bunknown\b` than the template counterpart (derived, not hardcoded) | universal |
| `product_table_filled` | every `## Purpose and identity` value cell non-empty and not `unknown` case-insensitively | universal |
| `platform_section_standalone` | `## Platform` exists; body non-empty and not `unknown`; not folded into boundaries/constraints. **The named regression check.** | universal |
| `roadmap_now_has_rows` | `## Now`/`## Next`/`## Later` present as H2s; `## Now` has ≥1 data row | universal |
| `state_checkpoint_resolved` | 5 bullets present; none retains its template value (`unknown.` ×4, `none recorded.` ×1); ≥1 contains a relative link | universal |
| `local_contract_is_pointer` | ≤ `max_lines`; links to the canonical contract; lacks `## Purpose and identity` | seed |
| `root_agents_pointer` | an agent file names the contract and `product/STATE.md`; **and** every non-blank line of the seed's original `AGENTS.md` survives | seed |
| `established_contract_preserved` | original H2s and fact stems present; blueprint table did not replace them | `existing-contract` |
| `front_matter_valid` | `schema_version: 1`; `type` ∈ MODEL's 10; `id` matches `^[A-Z]{2,4}-\d{3}$` or `^CYC-\d{8}-\d{2}$`, unique tree-wide; `status` legal *for that type*; ISO dates; no blank `id:`/`title:`/`created:`/`updated:` | universal |
| `no_premature_states` | no outcome `achieved`, feature `released`/`evaluated`, experiment `running`/`concluded`, cycle `completed` | universal |
| `no_fabricated_measurement` | METRICS registry has no data rows unless allowed; outcome baselines say `unknown`/`not measured` rather than a numeral | universal |
| `deferrals_recorded` | ≥1 explicit deferral with an owner and a discovery action in the same block | universal |
| `traceability` | stems present in the right destination; `section:` scopes to that H2's body | seed |
| `coverage_destinations_nonblank` | every destination for all eight areas exists and is non-blank | seed |
| `relative_links_resolve` | paths resolve; `#anchor` resolves to a heading slug; directory targets resolve to `README.md` | universal |
| `no_example_leakage` | no `**Fictional example.**` marker; no copy of `docs/`, `examples/`, `skills/`, `scripts/` in product context | universal |

`check_links` doubles as the repo-wide link checker `AGENTS.md`'s publish step asks for — a genuine reduction in manual work, not new machinery.

## The offline positive control

The negative tests need a known-good instance. **Capture one real live run, review it by hand, commit it as `golden/`.**

Rejected: a *hand-written* golden proves only "passes the checker I just wrote" and carries zero information about the agent. *Synthesizing* by mutating template blanks is rot-proof but is the algebraic inverse of the checker — it proves the checker accepts what the synthesizer emits, nothing more, and would never have caught the platform regression a real trial did catch.

Order matters, to avoid circularity: **write the checks from `MODEL.md` first, then capture.** When the capture disagrees with a check, decide deliberately which is wrong and record it — a checker bug gets fixed; an agent bug becomes a finding. Tuning checks until the capture passes would make the suite meaningless.

**How it rots, stated in `demo_project/README.md`:**
1. *Template drift.* `golden_provenance.json` records `{captured_at, framework_version, template_sha256, skill_sha256, claude_cli_version, model, seed, turns_sha256, total_cost_usd, num_turns}`, and a test recomputes the digests and **fails hard** on mismatch. Silent staleness is the real risk; make the failure loud. The fix is a recapture or a conscious digest bump with a CHANGELOG line.
2. *One sample of a nondeterministic process.* It shows one run satisfied the rules; nothing about reliability.
3. *Goldens invite editing to pass.* The golden is never hand-edited; the only sanctioned change is a recapture, recorded in provenance.

**Exclude `.agents/` from the golden** — it would duplicate `template/product/` in the repo and drift. `skill_assets_untouched` is exercised instead against a subject built at test time (golden copied to temp, then the real `install_skill.install()` run on top), which is rot-proof.

## Offline tests

`scripts/test_check_instance.py`, plain `unittest`, importing `snapshot` from `test_install_skill` and `install` from `install_skill`.

1. **`test_bare_install_fails_checker`** — *the load-bearing test.* Copy `seed/` to temp, run the real installer, run the checker. Assert a non-empty error list containing at minimum `required_paths_exist`, `adoption_stamp_set`, `state_checkpoint_resolved`, `platform_section_standalone`, `roadmap_now_has_rows`, `product_table_filled`. Both sides are generated from `template/` at runtime, so it **cannot rot**. If only one offline test ships, ship this.
2. `test_golden_passes_checker` — zero errors per seed, `subTest` each.
3. `test_golden_provenance_matches_template` — recompute digests; fail with the recapture command in the message.
4. `test_turns_match_example_walkthrough` — the drift guard.
5. `test_expect_specs_are_wellformed` — schema version parses; `must_exist` present in the golden; `must_not_exist` absent; every `skip_checks` and `traceability.id` is a real id; every `coverage` key is one of the eight areas.
6. `test_template_has_no_fixture_leakage` — grep `template/` and `skills/` for `PocketGarden`, `Mira`. Enforces the `AGENTS.md` convention mechanically.
7. `test_repository_relative_links_resolve` — `check_links(ROOT)` and on an isolated template copy; zero findings. Converts a manual publish step into a test.
8. The mutation suite.
9. `test_every_check_has_a_negative_case` — `CHECKS` minus a documented allowlist equals the ids covered by the mutation table. Delete a mutation row and this goes red.

Runtime: ~40 small Markdown files, well under a second, no network, no `claude`.

`scripts/test_onboarding_e2e.py` holds the live test, class-decorated `@unittest.skipUnless(os.environ.get("PRODUCT_OS_E2E_LIVE") == "1", ...)`, importing the runner **inside the test method** so the default run never touches `claude` or fails on its absence. The skip and its reason show in `-v` output — visible, not hidden.

## Negative tests

One table-driven helper: copy the golden to temp, install the skill on top, apply a mutation, assert the named check reports an error under `subTest`.

| Mutation | Must be rejected by |
| --- | --- |
| `## Platform` body → `unknown` | `platform_section_standalone` |
| Delete `## Platform`, fold "Platform: web app." into non-goals — **the historical regression** | `platform_section_standalone` |
| Restore STATE's five bullets to template values | `state_checkpoint_resolved` |
| Restore one `Updated:` line to the template string | `adoption_stamp_set` |
| Set an `Updated:` date to next year | `adoption_stamp_set` |
| Restore `Target users and context` → `Unknown` | `product_table_filled` |
| Restore `Current alternatives` → lowercase `unknown` (the case trap) | `product_table_filled` |
| Delete every `## Now` data row / rename `## Now` → `## Current` | `roadmap_now_has_rows` |
| Append a byte to / add a file to / delete a file from `assets/product/` | `skill_assets_untouched` |
| Outcome `status: achieved`; feature `status: released` | `no_premature_states` |
| Outcome `status: shipped` (not in MODEL's set) | `front_matter_valid` |
| `mkdir product/experiments` empty | `no_empty_record_dirs` |
| Blank `id:`; duplicate an `id:`; `created: 09/27/2026`; `schema_version: 2` | `front_matter_valid` |
| Retarget a link to a missing file; retarget an anchor to a missing heading; delete a heading an anchor points at | `relative_links_resolve` |
| `product/PRODUCT.md` ← full copy of the root contract | `local_contract_is_pointer` |
| Remove the product-context block from `AGENTS.md`; delete a seed `AGENTS.md` line | `root_agents_pointer` |
| Replace "web" with "native iOS" in `PRODUCT.md` | `traceability` (platform) |
| Delete the non-goal sentence / the keyboard requirement | `traceability` |
| Strip every "defer" from REQUIREMENTS and STATE | `deferrals_recorded` |
| Add `Baseline: 62% retrieval success (n=40)`; add a METRICS data row | `no_fabricated_measurement` |
| Copy `examples/onboarding.md` into `product/` | `no_example_leakage` |
| Delete `product/REQUIREMENTS.md` | `required_paths_exist` |
| Blank `product/VISION.md` to the template | `blank_markers_reduced`, `coverage_destinations_nonblank` |
| Modify `src/search.js` | `seed_preserved` |
| Add `product/NOTES.md` | `no_unexpected_paths` (warning) |
| (`existing-contract`) Overwrite the populated contract with the blueprint | `established_contract_preserved` |

## The live runner

`scripts/run_onboarding_e2e.py` — not named `test_*`, so `discover` never picks it up.

```
python3 scripts/run_onboarding_e2e.py --seed new-web-app
    [--out DIR] [--keep] [--model M] [--budget-usd 3]
    [--turn-timeout 900] [--extra-turns 2] [--no-check] [--json]
```

1. Preflight `shutil.which("claude")` and capture `claude --version`; exit 2 with a clear message if absent.
2. Run dir via `tempfile.mkdtemp(prefix="product-os-e2e-")`. `--out` is allowed for inspection but passed through the installer's own guard (`rundir != ROOT and ROOT not in rundir.parents`). **This guard, not `.gitignore`, keeps run output out of the repo** — an ignore rule would silently *hide* in-repo output; the guard refuses to create it. Say so in the CHANGELOG so a future maintainer doesn't "fix" it by adding an ignore.
3. `copytree(seed/"seed", rundir/"project")`, then `install_skill.install(...)` — **reuse the real installer**, so the e2e covers installer + skill discovery + guide together.
4. Turn 1, `cwd=rundir/"project"`: `claude -p --session-id <uuid4> --output-format json --permission-mode acceptEdits --permission-prompts none --strict-mcp-config --setting-sources project [--model M] [--max-budget-usd N] "<trigger>"`. Turns 2..N identical but `--resume <id>`. **Pass the permission and output flags on every turn** — do not assume they persist across resume.
   - `--permission-prompts none` is the difference between a test and a hang: anything that would prompt is denied rather than blocking forever. Cost: no Bash. `ONBOARDING.md` step 1 only needs reads, which Read/Glob/Grep cover. Verify once by hand.
   - `--strict-mcp-config` and `--setting-sources project` keep a developer's personal MCP servers, hooks, and settings out of the run.
5. Per turn, capture stdout → `transcript/turn-NN.json`, stderr → `.err`, pull `{session_id, num_turns, duration_ms, total_cost_usd, is_error, subtype}`, and take `snapshot()` before and after, recording `{created, modified, deleted}` in `run.json`. **That per-turn delta is how "saves progress between rounds" becomes observable.**
6. **Finished vs stalled, decided on files, never dialogue.** `finished` = all turns delivered and zero checker errors. `stalled`, each a distinct recorded `exit_reason`: non-zero exit; `is_error: true`; `subtype != "success"`; turn exceeds `--turn-timeout` (default 900s via `subprocess.run(timeout=…)`); cumulative cost over `--budget-usd`; **or the tree is byte-identical across two consecutive turns** (nothing being saved). No transcript parsing anywhere.
7. `--extra-turns K` (default 2): if the checker still errors after the scripted turns, resend the catch-all up to K times and re-check. Record `extra_turns_used` — needing nudges is itself a finding, not something to paper over.
8. Exit 0 finished, 1 checker errors, 2 stalled/infrastructure. Keep the run dir on failure, print its path either way.

## Execution order

1. **Recon, before writing code.** Do one throwaway manual `claude -p` run in a temp copy of the seed to confirm the project-local skill is discovered and a trigger phrase routes to `ONBOARDING.md`. *This is the biggest feasibility unknown* — `$product-os init` is Codex syntax, so the working Claude Code trigger has to be established here. Settle it first.
2. **Fixture**: `new-web-app/seed/`, `demo_project/README.md`, `brief.md`, `turns.json`. *Verify:* the installer succeeds on a temp copy; `grep -r PocketGarden template/ skills/` is empty.
3. **Checker, first pass** — the structural checks plus `CHECKS` and `main()`. *Verify:* against a bare install it reports exactly those errors; `--links-only --project template/product` reports zero, which also validates the link checker against a known-good tree.
4. **`test_bare_install_fails_checker` only.** *Verify:* the suite runs 7 tests under a second, no network.
5. **Live runner.** *Verify:* one live run with `--keep --budget-usd 3`; read the tree by hand against `ONBOARDING.md` step 3.
6. **Iterate to green** — see below. This is where the user's goal is actually met.
7. **Capture the golden** from a clean run; write `golden_provenance.json` from `run.json`.
8. **Remaining checks**, driven by what the golden contains; then the **mutation suite** and `test_every_check_has_a_negative_case`.
9. **Seed 2, `existing-contract`** — live-run once, capture, add its negatives.
10. **Docs, one commit** (`AGENTS.md`: update guides, templates, examples, and version notes together): `README.md` repository map; `docs/CUSTOMIZATION.md#improve-the-framework` (commands, recapture rule, which scenarios stay manual); `docs/ONBOARDING_IMPLEMENTATION.md` validation rows + limits; `docs/DEVELOPMENT_PLAN.md` capability row; `CHANGELOG.md` `## Unreleased`. **No new guide** in `docs/README.md` — the fixture README plus CUSTOMIZATION is the right weight. **No `.gitignore` change.**

## Iterating until the test project has every required file

The point of the goal, and the part that changes ProductOS rather than the test. Loop:

1. Run the live e2e. Read the checker findings.
2. For each finding, classify it explicitly — and record the classification, because this is the audit trail for how strict the suite really is:
   - **Checker bug** — the check misreads a legitimately correct instance. Fix the checker.
   - **Spec bug** — `expect.json` demands something `MODEL.md` does not require. Fix the spec.
   - **ProductOS gap** — the agent followed the guide and still produced a non-conforming instance. **Fix the guide**: `template/product/ONBOARDING.md`, `MODEL.md`, or `skills/product-os/SKILL.md`. This is the category the goal is about.
3. Re-run. Repeat until zero errors.

**Never loosen a check to go green.** If a check is relaxed, log the reason in `demo_project/README.md`. A suite quietly weakened to pass is worse than no suite.

### Findings to expect, and the likely fixes

- **No documented Claude Code entry point.** `README.md`, `docs/QUICKSTART.md`, `ONBOARDING.md`, and `SKILL.md` document only `$product-os init` (Codex). If step 1 shows the skill needs a different invocation, that is a real adopter-facing gap — the fix is documenting both entry points, not contorting the test.
- **`operations/README.md` is 17 `Unknown` cells across 8 capability rows.** `ONBOARDING.md` step 3 lists operations as a destination but the interview's four topic groups never systematically ask about environments, feedback sources, metrics access, or runner. Expect this file to come back barely touched, failing `coverage_destinations_nonblank`. Likely fix: `ONBOARDING.md` step 3 should say explicitly which operations rows a setup interview is expected to establish versus leave `unknown` with a discovery action.
- **The `success` area maps to "outcome records, METRICS when defined."** Whether a setup run must create an `outcomes/OUT-001-*.md` is genuinely ambiguous in `MODEL.md` — the walkthrough shows one, the "create a directory with its first real record" rule permits none. Resolve it in `MODEL.md` rather than encoding a guess in the spec.
- **`no_empty_record_dirs` vs. the agent's instinct** to scaffold all record directories. If the live run creates empty `features/`, that's a ProductOS gap: `ONBOARDING.md` should restate the rule at the point of writing.

## Verification

```sh
# Default offline run — fast, network-free, claude-free
python3 -m unittest discover -s scripts -p 'test_*.py' -v
#   6 installer + ~9 checker + ~40 mutation subtests, OK (skipped=1), under ~2s

# Checker as a tool, against the committed golden
python3 scripts/check_instance.py --project demo_project/new-web-app/golden \
    --expect demo_project/new-web-app/expect.json ; echo "exit=$?"
#   0 errors, 0 warnings / exit=0

# Prove it is not vacuous: revert the Platform body in a copy
cp -R demo_project/new-web-app/golden "$TMPDIR/pg"
python3 - "$TMPDIR/pg/PRODUCT.md" <<'PY'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1])
p.write_text(re.sub(r"(?ms)^## Platform\n\n.*?(?=^## )", "## Platform\n\nunknown\n\n", p.read_text(), count=1))
PY
python3 scripts/check_instance.py --project "$TMPDIR/pg" \
    --expect demo_project/new-web-app/expect.json ; echo "exit=$?"
#   exit=1 with a platform_section_standalone error naming PRODUCT.md

# Repo-wide link check (replaces a manual publish step)
python3 scripts/check_instance.py --links-only --project .
python3 scripts/check_instance.py --links-only --project template/product

# Live path, opt-in
PRODUCT_OS_E2E_LIVE=1 python3 scripts/run_onboarding_e2e.py \
    --seed new-web-app --keep --budget-usd 3
```

After the live run, confirm by hand:
- `git status --porcelain` is **empty** — nothing leaked into the repo.
- `run.json` shows a non-empty file delta after **each** answer turn (progress saved between rounds).
- `project/PRODUCT.md` has a standalone `## Platform` whose body says web.
- `project/product/PRODUCT.md` is a short pointer, not a contract.
- `diff -r project/.agents/skills/product-os/assets/product template/product` is empty.
- `extra_turns_used` is 0; if not, record it.

## Risks and honest limits

**Nondeterminism.** The offline suite tests the *checker*. The live run tests the agent once, with one model, one CLI version, one script. A pass means "one run satisfied the framework's own rules." Treat a red live run as a prompt to read the transcript, never as a metric.

**Golden bias.** The checker will be written while looking at the golden, so it is biased toward what that run produced. `test_bare_install_fails_checker` and the mutation suite defend against a *vacuous* checker; nothing here defends against a *biased* one. Say so rather than implying otherwise.

**Cost.** Roughly six substantial turns per seed — single-digit dollars and several minutes each, capped by `--max-budget-usd`. **No CI.** The repo has none today, and adding a hosted runner for this would cut against "Do not add a mandatory service, framework, SDK, or agent runtime just to adopt the documentation model."

**Runtime drift.** Flag names change — this design already had to drop the nonexistent `--max-turns`. The runner records the CLI version and exits 2 with a distinct reason rather than silently degrading if `--session-id`/`--resume` change behavior.

**Entry-point coupling.** This exercises the guide and the model through *one* runtime. It does not prove the Codex entry point the README documents.

### Draft wording for `docs/ONBOARDING_IMPLEMENTATION.md`

| Check | Observed result |
| --- | --- |
| Offline onboarding regression checks | Passed. A captured completed instance per seed satisfies the canonical-home, required-area, front-matter, lifecycle, and link rules; a bare installation fails the same checks; ~40 mutations are each rejected by their named check. Deterministic, offline, no agent involved. |
| Scripted live onboarding run (opt-in) | A single scripted six-turn headless run per seed, in a temporary project outside the checkout, produced an instance passing the checks above and left the installed skill assets byte-identical. One sample, one model, one CLI version, one runtime; not a measure of interview quality or reliability. |

> These are regression checks over one captured agent run per seed, not validation of onboarding. They cannot show that the interview asks good questions, that unscripted users reach the same coverage, that the Codex entry point behaves the same way, or that any product outcome improved. The read-only, ambiguous-scope, and contributor-orientation paths remain manual scenarios. A captured instance goes stale when the template changes; a provenance digest fails the suite when it does, and the only sanctioned fix is a recapture.
