# Gate C Agent Context and Human Interaction Plan

Version: 1.0  
Status: Planning Specification  
Implementation Track: 50_IMPLEMENTATION  
Scope: Gate C planning only — no implementation

Related Documents:
- MVP_WORK_PACKAGE_PLAN.md
- PB052_Agent_Runtime_Implementation.md
- PB053_Context_Engine_Implementation.md
- PB058_Authentication_and_Authorization_Implementation.md
- PB034_Enterprise_Memory_Specification.md
- CORE_Canonical_Data_Model.md
- CORE_Enterprise_Metadata_Standard.md
- CORE_Versioning_Framework.md

Primary Owners:
- AG009 Enterprise Architect
- AG002 Chief Orchestrator
- AG054 Memory Manager
- AG053 Knowledge Curator
- AG003 AI Auditor

Special Domain Owner:
- Legal and Regulatory Agent Group

---

## 00. Executive Summary

This document defines the planning requirements for using agents during Gate C — Platform Backbone.

It does not authorize implementation.

Its purpose is to ensure that Gate C is designed around four durable principles:

```text
Agents are replaceable.
Sessions are temporary.
Context is durable.
Sources are authoritative.
Human authority remains explicit.
```

The agent must never become the system of record.

The system of record is the Bizzi platform: objects, tasks, context records, decisions, sources, events, audit records, memory entries, and version histories.

A provider-specific model may disappear, fail, change behavior, lose a session, or be replaced. The enterprise context and decision history must remain available independently of that agent or provider.

---

## 01. Planning Objective for Gate C

Gate C must create the platform foundation required for later agent execution without prematurely implementing the full runtime.

Gate C planning must define:

- which enterprise objects agents may read or propose changes to;
- how agents receive task-scoped context;
- how context survives agent-session termination;
- how humans review, approve, reject, correct, or escalate agent work;
- how permanent and temporary context are separated;
- how context is versioned and refreshed;
- how multiple model providers consume the same canonical context;
- how legal and regulatory knowledge is monitored, validated, versioned, and applied;
- how provenance, permissions, confidence, and expiry are preserved.

---

## 02. Agent-Related Planning Problems in Gate C

The existing Agent Library contains many specialized roles. Their existence creates planning risks before implementation begins.

### 02.1 Role Proliferation

Problem:

A large list of agents may encourage one software component per agent.

Risk:

- duplicated logic;
- inconsistent context handling;
- different audit behavior;
- different permission models;
- difficult maintenance;
- provider lock-in.

Planning rule:

```text
Agent role != software service
```

Gate C must plan one canonical AgentDefinition model. Role differences should be expressed through configuration:

- purpose;
- capability profile;
- authority profile;
- context policy;
- tool policy;
- escalation policy;
- provider preference;
- output schema;
- review requirements.

### 02.2 Overlapping Agent Authority

Examples:

- Chief Orchestrator versus Enterprise Architect;
- Legal Agent versus Compliance Agent;
- Risk Manager versus AI Auditor;
- Business Analyst versus Process Analyst;
- Knowledge Curator versus Memory Manager.

Risk:

Two agents may believe they own the same decision.

Gate C planning requirement:

Each AgentDefinition must distinguish:

- advisory authority;
- proposal authority;
- execution authority;
- approval authority;
- veto authority;
- escalation authority.

No agent receives implied authority from its title.

### 02.3 Conflicting Recommendations

Problem:

Different specialists may produce incompatible plans.

Examples:

- Legal Agent recommends maximum compliance protection;
- Sales Agent recommends fastest execution;
- Finance Agent recommends minimum cost;
- Risk Manager recommends postponement.

Planning requirement:

Gate C must define a common Recommendation object containing:

```yaml
recommendation_id:
agent_definition_id:
provider_id:
model_id:
task_id:
context_snapshot_id:
proposal:
rationale:
evidence:
assumptions:
constraints:
confidence:
risks:
legal_basis:
dissent:
requires_human_decision:
created_at:
```

Conflicts must be preserved, not silently merged.

### 02.4 Hallucinated Competence

Problem:

An agent may answer outside its capability, jurisdiction, language, source coverage, or date range.

Planning requirement:

Every role must define competence boundaries:

- supported domains;
- unsupported domains;
- jurisdictions;
- applicable dates;
- mandatory sources;
- mandatory human review conditions;
- confidence floor;
- escalation triggers.

### 02.5 Context Leakage Between Agents

Problem:

An agent may receive data not required for its task.

Risk:

- privacy breach;
- trade-secret exposure;
- inappropriate influence;
- legal privilege loss;
- cross-tenant leakage in future stages.

