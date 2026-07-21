# ADW-01 — Domain Core

**Document ID:** ARCH-DOMAIN-001  
**Version:** 0.1-draft  
**Status:** Architecture Decision Workshop draft  
**Architecture Gate:** Gate C v1.1  
**Workshop:** ADW-01 — Domain Core  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Maintainers:** Chief Architect, Domain Architecture participants  
**Parent specification:** `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`

---

## 1. Purpose

This document defines the domain core of the Bizzi Platform.

Its purpose is to establish a stable business vocabulary, identify the primary domain boundaries, define the first set of aggregate roots and ownership rules, and prevent infrastructure, AI-provider, persistence, or interface concerns from becoming part of the core business model.

This chapter is the working specification for Architecture Decision Workshop ADW-01. It becomes authoritative only after explicit approval by the Project Owner and synchronization with the root Architecture Specification and the Architecture Decision Register.

---

## 2. Workshop Objective

ADW-01 must answer the following architectural question:

> What are the smallest stable concepts required to describe how Bizzi represents, governs, coordinates, executes, and evaluates business activity?

The session must produce decisions that remain valid independently of:

- programming language;
- web framework;
- database engine;
- LLM provider;
- user interface;
- deployment topology;
- integration mechanism.

---

## 3. Domain Mission

Bizzi is an AI-orchestrated business operating platform.

The platform represents an enterprise as a governed system of capabilities, processes, functions, actors, agents, tools, tasks, decisions, evidence, and results.

The core operating chain is:

```text
Vision
  -> Capabilities
  -> Processes
  -> Functions
  -> Actors and Agents
  -> Tasks and Actions
  -> Decisions
  -> Results
  -> Audit and Learning
```

The domain core must support this chain without assuming that AI is always involved. Humans, software services, external systems, and AI agents are all possible participants in enterprise activity.

---

## 4. Domain Boundaries

The Bizzi architecture is divided into the following high-level domains.

### 4.1 Enterprise Design Domain

Represents how an enterprise defines what it intends to achieve and how work is organized.

Primary concepts:

- Vision;
- Objective;
- Capability;
- Process;
- Function;
- Policy;
- Responsibility;
- Authority;
- Escalation route.

### 4.2 Work Coordination Domain

Represents executable business work and its coordination.

Primary concepts:

- Work Item;
- Task;
- Case;
- Project;
- Assignment;
- Dependency;
- Approval;
- Decision;
- Result.

### 4.3 Actor and Agent Domain

Represents participants that may perform, request, approve, observe, or govern work.

Primary concepts:

- Actor;
- Human Actor;
- Service Actor;
- Agent Definition;
- Agent Instance;
- Role;
- Capability Assignment;
- Authority Assignment.

Detailed identity, workspace membership, authentication, and authorization rules belong to ADW-02 and ADW-03.

### 4.4 Knowledge and Evidence Domain

Represents information used to understand business context and justify decisions.

Primary concepts:

- Knowledge Item;
- Memory Item;
- Document;
- Evidence;
- Context Package;
- Source;
- Provenance Reference.

Detailed memory and knowledge lifecycle rules belong to ADW-06.

### 4.5 Execution Domain

Represents the runtime performance of work by agents, humans, services, or tools.

Primary concepts:

- Execution Request;
- Runtime Session;
- Action;
- Tool Invocation;
- Human Intervention;
- Execution Result;
- Failure;
- Retry.

Detailed runtime rules belong to ADW-05.

### 4.6 Governance and Assurance Domain

Represents control, traceability, accountability, and review.

Primary concepts:

- Decision Record;
- Audit Record;
- Domain Event;
- Policy Evaluation;
- Exception;
- Escalation;
- Review;
- Approval;
- Provenance Chain.

Detailed event, audit, and provenance rules belong to ADW-07.

---

## 5. Core Domain Vocabulary

The following terms are reserved and must be used consistently across architecture documents, APIs, code, database schemas, user interfaces, and AI-agent instructions.

### 5.1 Workspace

A Workspace is the primary isolation, ownership, and governance boundary of the platform.

A Workspace contains enterprise configuration, actors, agents, business objects, work items, policies, knowledge, executions, events, and audit records that belong to one governed operating context.

Proposed invariant:

> Every business-state object belongs to exactly one Workspace unless explicitly classified as platform-global metadata.

Final tenancy and identity semantics are decided in ADW-02.

### 5.2 Enterprise Object

