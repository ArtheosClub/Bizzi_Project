# Bizzi Platform Architecture Specification

**Document ID:** ARCH-SPEC-001  
**Version:** 0.1-draft  
**Status:** Architecture Decision Workshop baseline  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Maintainers:** Chief Architect, Architecture Decision Workshop participants  
**Repository path:** `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`

---

## 1. Purpose

This document is the root architecture specification for the Bizzi Platform.

It defines the authoritative structure, governing principles, decision hierarchy, and evolution process for the platform architecture. It is the primary entry point for developers, architects, AI agents, reviewers, and governance participants who need to understand how Bizzi is designed and how architectural decisions are made.

The detailed architecture will be developed through ten Architecture Decision Workshop sessions. Each session will produce a dedicated chapter, one or more architecture decisions, and synchronized updates to related models and implementation plans.

This specification does not replace Architecture Decision Records, C4 diagrams, domain models, implementation work packages, or gate reviews. It governs how those artifacts relate to one another and identifies which source prevails when documents conflict.

---

## 2. Architectural Mission

Bizzi is designed as an AI-orchestrated business operating platform for managing enterprise capabilities, processes, tasks, decisions, knowledge, agents, tools, and human approvals within explicit governance and security boundaries.

The platform must support the operating chain:

```text
Vision
  -> Capabilities
  -> Processes
  -> Functions
  -> Agents and Humans
  -> Tools
  -> Actions
  -> Decisions
  -> Results
  -> Audit and Learning
```

AI is a platform capability, not the sole system boundary. Business state, authorization, auditability, provenance, and human accountability remain first-class architectural concerns.

---

## 3. Scope

This specification governs the architecture of:

- platform domain boundaries;
- workspace and tenancy isolation;
- identity, actor context, authorization, and policy enforcement;
- enterprise objects and their lifecycles;
- AI agent definitions, runtime execution, tools, and human intervention;
- knowledge, context, and memory;
- events, audit, provenance, correlation, and traceability;
- repository contracts, persistence, transactions, and retention;
- extension mechanisms, integrations, plugins, connectors, and MCP-compatible capabilities;
- architecture governance, change control, and gate approval.

The specification applies to the MVP and to future platform evolution unless a later approved version explicitly supersedes it.

---

## 4. Source-of-Truth Hierarchy

Architecture artifacts form a governed hierarchy.

When two artifacts conflict, the following order of precedence applies:

1. approved Project Owner decisions and approved gate decisions;
2. this Architecture Specification;
3. accepted Architecture Decision Records;
4. approved chapter specifications under `00_ARCHITECTURE/`;
5. security, domain, runtime, persistence, and platform contracts derived from the specification;
6. C4 diagrams and other architecture views;
7. implementation plans and work packages;
8. code comments, examples, drafts, and historical documents.

A lower-level artifact must not silently override a higher-level artifact. Any discovered conflict must be recorded and resolved through the architecture decision process.

---

## 5. Architecture Principles

### AP-01. Process First

Business processes and governed outcomes are primary. Agents, models, tools, and infrastructure exist to execute or support those processes.

### AP-02. Explicit Ownership

Every mutable business object, decision, task, runtime execution, policy, and architecture artifact must have an identifiable owner or accountable authority.

### AP-03. Workspace Isolation by Default

Workspace boundaries are mandatory security and data boundaries. Cross-workspace access must be explicit, authorized, auditable, and exceptional.

### AP-04. Actor Context Is Authoritative

Identity, workspace, role, delegation, and execution origin must be resolved into a trusted ActorContext. Client-supplied identifiers must not independently establish authorization scope.

### AP-05. Repository-Enforced Visibility

Repositories enforce workspace and visibility boundaries. Services enforce business rules. Authorization components evaluate access policy. These responsibilities must not be collapsed into an ambiguous layer.

### AP-06. Human Accountability

AI may analyze, recommend, generate, coordinate, and execute within policy. Decisions requiring human authority remain attributable to an accountable human or formally delegated authority.

### AP-07. Auditable by Design

Significant actions, decisions, state transitions, policy outcomes, and external effects must be reconstructable through audit and provenance records.

### AP-08. Provider Independence

Domain and platform contracts must not depend on a specific AI provider, model vendor, database-specific feature, or external integration unless an accepted ADR explicitly permits the dependency.

### AP-09. Versioned Behavior

Agent definitions, prompts, policies, capabilities, schemas, APIs, and architectural contracts that affect behavior must be versioned.

