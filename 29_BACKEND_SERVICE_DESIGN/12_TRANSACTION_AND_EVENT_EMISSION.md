# 12_TRANSACTION_AND_EVENT_EMISSION.md

# Bizzi Platform

## Transaction and Event Emission

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 10_AUDIT_AND_EVENT_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 07_MEMORY_AUDIT_EVENT_API.md, 10_ERROR_AND_VALIDATION_CONTRACTS.md  
**Previous Document:** 11_AUTHORIZATION_VALIDATION_SERVICES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend transaction and event emission design for Bizzi Platform.

It specifies how backend services should coordinate state changes, audit event creation, runtime event emission, idempotency, rollback behavior and background job coordination so that business operations remain consistent, traceable and AI-safe.

Core question:

```text
How should Bizzi backend services wrap mutations in transactions and emit audit/runtime events without losing business consistency or traceability?
```

---

# 2. Scope

This design covers:

```text
TransactionManager
UnitOfWork pattern
AuditService emission inside mutations
RuntimeEventService emission inside mutations
Outbox pattern option
Idempotency handling
Rollback behavior
Background job handoff
Correlation and causation propagation
Event processing status
Failure handling and retry design
```

This document applies to all state-changing backend services in `29_BACKEND_SERVICE_DESIGN`.

---

# 3. Design Principles

Transaction and event emission follows:

```text
business operation atomicity
audit evidence consistency
runtime coordination reliability
correlation propagation
idempotency for retryable mutations
no silent side effects
no business state without audit evidence
runtime events do not replace audit events
safe failure behavior
MVP simplicity with outbox expansion path
```

Rule:

```text
A meaningful state change should either complete with its required audit/runtime evidence or fail safely.
```

---

# 4. TransactionManager Responsibilities

TransactionManager is responsible for controlled transaction boundaries.

Responsibilities:

```text
begin transaction
provide transaction context to repositories
commit transaction
rollback transaction on failure
support nested or joined transactions according to implementation choice
ensure repositories use the same transaction context during one operation
```

Recommended service pattern:

```text
TransactionManager.runInTransaction(context, operation)
```

Rule:

```text
Feature services should not manually coordinate unrelated partial commits for one business operation.
```

---

# 5. Unit of Work Pattern

A unit of work represents one coherent business operation.

Examples:

```text
create workspace
create task
complete task
confirm decision
activate memory
create integration
trigger integration sync
request export
apply agent recommendation
```

A unit of work may include:

```text
primary record mutation
related record mutation
audit event creation
runtime event creation
idempotency record update
```

Rule:

```text
Each unit of work should have one correlation_id and clear result object references.
```

---

# 6. Canonical Mutation Transaction Flow

Canonical flow:

```text
validate input
check authorization
load existing state
validate business rules
capture before_state when needed
begin transaction
write primary state change
write related state changes
write audit event
write runtime event or outbox record
write idempotency result when applicable
commit transaction
return response DTO
```

Failure flow:

```text
validation or authorization failure before transaction when possible
transaction rollback on write failure
structured service error returned
no partial business state committed
```

---

# 7. Audit Event Emission Rules

Audit events provide business evidence.

Audit event should be emitted for:

```text
workspace creation/update/archive
settings changes
access grant/revoke
operating map confirmation/archive
function creation/update/archive
responsibility assignment/reassignment/archive
task creation/update/status change/archive
decision creation/confirmation/archive
memory creation/update/activation/archive
integration creation/update/revocation/sync request
security policy changes
export request/cancel/download link creation
AI recommendation application
```

Rule:

```text
If a change matters to business accountability, create an audit event in the same unit of work.
```

---

# 8. Audit Event Payload Pattern

Canonical audit input:

```text
workspace_id
actor_type
actor_id
agent_id optional
action
object_type
object_id
source_event_id optional
before_state optional
after_state optional
ai_assisted
human_confirmed
severity
correlation_id
metadata optional
```

Rules:

```text
before_state and after_state should be sanitized
raw secrets must not appear in audit payloads
audit action names must be canonical
audit object reference must point to the business object changed
```

---

# 9. Runtime Event Emission Rules

Runtime events coordinate platform behavior.

Runtime events should be emitted for:

```text
dashboard refresh requests
memory candidate creation
integration sync requests
export generation requests
access cache invalidation later
notification triggers later
background job coordination
```

Rule:

```text
Runtime events are coordination signals and must not be treated as legal or business audit evidence.
```

---

# 10. Runtime Event Payload Pattern

Canonical runtime event input:

