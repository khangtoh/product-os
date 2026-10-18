# ProductOS: journey metrics and experiment execution plan

Date: 2026-10-18  
Status: proposed implementation plan; the measurement runtime and integrations are not implemented.

Storage alignment: this repository copy incorporates the later [event logging and version-aware evolution requirements](../docs/EVENT_LOGGING_REQUIREMENTS.md). `.product-os/` is committed metadata; local measurement databases and raw receipts live outside it.

## Intended result

ProductOS will maintain versioned product measurement definitions, associate them with product journeys, manage experiments against those definitions, collect observations into local DuckDB, and create an HTML dashboard in each adopted product repository. It will be able to retrieve observations through MCP servers as well as local data imports.

The dashboard and the agent will consume the same measurement and evaluation results. ProductOS will use results to propose the next experiment, preserve decisions, and resume work across sessions.

This delivers the measurement and experiment part of a product improvement loop. Automated code changes, deployment, exposure allocation, continuous scheduling, and evaluated changes to ProductOS's own methods remain separate capabilities. They can connect to this foundation without being prerequisites for its first release.

## 1. Extend the current framework

The current framework already supplies:

- `product/METRICS.md`: canonical metric IDs and definitions, calculation, population, time handling, quality, baseline, target, ownership, and revision discipline.
- `product/experiments/`: experiment protocol, results, amendments, and the lifecycle `draft → ready → running → analyzing → concluded`, with `cancelled` available.
- `product/MODEL.md`: record metadata, relationships, lifecycle, and integrity rules.
- `product/EXECUTION.md`: bounded execution, verification, and resumable handoff.
- `product/operations/README.md`: actual sources, runner capability, access, and authority.

Keep those conventions. Add explicit journey references, parseable measurement contracts, a collector/evaluator, and an HTML view. Keep ordinary documentation adoption usable without installing the runtime.

## 2. Define one authoritative home for each fact

| Fact | Authoritative home | Derived representation |
| --- | --- | --- |
| Journey identity and definition | Existing project journey artifact; otherwise a ProductOS journey record | DuckDB journey index and dashboard |
| Metric meaning, version, formula, population, source binding, freshness | Structured entries in `METRICS.md`, with versioned query files where needed | DuckDB metric definition index |
| Metric-to-journey associations | Metric definition's `journey_ids` | DuckDB relationship table; journey dashboard |
| Experiment hypothesis, expected effect, comparison, criteria, and lifecycle | Experiment Markdown record with structured protocol | DuckDB experiment index and dashboard |
| Source configuration | `product/metrics/sources.yaml`; secret references only | Runtime configuration |
| Collected observations | Local DuckDB, with source references and collection history | API and dashboard values |
| Conclusion and subsequent action | Existing evidence, decision, and learning records | Dashboard links and indexed summaries |

Do not introduce a separately editable `metrics.yaml` containing the same definitions as `METRICS.md`. Use one schema-versioned YAML block per metric in the existing file. Generate its summary table from those blocks, or validate it against them. Explanatory prose can remain alongside the structured definition.

DuckDB is the local observation store and query engine. It does not replace a warehouse or telemetry provider as the original measurement source. Label imported aggregates as provider-computed and locally calculated values as locally computed. A provider value is comparable only when its semantics match the registered metric.

## 3. Journey and metric contracts

### Journeys

Reuse stable IDs from existing journey definitions, including AI Operable Product artifacts where present. Link those artifacts rather than copying their maintained content. A small journey index can resolve existing IDs to paths. For projects without journey records, add a generic journey template and a `journey` type to MODEL, with stable `Journey-01` IDs and `proposed`, `active`, and `retired` states.

A journey identifies the user/actor, trigger, intended successful outcome, important steps, observable completion, and relevant failure/recovery references. Retired journeys remain resolvable for historical experiments. Every new experiment must reference a primary journey; additional affected journeys are optional.

### Metrics

