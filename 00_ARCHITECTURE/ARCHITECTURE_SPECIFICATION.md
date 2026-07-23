# Bizzi Platform Architecture Specification

**Document ID:** ARCH-SPEC-001  
**Version:** 0.4-draft  
**Status:** Architecture Decision Workshop baseline — ADW-01 in progress; D09 closed  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Maintainers:** Chief Architect, Architecture Decision Workshop participants  
**Repository path:** `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`

---

## 1. Purpose

This document is the root architecture specification for the Bizzi Platform.

It defines the authoritative architecture hierarchy, governing principles, workshop structure, invariants, and evolution process. Detailed domain meaning is established by the Domain Foundation and approved Architecture Decision Workshop decisions.

---

## 2. Architectural Mission

Bizzi is an enterprise operating platform for modeling, governing, executing, observing, and improving business activity performed by humans, agents, services, and external participants under explicit authority.

The primary semantic construction is:

```text
Decision
+
Business Operation
```

The operating chain is:

```text
Enterprise Strategy and Objectives
  -> Governance and Policy
  -> Decisions
  -> Business Operations
  -> Work Coordination
  -> Runtime and Tools
  -> State Transitions and Outcomes
  -> Audit, Events, Provenance, and Learning
```

AI is a platform capability, not an authority source or sole system boundary. Business state, authorization, accountability, provenance, and human oversight remain first-class concerns.

---

## 3. Source-of-Truth Hierarchy

When architecture artifacts conflict, the following order applies:

1. explicit approved Project Owner and Gate decisions;
2. this Architecture Specification;
3. `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md` for constitutional domain semantics;
4. approved Architecture Decision Records;
5. approved ADW chapter specifications;
6. ADW Decision Registers for exact recorded workshop decisions;
7. security, domain, runtime, persistence, and platform contracts derived from the specification;
8. C4 diagrams and other architecture views;
9. implementation plans and work packages;
10. code comments, examples, drafts, and historical documents.

For ADW-01 specifically:

```text
DOMAIN_FOUNDATION.md
  -> ADW_01_CORE_DOMAIN_SEMANTICS.md
  -> D07_STATE_SEMANTICS.md and other approved constitutional decisions
  -> ADW_01_DECISION_REGISTER.md
  -> downstream contracts and implementation
```

The term `Domain Core` and the path `00_ARCHITECTURE/01_DOMAIN/DOMAIN_CORE.md` are retired from the active architecture baseline.

---

## 4. Fundamental Domain Model

Workspace is the primary ownership, authorization, governance, and isolation boundary.

Within a Workspace, Bizzi recognizes five fundamental concepts:

```text
Workspace
  ├── Enterprise Object
  ├── Actor
  ├── Work Item
  ├── Decision
  └── Business Operation
```

Their authoritative concerns are separate:

- Enterprise Object owns specialized business state and invariants.
- Actor owns operational identity and attribution.
- Work Item owns work coordination and accepted work outcome.
- Decision owns governance determination and authority basis.
- Business Operation owns end-to-end operational objective, execution coordination, validation progress, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.

Business Operation coordinates but does not become a universal super-aggregate.

---

## 5. Architecture Principles

### AP-01. Governed Outcomes First
Business objectives, Decisions, Business Operations, and validated outcomes are primary. Workflows, agents, tools, and infrastructure support them.

### AP-02. Explicit Ownership
Every mutable authoritative state has one owning aggregate or explicitly defined domain authority.

### AP-03. Workspace Isolation by Default
Cross-workspace access is explicit, authorized, auditable, and exceptional.

### AP-04. Actor Context Is Authoritative
Identity, Workspace, role, delegation, and execution origin are resolved from trusted context rather than untrusted identifiers.

### AP-05. Governance and Execution Are Separate
Decision establishes what should occur. Business Operation coordinates realization. Runtime performs attempts. None may be inferred solely from another.

### AP-06. Technical Success Is Not Business Success
Successful execution does not automatically establish accepted Result, completed Work Item, completed Business Operation, or achieved business outcome.

### AP-07. State Ownership
Only the owning aggregate or explicitly authorized domain process may commit authoritative State Transitions.

### AP-08. Derived State Is Not Domain Truth
Projections, indexes, caches, dashboards, search models, events, audit records, analytics, and AI interpretations do not silently become authoritative state.

### AP-09. Orthogonal State Dimensions
Phase, Status, Outcome, Progress, and Health represent separate semantic dimensions and must not be collapsed into one universal authoritative field.

### AP-10. Versioned and Idempotent Change
Competing state changes require expected-version or equivalent conflict protection. Repeated requests must produce at most one authoritative business effect.

