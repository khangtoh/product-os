# Operating context

Updated: unknown — set when adopted or changed.

Record the actual app and loop capabilities here. The template supplies no integrations, access, credentials, permissions, or claims about production state.

## Capabilities

| Capability | System / reference | Status | Owner / next action |
| --- | --- | --- | --- |
| App code and verification commands | Unknown | Unknown | Establish from project context |
| Environments and release workflow | Unknown | Unknown | Link actual systems |
| User feedback and observation sources | Unknown | Unknown | Verify available sources |
| Product metrics and queries | Unknown | Unknown | Define from the selected outcome |
| Quality evaluations, including AI where applicable | Unknown | Unknown | Link verified methods |
| Reliability and operating-cost signals | Unknown | Unknown | Establish definitions and limits |
| Runner, triggers, and logs | Unknown | Unknown | Record actual capability |
| Coordination, retries, and recovery | Unknown | Unknown | Verify before dependent actions |

## Authority

No authority is inherited from this template. Record existing project/session authorization with its source; carry it forward rather than asking again each cycle. Written records cannot expand runtime tool permissions.

| Actor / role | Allowed action and environment | Limits / expiry | Source | Stop / revocation condition |
| --- | --- | --- | --- | --- |

Unknown scope blocks only the action requiring it. Continue other authorized work. Keep credentials outside this folder and store references only.

## Runbooks and incidents

Create `runbooks/` and `incidents/` with their first real record, using the [runbook](../templates/runbook.md) and [incident](../templates/incident.md) templates.

Runbooks need observable triggers, actual authority, verified steps, failure handling, recovery, and final-state checks. Keep unverified procedures in draft. Incidents preserve impact, timeline, recovery evidence, uncertainty, and prevention follow-up.

## Runner handoff

When available, record runner identity, invocation, event/schedule source, logs, access references, and last successful cycle. Record external action IDs and idempotency keys where relevant. Use real coordination for overlapping work or serialize mutations.

A next-check field is not proof of scheduling. Verify registration, actual execution, persisted results, and recovery after interruption before claiming a continuous autonomous loop is running.
