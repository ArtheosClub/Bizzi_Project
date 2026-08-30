# WP19 / Q2-ST Recommendation v0.1

**Status:** Draft — recommendation only  
**Date:** 2026-08-30  
**Subject:** Q2-ST — subject-type ranging rule  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact recommends; it does not decide Q2-ST.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Recommendation

**Recommend Q2-ST-O2 — persisted-entity identity is the default ranging rule, with explicit architecture-controlled mapping exceptions.**

O2 is recommended because it best fits the already accepted D1 vocabulary, preserves the D5 authority gate, keeps the historical-identity contract comparatively simple, and changes the already-evaluated BR1–BR5/Q2-RI profile least.

This is not a recommendation that persistence-table topology alone is architecture authority. A new auditable persisted identity still requires explicit architecture authority under D5 before it becomes an admitted AuditRecord subject kind.

## 2. Recommended normative rule

> **AuditRecord subject kinds are architecture-authorized logical kinds whose default ranging rule follows canonical persisted subject identity. For an auditable persisted entity identity not already covered by an accepted subject kind, the default is that a new explicit subject kind requires separate architecture authority before AuditRecord use. Persistence existence or technical encodability alone does not authorize that kind.**
>
> **Where a persisted specialization shares the same canonical persisted identity as an already-authorized subject kind — including an ADR-0015 Option A specialization whose specialization primary key is the same identity as its corresponding `enterprise_objects` base row — the specialization does not create a second AuditRecord subject kind merely because a specialization table also exists. It may use the existing subject kind only where the accepted AuditRecord contract identifies that shared/base identity as the canonical audited-subject identity.**
>
> **Where a persisted specialization has a distinct standalone identity form — including an ADR-0015 Option B standalone D02 specialization with no corresponding `enterprise_objects` row — that identity is not automatically covered by `EnterpriseObject`. Before AuditRecord use it requires either (a) separate explicit authority for a new subject kind, or (b) a separate explicit mapping exception that authorizes the standalone identity form under an existing subject kind.**
>
> **A mapping exception is architecture authority, not implementation convenience. Approving a new mapping exception that makes a previously unauditable or uncovered persisted identity form admissible under an existing subject kind expands the audited-subject universe and requires the same explicit architecture control that D5 requires for adding a new subject kind. Mapping exceptions therefore cannot be used to bypass D5.**
>
> **Committed AuditRecords must retain stable historical subject identity across later persistence-form evolution. A later migration between standalone and base-row-plus-specialization forms must not silently reinterpret an already committed subject reference. Any such evolution must preserve the canonical identity semantics under which the record was committed or provide explicit versioned/historical resolution sufficient to satisfy D3 and D4.**

## 3. Why O1 is not recommended

O1 domain-concept-derived ranging is not currently decision-ready because the accepted D1 vocabulary is not a direct projection of the existing domain-owning taxonomy. Four of the five accepted D1 values would require either reinterpretation or a newly defined source concept set.

Choosing O1 now would therefore require an additional D1 reconciliation/amendment surface before it becomes a self-contained rule.

## 4. Why O3 is not recommended

O3 explicit mapping is architecturally viable only after adding two strong guards:

1. every mapping expansion into an existing subject kind requires D5-equivalent explicit authority; and
2. every committed record must bind to immutable or versioned mapping semantics so later mapping changes cannot alter historical interpretation.

With those guards, O3 remains more flexible than O2 but creates recurring case-by-case mapping decisions and two reopen-trigger classes: new identity forms and changes to mappings/permitted forms. It also more frequently changes ordinary FK availability under accepted Q2-RI.

The current corpus does not demonstrate a need for that additional mapping-governance layer as the default.

## 5. Q2-RI consequence

O2 does not select BR3 or any persistence representation.

It does preserve the current bounded BR3 Q2-RI credit for the five accepted subject kinds because the default keeps each kind associated with one canonical persisted target identity. A future approved mapping exception could change that RI profile and would require a bounded re-application of Q2-RI to the affected realization.

BR1 remains conforming without ordinary DB-RI credit; BR2 remains incomplete in its current corpus-grounded form; BR4/BR5 remain qualified alternatives with their resolver/content-contract burdens.

## 6. Recommended AuditRecord-specific reopen trigger

ADR-0015 is Accepted and must not be edited in place. Its current R7/R8/R9/R11 trigger therefore remains untouched.

If O2 is accepted, the Q2-ST authority should itself establish the following independent AuditRecord trigger:

> **Before implementation of an auditable mutation whose audited subject has a persisted identity form not already covered by an accepted AuditRecord subject kind and canonical identity contract, architecture MUST reopen subject-kind/mapping authority before that subject can be written to AuditRecord. This trigger also applies before a persistence-form change would materially change the canonical persisted identity target of an already-authorized AuditRecord subject kind.**

This trigger does not modify ADR-0015. It governs AuditRecord subject identity from ADW-07 and cites ADR-0015 only as a persistence-form source.

## 7. Boundaries

Acceptance of O2 would not:

- make AgentDefinition a current sixth subject kind;
- automatically map standalone AgentDefinition into `EnterpriseObject`;
- authorize AuditRecord production for AgentDefinition;
- decide GC-006 audit qualification;
- change ADR-0015 standalone default;
- select N1–N5 or BR1–BR5;
- define exact discriminator strings beyond already accepted D1 current scope;
- define FK layout, migrations, ORM relationships, resolver APIs, or actor attribution;
- authorize WP19 implementation.

## 8. Decision gate

**Recommendation ready for Project Owner review: Q2-ST-O2 — persisted-entity identity default with explicit architecture-controlled mapping exceptions.**

Until explicitly accepted:

- Q2-ST remains OPEN;
- no new subject kind or mapping exception is authorized;
- BR1–BR5 comparison remains provisional under the current five-kind rule;
- final Q2 representation remains OPEN;
- WP19 remains BLOCKED / UNAUTHORIZED.
