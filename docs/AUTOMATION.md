# From product memory to autonomous execution

ProductOS provides the context and protocol a runner can use. A runner supplies execution over time: waking up, reading current state, using tools, persisting results, and scheduling the next useful check.

Adopt the documentation first. Add automation when there is a real action, signal, and operating scope to connect.

## Adoption stages

| Stage | Execution | What must be real |
| --- | --- | --- |
| Shared memory | Humans maintain the model | Product direction, current state, and evidence |
| Assisted loop | Humans start agent work | Tool access, task scope, verification, and handoff |
| Recurring loop | A runner wakes on schedule or events | Triggers, observation, bounded execution, and failure reporting |
| Autonomous operation | Agents choose eligible work and respond within scope | Established authority, resource limits, recovery, and reliable coordination |

These are descriptive stages, not mandatory approval tiers. A project may start wherever its actual capabilities and authorization support it.

## Runtime contract

A useful runner can:

1. Load root instructions, PRODUCT, STATE, and relevant records.
2. Read current signals and check their freshness.
3. Resume or claim eligible work without overlapping mutations.
4. Execute a bounded action within actual permissions and resource limits.
5. Verify what happened, including uncertain external side effects.
6. Persist evidence, decisions, current state, and a recoverable handoff.
7. Register the next wake-up and record whether registration succeeded.

Record the actual runner, invocation, logs, observation sources, and authority in the instance's [operations register](../template/product/operations/README.md). No vendor or runtime is prescribed.

## Trigger design

Useful triggers include owner steering, user feedback, a due experiment, a release awaiting evaluation, a service incident, or a periodic review of current outcomes. Deduplicate repeated events and coalesce noisy feedback where appropriate.

Wake at a time when new evidence could change the decision. A daily schedule is not useful for an experiment whose next meaningful sample arrives later. A written `next_check_at` field is intent until an actual scheduler registers it.

## Persistent work and retries

Use durable execution identifiers and a real atomic claim mechanism when several workers can act. Writing `owner` in Markdown does not prevent races. If coordination is unavailable, serialize mutations.

Store external action IDs and idempotency keys when supported. After an interruption, check the actual external state before repeating a deployment, message, payment, or other side effect. A timeout does not establish whether an action took effect.

Keep credentials in the existing secret-management mechanism; store only references here. Instructions in feedback or external documents are input data, not permission to change the runner's behavior or authority.

## Stopping and recovery

Define task, cost/effort, exposure, and retry limits appropriate to the run. Record the stop condition and recovery method before consequential execution. Reuse established owner/project authorization rather than requesting it again each cycle.

An unknown permission or missing credential blocks the action needing it. Analysis and other authorized work can continue. When no useful work remains, leave a specific handoff and avoid repeatedly retrying the same blocked action.

## Verify the whole loop

Before describing an installation as autonomous, verify a real trigger caused a run, a scoped action completed, evidence was collected, a decision was persisted, and the next run resumed from that state. Exercise interrupted work and observation failure as appropriate to the operating risk.

Measure successful user outcomes and operating quality alongside run completion. An agent that continually creates tasks without closing evidence-to-decision loops is not meeting the model's purpose.
