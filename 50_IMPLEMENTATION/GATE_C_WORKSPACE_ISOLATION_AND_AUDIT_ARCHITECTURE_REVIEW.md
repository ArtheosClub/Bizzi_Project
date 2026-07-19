# Gate C Workspace Isolation and Audit Architecture Review

Version: 1.0  
Status: Architecture Review — Planning Only  
Implementation Track: 50_IMPLEMENTATION  
Scope: Gate C / WP13–WP22  
Decision Type: Pre-Implementation Blocking Review

Related Documents:
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
- `50_IMPLEMENTATION/GATE_C_AGENT_CONTEXT_AND_HUMAN_INTERACTION_PLAN.md`
- `docs/planning/PRE-CODING-BRIEF.md`
- `docs/c4/C3_COMPONENT.md`
- ADR-0004 — Workspace Isolation
- ADR-0005 — Audit and Event Integrity
- ADR-0006 — Authorization

---

## 00. Executive Summary

This document reviews the Gate C architecture before any Gate C models, repositories, migrations, or APIs are implemented.

The review addresses three critical gaps identified during inspection of PR #2:

1. `workspace_id` was documented as required, but no complete index strategy was defined;
2. `WorkspaceMembership` did not explicitly require uniqueness on `(workspace_id, user_id)`;
3. `AuditRecord.workspace_id` was described as repository-derived, but the required repository invariant and mutation contract were not specified.

Core conclusion:

```text
Workspace isolation must be enforced by schema, repository contracts,
authorization context, audit propagation, and tests together.
Documentation alone is not an isolation boundary.
```

No code is authorized by this document. It defines the architecture and acceptance conditions that must be approved before Gate C implementation begins.

---

# 01. Architecture Review

## 01.1 Current Intended Model

The current Gate C plan assumes:

- business entities are workspace-scoped;
- a human user may belong to multiple workspaces;
- membership is represented through `WorkspaceMembership`;
- repositories receive a trusted workspace context;
- `AuditRecord.workspace_id` is derived at the repository/audit boundary;
- services must not freely assign audit workspace identity.

These principles are directionally correct.

The missing element is an explicit, testable contract connecting:

```text
Database Schema
→ ActorContext
→ Authorization
→ Repository Query
→ Domain Mutation
→ AuditRecord
→ Integration Test
```

## 01.2 Primary Architectural Risks

| Risk | Severity | Description |
|---|---:|---|
| Missing workspace indexes | High | Workspace-filtered queries degrade as data grows |
| Duplicate memberships | Critical | A user can acquire conflicting duplicate roles in one workspace |
| Caller-controlled audit workspace | Critical | Audit records can be written into the wrong workspace |
| Repository methods without workspace input | Critical | Cross-workspace data access becomes possible |
| Global primary-key lookup | Critical | `get_by_id(id)` may return an object from another workspace |
| Incomplete composite indexes | High | Index on `workspace_id` alone may not support actual query patterns |
| Missing foreign-key workspace consistency | High | Related records may reference objects from different workspaces |
| Soft-delete ambiguity | Medium | Inactive records may remain queryable or block valid uniqueness |
| Non-versioned membership changes | Medium | Historical authorization cannot be reconstructed |
| Missing isolation tests | Critical | Architecture claims cannot be verified before Gate D |

---

# 02. Workspace Ownership Model

## 02.1 Entity Classification

