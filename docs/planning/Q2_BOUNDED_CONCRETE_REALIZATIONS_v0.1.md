# WP19 / Q2 Bounded Concrete Realizations v0.1

**Status:** Draft — evaluation design only  
**Date:** 2026-08-30  
**Subject:** Minimal concrete realizations of N1–N5 for post-Q2-RI evaluation  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. These are evaluation realizations, not approved persistence designs.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Purpose

Accepted Q2-RI attaches comparative DB-RI credit to a **concrete realization**, not to a candidate class. The normalized N1–N5 classes are therefore too abstract for the next comparison step.

This artifact defines one **minimal bounded realization** for each candidate solely to make D1–D5 and Q2-RI testable. A bounded realization specifies only the persisted subject-reference contract and the minimum validation/resolution behavior needed for evaluation. It does not specify SQLAlchemy code, migrations, indexes, API shape, repository methods, actor attribution, event publication, or operational implementation.

The current D1/D5 test scope remains exactly five subject kinds: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`. Q2-ST remains open. Nothing here authorizes a sixth kind or a generic standalone-D02 mapping.

## 2. Current implementation evidence relevant to the realizations

Implementation evidence is not architecture authority, but it constrains what counts as a realistic bounded proposal:

- `Workspace` has UUID primary key `id` and is itself the tenancy boundary; it has no `workspace_id`.
- `User` has UUID primary key `id` and no `workspace_id`.
- `WorkspaceMembership` has UUID primary key `id` plus DB FKs to `workspaces.id` and `users.id`.
- `EnterpriseObject` has UUID primary key `id` plus DB FK `workspace_id -> workspaces.id`.
- `Task` has UUID primary key `id` plus DB FK `workspace_id -> workspaces.id`.

This asymmetry is why a universal `(workspace_id, id)` target shape cannot be assumed for all five current subjects.

## 3. BR1 — N1 Polymorphic typed reference

### Minimal persisted contract

AuditRecord carries one explicit durable `subject_type` value and one durable UUID `subject_id` value.

`subject_type` is constrained semantically to the five accepted D1 values. The pair `(subject_type, subject_id)` is the canonical logical subject reference for the record.

### Resolution / validation

A subject-type dispatch contract maps each accepted `subject_type` to the corresponding persisted identity target. On write, validation confirms that the identified subject exists and that any applicable workspace/context invariant is satisfied. The committed pair is immutable and remains historically interpretable even if live dereference later becomes unavailable under D3.

### DB-RI position

No ordinary multi-target FK from one `subject_id` column to five heterogeneous tables is assumed. No registry/base table is introduced solely to manufacture such an FK.

### Explicit exclusions

No resolver API, registry, global UUID guarantee, auxiliary identity table, migration, or ORM polymorphic relationship is designed here.

## 4. BR2 — N2 Composite-FK family

### Minimal persisted contract

AuditRecord uses DB-enforced composite reference semantics where the target actually exposes the required composite identity shape.

For current workspace-scoped targets that already carry `(workspace_id, id)`, a concrete relation may use those key components. For `Workspace` and `User`, which do not expose the same shape, this bounded realization does **not** invent a synthetic `workspace_id` or universal registry.

### Resolution / validation

Applicable composite relations are DB-enforced. Structurally asymmetric current subject kinds require an additional target-specific adaptation before BR2 could become a complete five-type Q2 realization.

### DB-RI position

Strong DB-native RI exists locally where the documented composite shape applies. Q2-wide RI and Q2-wide subject coverage are not established.

### Explicit exclusions

No synthetic composite identity for Workspace/User, no registry, no five-target layout, and no GC-002 approval are invented.

## 5. BR3 — N3 Per-type nullable relations

### Minimal persisted contract

AuditRecord provides five subject-specific nullable UUID reference slots, one for each current D1 kind:

- Workspace reference;
- EnterpriseObject reference;
- User reference;
- WorkspaceMembership reference;
- Task reference.

Each slot targets the corresponding table's existing primary key with an ordinary DB foreign key. The durable `subject_type` discriminator remains explicit under D1.

A record-level exclusivity invariant requires exactly one subject-specific slot to be populated and requires that populated slot to correspond to `subject_type`.

### Resolution / validation

The populated FK identifies the live target while it exists. The committed `subject_type` plus identifier value remains the historical subject identity under D3 even where later lifecycle authority permits loss of live dereference. The exact DB/application mechanism enforcing the cross-slot exactly-one/discriminator match is not chosen here; the invariant itself is required for D1/D4 conformity.

### DB-RI position

Each concrete subject relation can use ordinary DB FK enforcement without adding an auxiliary persistence abstraction. Cross-slot exclusivity is a separate integrity property and is not credited as referential integrity merely because per-type FKs exist.

### Explicit exclusions

No FK delete action, CHECK expression, ORM relationship, index, migration, or future sixth slot is designed here.

## 6. BR4 — N4 Typed opaque identity plus durable resolution contract

### Minimal persisted contract

AuditRecord carries explicit durable `subject_type` plus an opaque durable `subject_key`. `subject_key` is not assumed to be directly FK-compatible with the concrete subject table.

### Resolution / validation

An explicit durable resolution contract maps `(subject_type, subject_key)` to the historical subject identity. On write, validation must establish a valid subject under the current mapping. Historical interpretation of committed keys must remain stable/versioned rather than silently repointed.

### DB-RI position

No DB-native FK is assumed. A registry/namespace table is not introduced because doing so solely to locate enforcement in the DB would require independent abstraction justification.

### Explicit exclusions

No concrete key encoding, namespace registry, resolver service, version table, or global identity system is designed here.

## 7. BR5 — N5 Explicit subject identity inside persisted AuditRecord content

### Minimal persisted contract

AuditRecord's persisted content contains a mandatory dedicated subject-identity object with explicit `subject_type` and durable `subject_id`. Generic before/after diff fields, actor data, workspace context, route data, or arbitrary payload content do not establish subject identity by implication.

### Resolution / validation

The dedicated content contract is validated on write against the accepted subject kind and target identity. Its schema/version semantics preserve historical interpretation of committed records. Subject identity remains queryable only to the extent the concrete persistence engine can address/index the dedicated content fields; no such index is assumed here.

### DB-RI position

No ordinary FK from content to heterogeneous target tables is assumed. DB JSON/content validation may validate shape but is not treated as target referential integrity unless a concrete realization actually provides that property.

### Explicit exclusions

No JSON dialect, JSON schema technology, expression index, generated column, trigger, resolver API, or GC-007 shape is selected.

## 8. Evaluation boundary

These BR1–BR5 realizations are deliberately asymmetric where the candidate class itself creates asymmetry. They are not optimized to make candidates look equally strong.

However:

- no realization receives an auxiliary abstraction solely to improve its Q2-RI score;
- no candidate is rejected because its bounded realization lacks ordinary DB FK enforcement;
- no realization is implementation authority;
- no candidate is selected by defining these realizations;
- Q2-ST remains open and may require a later bounded re-check.

## 9. Next step

Apply accepted D1–D5 and Q2-RI to BR1–BR5, recording reasoning for each realization. Do not select a final representation. After that comparison, resolve Q2-ST before final Q2 representation authority.