```text
workspace_id
event_type
status
source_object_type
source_object_id
actor_type
actor_id
agent_id optional
payload optional
correlation_id
causation_id optional
timestamp
```

Rules:

```text
payload should be minimal and sanitized
raw secrets must not appear in runtime payloads
source object must belong to workspace when workspace-scoped
correlation_id must connect request, audit event and runtime event
causation_id should link chained events where useful
```

---

# 11. Inline Event Write Pattern

MVP pattern:

```text
begin transaction
write primary state
write audit event
write runtime event with pending or processed status
commit transaction
```

Advantages:

```text
simple implementation
strong consistency between state and event records
sufficient for MVP
```

Limitations:

```text
runtime event dispatch is not guaranteed unless processed separately
long-running handlers should not run inside the transaction
```

MVP recommendation:

```text
Use inline persisted runtime events, then process them after commit or through a simple background worker.
```

---

# 12. Outbox Pattern Expansion

Future expansion may use an outbox pattern.

Flow:

```text
begin transaction
write business state
write audit event
write outbox event record
commit transaction
background dispatcher reads outbox
publishes or handles event
marks outbox processed
```

Advantages:

```text
reliable event dispatch
decoupled background processing
retry support
better observability
```

Rule:

```text
Outbox records should be created in the same transaction as the business state change.
```

---

# 13. Background Job Handoff

Long-running work should happen after commit.

Examples:

```text
export generation
integration sync execution
AI analysis
dashboard metric recomputation
large report generation
```

Recommended pattern:

```text
service creates job record in transaction
service emits runtime event or outbox record
transaction commits
job worker picks up job
worker updates job status
worker emits completion or failure event
```

Rule:

```text
Do not perform slow external provider calls inside core business transaction boundaries.
```

---

# 14. Idempotency Pattern

Idempotency protects retryable mutations.

Candidate operations:

```text
operating map generation
integration sync trigger
export job creation
AI recommendation application
```

Flow:

```text
validate idempotency key
compute request fingerprint
check existing idempotency record
if completed same fingerprint, return stored result
if same key different fingerprint, return idempotency_conflict
execute transaction
store result reference
```

Rule:

```text
Idempotency must prevent duplicate business effects without silently accepting changed payloads.
```

---

# 15. Correlation and Causation

Every important operation should carry:

```text
correlation_id
request_id
causation_id optional
```

Correlation connects:

```text
API request
service operation
audit event
runtime event
background job
logs
provider calls
```

Causation connects:

```text
runtime event that caused another runtime event
job that caused a completion event
AI recommendation that caused a task creation
```

Rule:

```text
No important backend operation should be untraceable.
```

---

# 16. Rollback Rules

Rollback should occur when:

```text
primary state write fails
audit event write fails for required audit operation
runtime event write fails when required for coordination
idempotency write fails for idempotent operation
business rule validation fails inside transaction
```

Rules:

```text
validation and authorization should run before transaction when possible
required audit failure should fail the business operation
non-critical optional runtime event failure may be handled according to policy
```

MVP rule:

```text
Required runtime event writes for core coordination should rollback the mutation if they fail.
```

---

# 17. Event Processing Status

Runtime events may use statuses:

```text
pending
processing
processed
failed
ignored
```

Status transitions:

```text
pending → processing → processed
pending → processing → failed
failed → processing → processed later
pending → ignored when event no longer relevant
```

Rule:

```text
Runtime event status changes are operational records and should not replace audit evidence.
```

---

# 18. Failure Handling and Retry

Runtime event failure should preserve:

```text
runtime_event_id
handler name
failure reason sanitized
attempt count
last_attempt_at
next_retry_at optional
correlation_id
```

Retryable failures may include:

```text
temporary provider outage
temporary file storage outage
job queue unavailable
transient database lock
```

Non-retryable failures may include:

```text
invalid payload schema
revoked integration
expired export job
missing required object
authorization policy changed
```

---

# 19. Transaction Boundary Examples

## Complete Task

```text
begin transaction
update task status to completed
record task.completed audit event
emit task.completed runtime event
emit dashboard.refresh_requested runtime event
commit transaction
```

## Confirm Decision

```text
begin transaction
update decision status to confirmed
record decision.confirmed audit event
emit decision.confirmed runtime event
emit memory.candidate_created optional runtime event
commit transaction
```

## Request Export

```text
begin transaction
create export_job queued
record export.requested audit event
emit export.requested runtime event
emit export.queued runtime event
commit transaction
enqueue export generation
```

## Trigger Integration Sync

