# WP19 / Q2 D4 Durable Subject-Reference Semantics Options v0.1

**Status:** Draft — D4 semantic/options analysis only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D4 — semantic contract of durable AuditRecord subject reference  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures and evaluates D4 semantic options; it does not decide D4.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. D4 bounded question

**What semantic contract must a durable persisted AuditRecord subject reference satisfy, beyond the already-accepted D1–D3 rules, so that subject identity remains unambiguous, historically meaningful, and distinguishable from context, association, and actor attribution over time?**

D4 is a semantic/options decision stage. It is not a persistence-design stage.

D4 must not choose N1–N5, FK structure, composite keys, payload shape, registry architecture, database enforcement, migration shape, runtime resolver, or implementation.

## 2. Authority already fixed by D1–D3

D4 inherits and MUST NOT redefine:

### D1 — type disambiguation

A persisted AuditRecord subject reference includes an explicit durable subject-type discriminator identifying exactly one current Q2 subject type:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

D4 cannot replace this discriminator with context inference, association inference, or actor inference.

### D2 — subject versus Workspace context

`Workspace` is a first-class audited subject. A Workspace associated with another subject is contextual metadata, not an implicit substitution for that subject.

D4 must keep subject identity, context, and association distinct.

### D3 — lifecycle and historical resolution

A committed AuditRecord preserves enough durable subject-reference information to identify its historical audited subject after later subject deletion or deactivation. Subject/context lifecycle change does not by itself authorize deletion or mutation of committed AuditRecord history.

D4 therefore must not define subject identity as “whatever live row currently resolves” or make historical meaning contingent on current availability.

D3 supplies lifecycle and historical-resolution boundaries only. It does not establish retention periods, legal/compliance erasure policy, or referential-integrity mechanics, and D4 must not attribute those decisions to D3.

## 3. D4 semantic surfaces

D4 evaluates seven semantic surfaces only.

### S4.1 — What constitutes subject identity?

At minimum, D1 already requires durable subject-type qualification. D4 must determine what further semantic property is required of the subject identifier portion of the reference.

The issue is not its physical column/layout; the issue is whether the committed reference identifies one historical subject instance in a stable namespace/identity convention.

### S4.2 — Which identity forms are admissible?

D4 may distinguish semantic identity forms such as:

- direct stable entity identity;
- type-qualified durable identity;
- durable external/legacy identity where canonical internal identity is unavailable;
- explicitly unresolved-but-preserved historical identity.

These are semantic classes, not persistence candidates.

### S4.3 — Subject versus context versus association

The subject is the entity whose mutation/action is being audited. Context scopes or describes the occurrence. Association connects entities but is not automatically the subject.

Examples:

- a `WorkspaceMembership` subject is not reduced to its User or Workspace;
- an `EnterpriseObject` subject is not replaced by its Workspace context;
- a User operating in a Workspace remains a User subject if User is the audited subject;
- an association may itself be a subject only where it is represented as an accepted subject type, such as `WorkspaceMembership`.

### S4.4 — Subject identity versus actor attribution

The audited subject answers **what entity was audited**. Actor attribution answers **who or what performed, initiated, authorized, or was attributed to the action**.

These are separate semantic axes. Actor identity, initiator identity, service identity, user identity acting in a Workspace, or other attribution data MUST NOT substitute for missing subject identity and MUST NOT be used to infer a different audited-subject type.

A `User` may be the audited subject in one AuditRecord and the actor in another; the semantic role in the record determines which axis the identity belongs to.

D4 does not define the actor-attribution contract itself.

### S4.5 — Temporal resolvability

The committed subject reference must remain semantically interpretable over time in accordance with D3 even if current live dereference fails.

D4 must distinguish:

- historical identity resolution: “which subject was this?”;
- current live resolution: “can I fetch an active/live entity now?”

The first is required by D3; the second is not universally required by D3.

