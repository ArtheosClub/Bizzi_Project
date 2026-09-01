# ADW-07 — Accepted Decision Record Lifecycle Decision

**Workshop:** ADW-07 — Events, Audit, and Provenance  
**Workshop Status:** OPEN  
**Decision:** Accepted ADW-07 decision record lifecycle  
**Decision Status:** ACCEPTED  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-08-30  
**Scope:** Governance of ACCEPTED ADW-07 decision records only

## Decision

Once an ADW-07 decision record is **ACCEPTED**, its canonical accepted text **MUST NOT be edited in place**.

Any later correction, clarification, identifier reconciliation, amendment, or supersession **MUST** be recorded through a separate explicit authority artifact that:

1. identifies the affected accepted record;
2. states the exact effect of the later authority; and
3. preserves the original accepted record as the historical record of what was accepted at that time.

Pointer/index artifacts MAY improve discoverability but MUST NOT alter, restate, or silently correct canonical normative meaning.

## Rationale

ADW-07 now contains multiple accepted decision records, including embedded Blocks and separate D-level authority files. Before this decision, no approved lifecycle rule established whether those accepted records could be edited in place.

That ambiguity became material when historical Q2 records retained the original framework label `D4 — DB-enforced referential integrity`, while a later accepted decision used `D4` for Subject Reference Semantics and the unresolved RI surface was reconciled under the identifier `Q2-RI`.

Editing earlier accepted records in place would obscure what the Project Owner actually accepted at the time and would create a mutable-authority precedent. A separate reconciliation/amendment mechanism preserves both historical provenance and current interpretability.

## Consequences

### 1. Accepted ADW-07 records are immutable historical authority records

Accepted Blocks and accepted standalone ADW-07 decision files are not silently rewritten after acceptance.

This applies to normative text and to later corrections whose apparent editorial nature could alter how a decision is interpreted, addressed, scoped, or traced.

### 2. O-1 historical identifier references are not repaired in place

Accepted D1 and D2 records currently contain historical references to `D4` as the then-open DB-enforced referential-integrity surface.

Those records MUST NOT be edited merely to replace `D4` with `Q2-RI`.

The future accepted Q2-RI authority MUST provide the required identifier reconciliation. That reconciliation must make clear that historical references to `D4 — DB-enforced referential integrity` refer to the unresolved surface now named `Q2-RI`, not to the later accepted `D4 — Subject Reference Semantics` decision.

### 3. Amendments / reconciliations / supersession are separate authority

A later authority may correct, clarify, amend, reconcile, or supersede an accepted ADW-07 decision, but it must do so explicitly rather than by replacing the original accepted text.

The later artifact must name the affected authority and state whether it:

- corrects an identifier or traceability issue without changing substantive meaning;
- clarifies an ambiguity;
- amends part of the decision;
- or supersedes the decision in whole or in part.

### 4. Decision index remains pointer-only

`ADW07_DECISION_INDEX.md` remains a discoverability mechanism only. It must not become a second source of normative decision wording or an implicit correction layer.

### 5. Recording-location convention remains a separate question

This lifecycle decision does **not** establish that all future ADW-07 decisions must be embedded in `EVENTS_AUDIT_AND_PROVENANCE.md` or must be recorded as separate files.

Current repository placement may be described factually for navigation. Any general future recording-location convention remains separate governance unless explicitly decided.

## Explicit non-decisions

This decision does not:

- change the substance of Blocks 1–4 or D1–D5;
- edit accepted D1/D2 historical identifier references;
- decide Q2-RI;
- decide Q2-ST;
- decide the final Q2 representation;
- establish a lifecycle rule for ADRs or other document classes;
- establish a universal ADW recording-location convention;
- authorize WP19 implementation.

## Current governance effect

From this decision forward:

**ACCEPTED ADW-07 RECORD → NO IN-PLACE EDIT → LATER CHANGE THROUGH SEPARATE EXPLICIT AUTHORITY.**

Q2-RI is the next substantive Q2 decision surface. Its future authority must contain the historical `D4`/`Q2-RI` reconciliation required above.