Each definition must include:

- Stable ID, definition version, name, purpose, owner, and proposed/active/retired definition status.
- One or more journey IDs, or an explicit product-wide scope. Product-wide reliability or economics metrics need not be artificially assigned to every journey.
- Unit, aggregation, calculation, eligibility, exclusions, deduplication, and allowed dimensions.
- Event-time/window semantics, reporting timezone, and late-data handling.
- Source binding and query reference/version, or an exact mapping to a provider-computed measurement.
- Expected refresh cadence, freshness limit, completeness checks, and known limitations.

For ratios, retain numerator and denominator so the runtime never averages daily percentages incorrectly. For percentiles, do not merge provider aggregates unless the source supplies a valid mergeable representation. Unsupported aggregation returns unavailable, not an approximation disguised as the defined metric.

Metric-definition status and observation health are different: an active metric can have missing, stale, partial, or errored observations.

Experiments reference `(metric_id, definition_version)`. Meaningful changes to formulas, populations, or windows create a new immutable definition revision. Preserve old definitions and query versions for completed and running experiments. Never silently reinterpret historical values under a new formula.

## 4. Experiments and expected metrics

Extend the existing experiment template with a structured protocol containing:

| Field | Required behaviour |
| --- | --- |
| Journey | One primary journey; optional additional affected journeys |
| Outcome and hypothesis | Existing outcome link, intervention, eligible population, and reason for expected change |
| Primary measure | Metric ID/version, expected direction, and proposed or adopted success threshold |
| Baseline and comparison | Measured baseline/reference; comparison design and its limits |
| Guardrails | Relevant metric IDs/versions and breach thresholds, or an explicit reason none applies |
| Exposure | Variant/cohort mapping, assignment unit, actual exposure source, intervention/commit/flag version |
| Observation plan | Window, sample or duration rationale, freshness and completeness requirements |
| Decision rules | Success, failure, inconclusive, stopping, and recovery criteria |
| Execution | Owner, operating scope, next check, actual scheduling reference if registered |

Store a baseline value only with its window, sample, source, and definition version. Store thresholds in the experiment; do not change a global metric target to fit each experiment.

### When no metric is supplied

1. Read the journey's intended outcome and the experiment hypothesis.
2. Search existing metric definitions for a suitable primary measure and guardrails.
3. If none fits, propose a new metric with calculation, source/instrumentation needs, expected direction, and candidate criteria with rationale.
4. Preserve missing baselines, thresholds, or source mappings as unknown/proposed. Do not invent observed numbers or silently treat a proposal as accepted direction.
5. Resolve required choices through existing project authority; ask the owner only where a material choice is unresolved. Prototype collection and instrumentation checks can proceed independently.

The experiment can remain draft while those gaps are resolved. `ready` requires a complete protocol and a successful observation preflight; `running` requires verified intervention/exposure and collection. A protocol amendment is dated and preserved. Material mid-experiment changes normally require a new experiment or an explicit interpretation limit.

Every experiment has a measurable evaluation contract. Discovery studies can use a defined rubric or coded research result when a numerical product metric would be misleading; label that method and its limits rather than manufacturing statistical significance.

## 5. Local runtime and dashboard

Add one optional TypeScript/Node.js runtime. Its responsibilities are indexing contracts, collecting observations, validating data, evaluating experiments, and serving HTML plus a small JSON API. This is the selected language for new executable ProductOS capabilities; existing Python installation/checking tools continue working during the transition.

### Implementation language and harness portability

Owner decision, 2026-10-18: use TypeScript for the new CLI, event writer, compatibility/migration engine, MCP client, measurement collector/evaluator, and local HTTP server. Use the official DuckDB Node.js client for native database access. Keep Markdown/YAML as the portable skill and product-context format and JSON as the event/API interchange format.