An Enterprise Object is a durable, workspace-owned representation of a business-relevant thing that has identity, lifecycle, ownership, state, relationships, and governance requirements.

Examples may include:

- customer;
- supplier;
- employee;
- contract;
- invoice;
- shipment;
- asset;
- opportunity;
- project;
- regulatory obligation.

Enterprise Object is a platform abstraction, not a single universal database table and not a replacement for specialized domain entities.

### 5.3 Work Item

A Work Item is the abstract representation of business work requiring coordination, execution, observation, or completion.

Task, Case, and Project are specialized Work Item types.

A Work Item may:

- reference one or more Enterprise Objects;
- be assigned to humans, agents, or services;
- contain dependencies and deadlines;
- require approvals;
- produce decisions and results;
- generate events and audit records.

### 5.4 Task

A Task is a bounded unit of work with a clear objective, lifecycle, responsible party, expected result, and completion condition.

A Task is not the same as a runtime execution.

A Task may require:

- zero executions when completed manually;
- one execution;
- multiple executions;
- human approval after execution;
- rework following rejection or failure.

### 5.5 Case

A Case is a governed collection of related work, evidence, decisions, and interactions addressing one business situation over time.

A Case may contain multiple Tasks and may remain open while individual Tasks are completed.

Examples:

- customer complaint;
- contract review;
- compliance investigation;
- incident resolution;
- supplier onboarding.

### 5.6 Project

A Project is a planned collection of coordinated work items directed toward a defined outcome, scope, timeline, and governance structure.

A Project may contain Tasks, Cases, milestones, dependencies, decisions, and results.

### 5.7 Action

An Action is an atomic attempt by an Actor to change state, obtain information, invoke a tool, communicate, decide, or produce a result.

An Action occurs within a governed context and must be attributable to an Actor.

### 5.8 Decision

A Decision is a governed conclusion that selects, approves, rejects, prioritizes, classifies, or commits to a course of action.

A Decision must identify:

- decision subject;
- deciding Actor;
- authority basis;
- inputs and evidence;
- outcome;
- time of decision;
- applicable policy;
- approval state when required.

A model output is not automatically a Decision.

### 5.9 Result

A Result is the outcome produced by completed work or execution.

A Result may be:

- a state change;
- a generated artifact;
- a recommendation;
- a completed transaction;
- a decision;
- a measurement;
- a failure outcome.

A Result must be distinguishable from the evidence used to produce it.

### 5.10 Actor

An Actor is an attributable participant capable of requesting, performing, approving, observing, governing, or receiving business activity.

Actor categories include:

- Human Actor;
- AI Agent Actor;
- Service Actor;
- External System Actor.

Every domain action must be attributable to one effective Actor, even when initiated through delegation or automation.

### 5.11 Agent Definition

An Agent Definition is a versioned configuration that describes an AI-operated role in the platform.

It may include:

- purpose;
- capabilities;
- responsibilities;
- authority limits;
- policies;
- prompt configuration;
- tool access;
- model requirements;
- escalation rules.

An Agent Definition is not an LLM model and is not a runtime execution.

### 5.12 Agent Instance

An Agent Instance is an Actor created from a specific version of an Agent Definition and operating within a Workspace and governance context.

The lifecycle and execution semantics of Agent Instance are finalized in ADW-05.

### 5.13 Runtime Session

A Runtime Session is a governed execution context in which one Actor or coordinated set of Actors performs work against a defined objective.

A Runtime Session is not a Task. It is one attempt or execution context associated with a Task, Action, Decision request, or other authorized operation.

### 5.14 Evidence

Evidence is information formally referenced to support, challenge, validate, or explain a Decision, Result, or finding.

Evidence must retain source and provenance references sufficient for later verification.

### 5.15 Domain Event

A Domain Event is a factual record that something meaningful occurred in the business domain.

A Domain Event is expressed in past tense and must not be used as a command.

Examples:

- `TaskAssigned`;
- `DecisionApproved`;
- `ExecutionFailed`;
- `EvidenceAttached`;
- `CaseClosed`.

### 5.16 Audit Record

An Audit Record is an immutable accountability record describing who did what, when, in which Workspace, under which authority, and with what outcome.

An Audit Record is not the source of operational state and is not interchangeable with a Domain Event.

---

## 6. Proposed Aggregate Roots

The following aggregate roots are proposed for validation during ADW-01.

### 6.1 Workspace Aggregate

Owns:

