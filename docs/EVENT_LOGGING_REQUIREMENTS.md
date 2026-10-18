# Event logging and version-aware evolution requirements

Status: **specified, not implemented**. Owner direction captured on 2026-10-18.

This document specifies the next ProductOS capability. The current skill, installer, and execution procedure do not yet emit these events or automatically migrate applied artifacts. This is a framework requirement, not an applied product's event history, a new released command, or a change to the canonical record lifecycle in [MODEL.md](../template/product/MODEL.md).

## Purpose and scope

ProductOS must leave a machine-readable, Git-versioned account of its commands, workflow progress, artifact changes, and the versions under which those actions occurred. A subsequent session or newer framework version must be able to determine what happened, where work stopped, and whether existing artifacts need a compatible structural upgrade.

The journal complements PRODUCT, STATE, and typed records. Those remain authoritative for product facts, current handoff, and decisions; events record observed actions and provenance. Logging a command does not prove it succeeded, and recording an upgrade proposal does not mean it was applied.

## E1. Committed project-owned journal

- Store the journal at `<project-root>/.product-os/`, inside the adopted product's repository. It belongs to the project, never the installed skill's asset directory. In a monorepo, identify each product scope explicitly; do not mix journals without product/instance identifiers.
- Track `.product-os/` in Git. Never add it or its journal files to `.gitignore`, `.git/info/exclude`, or a generated ignore rule. Detect effective global or inherited ignore patterns and report them; repair project-owned exclusions within existing scope rather than silently claiming the journal is tracked.
- Use UTF-8 JSON with a versioned envelope. Recommended layout: `instance.json` for current installation/layout metadata and `events/<UTC-date>/<run-id>/<sequence>_<event-id>.json` for immutable event records. Use one JSON object per event, not prose-only logs.
- Allocate unique run/event IDs, serialize writes within a run, and publish each event atomically without replacing an existing file. Independent runs write separate files. Sequence numbers order a run; UTC timestamps do not establish a total order across branches or concurrent runs.
- Commit the journal with the associated product changes through the project's established commit workflow. On read-only commands, journal files are still eligible for the next commit. Logging alone does not authorize an automatic commit or push, staging unrelated files, or changing the repository's branch policy. Report when events remain uncommitted.
- Preserve events across merges and upgrades. A correction is a new event referencing the original; never rewrite history merely to conform it to the latest schema. Git history is version control, not a tamper-proof audit system or an external action receipt.

`.product-os/` is the committed metadata boundary. Put future DuckDB databases, credentials, process locks, temporary files, and disposable caches outside it, for example under `.product-os-local/` with appropriate local exclusions. This supersedes the earlier metrics/dashboard proposal to ignore `.product-os/` and place `metrics.duckdb` there. Durable measurement storage and backups still need their own policy.

## E2. Parseable event envelope

All records must carry the following fields or explicitly documented null/unknown values where the fact cannot be observed. A future schema and validator must enforce field types and event-specific payloads.

| Field | Type and meaning |
| --- | --- |
| `event_schema_version` | Integer version of the event envelope; distinct from product-record schemas |
| `event_id`, `run_id`, `instance_id` | Stable unique strings identifying the event, invocation/run, and adopted instance |
| `sequence`, `occurred_at` | Positive per-run integer and UTC ISO timestamp |
| `event_type`, `status` | Stable machine identifiers for the event and its observed outcome; no parsing of prose required |
| `description` | Required short human-readable description of the actual event |
| `actor` | Object identifying human/agent/tool, host, and model when known; use explicit unknowns |
| `command_id`, `parent_event_id` | Correlation to a command and causal parent; null when not applicable |
| `scope` | Product identifier and repository-relative product root; never machine-specific absolute paths |
| `versions` | Loaded framework release and revision, skill/package identity or digest, instance layout version, and record-model version when available |
| `git_context` | Branch when available, observed HEAD commit, and dirty-worktree indicator; unknown outside Git |
| `data` | Event-specific structured payload: command, workflow progress, artifact changes, compatibility assessment, or migration |

`description` explains the event but must not substitute for structured IDs, step statuses, paths, or results. Readers must retain unknown fields and event types, and use schema versions to distinguish unsupported structures. An unsupported major schema permits inspection of known metadata but must not authorize automated mutation based on an incomplete interpretation.

## E3. Command coverage and honest capture

