# 01_BACKEND_ARCHITECTURE_PRINCIPLES.md

# Bizzi Platform

## Backend Architecture Principles

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Previous Document:** 00_BACKEND_SERVICE_DESIGN_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend architecture principles for Bizzi Platform.

It establishes the rules that backend services, controllers, repositories, validators, authorization policies, audit emitters and runtime event emitters must follow when implementing Bizzi API contracts.

Core question:

```text
Which backend architecture principles should guide every Bizzi service so that the platform remains secure, workspace-scoped, auditable, transactional and AI-safe?
```

---

# 2. Architecture Principles Role

Backend architecture principles ensure that implementation does not drift from the canonical architecture.

They provide consistency for:

- module design;
- controller/service/repository separation;
- workspace isolation;
- authorization enforcement;
- validation strategy;
- transaction handling;
- audit event creation;
- runtime event creation;
- AI authority enforcement;
- integration secret safety;
- dashboard and export coordination;
- future backend implementation.

---

# 3. Principle B01 — Workspace Context First

Every operating backend action must execute inside a workspace context.

Rule:

```text
No workspace context, no operating service action.
```

Required service inputs should include or derive:

```text
workspace_id
authenticated_actor
correlation_id
request_context
```

Backend services must never trust workspace ownership from request body alone.

---

# 4. Principle B02 — Controllers Route, Services Decide

Controllers should be thin.

Controller responsibilities:

```text
parse request
extract path parameters
extract authenticated actor
call application service
map result to response
map errors to API error contract
```

Controllers must not:

```text
perform direct database writes
contain lifecycle transition logic
bypass authorization
emit inconsistent audit events
apply AI actions directly
```

Rule:

```text
Business behavior belongs in services, not controllers.
```

---

# 5. Principle B03 — Services Own Business Behavior

Application services own the meaning of backend operations.

Services should:

```text
validate workspace state
check authorization
enforce business rules
coordinate repositories
open transaction boundaries
create audit events
create runtime events
return stable service DTOs
```

Rule:

```text
If an operation changes business meaning, an application service must own it.
```

---

# 6. Principle B04 — Repositories Encapsulate Persistence

Repositories should own database access details.

Repository responsibilities:

```text
load records by id and workspace_id
apply workspace filters
persist records
support list queries
support pagination
support controlled filtering and sorting
hide SQL or ORM details from services
```

Repositories should not:

```text
decide business authorization
apply AI confirmation rules
emit audit events
own lifecycle transitions
```

Rule:

```text
Repositories answer data questions. Services answer business questions.
```

---

# 7. Principle B05 — Authorization Is Server-Side

Authorization must be enforced by backend services or dedicated authorization middleware.

Rules:

```text
frontend authorization is advisory only
API clients cannot be trusted
workspace access must be checked server-side
role and authority checks must happen before mutation
```

Authorization sources may include:

```text
workspace owner
workspace_access
roles
permissions
resource ownership
agent authority scopes
integration scopes
export scopes
```

---

# 8. Principle B06 — Validation Is Layered

Validation should occur in layers.

Recommended sequence:

```text
API schema validation
↓
service business validation
↓
repository reference validation
↓
database constraints
```

Validation categories:

```text
required fields
field format
allowed values
workspace membership
object ownership
status transition
business rule
AI confirmation
agent authority
integration credential reference
export scope
```

Rule:

```text
Database constraints are the last safety net, not the only validation layer.
```

---

# 9. Principle B07 — Transactions Protect Business Meaning

Important mutations should execute in explicit transaction boundaries.

Examples:

```text
create task + audit event + runtime event
confirm decision + audit event + memory candidate event
apply recommendation + result object + audit event + runtime event
request export + export job + runtime event
```

Rule:

```text
A business operation should either complete coherently or fail safely.
```

---

# 10. Principle B08 — Audit Is a First-Class Backend Concern

Important business changes must emit audit events.

Audit event creation should capture:

```text
workspace_id
actor_type
actor_id
agent_id where applicable
action
object_type
object_id
before_state where useful
after_state where useful
ai_assisted
human_confirmed
correlation_id
```

Rule:

```text
Audit evidence must be created consistently and cannot be optional for meaningful state changes.
```

---

# 11. Principle B09 — Runtime Events Coordinate, Not Prove

Runtime events coordinate internal behavior.

They may trigger:

```text
dashboard refresh
memory candidate creation
export generation
integration sync
notifications later
observability later
```

Rule:

```text
Runtime events are not substitutes for audit events.
```

---

# 12. Principle B10 — AI Effects Require Governance

AI-generated output must pass backend governance before becoming official business state.

Backend must enforce:

```text
agent authority
human confirmation
security policy
result object validation
audit traceability
source object traceability
```

Rule:

```text
AI can recommend or draft. Backend services decide whether an AI effect becomes official state.
```