Use strict TypeScript and validate external data at runtime; static types alone do not validate a repository file, journal event, MCP response, or HTTP request. Define versioned schemas once and share their runtime validation and types across CLI, server, collector and harness adapters. Emit compiled JavaScript for execution and include required templates/assets in the distributable package. Choose and pin supported Node versions and dependency versions when implementing the package; this plan does not create an npm package or claim a published command exists.

Keep the shared operations independent of a harness. Thin adapters map skill discovery, invocation, host tools and available lifecycle/command hooks for Claude Code, Codex, Cursor, OpenCode, Gemini CLI and Pi. These are target integrations, not a claim of existing tested support. Each adapter must declare which operations and automatic event-capture capabilities actually work; ordinary skill installation does not establish full command interception.

Make the skill distribution self-contained, including its bundled blank product templates, and verify discovery/installation through the open Agent Skills ecosystem, including `npx skills`. Reuse that installer where it covers discovery and placement; add ProductOS-specific installation only for required runtime setup or native hooks. Installation must preserve existing product artifacts and intentional local changes.

Retain the current Python regression suite, installer and instance checker initially. Port existing helpers only when an equivalent TypeScript implementation has demonstrated preservation and behavioural parity; the language decision does not authorize replacing captured demo data, changing product-record conventions, or weakening checks. Keep documentation-only adoption usable without installing the optional runtime.

Implement the event writer and a small shared CLI operation first, then demonstrate it through more than one harness before expanding to DuckDB/MCP. Add a capability matrix and contract fixtures for the six target adapters; run live agent trials only with actual harness access and credentials, and report unsupported or untested cases explicitly.

Proposed layout inside an adopted product repository:

```text
product/METRICS.md
product/JOURNEYS.md                 # optional resolver for existing journey artifacts
product/journeys/                   # only when the project needs native journey records
product/experiments/                # existing records, extended protocol
product/metrics/sources.yaml
product/metrics/queries/            # only for sources requiring local SQL
product/metrics/index.html          # generated dashboard shell, tracked in Git
.product-os/instance.json           # committed instance/version metadata
.product-os/events/                 # committed structured event journal
.product-os-local/metrics.duckdb     # local measurement data, ignored by Git
.product-os-local/artifacts/         # local source receipts and evaluation snapshots
```

Collection, evaluation, and artifact-change operations must emit versioned metadata into the committed journal according to the linked event requirements. Record source/window, metric and experiment IDs, producer versions, result references, and artifact hashes; do not copy raw observations or secrets into journal events.

The HTML is created from a packaged template and reads live JSON from a same-origin localhost API. The runtime opens the native DuckDB file; browser JavaScript does not open that file directly. Dashboard regeneration is needed for template changes, not every new observation. Double-clicking the HTML should show a clear instruction to start the runtime. The live view is served by the runtime; an optional standalone snapshot can be added later.

Use one owning process for native DuckDB access and serialize writes. Dashboard queries, collection requests, and evaluations all pass through that process. CLI commands use its local API when it is running; a one-shot collection can own the database while it is stopped. Reject a second writer with a useful message. This follows DuckDB's documented in-process concurrency model.

Proposed API responsibilities: list journeys/metrics/experiments, query bounded metric series, retrieve an experiment evaluation, and report source health. Collection/control endpoints are local and protected; the dashboard starts as read-only. Bind to loopback, validate origin/host for control requests, keep credentials outside HTML, and avoid arbitrary browser-supplied SQL. Self-host the dashboard assets so the local view works offline after installation.

### Dashboard views

- **Product:** core outcomes, metric trends, active experiments, and measurement gaps.
- **Journey:** intended outcome, associated measures, affected experiments, and data health.
- **Experiment:** hypothesis, expected versus observed result, baseline/comparison, sample/exposure, guardrails, uncertainty, and linked decision.
- **Sources:** last successful refresh, actual observation window, freshness/completeness, and collection errors.

Missing data is never rendered as zero. Always show collection time separately from the period measured. Separate an experiment's lifecycle from its evidence quality and result classification.

