# Operating context

Updated: 2026-09-27.

Actual app and loop capabilities for PocketGarden, established during onboarding. Where a row says unknown, it has not been verified — it is not a claim that the capability is absent in principle, nor that things are healthy.

## Capabilities

| Capability | System / reference | Status | Owner / next action |
| --- | --- | --- | --- |
| App code and verification commands | `src/index.html`, `src/store.js`, `src/search.js` | Available. Verification is manual only: open `src/index.html` in a browser (root `AGENTS.md`). No tests, no build, no lint, no package scripts. | Unassigned. A verification step for FR-4 and QR-1/QR-2 would have to be a manual browser check. |
| Environments and release workflow | None | No hosting, no deployment pipeline, no staging. The product runs from a local file. | Unassigned. "Exposing a change" currently has no defined mechanism; QR-3's privacy verification gate applies whenever one is created. |
| User feedback and observation sources | Direct observation sessions, being arranged | No users have been observed yet and no feedback channel exists. Production health has not been inspected (owner, 2026-09-27). | Product owner: arranging the first observation session for [Outcome-01](../outcomes/Outcome-01_retrieve_an_old_article.md). Recruitment is the owner's, not the agent's; the agent has no channel to researchers. |
| Product metrics and queries | None | No instrumentation. Analytics, telemetry, and third-party scripts are forbidden by root `AGENTS.md`. [METRICS.md](../METRICS.md) defines no metric. | Unassigned. Evaluation must be direct observation, not telemetry. |
| Quality evaluations, including AI where applicable | None | Not applicable for AI: the product contains no AI behavior. No accessibility or functional evaluation has been run. | Unassigned. QR-1 keyboard operability is unverified and needs a manual check. |
| Reliability and operating-cost signals | None | No signals exist and no service is run, so there is no operating cost. | Unassigned. |
| Runner, triggers, and logs | None | No runner ships with ProductOS and none is configured here. No schedule is registered. | Unassigned. |
| Coordination, retries, and recovery | Not established | Single repository, no concurrent actors recorded. A Markdown owner field is not a lock. | Serialize mutations to this folder. |

## Authority

No authority is inherited from documentation. Recorded from the actual session in which this instance was adopted.

| Actor / role | Allowed action and environment | Limits / expiry | Source | Stop / revocation condition |
| --- | --- | --- | --- | --- |
| Claude Code agent, onboarding session 2026-09-27 | Read the repository; create and edit files in the working tree | No approval surface in that session, so any tool call needing permission is denied automatically. `cp` was denied on this basis. No git operations were run — the directory is not a git repository. | The session itself | Session end; a later session's permissions must be re-established, not assumed from this row |
| Product owner | Sets product direction and operating scope; owns [Outcome-01](../outcomes/Outcome-01_retrieve_an_old_article.md) and arranges observation sessions | None recorded | Self-identified during onboarding, 2026-09-27 | n/a |

Observation sessions expose a participant's own saved collection to whoever is observing. QR-3 privacy applies to the session, not only to the software: do not copy participant collections into this repository.

Unknown scope blocks only the action requiring it. Continue other authorized work. Keep credentials outside this folder and store references only.

## Runbooks and incidents

No runbooks and no incidents. Create `runbooks/` and `incidents/` with their first real record, using the [runbook](../templates/runbook.md) and [incident](../templates/incident.md) templates.

Runbooks need observable triggers, actual authority, verified steps, failure handling, recovery, and final-state checks. Keep unverified procedures in draft. Incidents preserve impact, timeline, recovery evidence, uncertainty, and prevention follow-up.

## Runner handoff

No runner exists, so there is no runner identity, invocation, schedule source, or log location to record, and no cycle has ever run. Nothing in this instance is scheduled or autonomous; work happens when a person or agent starts a session.

A next-check field is not proof of scheduling. Verify registration, actual execution, persisted results, and recovery after interruption before claiming a continuous autonomous loop is running.