---

# 13. Principle B11 — Secrets Are Never Normal Data

Integration credentials and secrets must not enter normal DTOs, logs, audit payloads or API responses.

Allowed:

```text
credential_ref
provider
scopes
status
revoked_at
last_sync_at
```

Not allowed:

```text
access_token
refresh_token
api_key
client_secret
password
private_key
raw credential payload
```

Rule:

```text
Backend services resolve secrets only inside secure execution boundaries.
```

---

# 14. Principle B12 — Error Mapping Must Be Predictable

Service errors must map to API error contracts.

Examples:

```text
ValidationError → validation_error
AuthorizationError → forbidden
NotFoundError → not_found
WorkspaceArchivedError → workspace_archived
InvalidStatusTransition → invalid_status_transition
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
```

Rule:

```text
Backend services must not leak raw database, stack trace or provider errors to API clients.
```

---

# 15. Principle B13 — Idempotency for Retryable Mutations

Some operations should support idempotency.

Candidates:

```text
operating map generation
integration sync trigger
export job creation
AI recommendation application
```

Rule:

```text
Retryable mutations should avoid duplicate business effects.
```

---

# 16. Principle B14 — Background Work Is Explicit

Long-running or external operations should be represented as jobs or events.

Examples:

```text
export generation
integration sync
operating map generation when expensive
AI analysis
metric refresh
```

Rule:

```text
Backend services should not hide long-running work behind unclear synchronous calls.
```

---

# 17. Principle B15 — Read Models May Be Optimized, Write Models Must Be Governed

Dashboard, activity and search views may use optimized read paths.

However, official state changes must use governed service flows.

Rule:

```text
Read optimization must not bypass write governance.
```

---

# 18. Principle B16 — MVP Simplicity With Enterprise Path

MVP backend may simplify:

```text
owner-only authorization
simple service modules
simple repository patterns
simple runtime event processing
basic dashboard computation
basic export job handling
```

But it must preserve:

```text
workspace isolation
auditability
AI confirmation
secret safety
transaction consistency
error consistency
```

---

# 19. Principle B17 — Contracts Are Canonical

Backend implementation must follow `28_API_CONTRACTS`.

Rule:

```text
If backend behavior diverges from API contracts, update the contract intentionally or fix the implementation.
```

---

# 20. Principle B18 — Observability Starts With Correlation

Every request and mutation should carry a correlation identifier.

Correlation should connect:

```text
API request
service operation
audit event
runtime event
logs
background job
provider call
```

Rule:

```text
No important backend operation should be untraceable.
```

---

# 21. Principle B19 — Safe Deletion and Archival

Backend services should prefer archive, revoke, cancel or expire for important business records.

Hard delete is reserved for:

```text
temporary data
test data
expired sessions
expired export files
unconfirmed accidental records
```

Rule:

```text
Confirmed business state should not be hard-deleted through normal service flows.
```

---

# 22. Principle B20 — Backend Must Be Testable

Service design should support testing.

Required test targets:

```text
service business rules
authorization decisions
validation failures
transaction consistency
audit event emission
runtime event emission
AI confirmation enforcement
repository workspace scoping
error mapping
```

Rule:

```text
If a service rule cannot be tested, it is not sufficiently designed.
```

---

# 23. Architecture Anti-Patterns

Avoid:

```text
fat controllers
cross-workspace queries without workspace filters
business rules hidden in frontend
business rules hidden in SQL only
raw secret values in DTOs
AI actions applied without backend confirmation
state changes without audit events
runtime events used as audit substitute
unbounded list queries
inconsistent error mapping
direct repository calls from unrelated modules without service boundary
```

---

# 24. MVP Backend Principle Set

Minimum MVP backend principles that must not be compromised:

```text
Workspace Context First
Controllers Route, Services Decide
Repositories Encapsulate Persistence
Authorization Is Server-Side
Validation Is Layered
Audit Is First-Class
AI Effects Require Governance
Secrets Are Never Normal Data
Error Mapping Must Be Predictable
Contracts Are Canonical
```

---

# 25. Acceptance Criteria

Backend Architecture Principles are accepted when:

- workspace-first backend rule is defined;
- controller, service and repository separation is defined;
- authorization and validation principles are documented;
- transaction and audit principles are documented;
- runtime event coordination is defined;
- AI governance is enforced server-side;
- integration secret safety is documented;
- error mapping expectations are defined;
- MVP simplifications are bounded;
- anti-patterns are identified.

Status:

```text
Accepted for Backend Module Catalog
```

---

# 26. Final Statement

```text
Bizzi Backend Architecture Principles define the rules that keep backend services workspace-scoped, secure, transactional, auditable, AI-safe, implementation-ready and aligned with API contracts.
```

These principles govern all remaining documents in the `29_BACKEND_SERVICE_DESIGN` layer.