Planning requirement:

Context is assembled per task and per requesting agent. Access must be based on least privilege and purpose limitation.

### 02.6 Agent Identity Versus Provider Identity

Problem:

The same Bizzi role may be executed by different providers or models.

Planning rule:

Keep these identities separate:

```text
AgentDefinition = enterprise role
AgentInstance = configured executable instance
Provider = external or internal model provider
Model = provider model/version
RuntimeSession = one temporary execution
```

### 02.7 Non-Deterministic Outputs

Problem:

The same task and context may produce different results.

Planning requirement:

Every session must preserve:

- context snapshot reference;
- prompt/configuration version;
- provider and model version;
- tool policy version;
- output schema version;
- execution timestamp;
- produced result;
- human disposition.

### 02.8 Planning Agents Planning Gate C

Agents may assist in planning Gate C, but they must not become the source of authority for the plan.

Recommended planning workflow:

```text
Architecture question
  -> specialist agent proposals
  -> conflict comparison
  -> Enterprise Architect synthesis
  -> Risk and Audit review
  -> Human Product Owner decision
  -> versioned planning record
```

---

## 03. Human–Agent Interaction Interface

The primary interface is not a free-form chat alone.

Chat may be one interaction surface, but the authoritative interaction model is a structured work item.

### 03.1 Human Interaction Object

```yaml
interaction_id:
task_id:
agent_session_id:
human_actor_id:
interaction_type:
question:
agent_proposal:
evidence_links:
confidence:
risk_level:
required_action:
due_at:
human_response:
decision_status:
created_at:
resolved_at:
```

### 03.2 Required Human Actions

The interface must support:

- Ask;
- Clarify;
- Approve;
- Reject;
- Request Rework;
- Correct Facts;
- Add Source;
- Limit Scope;
- Change Priority;
- Escalate;
- Delegate;
- Mark as Superseded.

### 03.3 Recommended Interaction Surfaces

Planning target:

1. **Task Workspace** — authoritative task, context, recommendation, evidence and status.
2. **Conversation Panel** — human dialogue with the assigned agent.
3. **Decision Panel** — explicit approval, rejection, rework or escalation.
4. **Context Inspector** — shows what the agent received and why.
5. **Source Inspector** — shows source, version, date, authority and validity.
6. **Audit Timeline** — shows all material actions and changes.

### 03.4 Human Control Rule

The system must distinguish:

- agent output;
- agent recommendation;
- proposed action;
- approved decision;
- executed action.

These are never treated as synonyms.

---

## 04. Context Survival After Agent Session Termination

An agent session is disposable.

Context must not live only in provider chat history, model memory, process memory, or temporary runtime state.

### 04.1 Required Durable Records

Gate C planning must include the following durable objects:

- ContextSource;
- ContextItem;
- ContextVersion;
- ContextSnapshot;
- ContextPackage;
- RuntimeSession reference;
- Recommendation reference;
- Decision reference;
- MemoryEntry;
- SourceValidityRecord.

### 04.2 Session Death Model

```text
Agent session ends or fails
  -> RuntimeSession closes
  -> ContextSnapshot remains immutable
  -> Result and evidence remain linked
  -> unfinished task remains recoverable
  -> replacement agent receives a newly assembled package
  -> prior snapshot remains available for audit
```

The replacement agent does not inherit undocumented hidden state.

### 04.3 Caching Principle

Cache is not memory and is not the system of record.

```text
Durable Store = authoritative context and history
Cache = temporary acceleration layer
Provider Session = disposable execution state
```

Gate C planning should define cache metadata even if caching is implemented later:

- cache key;
- source version set;
- permission scope;
- created_at;
- expires_at;
- invalidation reason;
- sensitivity class;
- context hash.

---

## 05. Permanent and Temporary Context

Context must be classified by lifecycle.

### 05.1 Permanent Context

Permanent does not mean immutable forever. It means durable, governed, versioned and retained.

Examples:

- company identity;
- organizational structure;
- approved policies;
- contracts;
- legal opinions;
- decisions;
- validated lessons;
- process definitions;
- authority maps;
- approved agent definitions;
- canonical taxonomies.

Required behavior:

- versioned;
- source-linked;
- effective date recorded;
- supersession preserved;
- owner assigned;
- review cycle defined;
- deletions controlled.

### 05.2 Temporary Context

Examples:

- current task instructions;
- working assumptions;
- current conversation;
- draft analysis;
- temporary tool results;
- short-lived market data;
- unvalidated external information;
- session-specific summaries.

Required behavior:

- explicit expiry;
- validation state;
- promotion rule into durable memory;
- isolation by task and permission scope;
- deletion or archival policy.