### AP-11. Reliable Side Effects
Aggregate mutation and durable audit/publication intent use an explicit consistency boundary. Loss of accountability-critical effects is prohibited.

### AP-12. Events Follow Commit
Domain Events record committed significant facts. They do not independently authorize or mutate authoritative state.

### AP-13. Reconstructable Truth
Recovery and reconstruction prefer owning aggregate state and committed transition history over events, projections, reports, caches, analytics, or AI interpretations.

### AP-14. Auditable by Design
Significant Decisions, Business Operations, State Transitions, policy outcomes, attribution, and external effects are reconstructable.

### AP-15. Provider Independence
Domain contracts remain independent of specific AI providers, models, databases, frameworks, or integrations unless an approved ADR permits coupling.

### AP-16. Historical Truth Preservation
Cancellation, reversal, compensation, supersession, and correction preserve prior Decisions, Operations, attribution, state versions, and outcomes.

### AP-17. Evolution Through Decisions
Material changes require impact analysis, explicit approval, and synchronized updates to affected sources of truth.

---

## 6. Target Architecture Shape

```text
Experience Layer
  - Command Center
  - Administrative interfaces
  - External APIs

Application Layer
  - Use cases
  - Decision coordination
  - Business Operation orchestration
  - Work coordination
  - Human approval coordination
  - Explicit cross-aggregate transition coordination

Domain Layer
  - Enterprise Objects
  - Actors
  - Work Items
  - Decisions
  - Business Operations
  - State ownership, dimensions, invariants, and transitions

Platform Services
  - Identity and ActorContext
  - Authorization and policy evaluation
  - Runtime and tools
  - Knowledge and memory
  - Audit, events, provenance
  - Integration and extension services

Persistence and Infrastructure
  - Repository implementations
  - Transactions and outbox
  - Databases, queues, storage, caches
  - Projection rebuild and recovery mechanisms
  - Observability and operational controls
```

Outer layers depend on stable inner contracts. Domain logic remains independent of frameworks, providers, and transport protocols.

---

## 7. Architecture Decision Workshop Structure

| Session | Chapter | Purpose | Planned path |
|---|---|---|---|
| ADW-01 | Core Domain Semantics | Define platform domain vocabulary, primary construction, ownership, state semantics, relationships, and historical rules. | `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md` |
| ADW-02 | Identity and Workspace Boundary | Define identity, memberships, Workspace isolation, ActorContext, and context propagation. | `00_ARCHITECTURE/02_IDENTITY/IDENTITY_AND_WORKSPACE.md` |
| ADW-03 | Authorization and Policy | Define roles, permissions, policies, delegation, escalation, and enforcement boundaries. | `00_ARCHITECTURE/03_SECURITY/AUTHORIZATION_AND_POLICY.md` |
| ADW-04 | Enterprise Object Model | Define canonical enterprise-object types, relationships, lifecycles, and ownership rules. | `00_ARCHITECTURE/04_ENTERPRISE_MODEL/ENTERPRISE_OBJECT_MODEL.md` |
| ADW-05 | Agent Runtime | Define agents, capabilities, tools, prompts, execution lifecycle, retries, and human intervention. | `00_ARCHITECTURE/05_RUNTIME/AGENT_RUNTIME.md` |
| ADW-06 | Knowledge and Memory | Define knowledge states, memory, context, validation, learning, retention, and retrieval. | `00_ARCHITECTURE/06_KNOWLEDGE/KNOWLEDGE_AND_MEMORY.md` |
| ADW-07 | Events, Audit, and Provenance | Define event semantics, immutable audit, provenance, correlation, and sensitive-data handling. | `00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md` |
| ADW-08 | Repository and Persistence | Define repositories, transactions, outbox, idempotency, storage, indexing, and retention. | `00_ARCHITECTURE/08_PERSISTENCE/REPOSITORY_AND_PERSISTENCE.md` |
| ADW-09 | Platform Extension Model | Define integrations, connectors, plugins, MCP-compatible interfaces, and extension boundaries. | `00_ARCHITECTURE/09_PLATFORM/PLATFORM_EXTENSION_MODEL.md` |
| ADW-10 | Governance and Architecture Freeze | Resolve conflicts, approve the specification, and close Gate C. | `00_ARCHITECTURE/10_GOVERNANCE/ARCHITECTURE_FREEZE.md` |

---

## 8. ADW-01 Decision State

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
| D10 | Deletion and Supersession | OPEN — NEXT |

D06 establishes `Decision + Business Operation` as the primary domain construction.

D07 establishes the binding Bizzi State Constitution. Its canonical specification is `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md`.