| Entity | Scope | Owns `workspace_id` | Derivation | Required Indexing Direction |
|---|---|---:|---|---|
| Workspace | Global root | No | It is the workspace identity | Primary key and normalized name/slug uniqueness |
| User | Global identity | No | May belong to multiple workspaces | Identity-provider subject and normalized email as applicable |
| WorkspaceMembership | Workspace relationship | Yes | Explicit join between Workspace and User | Unique `(workspace_id, user_id)`; lookup by user/workspace |
| EnterpriseObject | Workspace-scoped | Yes | Explicit | Workspace/type/status/owner query indexes |
| AgentDefinition | Workspace-scoped | Yes | Explicit | Workspace/status/name or key indexes |
| AgentInstance | Workspace-scoped | Yes | Explicit | Workspace/definition/status indexes |
| Provider | Global or workspace-configured | Conditional | See §02.2 | Depends on deployment model |
| Model | Global catalog or provider child | Conditional | See §02.2 | Provider/model-key uniqueness |
| Task | Workspace-scoped | Yes | Explicit | Workspace/status/assignee/priority/time indexes |
| Event | Workspace-scoped | Yes | Derived from source operation but persisted explicitly | Workspace/correlation/time/type indexes |
| AuditRecord | Workspace-scoped | Yes | Derived from trusted mutation context | Workspace/entity/time/actor indexes |
| ContextPackage | Workspace-scoped | Yes | From task | Workspace/task/status/expiry indexes |
| RuntimeSession | Workspace-scoped | Yes | From task and context | Workspace/task/agent/status/time indexes |
| PermissionProfile | Workspace-scoped unless system template | Conditional | Explicit for workspace profile; null/global only for immutable system template | Workspace/name/version indexes |
| ToolBinding | Workspace-scoped | Yes | From agent or permission profile | Workspace/agent/tool uniqueness |
| AgentCapability | Global catalog or workspace assignment | Conditional | Catalog entries may be global; assignments are workspace-scoped | Capability-key uniqueness; workspace assignment indexes |

## 02.2 Provider and Model Scope Decision

Recommended design:

- `Provider` and `Model` catalog definitions may be global;
- credentials, enablement, cost policy, residency policy, and permitted models must be workspace-scoped in a separate `WorkspaceProviderConfiguration` entity;
- no provider credential belongs in the global provider catalog;
- runtime execution must resolve provider access through the current workspace.

This avoids duplicating provider metadata while preventing one workspace from inheriting another workspace's credentials or policy.

## 02.3 Mandatory Rule

Every mutable business record must satisfy exactly one of these conditions:

1. it directly owns a non-null `workspace_id`; or
2. it is a documented immutable global catalog record; or
3. it is a child whose workspace is enforced through a parent and whose repository never permits independent lookup.

Implicit scope without an enforceable path is not permitted.

---

# 03. Database Index Strategy

## 03.1 Indexing Principle

An index must correspond to a real query pattern. A single index on `workspace_id` is necessary for some tables but is not sufficient for all workspace-scoped operations.

Typical repository queries will use:

```text
workspace_id + primary identifier
workspace_id + status
workspace_id + type
workspace_id + owner or assignee
workspace_id + created_at / occurred_at
workspace_id + correlation_id
workspace_id + external or natural key
```

Composite index column order should begin with `workspace_id` for queries that always scope by workspace.

## 03.2 Index Matrix

| Entity | Required Constraints / Indexes | Query Justification |
|---|---|---|
| WorkspaceMembership | `UNIQUE(workspace_id, user_id)` | Prevent duplicate membership and support membership resolution |
| WorkspaceMembership | index `(user_id, workspace_id)` if query planner cannot fully reuse uniqueness order for user-first lookup | Resolve all memberships or current role from authenticated user |
| WorkspaceMembership | index `(workspace_id, role)` | Workspace member and role administration |
| EnterpriseObject | index `(workspace_id, id)` or workspace-aware uniqueness strategy | Safe scoped object lookup |
| EnterpriseObject | index `(workspace_id, type, status)` | Common object filtering |
| EnterpriseObject | index `(workspace_id, owner_id, status)` | Owner work queues |
| AgentDefinition | `UNIQUE(workspace_id, agent_key)` | Stable role/config identity inside workspace |
| AgentDefinition | index `(workspace_id, status)` | Active agent selection |
| AgentInstance | index `(workspace_id, agent_definition_id, status)` | Runtime selection of configured instance |
| Task | index `(workspace_id, status, created_at)` | Workspace task list and queue |
| Task | index `(workspace_id, assignee_agent_id, status)` | Agent work queue |
| Task | index `(workspace_id, owner_user_id, status)` | Human-owned work queue |
| Task | index `(workspace_id, source_object_id)` | Related task lookup |
| Event | index `(workspace_id, occurred_at)` | Workspace timeline |
| Event | index `(workspace_id, correlation_id, occurred_at)` | Reconstruct one execution flow |
| Event | index `(workspace_id, event_type, occurred_at)` | Event filtering and operations |
| AuditRecord | index `(workspace_id, created_at)` | Workspace audit timeline |
| AuditRecord | index `(workspace_id, entity_type, entity_id, created_at)` | Entity history reconstruction |
| AuditRecord | index `(workspace_id, actor_type, actor_id, created_at)` | Actor accountability review |
| AuditRecord | index `(workspace_id, correlation_id, created_at)` | Mutation-chain reconstruction |
| ContextPackage | index `(workspace_id, task_id, created_at)` | Retrieve context snapshots for task |
| ContextPackage | index `(workspace_id, status, expires_at)` | Active/stale context management |
| RuntimeSession | index `(workspace_id, task_id, started_at)` | Session history for task |
| RuntimeSession | index `(workspace_id, agent_instance_id, status)` | Runtime operational view |
| RuntimeSession | index `(workspace_id, status, started_at)` | Stuck/running session detection |
| WorkspaceProviderConfiguration | `UNIQUE(workspace_id, provider_id)` | One effective provider policy per workspace |
| ToolBinding | `UNIQUE(workspace_id, agent_definition_id, tool_key)` | Prevent duplicate tool authorization |