## 6. DuckDB observation model

Keep the initial schema small:

| Table | Purpose |
| --- | --- |
| `journeys`, `metric_definitions`, `journey_metrics`, `experiments`, `experiment_metrics` | Rebuildable indexes of repository contracts, with content hashes/versions |
| `collection_runs` | Source, request signature, requested and returned windows, timestamps, status, cursor and completeness |
| `metric_observations` | Metric/version, window, cohort/variant, dimensions, value, numerator/denominator/sample where applicable, source and run ID |
| `experiment_evaluations` | Protocol hash, metric/query versions, exact observation revisions or snapshot, evaluator version, result and limitations |

Record source revision or payload hash and stable logical observation keys. Retrying the same import must not double-count it. Corrected upstream aggregates create a revision; live views select the current revision while historical evaluation snapshots retain the values actually used. A database without source receipts or snapshots is not sufficient to reproduce a prior decision.

Ingest aggregates first. Add raw events only when a metric requires local computation and the required event schema, deduplication, and assignment data are available. Retain enough source lineage to explain a number without collecting unnecessary personal data.

Keep the database and receipts out of Git. Persist them on the runner's durable volume with a backup policy when the loop runs continuously. Repository definitions alone cannot restore observations from a provider whose history has expired. A recovery check must restore a database snapshot and resume without duplicate collection.

## 7. MCP collection

ProductOS's optional runtime will include an MCP client adapter. The skill remains instructions; the runtime is the program that connects. Support two routes through the same normalized ingestion boundary:

1. **Host-assisted:** the coding agent uses its existing MCP client, then submits the structured result and request provenance to the local runtime.
2. **Runtime-managed:** the collector connects directly to configured MCP servers for repeatable retrieval without an interactive agent session.

Deliver runtime-managed retrieval for one verified server in the initial MCP phase. Use an official SDK and support the transport that source requires first; add other transports when needed. MCP defines host/client/server communication, not common business metric semantics, so each source needs a tested mapping.

For each source, configure server reference, credential reference, permitted retrieval tools/resources, argument mapping, response schema, metric mapping, timezone, pagination, rate/retry limits, and freshness expectations. Discover capabilities and validate bindings before collection; do not assume a vendor exposes standard `get_metrics` tools. Freeze the tested mapping version used by each run.

Normalize responses to metric ID/version, window, cohort/variant, dimensions, units, values/components, completeness, source-computed time, and source reference. Reject ambiguous units, mismatched definitions, incomplete pagination, or missing experiment assignment information for evaluations that need it. Preserve source errors and stale results without relabelling old data as fresh. Never silently switch providers or calculate a causal lift from incomparable source populations.

The browser reads local results, not remote MCP credentials. Existing analytics/feature-flag systems remain responsible for actual exposure and allocation; ProductOS imports their evidence. A metric collector does not create randomization by labelling rows control and treatment.

## 8. Evaluation and the improvement loop

The evaluator uses the frozen experiment protocol to return: observed primary result, guardrail results, evidence quality, uncertainty, classification (`supported`, `not_supported`, `inconclusive`), and a proposed next action. Expose that same result through the API and CLI so humans and agents do not use different formulas.

Separate deterministic computation from agent judgment. The agent explains findings and proposes interventions; versioned queries and evaluators compute values and apply predeclared rules. Start with descriptive baseline/comparison results. Only claim causal or statistical conclusions when the assignment design, sample plan, and implemented evaluation support them. Missing or stale data produces an unavailable/inconclusive result, not a win or loss.

ProductOS records evidence, persists an authorized decision, updates STATE/ROADMAP where warranted, and identifies the next useful check or experiment. Continuous wake-ups require an actual runner and registered trigger. The dashboard alone does not schedule collection or execute changes.

