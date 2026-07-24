# ADW-01 — Core Domain Semantics

**Document ID:** ARCH-DOMAIN-001  
**Version:** 1.0  
**Status:** ADW-01 decision set complete — D01–D10 all APPROVED (D06/D07/D09/D10 CLOSED)  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Foundation:** `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`  
**Decision register:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`  
**State constitution:** `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md`  
**Relationship constitution:** `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md`  
**Historical integrity constitution:** `00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md`  
**Authority Hierarchy and Vocabulary Baseline:** `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`

---

## 1. Purpose

ADW-01 defines the stable semantic foundation required for Bizzi to represent, govern, coordinate, execute, and evaluate enterprise activity.

`Core Domain Semantics` is the sole approved name of ADW-01. The former term `Domain Core` is retired from the active architecture vocabulary.

---

## 2. Governing Question

> What are the smallest stable concepts, ownership rules, state semantics, and relationships required to describe how an enterprise operates in Bizzi?

---

## 3. Foundation Model

Workspace is the primary ownership, authorization, governance, and isolation boundary.

Within a Workspace, Bizzi recognizes five fundamental domain concepts:

```text
Workspace
  ├── Enterprise Object
  ├── Actor
  ├── Work Item
  ├── Decision
  └── Business Operation
```

| Concept | Governing question |
|---|---|
| Enterprise Object | What does the enterprise manage? |
| Actor | Who participates or acts? |
| Work Item | What work must be organized? |
| Decision | What has been authoritatively determined? |
| Business Operation | How is an authorized intent or Decision realized? |

No concept replaces another.

---

## 4. Primary Construction

```text
Decision
+
Business Operation
```

Decision is the governance center of enterprise activity.

Business Operation is the operational center of enterprise activity.

Work Items organize required work. Runtime Sessions represent execution attempts. Actions record what was performed. Results record what execution produced. Domain aggregates validate and own authoritative state. Domain Events record significant committed facts.

---

## 5. Enterprise Behaviour Chain

```text
Intent
  -> Decision
  -> Authorization
  -> Business Operation
  -> Execution Plan
  -> Work Items and Runtime Sessions
  -> Actions
  -> Results
  -> Domain Validation
  -> State Transition
  -> Domain Event
  -> Business Outcome Evaluation