### AP-10. Secure Data Minimization

The platform stores only the sensitive data required for an approved purpose. Secrets, credentials, personal data, prompts, responses, context, memory, and logs must follow explicit classification, masking, retention, and deletion rules.

### AP-11. Reliable Side Effects

Business state changes, audit records, and emitted events must use a defined consistency model. Best-effort side effects are not permitted where loss would break accountability or system correctness.

### AP-12. Evolution Through Decisions

Material architectural changes require an Architecture Decision Record, impact analysis, synchronization of affected artifacts, and approval at the appropriate governance level.

---

## 6. Target Architecture Shape

The target platform is organized into the following logical layers:

```text
Experience Layer
  - Command Center
  - Administrative interfaces
  - External API clients

Application Layer
  - Use cases
  - Orchestration
  - Workflow coordination
  - Human approval coordination

Domain Layer
  - Enterprise objects
  - Tasks, cases, decisions, and relationships
  - Domain invariants and lifecycle rules

Platform Services
  - Identity and ActorContext
  - Authorization and policy evaluation
  - Agent runtime
  - Knowledge and memory
  - Audit, events, and provenance
  - Integration and extension services

Persistence and Infrastructure
  - Repository implementations
  - Transaction and outbox mechanisms
  - Databases, queues, object storage, caches
  - Observability and operational controls
```

The architecture must preserve dependency direction: outer layers may depend on stable inner contracts, while domain logic must remain independent of frameworks, providers, and transport protocols.

---

## 7. Architecture Decision Workshop Structure

Gate C v1.1 will be completed through ten ordered sessions.

| Session | Chapter | Purpose | Planned path |
|---|---|---|---|
| ADW-01 | Domain Core | Define platform identity, core concepts, boundaries, aggregates, ownership, and terminology. | `00_ARCHITECTURE/01_DOMAIN/DOMAIN_CORE.md` |
| ADW-02 | Identity and Workspace Boundary | Define identity, actors, memberships, workspace isolation, ActorContext, and context propagation. | `00_ARCHITECTURE/02_IDENTITY/IDENTITY_AND_WORKSPACE.md` |
| ADW-03 | Authorization and Policy | Define roles, permissions, profiles, policies, delegation, escalation, and enforcement boundaries. | `00_ARCHITECTURE/03_SECURITY/AUTHORIZATION_AND_POLICY.md` |
| ADW-04 | Enterprise Object Model | Define canonical enterprise entities, relationships, lifecycles, and ownership rules. | `00_ARCHITECTURE/04_ENTERPRISE_MODEL/ENTERPRISE_OBJECT_MODEL.md` |
| ADW-05 | Agent Runtime | Define agents, capabilities, tools, prompts, providers, execution lifecycle, state machine, and human intervention. | `00_ARCHITECTURE/05_RUNTIME/AGENT_RUNTIME.md` |
| ADW-06 | Knowledge and Memory | Define knowledge states, memory, context packages, validation, learning, retention, and retrieval. | `00_ARCHITECTURE/06_KNOWLEDGE/KNOWLEDGE_AND_MEMORY.md` |
| ADW-07 | Events, Audit, and Provenance | Define event semantics, immutable audit, decision provenance, correlation, traceability, and sensitive-data handling. | `00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md` |
| ADW-08 | Repository and Persistence | Define repository contracts, transactions, unit of work, outbox, idempotency, storage, indexing, and retention. | `00_ARCHITECTURE/08_PERSISTENCE/REPOSITORY_AND_PERSISTENCE.md` |
| ADW-09 | Platform Extension Model | Define integrations, connectors, plugins, MCP-compatible interfaces, external agents, SDK boundaries, and marketplace readiness. | `00_ARCHITECTURE/09_PLATFORM/PLATFORM_EXTENSION_MODEL.md` |
| ADW-10 | Governance and Architecture Freeze | Verify consistency, resolve conflicts, approve the specification, and close Gate C. | `00_ARCHITECTURE/10_GOVERNANCE/ARCHITECTURE_FREEZE.md` |

The paths above are reserved. The linked chapter files will be added sequentially as the corresponding workshop sessions are completed.

---

## 8. Required Output of Each ADW Session

Each Architecture Decision Workshop session must produce:

1. a clearly stated problem and decision scope;
2. agreed terminology and definitions;
3. architectural options considered;
4. trade-offs and rejected alternatives;
5. the selected decision and rationale;
6. invariants and non-negotiable rules;
7. interfaces, data, and lifecycle implications;
8. security, privacy, audit, and operational implications;
9. migration or implementation consequences;
10. one or more ADRs where the decision is material;
11. an updated chapter under `00_ARCHITECTURE/`;
12. a list of affected documents, diagrams, work packages, and code boundaries;
13. unresolved questions, each with an owner and closure condition;
14. approval status.

A session is not complete merely because a discussion occurred. It is complete only when its decision artifacts are recorded and internally consistent.

---

## 9. Chapter Status Model

Each architecture chapter uses one of the following statuses:

- `Planned` — reserved but not started;
- `In Workshop` — active decision work;
- `Draft` — written but not fully reviewed;
- `Ready for Approval` — review complete and awaiting authority decision;
- `Approved` — accepted as part of the architecture baseline;
- `Superseded` — replaced by a later approved version;
- `Retired` — intentionally no longer applicable.

The root specification remains `Architecture Decision Workshop baseline` until ADW-10 is approved.

---

## 10. Decision Classification

Architectural decisions are classified by impact:

### Class A — Constitutional

Changes platform identity, core domain boundaries, workspace isolation, accountability, or architecture governance. Requires Project Owner approval and Gate review.

### Class B — Structural

Changes major components, contracts, persistence strategy, runtime lifecycle, authorization model, or extension model. Requires architecture approval and an ADR.

### Class C — Implementation

Selects an implementation approach within an already approved architecture boundary. Requires technical review and may require an ADR when the choice is difficult to reverse.

### Class D — Local

A reversible, low-impact implementation detail that does not alter architecture contracts. Normal engineering review is sufficient.

When classification is uncertain, the decision must be treated as the higher-impact class until reviewed.

---

## 11. Architecture Invariants

The following invariants apply immediately and remain binding unless explicitly superseded by an approved Class A or Class B decision:

1. Every tenant-scoped business object belongs to exactly one workspace unless a future approved model defines a governed cross-workspace object.
2. Workspace scope is derived from trusted execution context, not accepted from an untrusted request as authority.
3. Authorization decisions are explicit and testable.
4. Repository queries must not expose objects outside the authorized visibility scope.
5. Domain services must not depend directly on FastAPI, database drivers, provider SDKs, or transport-specific request objects.
6. Agent execution is represented by a versioned definition and a traceable runtime instance.
7. Human approvals and overrides are attributable and auditable.
8. Audit records are append-oriented and protected from ordinary business mutation.
9. Business state, audit, and event publication use an explicitly documented consistency boundary.
10. Secrets and credentials are never stored in prompts, memory, audit payloads, or ordinary domain records.
11. External side effects support idempotency or an equivalent duplicate-control mechanism where retries are possible.
12. Material decisions retain provenance sufficient to explain who or what decided, on which evidence, under which policy, using which versioned agent or human authority.
13. Architecture documentation and implementation must use the technology direction approved by existing ADRs, including the FastAPI/Python/PostgreSQL baseline, unless superseded by a later accepted ADR.
14. Gate C approval cannot be inferred from implementation progress; it requires explicit architecture review and approval.

---

## 12. Relationship to Existing Gates

### Gate A — Product Definition

Gate A defines the MVP purpose, primary user, first business scenario, value hypothesis, and acceptance criteria. Architecture must enable that approved product scope and must not redefine it silently.

### Gate B — Technical Baseline

Gate B establishes the initial technical baseline and pre-coding readiness. Gate C may refine architecture contracts without invalidating completed Gate B work, provided conflicts are documented and migration consequences are addressed.

### Gate C — Architecture Definition and Freeze

Gate C v1.1 is completed when all ten ADW chapters are approved, required ADRs are accepted, architecture views are synchronized, material contradictions are resolved, and `GATE_C_REVIEW_AND_APPROVAL.md` records an explicit PASS.

### Gate D and Later Gates

Later implementation and release gates must verify conformance to the approved Gate C architecture. Deviations require documented exceptions or new architecture decisions.

---

## 13. Conformance Requirements

A work package, pull request, service, database schema, integration, or agent definition conforms to this specification when it:

- references the applicable approved architecture chapter or ADR;
- respects defined boundaries and invariants;
- does not introduce undocumented cross-layer dependencies;
- includes required authorization, audit, provenance, and idempotency behavior;
- includes tests or evidence appropriate to the architectural risk;
- records any intentional deviation and its approval.

Architecture conformance review must focus on observable contracts and behavior, not only naming or folder structure.

---

## 14. Change Control