- workspace identity;
- workspace status;
- high-level governance configuration;
- lifecycle state.

Does not directly own all workspace data as one in-memory or transactional aggregate.

### 6.2 Enterprise Object Aggregate

Owns:

- enterprise object identity;
- object type;
- lifecycle state;
- object-specific data contract;
- object relationships governed by the aggregate;
- object ownership metadata.

### 6.3 Work Item Aggregate

Owns:

- objective;
- status;
- priority;
- ownership;
- assignments;
- due conditions;
- dependency references;
- acceptance conditions;
- completion or cancellation outcome.

Task, Case, and Project may become separate aggregate roots if their invariants materially differ. This remains an ADW-01 decision.

### 6.4 Decision Aggregate

Owns:

- decision subject;
- authority basis;
- evidence references;
- proposed outcome;
- approval requirements;
- final outcome;
- decision status;
- supersession relationship.

### 6.5 Agent Definition Aggregate

Owns:

- immutable version identity;
- role purpose;
- capabilities;
- policy references;
- tool permissions;
- prompt template references;
- runtime requirements;
- activation status.

### 6.6 Runtime Session Aggregate

Owns:

- session identity;
- execution objective;
- initiating Actor;
- effective Actor;
- related Work Item;
- state machine;
- attempts;
- outcome references;
- failure classification.

The final runtime state machine belongs to ADW-05.

---

## 7. Relationships

The following relationship model is proposed.

```text
Workspace
  owns -> Enterprise Objects
  owns -> Work Items
  owns -> Actors and Agent Instances
  owns -> Knowledge and Evidence
  owns -> Runtime Sessions
  owns -> Policies
  owns -> Events and Audit Records

Enterprise Object
  referenced by -> Work Item
  supported by -> Document and Evidence
  affected by -> Action and Decision

Work Item
  assigned to -> Actor
  contains or coordinates -> Actions
  may create -> Runtime Sessions
  may require -> Decisions and Approvals
  produces -> Results

Runtime Session
  executes for -> Work Item or authorized request
  acts through -> Actor
  invokes -> Tools
  produces -> Actions and Results

Decision
  concerns -> Enterprise Object or Work Item
  uses -> Evidence
  made by -> Actor
  constrained by -> Policy and Authority
```

Relationships across aggregate boundaries must use stable identifiers and explicit domain services or application services. Direct mutation across aggregate boundaries is prohibited.

---

## 8. Domain Ownership Rules

### 8.1 Workspace Ownership

Every workspace-scoped aggregate must contain or derive an immutable `workspace_id`.

A domain object must never change Workspace through ordinary update operations. Transfer, migration, or import requires an explicit governed process.

### 8.2 Actor Attribution

Every state-changing operation must identify:

- initiating Actor;
- effective Actor;
- delegation or automation chain when applicable;
- applicable Workspace.

### 8.3 Aggregate Ownership

Only an aggregate root may authorize mutation of state inside its aggregate boundary.

External services may request a change but must not mutate internal aggregate state directly.

### 8.4 Lifecycle Ownership

Every durable aggregate must define:

- creation conditions;
- valid states;
- allowed transitions;
- terminal states;
- archival or retention behavior;
- supersession rules when applicable.

### 8.5 Cross-Domain References

Cross-domain references must be explicit, typed, and traceable.

Unstructured identifiers embedded in free-form text must not be treated as authoritative relationships.

---

## 9. Domain Invariants

The following invariants are proposed as mandatory.

1. Every business-state aggregate belongs to exactly one Workspace.
2. Every state-changing Action is attributable to an Actor.
3. Every Decision identifies its authority basis and evidence references.
4. A model response is not a Decision until accepted by the applicable domain process.
5. A Runtime Session is never the authoritative source of Task state.
6. Audit Records are not mutable business state.
7. Domain Events describe facts that already occurred.
8. Infrastructure identifiers and provider-specific fields do not define domain identity.
9. Aggregate state changes occur only through valid domain operations.
10. Cross-workspace references are prohibited unless an explicit platform-level contract permits them.
11. Completion of a Task requires satisfaction of its declared completion conditions.
12. Results, Evidence, Decisions, and Audit Records remain semantically distinct.
13. Deletion of durable business records must respect governance, retention, and audit requirements.
14. Human approval is required whenever policy, authority, or risk classification demands it.
15. No Actor may exercise authority not explicitly granted or delegated.

---

## 10. Domain Services