## 03.3 Primary-Key Strategy

Globally unique UUID primary keys are acceptable, but they do not replace workspace filtering.

The canonical repository lookup is:

```text
get(workspace_id, entity_id)
```

The following repository method is prohibited for workspace-scoped entities:

```text
get_by_id(entity_id)
```

unless it is private to an already workspace-constrained query path and cannot be called without a trusted scope.

## 03.4 Foreign-Key Workspace Consistency

A foreign key to a globally unique ID does not guarantee that two related records belong to the same workspace.

The implementation plan must choose one of the following patterns per relationship:

### Recommended default: repository and service invariant plus integration tests

- load related objects using the same `workspace_id`;
- reject any relationship where either object cannot be found in that workspace;
- never attach a raw foreign ID without scoped resolution.

### Stronger optional pattern: composite foreign keys

Use composite keys such as:

```text
(workspace_id, task_id)
→ Task(workspace_id, id)
```

This gives database-level protection but increases schema complexity. It is recommended for the most critical relationships if SQLAlchemy/Alembic complexity remains manageable:

- AuditRecord to audited aggregate reference where relationally represented;
- ContextPackage to Task;
- RuntimeSession to Task;
- Event to Task or source aggregate when a direct foreign key exists.

Gate C architecture approval must explicitly record which relationships receive composite database enforcement and which rely on repository invariants.

---

# 04. WorkspaceMembership Design

## 04.1 Required Uniqueness

Mandatory constraint:

```text
UNIQUE(workspace_id, user_id)
```

Reason:

- one effective membership record per user per workspace;
- deterministic role resolution;
- no duplicated permissions;
- no ambiguous authorization results;
- safe idempotent invitation/acceptance flows.

## 04.2 Membership Lifecycle

Recommended state model:

```text
Invited
→ Active
→ Suspended
→ Revoked
```

Do not physically delete a membership that has participated in business or audit history.

## 04.3 Role Changes

Recommended design:

- update the effective role on the current membership record;
- create an immutable audit record for every role or status change;
- optionally add `WorkspaceMembershipHistory` later if high-volume temporal queries require it;
- do not create duplicate active membership rows merely to represent role history.

This preserves the uniqueness invariant while retaining reconstructable history through audit.

## 04.4 Soft Delete

Prefer `status = revoked` plus `revoked_at` over generic `deleted_at`.

Reason:

- membership revocation is a business/security event, not ordinary deletion;
- the unique pair remains reserved;
- reactivation can restore the same membership identity;
- historical references remain valid.

If product requirements later demand a fresh membership lifecycle, a versioned membership model requires a new ADR because it changes uniqueness semantics.

## 04.5 Membership Resolution Contract

Authentication identifies a global user.

Authorization resolves:

```text
(user_id, requested_workspace_id)
→ exactly one active WorkspaceMembership
→ ActorContext(workspace_id, user_id, role, permissions)
```