### 05.3 Context Lifecycle States

```text
Draft
  -> Collected
  -> Validated
  -> Active
  -> Superseded
  -> Deprecated
  -> Archived
  -> Deleted under policy
```

Temporary context may be promoted to permanent context only after validation and ownership assignment.

### 05.4 Continuous Updating

Persistent context must be continuously maintainable, not silently overwritten.

Update pattern:

```text
New fact or source received
  -> existing context located
  -> contradiction detected
  -> new version created
  -> validity dates assigned
  -> owner/reviewer notified if material
  -> dependent context marked stale
  -> affected agents receive refreshed package on next execution
```

---

## 06. Multi-Provider Agent Context Portability

Bizzi must own the context format.

No provider-specific conversation format may become the canonical enterprise memory format.

### 06.1 Canonical Provider-Neutral Context Envelope

```yaml
context_envelope_version:
context_snapshot_id:
task:
agent_role:
object_references:
facts:
policies:
constraints:
decisions:
memory:
sources:
permissions:
sensitivity:
validity:
confidence:
known_gaps:
required_output_schema:
```

### 06.2 Provider Adapter Responsibility

Each provider adapter converts the canonical envelope into provider-specific request format.

```text
Canonical Context Envelope
  -> Provider Adapter
  -> Provider-Specific Prompt / Message Format
  -> Model Execution
  -> Canonical Result Envelope
```

### 06.3 Provider-Neutral Result Envelope

```yaml
result_envelope_version:
provider_id:
model_id:
model_version:
agent_definition_id:
context_snapshot_id:
output:
evidence:
assumptions:
confidence:
limitations:
tool_calls:
usage_metadata:
escalation:
```

### 06.4 Provider Switching Rules

Provider switching must preserve:

- the same task ID;
- the same enterprise object references;
- the same immutable context snapshot when comparison is intended;
- provider/model identity;
- output differences;
- human selection or synthesis decision.

Provider-specific hidden memory is not trusted as enterprise memory.

### 06.5 Context Size Differences

Different models have different context-window limits.

Planning requirement:

Context Engine must support provider-independent prioritization:

- mandatory context;
- high-priority context;
- optional context;
- summary-only context;
- excluded context;
- retrievable-on-demand references.

Truncation must be visible and recorded in `limitations`.

---

## 07. Legal and Regulatory Change Management

Legal agents require a stricter context policy than ordinary analytical agents.

### 07.1 Legal Source Hierarchy

Planning must distinguish:

1. official legislation and official gazettes;
2. regulator and ministry materials;
3. binding court decisions where applicable;
4. authoritative administrative guidance;
5. internal legal opinions;
6. secondary commentary;
7. unverified external material.

The agent must never present all source classes as equally authoritative.

### 07.2 Legal Context Metadata

```yaml
jurisdiction:
authority:
source_type:
instrument_type:
instrument_number:
publication_date:
effective_from:
effective_to:
consolidated_version_date:
amended_by:
repealed_by:
status:
language:
official_source_link:
retrieved_at:
verified_at:
verified_by:
```

### 07.3 Change Detection Plan

```text
Official source monitored
  -> new or amended instrument detected
  -> legal source record created
  -> jurisdiction and effective date verified
  -> affected legal context identified
  -> prior context marked superseded or partially stale
  -> legal agent analysis requested
  -> human legal reviewer validates material impact
  -> approved legal memory version published
  -> dependent tasks, policies and decisions flagged
```

### 07.4 Legal Agent Output Requirements

Every material legal answer must identify:

- jurisdiction;
- question date;
- applicable law date;
- official sources;
- assumptions;
- uncertainty;
- whether law is proposed, adopted, published, effective, suspended, repealed or transitional;
- need for human legal review.

### 07.5 No Automatic Legal Truth Replacement

A newly detected law or amendment must not automatically overwrite approved legal guidance.

It creates a change event and review requirement.

### 07.6 Legal Context Expiry

Legal context should use review and validity triggers rather than a simple universal TTL.

Triggers include:

- new amendment;
- new consolidated text;
- new court interpretation;
- regulator guidance;
- jurisdiction change;
- transaction date change;
- user fact change;
- scheduled review date.

---

## 08. Gate C Planning Additions

The following planning work packages should be inserted into or linked from Gate C before implementation begins.

### GC-P01 — Agent Role and Authority Matrix

Deliverable:

- mapping of Agent Library roles to advisory, proposal, execution, approval, veto and escalation authority.

Acceptance criterion:

- no overlapping authority remains unresolved.

### GC-P02 — Canonical Agent Identity Model