A Domain Service is permitted only when business behavior:

- spans more than one aggregate;
- does not naturally belong to one entity or value object;
- remains independent of infrastructure;
- expresses a genuine domain rule.

Candidate domain services include:

- Assignment Service;
- Decision Authority Resolver;
- Escalation Resolver;
- Work Dependency Evaluator;
- Completion Criteria Evaluator;
- Delegation Validator;
- Enterprise Object Relationship Validator.

Repository access, HTTP calls, LLM calls, queues, file storage, and database transactions are application or infrastructure concerns and must not be implemented inside domain services.

---

## 11. Value Objects

The domain model should prefer immutable value objects for concepts without independent identity.

Candidate value objects include:

- WorkspaceId;
- ActorId;
- EnterpriseObjectId;
- WorkItemId;
- DecisionId;
- RuntimeSessionId;
- CorrelationId;
- Objective;
- Deadline;
- Priority;
- AuthorityScope;
- CapabilityReference;
- PolicyReference;
- EvidenceReference;
- ProvenanceReference;
- CompletionCriteria;
- FailureReason;
- ResultReference.

Value objects must validate their own internal consistency and must not depend on persistence or network services.

---

## 12. Commands, Events, and Decisions

The domain must distinguish three different concepts.

### Command

A request that something should happen.

Examples:

- `AssignTask`;
- `ApproveDecision`;
- `StartExecution`.

### Domain Event

A fact that something meaningful already happened.

Examples:

- `TaskAssigned`;
- `DecisionApproved`;
- `ExecutionStarted`.

### Decision

A governed business conclusion with authority, evidence, and an outcome.

Examples:

- approve supplier onboarding;
- reject contract clause;
- escalate compliance case;
- select procurement option.

Commands, Events, and Decisions must not share one generic data model merely because they have similar metadata.

---

## 13. State Ownership

The authoritative source of current operational state is the relevant aggregate.

The following are not authoritative substitutes for aggregate state:

- audit logs;
- event transport queues;
- observability logs;
- LLM conversation history;
- generated summaries;
- vector indexes;
- cached read models.

Event sourcing is not adopted by this chapter. It may be introduced only through a separate architecture decision defining scope, reconstruction guarantees, migration, and operational impact.

---

## 14. Technology Independence

The domain core must not depend on:

- FastAPI;
- SQLAlchemy;
- PostgreSQL-specific column types;
- Redis;
- Kafka;
- cloud SDKs;
- OpenAI, Anthropic, Google, or other provider SDKs;
- HTTP request objects;
- JWT payload objects;
- UI forms;
- ORM entities as the only domain representation.

Mapping between domain objects and persistence or transport models is owned by application and infrastructure layers.

---

## 15. Naming Rules

1. Domain terms use singular nouns for entity types.
2. Commands use imperative verb phrases.
3. Events use past-tense verb phrases.
4. Boolean concepts use affirmative names where possible.
5. Provider names must not appear in core domain type names.
6. `Task`, `Action`, `Decision`, `Result`, `Evidence`, `Event`, and `Audit Record` are not interchangeable terms.
7. `Agent Definition`, `Agent Instance`, and `Runtime Session` must remain separate concepts.
8. `Workspace` is the preferred platform term; `tenant` may be used only in infrastructure or security discussions where tenancy is specifically meant.
9. Deprecated terms must be recorded in a migration glossary before removal.

---

## 16. Out of Scope for ADW-01

The following are intentionally deferred:

- authentication mechanisms;
- membership and identity federation;
- role and permission implementation;
- authorization query semantics;
- runtime provider selection;
- prompt construction;
- model routing;
- tool invocation protocols;
- memory storage technology;
- vector databases;
- event broker selection;
- audit storage design;
- transaction and outbox implementation;
- plugin SDK;
- MCP integration details;
- API resource design;
- physical database schema.

These topics belong to later ADW sessions.

---

## 17. Decisions Required from ADW-01

The workshop must explicitly approve, reject, or revise the following proposals.

### D01. Primary Boundary

Proposed decision:

> Workspace is the primary ownership and isolation boundary for business-state objects.

Status: `PENDING`

### D02. Core Business Abstraction

Proposed decision:

> Enterprise Object is the stable platform abstraction for durable business-relevant things, while specialized domain entities retain their own contracts.

Status: `PENDING`

### D03. Work Model

Proposed decision:

> Work Item is the abstract coordination concept, with Task, Case, and Project as specialized forms.