Changes to this specification follow this sequence:

1. identify the architectural problem or inconsistency;
2. classify the decision impact;
3. create or update the relevant ADR proposal;
4. assess effects on chapters, diagrams, work packages, schemas, APIs, and code;
5. obtain the required approval;
6. update this root specification when principles, hierarchy, structure, or invariants change;
7. update all affected downstream artifacts in the same change set or record an explicit synchronization work package;
8. mark superseded decisions and preserve decision history.

Silent architecture drift is prohibited.

---

## 15. Review and Approval Model

The Architecture Decision Workshop uses the following roles:

- **Project Owner** — approves constitutional decisions and final Gate C PASS;
- **Chief Architect** — maintains architectural coherence and prepares recommendations;
- **Domain Owner** — validates business meaning and invariants;
- **Security Reviewer** — validates identity, authorization, data protection, and threat implications;
- **Engineering Reviewer** — validates implementability and operational consequences;
- **AI Governance Reviewer** — validates agent behavior, model independence, provenance, human oversight, and safety boundaries;
- **Recorder** — ensures decisions, alternatives, evidence, and unresolved items are captured.

One person may hold multiple roles during the current project phase, but the responsibility represented by each role must still be addressed explicitly.

---

## 16. Gate C v1.1 Completion Criteria

Gate C v1.1 is ready for final approval only when:

- all ten chapters exist and have status `Approved` or `Ready for Approval`;
- every material unresolved decision has an owner and closure date or is explicitly deferred outside the implementation boundary;
- required ADRs are accepted and indexed;
- terminology is consistent across the specification, domain model, C4 views, and implementation plans;
- workspace isolation and authorization boundaries are testable;
- agent runtime and execution state transitions are defined;
- audit, event, provenance, and transaction consistency rules are defined;
- sensitive data handling and retention rules are defined;
- repository, transaction, idempotency, and outbox contracts are defined;
- extension boundaries are defined without exposing provider-specific coupling to the domain;
- Gate A and Gate B dependencies have been checked for contradiction;
- a formal `GATE_C_REVIEW_AND_APPROVAL.md` has been completed;
- the Project Owner records an explicit PASS.

---

## 17. Planned Repository Structure

```text
00_ARCHITECTURE/
├── ARCHITECTURE_SPECIFICATION.md
├── 01_DOMAIN/
│   └── DOMAIN_CORE.md
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

Git does not retain empty directories. Each chapter directory will therefore be created by the commit that adds its first approved or draft chapter artifact.

---

## 18. Open Decisions Register

The following decision areas are intentionally open and will be resolved through the ADW sequence:

| Decision area | Owning session | Current status |
|---|---|---|
| Canonical domain core and aggregate boundaries | ADW-01 | Planned |
| Workspace, organization, tenant, and identity semantics | ADW-02 | Planned |
| Permission profiles, RBAC, ABAC, delegation, and policy evaluation | ADW-03 | Planned |
| Canonical enterprise object taxonomy and relationships | ADW-04 | Planned |
| Agent definition, provider normalization, runtime state machine, and human checkpoints | ADW-05 | Planned |
| Validated knowledge, memory lifecycle, context packaging, and retention | ADW-06 | Planned |
| Audit immutability, sensitive payload policy, event semantics, provenance, and correlation | ADW-07 | Planned |
| Transaction boundary, outbox, repository contracts, idempotency, and persistence | ADW-08 | Planned |
| Plugins, connectors, MCP-compatible interfaces, integrations, and external agents | ADW-09 | Planned |
| Final consistency review, architecture freeze, and Gate C approval | ADW-10 | Planned |

---

## 19. Current Baseline Statement

At this version, the document establishes the architecture governance baseline and reserves the chapter structure. It does not claim that the detailed architecture is frozen or that Gate C has passed.

Current state:

```text
Architecture Specification: BASELINE CREATED
Architecture Decision Workshop: NOT STARTED
Gate C v1.1: IN PREPARATION
Gate C decision: PENDING
```

---

## 20. Approval Record

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Project Owner | Pending | PENDING | — | Final Gate C approval occurs after ADW-10. |
| Chief Architect | Pending | DRAFT BASELINE | — | Root structure prepared for workshop execution. |

---

## 21. Revision History

| Version | Date | Status | Change |
|---|---|---|---|
| 0.1-draft | 2026-07-21 | Architecture Decision Workshop baseline | Created root specification, governing principles, chapter map, decision hierarchy, invariants, and Gate C v1.1 completion criteria. |