Failure cases:

- no membership: deny;
- suspended/revoked membership: deny;
- multiple membership rows: schema violation and security alert;
- workspace not supplied or not resolvable: deny for workspace-scoped endpoints.

---

# 05. AuditRecord Architecture

## 05.1 Core Decision

`AuditRecord.workspace_id` must be assigned inside the trusted audit/repository boundary.

Calling routers and ordinary domain services must not provide it as a free-form field.

## 05.2 Permitted Sources

The audit boundary may derive workspace identity from:

1. a workspace-scoped domain entity loaded through a scoped repository;
2. the trusted `ActorContext` for workspace-level actions without an existing entity;
3. a trusted mutation envelope produced by the transaction boundary and containing both entity reference and resolved workspace.

It must never derive workspace identity from:

- request payload;
- agent-generated content;
- client headers without authenticated resolution;
- an unverified foreign ID;
- a service-supplied arbitrary string.

## 05.3 Recommended Mutation Flow

```text
Authenticated Request
→ Workspace requested
→ WorkspaceMembership resolved
→ ActorContext created
→ Repository performs workspace-scoped lookup
→ Authorization checks operation and role
→ Domain service validates mutation
→ Transaction writes business entity
→ Audit service receives trusted entity/mutation envelope
→ Audit repository derives workspace_id
→ Audit record written in same transaction where practical
→ Event emitted after successful commit
```

## 05.4 Audit Repository Contract

Conceptual contract:

```text
record_entity_mutation(
    actor_context,
    audited_entity,
    action,
    before_state,
    after_state,
    correlation_id,
    metadata
)
```

No public parameter named `workspace_id` is permitted in this method.

For workspace-level actions without an existing entity:

```text
record_workspace_action(
    actor_context,
    action,
    target_reference,
    correlation_id,
    metadata
)
```

Here the workspace comes only from `actor_context.workspace_id`.

## 05.5 Cross-Workspace Audit Protection

Before writing an entity audit record:

```text
actor_context.workspace_id == audited_entity.workspace_id
```

If the values differ:

- reject the operation;
- roll back the transaction;
- emit a security log outside the rejected audit transaction;
- never silently normalize one value to the other.

System-level background operations must use an explicit system actor whose workspace is still resolved for each mutation.

## 05.6 Immutability

Audit records are append-only.

Gate C must prohibit ordinary application paths for:

- update;
- delete;
- workspace reassignment;
- actor reassignment;
- target reassignment.

Corrections must be represented by a new compensating audit record.

---

# 06. Repository Invariants

Every repository for a workspace-scoped entity must satisfy all invariants below.

## R-01. Workspace Is Mandatory

Every public read, write, list, count, and delete-like operation requires a trusted `workspace_id` or `ActorContext`.

## R-02. Scoped Lookup

Entity IDs are never resolved globally for business operations.

```text
WHERE workspace_id = :workspace_id
  AND id = :entity_id
```

## R-03. Scoped Collections

Every collection query starts with workspace scope before filters, sorting, or pagination.

## R-04. Scoped Mutation

Update and delete statements include workspace scope in the database predicate, not only in a prior in-memory check.

## R-05. Related Entity Validation

Every related entity must be resolved through the same workspace scope before association.

## R-06. No Caller-Controlled Workspace Reassignment

Ordinary update DTOs cannot change `workspace_id`.

Moving an entity between workspaces is not supported in Gate C.

## R-07. Deterministic Failure

Attempting to access an entity from another workspace must behave as not found or denied according to the API security policy, without revealing its existence.

## R-08. Audit Coupling

High-impact mutations cannot commit without their required audit record.

## R-09. Transaction Boundary

Business mutation and mandatory audit write occur in one transaction whenever technically feasible.

## R-10. Test Obligation

Every repository has positive same-workspace and negative cross-workspace tests.

---

# 07. Authorization Invariants

Authorization is not a substitute for repository isolation, and repository isolation is not a substitute for authorization.

Both are required.

```text
Authentication answers: Who are you?
Membership answers: Which workspace may you enter?
Authorization answers: What may you do there?
Repository scope answers: Which records can the operation touch?
Audit answers: What actually happened?
```