```

This chain is semantic rather than a mandatory synchronous workflow. No governed action may lack an auditable authority basis.

---

## 6. Decision Status

| Decision | Subject | Status |
|---|---|---|
| D01 | Primary Boundary | APPROVED |
| D02 | Core Business Abstraction | APPROVED |
| D03 | Work Model | APPROVED |
| D04 | Task versus Execution | APPROVED |
| D05 | Actor Model | APPROVED |
| D06 | Decision and Business Operation Semantics | APPROVED — CLOSED |
| D07 | State Semantics | APPROVED — CLOSED |
| D08 | Aggregate Strategy | APPROVED |
| D09 | Relationship Model | APPROVED — CLOSED |
| D10 | Deletion and Supersession | APPROVED — CLOSED |

---

## 7. Approved Decisions Summary

### D01 — Primary Boundary

Workspace is the primary ownership, authorization, governance, and isolation boundary for workspace-scoped business state.

### D02 — Core Business Abstraction

Enterprise Object is the shared platform abstraction for durable business-relevant things while specialized types retain explicit contracts and invariants.

### D03 — Work Model

Work Item is the shared representation of governed business work. Task, Case, and Project are specialized Work Item types.

### D04 — Task versus Execution

Task and Runtime Session are separate aggregates. A successful Runtime Session does not automatically complete a Task.

### D05 — Actor Model

Actor is the stable operational identity of a human, agent, service, or external participant. Actor is distinct from User Account, Role, Agent Definition, and Runtime Session.

### D06 — Decision and Business Operation Semantics

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21  
**Closure date:** 2026-07-21

Decision and Business Operation are separate, first-class Workspace-scoped domain concepts. Decision defines an authoritative determination. Business Operation coordinates realization of an intent or Decision. Technical execution success does not automatically imply business success.

### D07 — State Semantics

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-22  
**Closure date:** 2026-07-22  
**Canonical decision:** `D07_STATE_SEMANTICS.md`

D07 establishes the Bizzi State Constitution:

1. authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority;
2. execution, workflow, events, projections, reports, caches, analytics, and AI outputs do not own business truth;
3. State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another;
4. significant transitions additionally produce durable immutable transition records;
5. Phase, Status, Outcome, Progress, and Health are separate semantic dimensions;
6. authority to request, approve, validate, and commit change are distinct powers;
7. competing mutations require expected-version or equivalent conflict protection;
8. repeated requests must produce at most one authoritative business effect;
9. aggregate mutation and durable audit/publication intent share an explicit consistency boundary;
10. reconstruction follows authoritative ownership and committed history rather than events, projections, reports, caches, or AI interpretations.

D07 routes detailed authorization to ADW-03, runtime state to ADW-05, audit and provenance to ADW-07, persistence mechanics to ADW-08, typed relationships to D09, and deletion/supersession semantics to D10.

### D08 — Aggregate Strategy

Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root. Task, Case, and Project are separate aggregate roots.

### D09 — Relationship Model

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-23  
**Closure date:** 2026-07-23  
**Canonical decision:** `D09_RELATIONSHIP_MODEL.md`

D09 establishes the Bizzi Relationship Constitution: eleven canonical relationships among Enterprise Object, Actor, Work Item, Decision, Business Operation, and Runtime Session, each with an explicit category, ownership assignment, reference direction, cardinality, and mutation authority. No relationship among these six concepts transfers ownership, grants cross-aggregate mutation authority, or creates a universal super-aggregate. The inverse view of every relationship is a derived projection of one authoritative forward assertion, never an independent fact.

### D10 — Deletion and Supersession

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-23  
**Closure date:** 2026-07-23  
**Canonical decision:** `D10_DELETION_AND_SUPERSESSION.md`

D10 establishes the Bizzi Historical Integrity Constitution: Physical Deletion is constitutionally available only to a subject with zero committed relationships, transitions, or attributions referencing it — the narrow exception, never the default. No lifecycle transition ever deletes, rewrites, or retroactively judges a subject's own already-committed history. Supersession creates a new identity rather than mutating an old one. Runtime Session remains freely deletable throughout, because it never owns authoritative state belonging to any other concept.

**ADW-01's decision set is complete: D01–D10 constitute the full Core Domain Semantics baseline.**

---

## 8. Domain Ownership Rules

- Enterprise Object owns specialized business state and invariants.
- Actor owns operational identity and historical attribution.
- Work Item owns work-coordination lifecycle and accepted work outcome.
- Decision owns authoritative determination, authority basis, conditions, status, and supersession history.
- Business Operation owns operational objective, coordination history, execution trace, validation progress, completion criteria, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.
- Domain Event records a committed fact and is not the source of authoritative operational state.
- Projection represents derived observation and is never the silent owner of domain truth.

Business Operation coordinates but does not absorb foreign aggregates.

---

## 9. State Semantics Binding Rules

The following D07 rules are binding for all downstream ADWs:

1. request is not commitment;
2. validation is not mutation;
3. mutation is not publication;
4. publication is not projection;
5. projection is not authority;
6. technical completion is not business outcome;
7. Phase, Status, Outcome, Progress, and Health must not be collapsed into one universal authoritative field;
8. competing state changes require explicit concurrency protection;
9. retries require idempotent business-effect semantics;
10. cross-aggregate consistency requires explicit coordination;
11. reconstruction prefers owning aggregate state and committed transition history;
12. AI output remains advisory until accepted through a governed domain process.

---

## 10. Decision Set Status

No decisions remain open within ADW-01. D01–D10 are all approved; D09 and D10's canonical decisions are summarized in §7 above.

Responsibilities each explicitly and correctly deferred beyond ADW-01's own scope, per D07's, D09's, and D10's own deferred-responsibilities records:

- ADW-02 (Identity and Workspace Boundary): identity, membership, and Actor's relationship to User Account/credential mechanics.
- ADW-03 (Authorization and Policy): authorization policy evaluation, roles, delegation.
- ADW-05 (Agent Runtime): Runtime Session's internal execution-attempt state machine.
- ADW-07 (Events, Audit, and Provenance): the durable audit/event record schema.
- ADW-08 (Repository and Persistence): physical persistence, transactions, and projection mechanics.
- A future business/compliance decision, outside any ADW chapter: retention duration for preserved historical records (D10 §9).

---

## 11. Workshop Completion Criteria

ADW-01 is complete when:

1. D01 through D10 have explicit Project Owner decisions;
2. the Decision Register is synchronized with this chapter;
3. the root Architecture Specification references the final semantic model;
4. the domain vocabulary contains no unresolved collisions;
5. aggregate ownership and typed relationship rules are explicit;
6. deletion, supersession, reversal, compensation, and retention semantics are resolved;
7. follow-up responsibilities are assigned to later ADWs without semantic gaps.

---

## 12. Current Progress

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04: APPROVED
D05: APPROVED
D06: APPROVED — CLOSED
D07: APPROVED — CLOSED
D08: APPROVED
D09: APPROVED — CLOSED
D10: APPROVED — CLOSED

ADW-01 decision-level status: COMPLETE.

Governance-level baseline activation (Authority Hierarchy and Vocabulary
Baseline approved per DECISION_0002; repository synchronization across
ARCHITECTURE_SPECIFICATION.md, CLAUDE.md, Gate A, GATE_C_ARCHITECTURE_
DECISION_PROPOSALS.md, and DOMAIN_FOUNDATION.md; and the Architecture
Baseline Resolution signature) remains in progress per the Architecture
Baseline Resolution Package. ADW-01 is not yet the activated official
baseline.
```
