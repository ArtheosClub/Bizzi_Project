# ADW-07 / Q2-ST — Subject-Type Ranging Rule Decision

**Workshop:** ADW-07 — Events, Audit, and Provenance  
**Workshop Status:** OPEN  
**Decision:** Q2-ST — rule determining the admissible AuditRecord subject-type discriminator vocabulary  
**Decision Status:** ACCEPTED  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-08-30  
**Accepted option:** Q2-ST-O2 — persisted-entity identity default, with explicit architecture-controlled mapping exceptions

## Definition — canonical persisted subject identity

For Q2-ST purposes, **canonical persisted subject identity** means the persisted identity to which the accepted AuditRecord subject-reference contract resolves for a given authorized subject kind.

Where a persistence form exposes more than one candidate identity for the same logical entity — for example, a base row plus a specialization row — the canonical identity is **not** inferred from table topology. It must be identified by explicit architecture authority or by the accepted Q2 representation contract.

A persistence form that does not fit an already-authorized canonical-identity rule is not automatically admitted. It triggers subject-kind/mapping review before AuditRecord use.

This definition does not restrict future persistence to ADR-0015 Options A and B; it gives a rule for any later form. A third form, such as a specialization with its own surrogate primary key plus a separate foreign key to a base row, therefore requires explicit authority to identify which persisted identity is canonical before it can participate in the AuditRecord subject contract.

## Decision

**AuditRecord subject kinds are architecture-authorized logical kinds whose default ranging rule follows canonical persisted subject identity. For an auditable persisted entity identity not already covered by an accepted subject kind, the default is that a new explicit subject kind requires separate architecture authority before AuditRecord use. Persistence existence or technical encodability alone does not authorize that kind.**

**Where a persisted specialization shares the same canonical persisted identity as an already-authorized subject kind — including an ADR-0015 Option A specialization whose specialization primary key is the same identity as its corresponding `enterprise_objects` base row — the specialization does not create a second AuditRecord subject kind merely because a specialization table also exists. It may use the existing subject kind only where the accepted AuditRecord contract identifies that shared/base identity as the canonical audited-subject identity. This permission is inoperative until the final Q2 persisted-representation contract establishing that canonical identity has been accepted.**

**Where a persisted specialization has a distinct standalone identity form — including an ADR-0015 Option B standalone D02 specialization with no corresponding `enterprise_objects` row — that identity is not automatically covered by `EnterpriseObject`. Before AuditRecord use it requires either (a) separate explicit authority for a new subject kind, or (b) a separate explicit mapping exception that authorizes the standalone identity form under an existing subject kind.**

**A mapping exception is architecture authority, not implementation convenience. Approving a new mapping exception that makes a previously unauditable or uncovered persisted identity form admissible under an existing subject kind expands the audited-subject universe and requires the same explicit architecture control that D5 requires for adding a new subject kind. Mapping exceptions therefore cannot be used to bypass D5.**

**Committed AuditRecords must retain stable historical subject identity across later persistence-form evolution. A later migration between standalone and base-row-plus-specialization forms must not reinterpret an already committed subject reference. Any such evolution must preserve the canonical identity semantics under which the record was committed or provide explicit versioned/historical resolution sufficient to satisfy D3 and D4.**

**This ranging rule governs only the AuditRecord subject discriminator and durable subject-reference contract. It does not define the domain taxonomy, does not claim that a persistence entity is itself a domain-owning concept, and does not authorize domain-semantic conclusions from discriminator vocabulary.**

## Relationship to accepted D1 and D5

This decision does not amend, supersede, or reinterpret D1 or D5; their canonical authority remains exclusively in their respective accepted decision records.

D1's five accepted values remain in force unchanged. This decision states the ranging rule those five instantiate; it does not re-derive, re-authorize, or extend them. No sixth subject kind and no mapping exception is authorized by this decision.

D5's separate-authority requirement remains unchanged. This decision establishes an equivalent explicit-architecture-authority guard for expansion of the audited-subject universe achieved by widening an existing subject kind through a mapping exception.

## AuditRecord subject-kind reopen trigger