Mandatory rules:

- workspace membership is resolved before workspace-scoped service execution;
- role and permission checks use the resolved membership;
- agent identities are subject to the same workspace boundary;
- service identities receive explicit workspace assignments per execution;
- no superuser bypass is included in the MVP unless separately approved and audited;
- system maintenance operations must be explicit and cannot reuse normal user repositories without scope.

---

# 08. Acceptance Criteria

The following are blocking exit conditions for Gate C.

## 08.1 Database Acceptance Criteria

### GC-DB-01
Every workspace-scoped Gate C table has a non-null `workspace_id` unless this document explicitly classifies it as a global catalog.

### GC-DB-02
Every workspace-scoped table has indexes that support its documented workspace query patterns.

### GC-DB-03
`WorkspaceMembership` has `UNIQUE(workspace_id, user_id)`.

### GC-DB-04
Foreign keys, nullability, uniqueness, and indexes are present in committed migrations, not only ORM metadata.

### GC-DB-05
Migration downgrade and clean-database upgrade are verified.

### GC-DB-06
Audit records cannot be updated or deleted through ordinary repository methods.

## 08.2 Repository Acceptance Criteria

### GC-REP-01
No public workspace-scoped repository exposes `get_by_id(id)` without workspace scope.

### GC-REP-02
All update/delete predicates include `workspace_id`.

### GC-REP-03
Cross-workspace relation creation is rejected.

### GC-REP-04
Workspace reassignment through normal updates is impossible.

### GC-REP-05
Every repository documents its primary query patterns and maps them to schema indexes.

## 08.3 Membership Acceptance Criteria

### GC-MEM-01
Duplicate `(workspace_id, user_id)` insertion fails at database level.

### GC-MEM-02
Membership resolution returns exactly one effective membership or denies access.

### GC-MEM-03
Suspended and revoked memberships cannot authorize operations.

### GC-MEM-04
Role and status changes create immutable audit records.

## 08.4 Audit Acceptance Criteria

### GC-AUD-01
Ordinary callers cannot set `AuditRecord.workspace_id`.

### GC-AUD-02
The audit repository derives workspace from a trusted entity or `ActorContext`.

### GC-AUD-03
Mismatch between actor workspace and entity workspace rejects and rolls back the mutation.

### GC-AUD-04
Business mutation and mandatory audit record commit atomically where practical.

### GC-AUD-05
Audit records preserve actor, action, target, timestamp, correlation ID, and before/after references or approved summaries.

## 08.5 Testing Acceptance Criteria

### GC-TEST-01
Migration tests inspect actual database constraints and indexes.

### GC-TEST-02
Each workspace-scoped repository has cross-workspace read tests.

### GC-TEST-03
Each mutable repository has cross-workspace update/delete tests.

### GC-TEST-04
Membership duplicate and status tests pass.

### GC-TEST-05
Audit workspace derivation and mismatch rollback tests pass.

### GC-TEST-06
At least two workspaces with overlapping entity shapes are included in integration fixtures to prevent false-positive isolation tests.

### GC-TEST-07
Tests verify that pagination, counting, search, and dashboard-style aggregation remain workspace-scoped.

---

# 09. Required ADR Changes

## 09.1 ADR-0004 — Workspace Isolation

Proposed clarification:

- define the complete Gate C workspace ownership matrix;
- require schema and repository enforcement together;
- prohibit global ID-only repository access;
- require index strategy based on workspace query patterns;
- define `WorkspaceMembership` as the identity-to-workspace bridge;
- require `UNIQUE(workspace_id, user_id)`;
- define cross-workspace relationship validation;
- state that workspace reassignment is not supported in Gate C.

## 09.2 ADR-0005 — Audit and Event Integrity

Proposed clarification:

- `AuditRecord.workspace_id` is derived only at the trusted audit/repository boundary;
- ordinary services and request payloads cannot assign it;
- actor/entity workspace mismatch is a transaction-blocking error;
- mandatory audit records commit atomically with high-impact mutations;
- audit records are append-only;
- events are coordination signals and do not replace durable audit records.

## 09.3 ADR-0006 — Authorization