### S4.6 — Unknown, legacy, unavailable, deleted, or inactive subject

D4 must define whether lack of current resolution invalidates historical identity.

It must not silently invent a new current Q2 subject type such as `Unknown` or `Legacy` because D1 currently permits exactly the five accepted discriminator values.

### S4.7 — Relationship to D3 lifecycle/history boundaries

D4 may rely on D3's historical-identity invariant but must not establish retention periods, legal/compliance erasure policy, FK delete actions, or physical preservation mechanics.

## 4. D4 options

### D4-O1 — Live-resolvable entity identity only

**Rule:** a valid AuditRecord subject reference must always resolve to a currently live and active subject entity.

**Result: FAIL.**

This conflicts with D3 because historical identity must survive deletion/deactivation even when current live dereference is unavailable.

### D4-O2 — Stable type-qualified historical subject identity

**Rule:** a durable subject reference identifies exactly one historical subject instance using the accepted D1 subject type plus a durable subject-identity value/convention whose committed meaning remains stable over time. Current live dereference may succeed or fail without changing that committed identity.

**Result: PASS.**

This is representation-neutral and directly supports D1–D3.

It does not decide whether the identity value is a UUID, database key, externally assigned key, opaque token, payload field, composite value, or another physical representation.

### D4-O3 — Context-qualified identity can substitute for subject identity

**Rule:** where subject resolution is difficult, Workspace/context/association may stand in for the audited subject.

**Result: FAIL.**

This conflicts with D2 and weakens D1 subject-type meaning.

### D4-O4 — Association participants may substitute for association subject

**Rule:** when `WorkspaceMembership` or another association-like subject is unavailable, one or more participant identities may replace the committed subject identity.

**Result: FAIL.**

This changes the audited subject and conflicts with D2/D3 historical meaning.

### D4-O5 — Actor attribution may substitute for subject identity

**Rule:** where subject identity is missing or unavailable, actor/initiator/attribution identity may be used as the audited-subject identity or as evidence sufficient to infer it.

**Result: FAIL.**

Actor attribution and audited-subject identity answer different semantic questions. Substitution would collapse two independent audit dimensions and could falsely identify the actor as the entity that was mutated or audited.

### D4-O6 — Preserved historical identity may remain currently unresolved

**Rule:** a committed subject reference may be historically valid even when no current live entity can be resolved, provided the durable reference still preserves the accepted subject type and a stable historical identity sufficient to distinguish the audited subject according to D1–D3.

**Result: PASS.**

This covers deleted, unavailable, archived, disconnected, or legacy-resolution cases without inventing a persistence mechanism.

### D4-O7 — Unknown subject type/value as a sixth current subject category

**Rule:** persist `Unknown`, `Legacy`, or equivalent as another subject type whenever resolution is unavailable.

**Result: FAIL under current authority.**

D1 explicitly requires the discriminator's committed value to identify exactly one of the five current Q2 subject types. D4 cannot add a sixth type by implication.

A legacy record may have incomplete or non-conforming historical data, but that is different from creating a new accepted subject type.

### D4-O8 — Legacy identity may be preserved without pretending it is canonical

**Rule:** where a historical/legacy AuditRecord has an identity value that cannot be normalized to the current canonical identity convention without invention, the original durable evidence may be preserved and explicitly treated as legacy/unresolved metadata while the record's compliance with the current D1–D4 contract is reported separately.

**Result: CONDITIONAL / PASS as a compatibility rule.**

This avoids fabricating identity. It does not declare non-conforming legacy records equivalent to newly compliant records and does not define a migration strategy.

## 5. Current five subject types

D4-O2/O6 apply uniformly at semantic-contract level to all five accepted D1 types:

### `Workspace`

The reference identifies one historical Workspace subject, not “the current workspace context.” Later closure/deletion/unavailability does not rewrite that identity.

### `EnterpriseObject`