Status: `PENDING`

### D04. Task versus Execution

Proposed decision:

> Task represents business work; Runtime Session represents one governed execution context. They are separate aggregates.

Status: `PENDING`

### D05. Actor Model

Proposed decision:

> Human, AI agent, service, and external-system participants share the Actor abstraction while preserving category-specific behavior.

Status: `PENDING`

### D06. Decision Semantics

Proposed decision:

> A Decision is a governed domain object requiring authority and evidence; an AI-generated answer is not automatically a Decision.

Status: `PENDING`

### D07. Operational State

Proposed decision:

> Aggregate state is authoritative. Audit, event transport, logs, memory, and read models are supporting records or projections.

Status: `PENDING`

### D08. Aggregate Strategy

Decision required:

> Determine whether Task, Case, and Project remain specializations of one Work Item aggregate or become separate aggregate roots with shared interfaces.

Status: `OPEN`

### D09. Relationship Model

Decision required:

> Determine which Enterprise Object relationships are aggregate-owned, independently versioned, or represented through a relationship aggregate.

Status: `OPEN`

### D10. Deletion and Supersession

Decision required:

> Define the minimum domain semantics for archive, soft deletion, legal retention, anonymization, and supersession.

Status: `OPEN`

---

## 18. Workshop Questions

The Project Owner and architecture participants must answer:

1. Is Workspace the correct primary business boundary for MVP and future platform growth?
2. Is an Enterprise allowed to contain multiple Workspaces, and is that relationship required now or deferred?
3. Which concrete Enterprise Object types are required for the first business scenario?
4. Do Task, Case, and Project need distinct lifecycle models?
5. Can one Work Item reference multiple Enterprise Objects?
6. Can one Enterprise Object participate in multiple concurrent Work Items?
7. Which Decisions always require human approval?
8. Can an AI Agent be the final deciding Actor within explicitly delegated authority?
9. Is Result immutable, replaceable, or supersedable?
10. Which domain records may be deleted, and which may only be archived or anonymized?
11. Must every Action belong to a Work Item, or may authorized standalone Actions exist?
12. Is a Runtime Session always linked to one Task, or may it serve a Case, Project, Decision request, or standalone operation?
13. Which relationships require their own lifecycle and audit history?
14. What minimum metadata is mandatory for every aggregate?
15. Which terms in existing project documents conflict with this vocabulary and require migration?

---

## 19. Required Deliverables

ADW-01 is complete only when the following artifacts exist and are consistent:

- approved `DOMAIN_CORE.md`;
- accepted Domain Core ADR;
- domain context map;
- aggregate ownership table;
- core vocabulary and deprecated-term glossary;
- initial aggregate diagram;
- documented domain invariants;
- mapping to the Gate A MVP scenario;
- mapping to implementation work packages;
- synchronized references in `ARCHITECTURE_SPECIFICATION.md`.

---

## 20. Definition of Done

ADW-01 may be marked `PASS` only when:

1. all D01-D10 decisions are approved, rejected, or explicitly deferred with owner and target session;
2. core terms have one agreed meaning;
3. the MVP business scenario can be represented without adding undefined core concepts;
4. aggregate roots and ownership boundaries are documented;
5. Task and Runtime Session are unambiguously separated;
6. Actor, Agent Definition, Agent Instance, and Runtime Session are unambiguously separated;
7. Decision, Result, Evidence, Domain Event, and Audit Record are unambiguously separated;
8. cross-workspace behavior is either prohibited or explicitly specified;
9. no infrastructure or provider-specific dependency exists in the domain core;
10. the Project Owner explicitly records `PASS`.

---

## 21. Review Record

### Architecture Review

- Reviewer: `PENDING`
- Review date: `PENDING`
- Findings: `PENDING`
- Required changes: `PENDING`

### Project Owner Decision

- Decision: `PENDING`
- Decision date: `PENDING`
- Conditions: `PENDING`
- Approved version: `PENDING`

Allowed decisions:

- `PASS` — ADW-01 is approved and may govern downstream architecture;
- `REWORK` — specific issues must be corrected before approval;
- `FAIL` — the proposed domain model is rejected and must be redesigned.

---

## 22. Current Status

```text
ADW-01 document: CREATED
Domain vocabulary: PROPOSED
Aggregate model: PROPOSED
Architecture decisions: PENDING
Project Owner approval: PENDING
ADW-01 result: NOT YET PASS
```
