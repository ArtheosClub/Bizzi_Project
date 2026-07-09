# CORE Canonical Data Model

Version: 1.0
Status: Architecture Closure Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Enterprise_Domain_Model.md
- CORE_Enterprise_Metadata_Standard.md
- CORE_Object_Registry.md
- CORE_Architecture_Traceability_Matrix.md

Primary Owner:
- AG065 Data Engineer

Architecture Owner:
- AG009 Enterprise Architect

Runtime Owner:
- AG080 Runtime Manager

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Canonical Data Model defines the minimum shared data structures Bizzi should use across implementation components.

It is not the final database schema. It is the canonical implementation vocabulary for data objects that must remain consistent across backend, runtime, context engine, knowledge graph, decision engine, command center, and audit.

Core principle:

```text
One concept should have one canonical data meaning across Bizzi.
```

---

## 01. Purpose

This document defines:

- canonical implementation entities;
- minimum fields;
- shared identifiers;
- relationships between implementation data objects;
- MVP data scope;
- rules for avoiding data model complexity.

---

## 02. Canonical Data Model vs Domain Model

| Model | Purpose |
|---|---|
| Domain Model | Business language and business entities |
| Canonical Data Model | Shared implementation data structures |
| Database Schema | Physical storage design |
| API DTO | Request/response contract for APIs |

The Canonical Data Model should guide database schemas, APIs, events, and service models without forcing all systems into one giant table structure.

---

## 03. Core Canonical Entities

Initial canonical entities:

| Entity | Purpose |
|---|---|
| EnterpriseObject | Base record for managed object identity |
| Metadata | Standard metadata block |
| Agent | AI or human/AI operational actor |
| Task | Unit of executable work |
| Workflow | Managed state machine or process path |
| Event | Timestamped enterprise activity record |
| Decision | Governed choice and approval record |
| Option | Candidate decision option |
| KPI | Governed performance measure |
| Risk | Risk or exposure object |
| MemoryEntry | Enterprise Memory object |
| GraphNode | Knowledge graph node |
| GraphRelationship | Knowledge graph relationship |
| ContextPackage | Runtime context package |
| RuntimeSession | Agent execution session |
| Alert | Condition requiring attention or action |
| AuditRecord | Audit or evidence trace |
| Configuration | Controlled setting or baseline |
| Integration | API/tool/system connection |

---

## 04. Universal Base Fields

Most canonical entities should include:

```yaml
id:
type:
title:
description:
status:
version:
owner_agent:
created_at:
created_by:
updated_at:
updated_by:
metadata:
```

---

## 05. EnterpriseObject

```yaml
id:
object_type:
title:
description:
status:
version:
owner_agent:
related_capabilities:
related_functions:
related_playbooks:
risk_rating:
confidence_level:
audit_required:
created_at:
updated_at:
```

Purpose:
- common managed object identity;
- source for graph nodes;
- link point for tasks, decisions, events, memory, and audit.

---

## 06. Task

```yaml
id:
task_type:
title:
description:
source_object:
source_event:
assigned_agent:
owner_agent:
priority:
decision_level:
risk_rating:
status:
due_date:
created_at:
updated_at:
```

---

## 07. Event

```yaml
id:
event_type:
event_name:
timestamp:
source_service:
source_agent:
related_object:
trace_id:
correlation_id:
severity:
payload_reference:
status:
```

---

## 08. Decision

```yaml
id:
decision_type:
decision_level:
decision_owner:
requesting_agent:
related_object:
options:
selected_option:
rationale:
confidence_level:
human_override_required:
status:
created_at:
decided_at:
```

---

## 09. ContextPackage

```yaml
id:
source_task:
requesting_agent:
related_objects:
retrieved_memory:
retrieved_graph:
constraints:
permissions:
confidence_summary:
limitations:
expires_at:
status:
```

---

## 10. RuntimeSession

```yaml
id:
task_id:
agent_id:
context_package_id:
permission_profile:
allowed_tools:
execution_state:
started_at:
ended_at:
result_reference:
status:
```

---

## 11. GraphNode and GraphRelationship

```yaml
GraphNode:
  id:
  node_type:
  source_object:
  title:
  status:
  confidence_level:

GraphRelationship:
  id:
  relationship_type:
  source_node:
  target_node:
  source_evidence:
  confidence_level:
  status:
```

---

## 12. MVP Data Scope

The MVP should implement only the canonical entities required for the first vertical slice:

- EnterpriseObject;
- Agent;
- Task;
- Event;
- ContextPackage;
- RuntimeSession;
- Decision;
- MemoryEntry;
- GraphNode;
- GraphRelationship;
- Alert;
- AuditRecord.

Avoid implementing all possible domain entities before they are needed.

---

## 13. Simplicity Rules

Data model simplicity rules:

- avoid giant universal tables for everything;
- avoid duplicating the same concept under different names;
- start with minimal fields that support real workflows;
- preserve source references instead of copying large payloads;
- prefer explicit relationships over hidden JSON blobs for core links;
- do not model business domains before a playbook requires them;
- make every field useful for execution, governance, search, audit, or UI.

---

## 14. Governance Rules

Canonical data governance rules:

- new canonical entities require architecture review;
- entity names must align with Domain Model and Object Registry;
- breaking field changes require versioning;
- sensitive fields require access rules;
- audit-relevant entities must preserve history;
- implementation schemas must map back to canonical entities.

---

## 15. Success Criteria

This model is successful if Bizzi can:

- implement services consistently;
- keep API, database, event, and graph models aligned;
- reduce naming drift;
- support MVP without over-modeling;
- evolve data structures safely over time.

---

## 16. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-09 | Initial Canonical Data Model architecture closure specification |