The reference identifies one historical EnterpriseObject subject. Workspace association, specialization state, or later lifecycle change does not substitute for the EnterpriseObject identity.

### `User`

The reference identifies one historical User subject when User is the audited subject. Disabled/deleted/unavailable account state does not convert the subject into Workspace/context identity. A User acting on another subject is actor attribution and does not make User the audited subject. Legal/compliance handling remains separate.

### `WorkspaceMembership`

The reference identifies the membership itself as the historical subject. User + Workspace participants are not substitutes for membership identity unless a later explicit architecture decision changes the subject model.

### `Task`

The reference identifies one historical Task subject. Completion, cancellation, archival, deletion, or loss of Workspace context does not rewrite the Task identity.

## 6. Unknown / legacy / unavailable cases

D4 must distinguish these states:

- **Unknown current availability:** the subject identity is known historically, but live fetch status is unknown.
- **Unavailable current subject:** historical identity is known, but the live subject cannot currently be fetched/resolved.
- **Deleted/deactivated subject:** D3 applies; historical identity remains stable.
- **Legacy identity evidence:** historical data exists under an earlier/non-canonical convention; do not fabricate canonical identity.
- **Missing/insufficient subject identity:** the record cannot be claimed compliant with the current durable subject-reference contract merely because context, association, or actor-attribution data exists.

D4 does not define migration, repair, reconciliation, or legacy-data rewriting procedures.

## 7. Preferred D4 proposal

The narrowest rule consistent with D1–D3 is:

> **A durable committed AuditRecord subject reference MUST identify exactly one historical audited subject instance using the accepted D1 subject type together with a durable subject-identity value or identity convention whose committed meaning remains stable over time. Subject identity MUST remain distinct from context, association participants, and actor attribution. Historical validity does not depend on successful current live dereference: an unavailable, deleted, deactivated, or otherwise non-live subject may remain historically resolvable when the committed reference still identifies that subject under the durable identity contract. D4 does not create additional subject types, does not permit context, association participants, or actor attribution to substitute for subject identity, and does not select the physical representation or referential-integrity mechanism. Legacy or insufficient identity evidence MUST NOT be silently normalized by invention; its compatibility with the current contract must be handled explicitly.**

## 8. What D4 does not decide

D4 does not decide:

- actor-attribution semantics, fields, identity model, or attribution mechanism;
- exact field/column names;
- UUID versus integer versus string versus composite identity values;
- FK or composite-FK structure;
- payload versus relational placement;
- opaque identifier mechanism;
- registry architecture;
- database-enforced referential integrity;
- application/domain enforcement;
- GC-002 Alternative B approval;
- N1–N5 selection/default/ranking/rejection;
- retention duration;
- legal/compliance erasure/anonymization policy;
- D5 extensibility requirement;
- migration/legacy repair procedure;
- runtime resolver/API contract;
- models, repositories, services, APIs, backend implementation, migrations, or tests;
- WP19 implementation.

## 9. D4 decision status

**PROPOSED — NOT YET ACCEPTED.**

**Authority: NOT YET ESTABLISHED.**

This artifact is an options/evaluation document only. A separate Project Owner acceptance and authority artifact are required before D4 becomes normative.

## 10. Gate result

**D4 SEMANTIC OPTIONS STRUCTURED — D1–D3 PRESERVED — SUBJECT / CONTEXT / ASSOCIATION / ACTOR ATTRIBUTION KEPT DISTINCT — TEMPORAL HISTORICAL RESOLUTION DEFINED WITHOUT LIVE-DEREFERENCE REQUIREMENT — UNKNOWN/LEGACY/UNAVAILABLE CASES EXPOSED — D3 LIFECYCLE/HISTORY BOUNDARY PRESERVED WITHOUT RETENTION-POLICY SUBSTITUTION — NO PERSISTENCE SHAPE OR N1–N5 SELECTION — GC-002 ALTERNATIVE B REMAINS PROPOSED ONLY — D4 OPEN / NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.