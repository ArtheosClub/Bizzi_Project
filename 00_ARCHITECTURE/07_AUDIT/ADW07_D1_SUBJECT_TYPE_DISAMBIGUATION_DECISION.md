# ADW-07 — Q2 D1 Subject-Type Disambiguation Decision

**Workshop:** ADW-07 — Events, Audit and Provenance  
**Workshop Status:** OPEN  
**Decision:** Q2 / D1 — Subject-Type Disambiguation  
**Decision Status:** ACCEPTED  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-08-30

## Decision

A persisted AuditRecord subject reference MUST include an explicit durable subject-type discriminator as part of its durable reference contract. The discriminator’s committed value MUST identify exactly one of the current Q2 subject types: Workspace, EnterpriseObject, User, WorkspaceMembership, or Task. Type qualification within a durable subject identity satisfies this rule. D1 does not decide the physical placement or persistence mechanism of the discriminator.

## Scope

This decision closes **D1 — subject-type disambiguation only**.

It establishes that the durable subject-reference contract must make subject type explicit and unambiguous across the five current Q2 subject types.

## Explicit non-decisions

This decision does **not** decide:

- D2 — reference-level workspace semantics;
- D3 — subject deletion / historical-resolution policy;
- D4 — DB-enforced referential-integrity policy;
- D5 — subject-type-set / future-extensibility requirement;
- persistence shape;
- physical placement of the discriminator;
- FK strategy or database-level integrity;
- migration policy;
- ownership;
- runtime resolver/API contract;
- actor attribution;
- implementation;
- final Q2 persisted representation.

It does not approve or reject N1–N5 and does not approve GC-002 Alternative B.

## Consequence for Q2 state

- D1: **CLOSED — ACCEPTED**.
- D2–D5: **OPEN**.
- Q2 persisted representation: **OPEN**.
- ADW-07: **OPEN**.
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.
- WP18 dependency: **NOT RESTORED**.

The accepted D1 rule is an input to subsequent Q2 decision work. It must not be used to answer D2–D5 by implication.

## Next bounded step

Proceed separately to **D2 options / evaluation**. Do not begin implementation and do not record a final Q2 persisted-representation decision until the remaining decision surfaces have been explicitly addressed to the extent required.