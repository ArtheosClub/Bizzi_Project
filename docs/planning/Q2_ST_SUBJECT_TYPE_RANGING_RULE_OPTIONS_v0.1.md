# WP19 / Q2-ST Subject-Type Ranging Rule Options v0.1

**Status:** Draft — options/evaluation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — rule determining the admissible AuditRecord subject-type discriminator vocabulary  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures Q2-ST; it does not decide it.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Bounded question

**What architecture-level rule determines the admissible durable AuditRecord subject-type discriminator vocabulary: domain subject concepts, persisted subject entity identities, or another explicitly defined mapping between the two?**

Q2-ST does not decide whether `AgentDefinition` is a sixth current subject type. It decides the rule by which that question, and analogous future questions, must be answered.

## 2. Why Q2-ST exists

Accepted D1 fixes the current discriminator vocabulary to:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

Accepted D5 treats those five as the current Q2 acceptance scope and requires separate architecture authority for future auditable subject types.

What D1 and D5 do **not** state is the generative rule behind the vocabulary: whether discriminator kinds range over domain concepts, concrete persisted subject identities, or an explicit architecture mapping between them.

Repository review shows why this matters:

- the current five names are not a clean projection of the six ADW-01/D09 domain-owning concepts;
- `User` appears rather than the broader domain concept `Actor`;
- `WorkspaceMembership` is a concrete persisted association entity rather than one of the six domain-owning concepts;
- ADR-0015 classifies `AgentDefinition` as D02 `EnterpriseObject` while persisting it standalone, with no corresponding `enterprise_objects` row and no universal specialization discriminator established.

These observations expose ambiguity. They do not themselves decide the ranging rule.

## 3. AgentDefinition as a test case, not a pre-decided answer

ADR-0015 establishes for the MVP default:

- `AgentDefinition` is a D02 EnterpriseObject specialization;
- AgentDefinition uses standalone persistence;
- no corresponding `enterprise_objects` row exists for it;
- `enterprise_objects.type` is not established as a universal physical specialization discriminator;
- the existing mandatory reopen trigger covers only concrete R7/R8/R9/R11 references to standalone D02 specializations.

Therefore current authority does not establish either of these conclusions:

1. `AgentDefinition` MUST be a separate AuditRecord subject-type discriminator value; or
2. every standalone `AgentDefinition` can automatically be durably resolved under the existing discriminator value `EnterpriseObject`.

Q2-ST exists to make the general rule explicit rather than deciding AgentDefinition ad hoc.

## 4. Inherited constraints

Any Q2-ST answer must preserve:

- D1: subject type is explicit and durable;
- D2: context does not substitute for subject identity;
- D3: historical identity survives lifecycle change;
- D4: subject identity is mandatory, stable, independently resolvable, and not inferred from actor/context/payload;
- D5: current five remain the present Q2 scope until separate architecture authority changes that scope.

Q2-ST may not silently add a sixth current discriminator value or rewrite D1/D5 by implication.

## 5. Options

### Q2-ST-O1 — Domain-concept ranging

**Rule:** AuditRecord subject types range over approved domain subject concepts. Concrete persistence specializations/rows map to the applicable domain concept and do not automatically create a new discriminator kind.

**Implication for standalone specializations:** A standalone D02 specialization such as AgentDefinition would normally use the domain subject kind `EnterpriseObject`, provided a durable resolution contract exists that can identify that concrete historical specialization instance without relying on a nonexistent base row.

**Strengths:**

- discriminator vocabulary follows domain semantics rather than table growth;
- new persistence tables do not automatically enlarge the architectural subject vocabulary;
- domain refactoring can remain conceptually separated from persistence shape.

**Unresolved burden:** The architecture must define how a domain-level kind such as `EnterpriseObject` durably resolves standalone specializations with heterogeneous physical storage. Without such a contract, D4 independently resolvable identity is not satisfied by the label alone.

### Q2-ST-O2 — Persisted-entity-identity ranging

**Rule:** AuditRecord subject types range over concrete persisted subject entity identities. A persisted entity kind that can be audited has its own explicit discriminator kind unless separate authority maps it otherwise.