This is the product improvement loop. A later recursive loop can treat prompts, skills, or workflow versions as interventions, associate them with an engineering journey, and measure whether they improve quality/cost/time on fixed evaluation cases. Keep a held-out evaluation and independent guardrails so changing the mechanism cannot quietly make its own test easier.

## 9. Delivery sequence and acceptance

| Phase | Changes | Acceptance evidence |
| --- | --- | --- |
| 1. Contracts | Journey references, structured metric/experiment schema, templates and checker extensions | One fictional journey with primary/guardrail metrics validates; invalid IDs, absent metrics, unresolved criteria and incompatible versions fail readiness checks |
| 2. Local vertical slice | Optional runtime, DuckDB migrations, file import, query/evaluator API, HTML generation and serving | Import fixture aggregates; dashboard and CLI return identical values; retry imports without duplicates; missing/stale data displayed correctly; second writer rejected |
| 3. MCP source | Direct client adapter for one real configured metrics source and host-assisted ingestion | Retrieve real windows, validate mappings, ingest results and exercise pagination/retry/failure behaviour with provenance |
| 4. Experiment integration | Metric proposal path, start preflight, frozen protocol, evaluations, evidence and handoff | Missing-metric request produces an explicit proposal; uninstrumented experiment cannot start; concluded experiment links reproducible evidence and a decision |
| 5. Real getintro pilot | Select one existing journey, instrument it, measure baseline, run one authorized intervention | Trace one genuine change from hypothesis to observed result and next decision; use inconclusive if traffic/evidence is insufficient |

Phases are dependency-ordered deliverables, not time estimates. The first usable release is phases 1–2; the requested MCP-enabled loop follows in phases 3–4. The real pilot closes only when evidence is available, not when a development milestone is finished.

Framework changes must update MODEL, METRICS, experiment/journey templates, onboarding, execution, operations, skill packaging, examples, changelog, and compatibility guidance together. Existing narrative definitions remain readable: migrate selected definitions explicitly, preserve IDs/history, and require structured contracts for runtime participation. Do not silently make every adopted instance install dependencies or migrate all its records.

Run the repository's required link checks, isolated-template check, and Python tests when template/installer/checker changes land. Add meaningful runtime checks for version pinning, ratio aggregation, source mapping, idempotency, freshness, missing/zero distinctions, experiment readiness, historical reproducibility, and interrupted collection. Exercise the HTML against the local API and a representative MCP source. A fixture validates mechanics; the pilot validates actual integrations and observation.

## 10. Defaults and remaining integration choices

Selected defaults: TypeScript/Node.js runtime, strict types plus runtime schema validation, thin harness adapters, one DuckDB owner, same-origin localhost dashboard, Git-owned definitions, DuckDB-owned observations, aggregate-first ingestion, one primary journey per experiment, existing lifecycle states, and agent-host MCP plus a direct collector adapter. Existing Python checks remain in use until a verified replacement exists.

The framework plan can proceed on those defaults. Before the real pilot, establish the first getintro journey, existing telemetry/experiment provider, available MCP server and tool schema, metric semantics and instrumentation, actual rollout authority, and where a continuous runner's database will persist. Those are integration facts to discover, not values the generic template should invent.

## References

- [ProductOS measurement contract](https://github.com/khangtoh/product-os/blob/main/template/product/METRICS.md)
- [ProductOS record model](https://github.com/khangtoh/product-os/blob/main/template/product/MODEL.md)
- [ProductOS experiment template](https://github.com/khangtoh/product-os/blob/main/template/product/templates/experiment.md)
- [ProductOS execution procedure](https://github.com/khangtoh/product-os/blob/main/template/product/EXECUTION.md)
- [DuckDB concurrency](https://duckdb.org/docs/current/connect/concurrency.html)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [DuckDB Node.js client](https://duckdb.org/docs/current/clients/node_neo/overview)
- [Agent Skills specification](https://agentskills.io/specification)
- [Open skills installer](https://github.com/vercel-labs/skills)