D09 establishes the binding Bizzi Relationship Constitution. Its canonical specification is `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md`.

D10 is the next ADW-01 decision and must define deletion, archival, revocation, reversal, compensation, and retention semantics without violating D07's state-ownership rules or D09's relationship and Historical-classification rules.

---

## 9. Binding D07 State Constitution

The following rules are binding for all downstream architecture:

1. Authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority.
2. Execution, workflow, events, projections, reports, caches, analytics, and AI outputs do not own business truth.
3. State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another.
4. Significant transitions additionally produce durable immutable transition records.
5. Phase, Status, Outcome, Progress, and Health are separate semantic dimensions.
6. Authority to request, approve, validate, and commit change are distinct powers.
7. Competing mutations require expected-version or equivalent conflict protection.
8. Repeated requests must produce at most one authoritative business effect.
9. Aggregate mutation and durable audit/publication intent share an explicit consistency boundary.
10. Domain Events record committed facts and do not independently mutate authoritative state.
11. Projections are derived, rebuildable, version-aware, and may be stale.
12. Reconstruction follows owning aggregate state and committed transition history.

---

## 10. Architecture Invariants

1. Every workspace-scoped business object belongs to exactly one Workspace unless an approved model defines otherwise.
2. Workspace scope is derived from trusted execution context.
3. Every governed action has an attributable effective Actor and authority basis.
4. Decision, Business Operation, Work Item, Runtime Session, Result, State Transition, and Domain Event remain distinct concepts.
5. Only the owning aggregate or authorized domain process commits authoritative state.
6. Command requests change; Result reports output; Domain Event records a committed fact.
7. Runtime state does not automatically determine Work Item, Business Operation, Decision, or Enterprise Object state.
8. Phase, Status, Outcome, Progress, and Health remain separate dimensions.
9. Projections and read models are derived, rebuildable, source-version-aware, and explicitly allowed to be stale.
10. Significant transitions retain attribution, authority basis, reason, causation, and version history.
11. Competing mutations use expected-version or equivalent concurrency protection.
12. Retries and duplicate delivery produce at most one authoritative business effect.
13. Aggregate mutation and required durable audit/publication intent use an explicitly documented consistency boundary.
14. Publication failure after commit does not erase authoritative business truth.
15. Cross-aggregate consistency uses explicit coordination; hidden distributed mutation is prohibited.
16. Domain services do not depend directly on FastAPI, database drivers, provider SDKs, or transport objects.
17. AI-generated output is not authoritative merely because it was generated by an agent.
18. Audit records are append-oriented and are not the operational source of truth.
19. Compensation and reversal are new governed Operations rather than deletion of history.
20. Recovery prefers owning aggregate state and committed transition history over events and projections.
21. Gate C approval requires explicit review and cannot be inferred from implementation progress.

---

## 11. Required Output of Each ADW Session

Each session must produce:

1. problem and decision scope;
2. agreed terminology;
3. options and trade-offs;
4. selected decision and rationale;
5. invariants and ownership rules;
6. lifecycle, state, interface, security, audit, and persistence implications;
7. migration and implementation consequences;
8. synchronized chapter and decision-register updates;
9. unresolved questions with owner and closure condition;
10. explicit approval status.

A session is complete only when its decision artifacts are recorded and internally consistent.

---

## 12. Change Control

Architecture changes follow this sequence:

1. identify the problem or inconsistency;
2. classify impact;
3. prepare the decision and alternatives;
4. assess affected chapters, diagrams, APIs, schemas, work packages, and code;
5. obtain required approval;
6. update all authoritative artifacts in the same stabilization set;
7. preserve superseded decisions and history.

Silent architecture drift is prohibited.

---

## 13. Gate C v1.1 Completion Criteria

Gate C is ready for final approval only when:

- all ten ADW chapters are approved or ready for approval;
- all material Decisions are closed or explicitly deferred outside the implementation boundary;
- terminology is synchronized across foundation, chapters, registers, ADRs, diagrams, plans, and contracts;
- state ownership, authority, consistency, audit, eventing, persistence, security, and runtime boundaries are explicit;
- D09 and D10 are resolved and ADW-01 is closed;
- architecture risks and implementation consequences are recorded;
- Project Owner explicitly approves Gate C.

---

## 14. Current Architecture Status

```text
Gate C v1.1: IN PROGRESS
ADW-01: IN PROGRESS
D06: APPROVED — CLOSED
D07: APPROVED — CLOSED
D08: APPROVED
D09: APPROVED — CLOSED
D10: OPEN — NEXT
Next constitutional step: D10 — Deletion and Supersession
```