ADR-0015 is Accepted and is not edited by this decision. Its R7/R8/R9/R11 reopen trigger remains untouched and unextended. This decision establishes the following independent AuditRecord trigger from ADW-07, citing ADR-0015 only as a persistence-form source:

**Before implementation of an auditable mutation whose audited subject has a persisted identity form not already covered by an accepted AuditRecord subject kind and canonical persisted subject-identity contract, architecture MUST reopen subject-kind/mapping authority before that subject can be written to AuditRecord. This trigger also applies before a persistence-form change would materially change the canonical persisted identity target of an already-authorized AuditRecord subject kind.**

## Abstraction Justification Rule reference

Q2-ST-O3 (a reusable explicit mapping layer between logical subject kinds and permitted persisted identity forms) is architecturally viable but is not adopted as the default now.

`CLAUDE.md`'s Abstraction Justification Rule states that a new architectural abstraction must either solve an existing, demonstrated problem or be a necessary precondition for implementing the next Work Packages, and that anticipated future need is not sufficient justification. No mapping exception currently exists, so the governance, resolver, and versioning machinery O3 requires would be introduced against predicted rather than demonstrated need. ADR-0015 rejected its Option A on the same rule and the same absence of a demonstrated cross-specialization reference need; adopting O3 now would take the equivalent abstraction one level higher against the same absence.

The choice is additionally supported by reversibility asymmetry: adopting O2 now leaves O3 available later without reinterpreting committed records, because a later mapping layer can preserve existing kinds and committed semantics while adding explicitly authorized mappings. The reverse move — retiring an O3 mapping layer in favor of an O2 default — would carry a materially higher historical-compatibility burden because previously committed records could remain dependent on legacy mapping semantics. Those semantics would have to be preserved or version-resolved for historical records; they could not simply be collapsed into the new default without risking reinterpretation prohibited by D3 and D4.

O3 is therefore **deferred, not discarded**, and is recorded as D-11 in `docs/planning/DEFERRED_ARCHITECTURE_INITIATIVES.md`, with the first explicitly accepted mapping exception as its concrete reopen condition.

## Consequences for candidate evaluation

This decision selects no Q2 representation and no bounded realization.

It preserves the current bounded BR3 Q2-RI credit for the five accepted subject kinds only while each kind resolves to one canonical persisted target identity under the current bounded realization. A future approved mapping exception or persistence-form change may alter that RI profile and requires a bounded re-application of accepted Q2-RI to the affected realization.

BR1 remains conforming without ordinary DB-RI credit; BR2 remains incomplete in its current corpus-grounded form; BR4/BR5 remain qualified alternatives carrying their resolver and content-contract burdens.

## Explicit non-decisions

This decision does not:

- make `AgentDefinition` a sixth current subject kind;
- map standalone `AgentDefinition` into `EnterpriseObject`;
- authorize AuditRecord production for `AgentDefinition` or any other subject;
- authorize any mapping exception;
- decide GC-006 audit qualification;
- change ADR-0015's standalone-persistence default or edit ADR-0015;
- adopt Q2-ST-O3 or authorize any mapping-layer infrastructure;
- select N1–N5 or BR1–BR5;
- define discriminator strings beyond D1's accepted current scope;
- define FK layout, CHECK constraints, indexes, migrations, ORM relationships, or resolver APIs;
- define actor attribution or ActorContext persistence semantics;
- restore a WP18 → WP19 dependency;
- authorize WP19 implementation;
- close ADW-07.

## Current Q2 state

- D1–D5: **CLOSED — ACCEPTED**;
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**;
- Q2-ST: **CLOSED — ACCEPTED — O2 persisted-entity default with explicit mapping exceptions**;
- Q2-ST-O3: **DEFERRED — D-11**, reopen on first accepted mapping exception;
- Current subject kinds: the five accepted D1 values, unchanged;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5 and BR1–BR5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.

## Next bounded step

Re-run the bounded BR1–BR5 comparison once under accepted D1–D5, Q2-RI, and Q2-ST, removing its provisional status, and then prepare the separate Project Owner Q2 persisted-representation decision. This decision authorizes no implementation.