- Log every ProductOS entry invocation, including `init`, `resume`, `orient`, `run`, equivalent natural-language requests, and subsequent supported commands. Record the normalized operation and entry route without requiring the full user prompt.
- Also log each tool/shell command ProductOS dispatches to perform that work, including reads, verification, artifact generation, MCP retrieval, and attempted commands that fail. Child operations reference their invoking command and run. Capture structured tool name or sanitized executable/arguments, relative working directory, start/end time, exit code when applicable, and result/artifact references.
- Write a `command.started` event before dispatch and a `command.finished` event with `succeeded`, `failed`, `blocked`, `cancelled`, or `interrupted` status when observed. A start without a terminal event means unresolved/interrupted work, not success. On resume, inspect actual state and append reconciliation; do not blindly rerun an uncertain side effect.
- Define the capture boundary: ProductOS-dispatched work is covered; unrelated terminal activity is not. Use actual host hooks, tool wrappers, or runner callbacks for automatic capture. When a host cannot intercept some commands or nested subprocesses, record the capture mode and gap; agent-written summaries must not be presented as complete command interception.
- Exclude the logger's own atomic writes, sequencing, and internal journal-maintenance operations from recursive command logging. Their failure is a diagnostic attached to the invocation, not an unbounded stream of logging events.
- Store sanitized metadata and concise results, not secrets, environment dumps, raw interview transcripts, complete tool payloads, or arbitrary stdout/stderr by default. Preserve executable/tool identity and redacted argument structure when values cannot be committed. Bound description/error sizes and record omitted/redacted fields explicitly.
- If journaling is unavailable, report the failure and do not perform dependent product mutations claiming full provenance. Read-only diagnosis may continue with a visible coverage limitation. If work succeeds but its terminal event cannot be written, preserve the artifact/result, report uncertainty, and reconcile it in the next run instead of asserting failure or duplicating execution.

## E4. Interview and artifact provenance

An interview must have a stable `workflow_id` across sessions and runs, a procedure/version reference, stable step IDs, and explicit step state. Log interview start, completed steps, saved checkpoints, resume, and finish. Step state must distinguish `pending`, `in_progress`, `completed`, `deferred`, and `blocked`; these are workflow progress values, not additions to MODEL's typed-record lifecycles.

