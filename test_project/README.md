# End-to-end test fixtures

**Fictional example.** Every product detail, person, and answer under this directory is invented to exercise ProductOS's onboarding procedure. None of it is live product evidence or proof that ProductOS improves outcomes. Nothing under this directory is included in the bare template or the installed skill assets.

These fixtures test whether an agent following [ONBOARDING.md](../template/product/ONBOARDING.md) produces an instance satisfying the rules [MODEL.md](../template/product/MODEL.md) already states. They do not test prose wording.

## What is here

| Path | Purpose |
| --- | --- |
| `<seed>/seed/` | The starting state of a target project. The only subtree copied into a run. |
| `<seed>/brief.md` | The mock product and its scripted answers, in readable form. |
| `<seed>/turns.json` | The same answers as ordered machine-readable turns. |
| `<seed>/expect.json` | Per-seed assertion data for the checker. |
| `<seed>/golden/` | A captured completed instance, used as the checker's positive control. |
| `<seed>/golden_provenance.json` | Capture metadata and digests of the template the golden was produced from. |

The brief lives outside `seed/` on purpose. Its facts reach the agent only as conversation turns, never as a file in the target project, so fictional content appearing in `product/` has no legitimate source and the leakage check means something.

## Running

```sh
# Offline. No network, no agent, no claude CLI.
python3 -m unittest discover -s scripts -p 'test_*.py' -v

# The checker as a tool.
python3 scripts/check_instance.py --project test_project/new-web-app/golden \
    --expect test_project/new-web-app/expect.json

# A real scripted interview. Opt-in, costs tokens, takes minutes.
PRODUCT_OS_E2E_LIVE=1 python3 scripts/run_onboarding_e2e.py --seed new-web-app --keep
```

Runs never happen inside this checkout. The runner copies `seed/` to a temporary directory and refuses an output path inside the framework, because the installer refuses an in-checkout target. That refusal is deliberate and is not fixed by adding a `.gitignore` rule — an ignore rule would hide in-repo output rather than prevent it.

## Rules for these fixtures

**The golden is never hand-edited.** The only sanctioned change is a fresh capture, recorded in `golden_provenance.json`. A golden edited to pass tells you nothing.

**Never loosen a check to make a run pass.** When a live run disagrees with the checker, classify it before changing anything: a checker bug, a spec bug in `expect.json`, or a genuine ProductOS gap to fix in the guide. Record relaxations below so the suite's real strictness stays auditable.

**The golden goes stale when the template changes.** `test_golden_provenance_matches_template` recomputes the template digest and fails loudly rather than letting a stale capture pass quietly. Recapture, or bump the digest deliberately with a changelog note.

## Recorded relaxations

Add an entry here whenever a check is weakened, with the reason and the date.

- **2026-09-27 — `state_checkpoint_resolved` no longer requires a minimum bullet count.** It previously required at least as many bullets as the template defines. A captured run replaced the bullets with a coverage table and a deferrals table carrying strictly more information, and was rejected for it. The check now requires the checkpoint to address coverage, completion, deferrals, and readiness in any form, and still rejects retained template values and a missing link. This is classified as a checker bug in the findings below, but it is also genuinely less strict about shape, so it is recorded here too. The risk it accepts: a checkpoint could satisfy all four topics with thin content.
- **2026-09-27 — `no_fabricated_measurement` scrubs dates, record ids, and backticked references before looking for a numeral.** It previously flagged any numeral near the word "baseline". The risk it accepts: a fabricated measurement written only as a bare year, or inside backticks, would pass. It remains a warning, not an error, for this reason.

## Findings from live runs

| Date | Finding | Classification | Resolution |
| --- | --- | --- | --- |
| 2026-09-27 | `install_skill.py` installed only into `.agents/skills/`, which Claude Code does not read, so the skill was inert under that runtime. | ProductOS gap | Added `--agent codex\|claude\|both` to the installer and documented both invocations. |
| 2026-09-27 | A headless run with `--permission-prompts none` and no tool allowlist had its `ls` denied, and the agent abandoned inspection instead of falling back to file tools. | Harness | The runner passes an explicit `--allowedTools` list covering the file tools and omits Bash, so a run is hermetic by construction. |
| 2026-09-27 | The turn that saves most of the instance ran past a 420-second timeout, having already written 12 files. Earlier turns took 100–150 seconds. | Harness | Raised the per-turn default to 1500 seconds. |
| 2026-09-27 | On a stalled run the runner printed "0 errors, 0 warnings" because the checker never ran, so a timeout looked like a pass. | Harness | The checker now runs even on a stall, and the summary says whether it ran and that the instance is partial. |
| 2026-09-27 | A run truncated during scripted answer 4 still passed the whole spec: nothing required a fact that only the later answers supply. | Spec bug | Added the `later-deferred`, `study-protocol-deferral`, and `direction-owner` traceability entries. The truncated instance now fails, as it should. |
| 2026-09-27 | `relative_links_resolve` rejected `[outcomes/](outcomes/)`, a link to a directory that exists and holds two records. | Checker bug | A bare directory link renders as a listing and needs no README inside it. The check now accepts any target that exists. |
| 2026-09-27 | `state_checkpoint_resolved` rejected a checkpoint with "2 bullets; the template defines 5". The instance had replaced the bullets with an eight-row coverage table with resolving links and a deferrals table with owners and discovery actions — strictly more informative. | Checker bug | Counting bullets judged shape over substance. The check now requires the checkpoint to address coverage, completion, deferrals, and readiness in any form, and still rejects retained template values. |
| 2026-09-27 | `no_fabricated_measurement` warned on two lines whose only numerals were an ISO date and a record id, in text reading "no baseline" and "none". | Checker bug | Dates, record ids, and backticked references are scrubbed before looking for a measurement, and "no baseline" now counts as an explicit non-measurement. |
| 2026-09-27 | The `non-goals` traceability stem `team librar` missed a correct instance that recorded the non-goal as "team **or shared** libraries" in both canonical homes. | Spec bug | Stems must survive paraphrase; the entry now matches `librar` and `summar` independently. |
| 2026-09-27 | Three mutation rows did not fire: one asserted error severity for a check that is a warning by design, one relied on `_edit` replacing every occurrence when it replaced one, and one assumed a METRICS.md structure the instance had legitimately rewritten. | Test bug | Mutations now assert a check fires at any severity, `_edit` takes a count, and the metrics mutation adds the registry section it needs. |
| 2026-09-27 | The link checker reported a broken link inside a code span, where the text was an example of link syntax rather than a link. | Checker bug | Fenced blocks and inline code are stripped before links and heading anchors are collected. A broken link in prose is still reported. |

No ProductOS gap was found in the first complete run. Every finding was in the checker, the expectation spec, or the test harness. That is worth stating plainly: the procedure produced a conforming instance on the first complete attempt, and the suite's early value was mostly in exposing its own bugs.
