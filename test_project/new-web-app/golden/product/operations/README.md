# Operating context

Updated: 2026-09-27 — established during ProductOS adoption, interview round 3.

The owner stated on 2026-09-27 that **production health and analytics have not been inspected**. Nothing below claims a verified production state. Entries marked *not inspected* are genuinely unchecked, not assumed absent.

## Capabilities

| Capability | System / reference | Status | Owner / next action |
| --- | --- | --- | --- |
| App code and verification commands | `src/index.html`, `src/store.js`, `src/search.js` | Available. No build step, no test suite. Project instruction is to verify by opening `src/index.html` in a browser ([AGENTS.md](../../AGENTS.md)). | Manual browser check is the only verification method today. |
| Environments and release workflow | None found in the repository. | No server, no deployment pipeline, no hosting configuration. The app is a local file. | Whether to host is an open decision ([REQUIREMENTS.md](../REQUIREMENTS.md#open-decisions)). |
| Production health | Not inspected. | Unknown. The owner has not inspected it, and no environment is known to exist. | Establish whether any deployed instance exists before treating health as a signal. |
| User feedback and observation sources | None established. | No feedback channel, no users known to be using it. | Depends on the evaluation method, still unanswered. |
| Product metrics and queries | None. [METRICS.md](../METRICS.md) is not populated. | No measurement exists. Analytics are forbidden by project instruction, so no instrumentation is available. | Choose an evaluation approach that respects the no-telemetry constraint. Unanswered. |
| Analytics | Not inspected, and forbidden. | The owner has not inspected analytics; the project also prohibits analytics, telemetry, and third-party scripts. | Treat measurement as a design problem, not an integration task. |
| Quality evaluations | None. | No tests, no accessibility audit, no performance baseline. | R5 (keyboard) and R6 (labels) need a manual check; the speed target is deferred to the owner. |
| Reliability and operating-cost signals | None applicable. | No server and no third-party service, so no operating cost or uptime signal exists. | Revisit if hosting is adopted. |
| Runner, triggers, and logs | None. | ProductOS installs no runner and none is configured here. | A next-review trigger in [STATE.md](../STATE.md) is a resume condition, not a registered schedule. |
| Coordination, retries, and recovery | Not applicable yet. | Single actor, single working copy, no external mutations. Note the project is **not a git repository**, so there is no version history to recover from. | Serialize edits. Consider version control before substantial change. |

## Authority

No authority is inherited from the ProductOS files. These documents cannot expand runtime tool permissions.

| Actor / role | Allowed action and environment | Limits / expiry | Source | Stop / revocation condition |
| --- | --- | --- | --- | --- |
| Product owner | Sets product direction; owns the deferred speed-target follow-up | None stated | Owner statements during onboarding, 2026-09-27 | Owner's own change of direction |
| Agent in this session | Read the project; write ProductOS documents under `product/` and the root `PRODUCT.md` | Setup only. No code changes were authorized by `init`. Shell `cp` and shell-expansion commands were denied in this session and could not be approved. | This onboarding session's scope | Execution requires a separate `run` request |

**Release gate, owner-stated:** verify that each user's collection stays private before exposing any change (R7 in [REQUIREMENTS.md](../REQUIREMENTS.md#quality-requirements-and-constraints)).

Unknown scope blocks only the action requiring it. Continue other authorized work. Keep credentials outside this folder and store references only.

## Runbooks and incidents

No runbooks or incidents exist. Create `runbooks/` and `incidents/` with their first real record, using the [runbook](../templates/runbook.md) and [incident](../templates/incident.md) templates.

Runbooks need observable triggers, actual authority, verified steps, failure handling, recovery, and final-state checks. Keep unverified procedures in draft. Incidents preserve impact, timeline, recovery evidence, uncertainty, and prevention follow-up.

## Runner handoff

No runner exists. Nothing is scheduled, and no wake-up has been registered.

A next-check field is not proof of scheduling. Verify registration, actual execution, persisted results, and recovery after interruption before claiming a continuous autonomous loop is running.