Map steps to the canonical [onboarding coverage areas](../template/product/MODEL.md#onboarding-completion). Save completed step IDs, unresolved/deferred areas with reason and next action, and links to canonical answers/artifacts at each checkpoint. Do not mark a step complete solely because a file exists or treat silence as an answer. STATE remains the current resumable handoff; any derived journal progress view must detect and explain disagreement with actual artifacts.

Log artifact creation, update, move, and deletion with:

- Stable record ID where one exists, repository-relative before/after paths, and action.
- Before/after content digests, using SHA-256; null for a nonexistent side.
- Record schema or format version when present, and the producer/framework version from the event envelope. Root summary documents without record frontmatter must not receive invented record schema values.
- Producing command/workflow/step, change description, and verification result or explicit absence of verification.

A checkpoint event is written after the referenced artifact writes and records their resulting hashes. The writer is not a cross-file transaction: interruption can leave an artifact without its event or a checkpoint without later work. A resume/reconciliation checks files against recorded hashes, detects missing or changed content, and records what was actually recovered. Human or external edits are identified as externally observed changes; never fabricate the original actor or command.

### Illustrative checkpoint event

This is fictional example data, not evidence of a completed interview or an implemented emitter. The placeholder digests and revisions below would be replaced by actual observed values. IDs are abbreviated only for readability.

```json
{
  "event_schema_version": 1,
  "event_id": "event-example-03",
  "run_id": "run-example-01",
  "instance_id": "instance-example",
  "sequence": 3,
  "occurred_at": "2026-10-18T04:30:00Z",
  "event_type": "interview.checkpoint_saved",
  "status": "succeeded",
  "description": "Saved identity and user/problem answers; requirements remain next.",
  "actor": {"kind": "agent", "host": "codex", "model": "unknown"},
  "command_id": "command-example-01",
  "parent_event_id": "event-example-02",
  "scope": {"product_id": "example-product", "product_root": "."},
  "versions": {
    "framework_version": "0.3.0",
    "framework_revision": "unknown",
    "skill_digest": "unknown",
    "instance_layout_version": 1,
    "record_model_version": "unknown"
  },
  "git_context": {"branch": "product-brief", "head_commit": "unknown", "dirty": true},
  "data": {
    "workflow_id": "interview-example-01",
    "procedure": "product/ONBOARDING.md",
    "procedure_digest": "unknown",
    "steps": [
      {"id": "identity_vision", "status": "completed", "artifacts": ["PRODUCT.md", "product/VISION.md"]},
      {"id": "users_problem", "status": "completed", "artifacts": ["PRODUCT.md"]},
      {"id": "initial_requirements", "status": "pending", "artifacts": []}
    ],
    "next_step_id": "initial_requirements",
    "artifacts": [
      {"path": "PRODUCT.md", "action": "updated", "before_sha256": "unknown", "after_sha256": "unknown"},
      {"path": "product/VISION.md", "action": "created", "before_sha256": null, "after_sha256": "unknown"},
      {"path": "product/STATE.md", "action": "updated", "before_sha256": "unknown", "after_sha256": "unknown"}
    ]
  }
}
```

Actual checkpoint events include real digests for existing readable artifacts; `unknown` is a coverage defect to report, not a shortcut around verification.

## E5. Versions and Git context

Distinguish the framework release/revision actually loaded by this invocation, the installed package version, instance layout version, event schema version, each artifact's record/format version, and the project's code revision. An installed skill can be older than the framework checkout. A release string alone is insufficient for unreleased or locally edited packages; preserve revision/digest and a local-modification indicator where observable.

`instance.json` records stable instance/product identity, adopted and installed framework/package versions, current layout version, intentional local deviations, and the last verified migration reference. Its current values are a convenience, not a replacement for per-event provenance. Compare it with the loaded package and actual artifacts before relying on it.

The journal records the HEAD visible at event time and artifact hashes for uncommitted changes. Do not claim that HEAD contains those changes. The Git commit containing an event cannot be embedded into itself without changing its hash: obtain containment from Git history or record a later `git.commit_observed` event. Historical events must not be rewritten after each commit. Git context refers to the target product repository; framework source revision belongs in `versions`.

## E6. Compatibility assessment and migration

On entry, compare the loaded capability/schema versions with instance metadata and actual artifacts. Consult versioned, packaged migration definitions and record a `compatibility.checked` event identifying the inspected versions, artifact hashes, known deviations, and gaps. A newer version is not a reason to replace an applied instance with a blank template.

Each migration definition must name its ID, supported source/target layout or artifact versions, required tool capability, preconditions, affected paths, deterministic changes, validation, recovery, and idempotency rule. Installed package updates and applied product-artifact migrations are separate operations. Do not pretend to update a live agent's already loaded skill in place.

| Assessment | Required handling |
| --- | --- |
| Compatible; no changes needed | Record assessment and continue ordinary work |
| Known additive or lossless structural migration, within established authority | Show or persist the proposed diff; auto-apply only after preconditions pass; validate and record results |
| Ambiguous mapping, conflicting local customization, or changed product meaning/policy | Save a proposed migration and explain the unresolved choice; seek direction only where existing authority does not settle it |
| Unsupported newer schema or unknown migration path | Preserve artifacts; limit dependent mutation and report the missing capability; independent work can continue |

Automatic migration must preserve product facts, stable IDs, unknown fields/sections, links, historical hypotheses/results, metric definition versions, and operating authority. It must not rename or delete populated artifacts without a verified lossless mapping and recoverable preimages. Use an explicit preview/diff and expected-before hashes; abort on unexpected concurrent changes instead of overwriting them.

Record `migration.proposed`, `migration.started`, and `migration.finished` events with migration ID, source/target versions, plan/diff references, affected before/after hashes, validation outcome, authority reference, and any unresolved work. For multi-file migrations, stage recoverable writes and detect partial application after interruption. Do not report the target version as applied until all required validation succeeds. Failed rollback or partial recovery must remain visible; do not restore files that have subsequently changed without reconciling those changes.

Repeat application must be a no-op or a verified resume of that same migration, never duplicated content. Keep prior event envelopes as recorded; readers adapt old versions without rewriting them. Any migration that changes product intent remains governed by existing owner/project authority rather than by the availability of a newer feature.

## E7. Connection to metrics, experiments, and RSI

Use the same journal for future metric proposal/definition, collection, experiment lifecycle, evaluation, and decision events. Include journey/metric/experiment IDs, definition versions, data-window/source references, evaluator version, evidence links, and next-action references as applicable. Raw observations remain in the measurement store, not duplicated in the Git journal.

This provenance lets a newer ProductOS assess artifact compatibility and lets an improvement loop compare workflow versions. A logged feature upgrade is not proof of better outcomes: measured evaluations still determine whether the new workflow improves quality, cost, time, or product results.

## Implementation sequence and acceptance

| Slice | Deliverable and required evidence |
| --- | --- |
| Envelope and writer | Versioned schema and stdlib-compatible atomic writer/reader; invalid envelopes fail; concurrent runs preserve both histories; no logger recursion |
| Entry/command capture | Wire supported host hooks/wrappers and skill/installer entry paths; successful, failed, unknown-command, interrupted and read-only invocations leave parseable correlated events; unobservable coverage is explicit |
| Interview/artifact capture | Resume one interview across two runs; parser reports completed/deferred/pending steps and generated artifacts; hashes match actual files and external edits are detected |
| Git/version checks | Verify effective ignore rules and committed journal alongside product changes; distinguish loaded, installed, instance, record and code versions; no self-referential commit-hash requirement |
| Migration support | Preview a known migration, auto-apply within established authority, validate and recover; retry is idempotent; conflicting customization becomes a proposal; unknown newer schemas remain intact |
| End-to-end trial | Exercise a fictional old instance through interruption, upgrade and resume; preserve user content and old events, identify exact applied versions and prove validated current state |

Update the canonical model only for actual new metadata/lifecycle conventions, then align templates, onboarding/execution guides, operations, skill packaging, installer/checker behaviour, examples, compatibility guidance, and release notes in the implementation change. No new typed product record or mandatory hosted service is required just to log events. Older instances can continue through a declared legacy path; initialize provenance from inspected reality and record a history gap instead of inventing past events.

Requirements are complete when their implementation and behavioural checks satisfy the slices above. This document alone installs no hooks, starts no runner, writes no product journal, and migrates no applied instance.