```text
begin transaction
create integration_sync_job queued
record integration.sync_requested audit event
emit integration.sync_requested runtime event
emit integration.sync_queued runtime event
commit transaction
enqueue sync execution
```

---

# 20. Cross-Service Coordination

Feature services may call other services inside a unit of work when one operation creates related records.

Examples:

```text
apply recommendation creates task
resolve operating gap creates responsibility
confirm decision creates memory candidate event
archive responsibility creates ownership gap
```

Rules:

```text
only one service should own the primary business operation
called services must share transaction context when part of same unit of work
avoid circular service dependencies
result_object_type and result_object_id must be recorded when AI/recommendation causes official state
```

---

# 21. AI-Assisted Transaction Rules

AI-assisted operations must preserve:

```text
agent_id
ai_assisted flag
human_confirmed flag
authority decision
source recommendation or draft reference
result object reference
correlation_id
```

Rules:

```text
AI draft or recommendation is not official state until applied transactionally
human confirmation must be recorded for sensitive actions
agent authority must be checked before mutation
AI-generated memory must be activated before active context use
```

---

# 22. Secret Safety Rules

Transactions and events must not persist raw secrets.

Forbidden in business records, audit events, runtime events and logs:

```text
access_token
refresh_token
api_key
client_secret
password
private_key
raw credential payload
signed download URL values where avoidable
```

Allowed:

```text
credential_ref
provider
scope names
status
revoked_at
last_sync_at
```

---

# 23. Audit vs Runtime Event Decision Table

| Change | Audit Event | Runtime Event |
|---|---|---|
| Business state changed | Required | Usually required |
| Dashboard refresh needed | Optional | Required |
| Background job requested | Required for user action | Required |
| Internal retry occurred | Optional | Required operationally |
| Read-only normal list request | Not required | Not required |
| Sensitive download link created | Required | Optional |
| Forbidden security action | Sometimes required | Optional |
| AI recommendation applied | Required | Required |

---

# 24. Service Implementation Rules

Feature services should:

```text
build one service context per request
validate before transaction when possible
capture before_state before mutation
use TransactionManager for mutations
use AuditService for audit events
use RuntimeEventService for runtime events
return DTO after commit
map failures to canonical errors
```

Feature services should not:

```text
write audit_events manually with inconsistent schema
emit runtime events without correlation_id
call external providers inside transaction
store raw secrets in payloads
commit state before required audit evidence
```

---

# 25. MVP Simplifications

MVP may simplify by:

```text
single database transaction per mutation
inline audit event writes
inline runtime event writes
simple background worker polling runtime events
limited idempotency for export and integration sync
simple retry strategy
no distributed transactions
no external message broker
```

MVP must preserve:

```text
state + audit consistency
workspace scope
correlation_id propagation
runtime event records for coordination
safe rollback behavior
secret exclusion
authority and confirmation traceability for AI effects
```

---

# 26. Future Expansion

Future expansion may add:

```text
outbox dispatcher
event handler registry
event handler run records
event failure records
advanced retry scheduling
dead-letter queues
message broker integration
saga orchestration for multi-step workflows
distributed tracing
transactional idempotency table
operation logs
```

---

# 27. Testing Expectations

Transaction tests should cover:

```text
primary state and audit event commit together
failure in audit write rolls back mutation
failure in required runtime event write rolls back mutation
validation failure does not write partial state
idempotent retry returns same result
idempotency conflict rejects changed payload
AI recommendation application records result object
external provider call is not executed inside transaction
```

Event tests should cover:

```text
runtime event includes correlation_id
runtime event includes source object
payload is sanitized
secret values are excluded
event status transitions work
failed event can be retried
processed event is not processed twice by same handler
```

---

# 28. Acceptance Criteria

Transaction and Event Emission is accepted when:

- TransactionManager responsibilities are defined;
- Unit of Work pattern is documented;
- canonical mutation transaction flow is defined;
- audit event emission rules are defined;
- runtime event emission rules are defined;
- inline event write and outbox patterns are documented;
- background job handoff is defined;
- idempotency behavior is documented;
- correlation and causation propagation is defined;
- rollback, failure and retry rules are documented;
- AI-assisted transaction rules are defined;
- secret safety rules are documented;
- MVP simplifications and testing expectations are documented.

Status:

```text
Accepted for Backend Service Milestone
```

---

# 29. Final Statement

```text
Bizzi Transaction and Event Emission defines how backend services commit business state, audit evidence and runtime coordination signals as coherent, traceable and AI-safe units of work.
```

This service layer ensures that Bizzi operations are not only performed, but also explainable, recoverable and governable.