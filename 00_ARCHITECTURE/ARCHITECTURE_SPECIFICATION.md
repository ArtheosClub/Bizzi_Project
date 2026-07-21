# Bizzi Platform Architecture Specification

**Document ID:** ARCH-SPEC-001  
**Version:** 0.2-draft  
**Status:** Architecture Decision Workshop baseline — ADW-01 in progress  
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
6. ADW Decision Registers for the exact recorded workshop decisions;
7. security, domain, runtime, persistence, and platform contracts derived from the specification;
8. C4 diagrams and other architecture views;
9. implementation plans and work packages;
10. code comments, examples, drafts, and historical documents.

A lower-level artifact must not silently override a higher-level artifact. Conflicts must be recorded and resolved through the architecture decision process.

For ADW-01 specifically:

```text
DOMAIN_FOUNDATION.md
  -> ADW_01_CORE_DOMAIN_SEMANTICS.md
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

Projections, indexes, caches, dashboards, search models, events, and audit records do not silently become the authoritative owner of specialized state.

### AP-09. Auditable by Design

Significant Decisions, Business Operations, State Transitions, policy outcomes, attribution, and external effects are reconstructable.

### AP-10. Provider Independence

Domain contracts remain independent of specific AI providers, models, databases, frameworks, or integrations unless an approved ADR permits coupling.

### AP-11. Versioned Behaviour

Agent definitions, policies, prompts, schemas, APIs, Decisions, transition contracts, and other behaviour-affecting artifacts are versioned.

### AP-12. Reliable Side Effects

Aggregate mutation, audit intent, and event publication use an explicit consistency model. Loss of accountability-critical effects is prohibited.

### AP-13. Historical Truth Preservation

Cancellation, reversal, compensation, supersession, and correction preserve prior Decisions, Operations, attribution, and outcomes.

### AP-14. Evolution Through Decisions

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

Domain Layer
  - Enterprise Objects
  - Actors
  - Work Items
  - Decisions
  - Business Operations
  - State ownership and invariants

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
| D07 | State Semantics | IN WORKSHOP |
| D08 | Aggregate Strategy | APPROVED |
| D09 | Relationship Model | OPEN |
| D10 | Deletion and Supersession | OPEN |

D06 establishes `Decision + Business Operation` as the primary domain construction.

D07 is the final major foundational decision before ADW-02. It must define authoritative state, transition semantics, state-domain separation, projection status, concurrency, and consistency boundaries without creating one universal state machine.

---

## 9. Architecture Invariants

1. Every workspace-scoped business object belongs to exactly one Workspace unless an approved model defines otherwise.
2. Workspace scope is derived from trusted execution context.
3. Every governed action has an attributable effective Actor and authority basis.
4. Decision, Business Operation, Work Item, Runtime Session, Result, State Transition, and Domain Event remain distinct concepts.
5. Only the owning aggregate or authorized domain process commits authoritative state.
6. Command requests change; Result reports output; Domain Event records a fact.
7. Runtime state does not automatically determine Work Item, Business Operation, Decision, or Enterprise Object state.
8. Projections and read models are derived, rebuildable, and explicitly allowed to be stale.
9. Significant transitions use concurrency protection and retain attribution and reason.
10. Repositories enforce Workspace visibility; services enforce business rules; authorization components evaluate policy.
11. Domain services do not depend directly on FastAPI, database drivers, provider SDKs, or transport objects.
12. AI-generated output is not authoritative merely because it was generated by an agent.
13. Audit records are append-oriented and are not the operational source of truth.
14. Aggregate mutation, audit intent, and event publication use an explicitly documented consistency boundary.
15. External side effects support idempotency or equivalent duplicate control where retries are possible.
16. Compensation and reversal are new governed Operations rather than deletion of history.
17. Gate C approval requires explicit review and cannot be inferred from implementation progress.

---

## 10. Required Output of Each ADW Session

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

## 11. Change Control

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

## 12. Planned Repository Structure

```text
00_ARCHITECTURE/
├── ARCHITECTURE_SPECIFICATION.md
├── 00_FOUNDATION/
│   └── DOMAIN_FOUNDATION.md
├── 01_DOMAIN/
│   ├── ADW_01_CORE_DOMAIN_SEMANTICS.md
│   └── ADW_01_DECISION_REGISTER.md
├── 02_IDENTITY/
│   └── IDENTITY_AND_WORKSPACE.md
├── 03_SECURITY/
│   └── AUTHORIZATION_AND_POLICY.md
├── 04_ENTERPRISE_MODEL/
│   └── ENTERPRISE_OBJECT_MODEL.md
├── 05_RUNTIME/
│   └── AGENT_RUNTIME.md
├── 06_KNOWLEDGE/
│   └── KNOWLEDGE_AND_MEMORY.md
├── 07_AUDIT/
│   └── EVENTS_AUDIT_AND_PROVENANCE.md
├── 08_PERSISTENCE/
│   └── REPOSITORY_AND_PERSISTENCE.md
├── 09_PLATFORM/
│   └── PLATFORM_EXTENSION_MODEL.md
└── 10_GOVERNANCE/
    └── ARCHITECTURE_FREEZE.md
```

---

## 13. Gate C v1.1 Completion Criteria

Gate C is ready for final approval only when:

- all ten ADW chapters are approved or ready for approval;
- all material Decisions are closed or explicitly deferred outside the implementation boundary;
- terminology is synchronized across foundation, chapters, registers, ADRs, diagrams, plans, and code boundaries;
- Workspace, Actor, authorization, state, runtime, audit, event, persistence, idempotency, retention, and extension rules are testable;
- Gate A and Gate B dependencies have been checked for contradiction;
- `GATE_C_REVIEW_AND_APPROVAL.md` records an explicit Project Owner PASS.

---

## 14. Current Baseline Statement

```text
Architecture Specification: STABILIZED BASELINE v0.2
Domain Foundation: STABILIZED BASELINE
ADW-01: IN PROGRESS
D06: APPROVED — CLOSED
D07: IN WORKSHOP
Gate C v1.1: IN PREPARATION
Gate C decision: PENDING
```

---

## 15. Revision History

| Version | Date | Status | Change |
|---|---|---|---|
| 0.1-draft | 2026-07-21 | Workshop baseline | Created root specification, chapter map, hierarchy, principles, and Gate C criteria. |
| 0.2-draft | 2026-07-21 | Architecture stabilization | Retired `Domain Core`; synchronized Domain Foundation, ADW-01, Decision Register, and root specification; closed D06; opened D07 State Semantics. |