Deliverable:

- distinction between AgentDefinition, AgentInstance, Provider, Model and RuntimeSession.

Acceptance criterion:

- provider replacement does not change enterprise role identity.

### GC-P03 — Human–Agent Interaction Contract

Deliverable:

- interaction types, decision states, structured recommendation and human disposition model.

Acceptance criterion:

- agent recommendation cannot become an executed decision without an explicit authority path.

### GC-P04 — Context Classification and Lifecycle Plan

Deliverable:

- permanent/temporary classification, lifecycle states, retention, promotion, expiry and supersession rules.

Acceptance criterion:

- every context item has owner, source, lifecycle class and validity metadata.

### GC-P05 — Context Snapshot and Session Recovery Plan

Deliverable:

- immutable snapshot model and recovery behavior after agent termination or provider failure.

Acceptance criterion:

- another agent can resume the task using durable records without relying on hidden prior-session memory.

### GC-P06 — Provider-Neutral Context Contract

Deliverable:

- canonical context and result envelopes plus provider adapter responsibilities.

Acceptance criterion:

- the same task can be sent to two providers while preserving traceability and comparable inputs.

### GC-P07 — Context Refresh and Invalidation Plan

Deliverable:

- source versioning, stale marking, dependency invalidation, cache invalidation and refresh triggers.

Acceptance criterion:

- changed source data never silently leaves dependent context marked current.

### GC-P08 — Legal and Regulatory Knowledge Plan

Deliverable:

- source hierarchy, metadata, change-detection, validation, approval and legal-context versioning rules.

Acceptance criterion:

- legal answers can be reconstructed against the law and source versions applicable on the relevant date.

### GC-P09 — Context Security and Sensitivity Plan

Deliverable:

- least-privilege context assembly, sensitivity classes, redaction, privilege handling and provider restrictions.

Acceptance criterion:

- each context package is explainably limited to authorized task purpose.

### GC-P10 — Gate C Agent Planning Review

Deliverable:

- consolidated review by Enterprise Architect, Chief Orchestrator, Memory Manager, Knowledge Curator, AI Auditor and human Product Owner.

Acceptance criterion:

- Gate C implementation remains blocked until all nine preceding planning packages are approved.

---

## 09. Recommended Planning Sequence

```text
GC-P01 Role and Authority Matrix
  + GC-P02 Canonical Agent Identity
        -> GC-P03 Human–Agent Interaction Contract

GC-P04 Context Classification
  -> GC-P05 Snapshot and Recovery
  -> GC-P07 Refresh and Invalidation

GC-P06 Provider-Neutral Context Contract
  depends on GC-P02, GC-P04 and GC-P05

GC-P08 Legal and Regulatory Knowledge Plan
  depends on GC-P04 and GC-P07

GC-P09 Context Security and Sensitivity Plan
  depends on GC-P01, GC-P04 and GC-P06

All
  -> GC-P10 Gate C Agent Planning Review
```

---

## 10. Decisions Required Before Implementation

The following decisions must be made at planning stage:

1. Which Agent Library roles are allowed in Gate C planning?
2. Which roles are advisory only?
3. Who is the human Product Owner and final Gate C authority?
4. Which context categories are permanent, temporary, regulated or privileged?
5. Which records are immutable snapshots and which are mutable current views?
6. What conditions promote temporary context into durable memory?
7. What is the canonical provider-neutral context envelope version 1.0?
8. What provider data-retention restrictions apply by sensitivity class?
9. Which legal jurisdictions are initially supported?
10. Which official legal sources are authoritative for each jurisdiction?
11. Who validates legal updates before publication into approved memory?
12. Which events invalidate cached context or mark context stale?

---

## 11. Explicit Non-Goals

This plan does not include:

- coding agents;
- selecting a final LLM provider;
- building runtime adapters;
- implementing databases;
- implementing caches;
- implementing legal monitoring;
- implementing UI;
- creating production workflows;
- deploying infrastructure.

These activities remain prohibited until the planning packages and Gate C review are approved.

---

## 12. Gate C Planning Exit Criteria

Gate C agent/context planning is complete only when:

- agent role and authority conflicts are resolved;
- the human interaction contract is approved;
- provider-neutral context and result contracts are approved;
- permanent and temporary context lifecycle rules are approved;
- context snapshot and recovery behavior is approved;
- refresh and invalidation rules are approved;
- legal-source governance is approved;
- context security and sensitivity rules are approved;
- all decisions are versioned and linked to owners;
- no implementation work has been authorized by this document alone.

---

## 13. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-19 | Initial Gate C agent, context, human interaction, provider portability and legal knowledge planning specification |