Proposed clarification:

- global identity is separated from workspace membership;
- authorization consumes resolved `ActorContext`;
- repository scoping remains mandatory after authorization succeeds;
- agents, humans, and service identities obey the same workspace isolation model;
- revoked/suspended memberships are denied;
- no implicit superuser bypass in MVP.

## 09.4 Proposed New ADR

Recommended new ADR:

```text
ADR-0008 — Gate C Data Isolation, Indexing, and Repository Invariants
```

Purpose:

- centralize schema/index/repository rules that span ADR-0004, ADR-0005, and ADR-0006;
- define the Index Matrix as an implementation obligation;
- define required negative isolation tests;
- avoid overloading the older ADRs with implementation-level database detail.

This new ADR should reference, not replace, ADR-0004 through ADR-0006.

---

# 10. Implementation Checklist

This checklist is planning output only. It does not authorize implementation.

## Schema Preparation

- [ ] Approve final Gate C entity list.
- [ ] Classify every entity as workspace-scoped, global, or inherited child.
- [ ] Approve provider/model global catalog split.
- [ ] Approve all natural keys and uniqueness rules.
- [ ] Approve Index Matrix against expected query patterns.
- [ ] Select relationships requiring composite foreign-key enforcement.

## Membership Preparation

- [ ] Approve `UNIQUE(workspace_id, user_id)`.
- [ ] Approve membership state lifecycle.
- [ ] Approve role-change audit behavior.
- [ ] Confirm no duplicate-row role history model for Gate C.

## Repository Preparation

- [ ] Approve repository method signature standard.
- [ ] Prohibit global ID-only lookup.
- [ ] Define failure behavior for cross-workspace access.
- [ ] Define transaction boundary for audit-required mutations.
- [ ] Define repository test template.

## Audit Preparation

- [ ] Approve trusted workspace derivation sources.
- [ ] Prohibit caller-supplied audit workspace.
- [ ] Approve actor/entity mismatch behavior.
- [ ] Approve immutable append-only contract.
- [ ] Approve event-after-commit behavior.

## Test Preparation

- [ ] Define two-workspace integration fixture.
- [ ] Define index/constraint inspection tests.
- [ ] Define cross-workspace read/write/delete tests.
- [ ] Define membership uniqueness tests.
- [ ] Define audit mismatch rollback tests.
- [ ] Define aggregation and pagination isolation tests.

## Governance Preparation

- [ ] Update ADR-0004.
- [ ] Update ADR-0005.
- [ ] Update ADR-0006.
- [ ] Decide whether to create ADR-0008.
- [ ] Add Gate C acceptance criteria to the authoritative work package register.
- [ ] Obtain project-owner approval before implementation.

---

# 11. Open Questions

The following questions must be resolved before Gate C coding begins:

1. Are `Provider` and `Model` global catalog entities, or fully duplicated per workspace?
2. Which Gate C relationships require composite foreign keys for database-level workspace consistency?
3. Should membership invitations occupy the unique membership row before acceptance?
4. Is one role per membership sufficient for MVP, or is a membership-to-role join required?
5. What API behavior is preferred for cross-workspace access: uniform 404, explicit 403, or policy-dependent response?
6. Which mutations are classified as high-impact and therefore require atomic audit writes?
7. Will audit before/after state store full snapshots, diffs, references, or a sensitivity-aware combination?
8. Are system templates allowed to have `workspace_id = NULL`, or should they live in separate global tables?
9. What retention policy applies to revoked memberships and audit records?
10. Which expected list and dashboard queries must be benchmarked before index approval?

---

# 12. Gate C Approval Rule

Gate C implementation must not begin until:

```text
Entity Scope Matrix approved
+ Index Matrix approved
+ WorkspaceMembership uniqueness approved
+ Audit workspace derivation approved
+ Repository invariants approved
+ ADR changes approved
+ Negative isolation test plan approved
```

Final architectural principle:

```text
A workspace boundary is valid only when the database, repository,
authorization layer, audit trail, and tests all agree on the same scope.
```

---

## 13. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-19 | Initial Gate C workspace isolation, indexing, membership, repository, and audit architecture review |