**Implication for standalone specializations:** If AgentDefinition becomes an auditable persisted subject, its standalone identity would normally require a separately authorized discriminator kind rather than being collapsed into `EnterpriseObject` by domain classification alone.

**Strengths:**

- discriminator kind aligns closely with the concrete persistence target used for resolution;
- direct historical resolution semantics can be simpler where each type maps to one persisted entity identity.

**Burdens:**

- subject-type vocabulary can grow with persistence entities and specializations;
- persistence refactoring can force architecture-level discriminator decisions;
- D5 separate-authority requirement may become frequent if many auditable persisted entities are added.

### Q2-ST-O3 — Explicit architecture mapping between subject concepts and persisted identities

**Rule:** The discriminator vocabulary is an explicit architecture-controlled logical subject-kind set. Each kind has an explicit durable mapping to one or more permitted persisted identity forms. Neither domain taxonomy nor table identity alone automatically determines the vocabulary.

**Implication for standalone specializations:** Architecture could keep `EnterpriseObject` as a logical subject kind while explicitly mapping standalone D02 specialization identities into its durable resolution contract, or could authorize a specialization-specific subject kind where warranted. Either result requires explicit mapping authority rather than inference.

**Strengths:**

- separates logical audited-subject semantics from accidental table topology;
- can handle structurally heterogeneous persistence without requiring one discriminator per table;
- avoids assuming that every domain concept or every persistence entity is automatically auditable.

**Burdens:**

- introduces a mapping contract that must itself be governed and historically stable;
- may require additional resolver semantics depending on the final persistence representation;
- if underspecified, it merely relocates the ambiguity rather than resolving it.

### Q2-ST-O4 — Implementation-defined ranging

**Rule:** implementation may add/reuse subject kinds as convenient so long as the persisted representation can encode them.

**Evaluation: FAIL against existing governance.**

This conflicts with D1/D5 authority boundaries and D5's explicit rule that technical encodability does not confer architecture authority.

## 6. Relation to D1 and D5

Q2-ST supplements but does not silently amend D1/D5.

Before Q2-ST is decided:

- the five current D1 values remain authoritative;
- no sixth value is authorized;
- no generic mapping from all standalone D02 specializations into `EnterpriseObject` is authorized;
- no rule that every persisted model becomes a subject type is authorized.

After Q2-ST is decided, any required change to the current D1 vocabulary must still be made through explicit architecture authority rather than being inferred from this planning artifact.

## 7. Required reopen-trigger follow-up

ADR-0015 currently requires architecture reopen only when a concrete Work Package needs an R7, R8, R9, or R11 reference to AgentDefinition or another standalone D02 specialization.

AuditRecord subject references are outside those D09 relationship rows. Therefore the current ADR-0015 trigger does not ensure reconsideration when a standalone specialization becomes relevant to AuditRecord subject identity.

After Q2-ST is accepted, a separate narrow authority update should connect standalone/new persisted subject identity with the accepted subject-type ranging rule. The trigger wording must be derived from the accepted Q2-ST option and is therefore **not drafted or approved here**.

## 8. What Q2-ST does not decide

Q2-ST does not decide:

- whether AgentDefinition is currently audited;
- whether AgentDefinition is a sixth current subject type;
- whether `EnterpriseObject` physically resolves via `enterprise_objects` only;
- the final N1–N5 representation;
- Q2-RI;
- actor attribution / ActorContext;
- GC-006 audit-qualification semantics;
- GC-002 or GC-007;
- repository/service/API authorization for WP14;
- migration or runtime resolver design;
- WP19 implementation.

## 9. Decision gate

A Project Owner decision is required before Q2-ST becomes normative.

Until then:

**Q2-ST OPEN — CURRENT FIVE D1 VALUES REMAIN IN FORCE — AGENTDEFINITION IS NOT DECLARED A SIXTH TYPE OR AUTOMATICALLY COLLAPSED INTO ENTERPRISEOBJECT — NO REOPEN TRIGGER CHANGE YET.**
