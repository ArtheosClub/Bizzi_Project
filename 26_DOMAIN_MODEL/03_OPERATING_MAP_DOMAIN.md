# 03_OPERATING_MAP_DOMAIN.md

# Bizzi Platform

## Operating Map Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 01_RUNTIME_ARCHITECTURE.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Operating Map Domain for Bizzi Platform.

The Operating Map Domain describes how Bizzi represents the company’s operating structure, gaps, recommended improvements and links between functions, responsibilities, agents, processes, tasks, decisions, memory and audit.

Core question:

```text
How does Bizzi turn business context into a structured operating map that shows how the company works and what needs attention?
```

---

# 2. Domain Role

The Operating Map Domain is the first structural representation of the company inside Bizzi.

It provides:

- operating visibility;
- functional structure;
- gap detection;
- recommended actions;
- first-hour value;
- links to execution objects;
- dashboard foundation;
- AI-generated draft structure with human confirmation.

---

# 3. Domain Principle

```text
Operating Clarity Before Execution
```

Bizzi should not create disconnected tasks or agents before the company’s operating structure is understood.

The Operating Map provides the bridge from onboarding context to structured execution.

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
OperatingMap
```

Entities inside or attached to the aggregate:

```text
OperatingMapNode
OperatingGap
OperatingRecommendation
SuggestedFunction
SuggestedAgent
SuggestedTask
```

Related external entities:

```text
CompanyWorkspace
Function
Responsibility
Agent
Process
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
DashboardMetric
```

---

# 5. Core Entities

## 5.1 OperatingMap

Represents the structured operating view of a workspace.

Minimum domain attributes:

```text
id
workspace_id
title
status
version
created_at
updated_at
created_by
```

Optional domain attributes:

```text
summary
source_context_id
generated_by_ai
confirmed_by
confirmed_at
last_reviewed_at
```

Domain responsibility:

```text
OperatingMap organizes the company’s operating structure and serves as the source for gaps, recommendations and execution objects.
```

---

## 5.2 OperatingMapNode

Represents one structural element inside the operating map.

Potential node types:

```text
function
capability
process
responsibility
agent
task
decision
gap
```

Minimum domain attributes:

```text
id
workspace_id
operating_map_id
node_type
title
status
created_at
updated_at
```

Optional domain attributes:

```text
parent_node_id
linked_object_type
linked_object_id
position
metadata
```

Domain responsibility:

```text
OperatingMapNode allows the operating map to represent structured business elements and their relationships.
```

MVP simplification:

```text
OperatingMap may initially use a simple list of functions and gaps instead of a full node graph.
```

---

## 5.3 OperatingGap

Represents a missing, weak or unclear part of the operating model.

Minimum domain attributes:

```text
id
workspace_id
operating_map_id
gap_type
title
description
severity
status
created_at
updated_at
```

Optional domain attributes:

```text
function_id
process_id
responsibility_id
source_object_type
source_object_id
recommended_action
resolved_by_object_type
resolved_by_object_id
```

Domain responsibility:

```text
OperatingGap identifies where the business lacks clarity, ownership, process, execution or control.
```

---

## 5.4 OperatingRecommendation

Represents a recommendation generated from the operating map or gap analysis.

Minimum domain attributes:

```text
id
workspace_id
operating_map_id
recommendation_type
title
description
status
created_at
updated_at
```

Optional domain attributes:

```text
source_gap_id
suggested_object_type
suggested_object_payload
confidence
created_by_agent_id
confirmed_by
confirmed_at
```

Domain responsibility:

```text
OperatingRecommendation converts map insights into suggested functions, tasks, agents, processes or decisions.
```

---

# 6. Operating Map Lifecycle

Recommended lifecycle:

```text
draft
↓
generated
↓
reviewed
↓
confirmed
↓
active
↓
updated
↓
archived
```

MVP lifecycle:

```text
generated
confirmed
active
archived
```

---

# 7. Gap Lifecycle

Recommended lifecycle:

```text
detected
↓
reviewed
↓
accepted
↓
in_progress
↓
resolved
↓
archived
```

MVP lifecycle:

```text
detected
accepted
resolved
archived
```

---

# 8. Gap Types

Initial gap types:

```text
missing_function
missing_owner
missing_process
missing_task
missing_decision
missing_agent_support
unclear_responsibility
operational_risk
memory_gap
audit_gap
integration_gap
```

The MVP should prioritize:

```text
missing_function
missing_owner
missing_process
missing_task
operational_risk
```

---

# 9. Recommendation Types

Initial recommendation types:

```text
create_function
assign_owner
create_task
create_process
suggest_agent
log_decision
create_memory
review_risk
```

MVP recommendations should remain simple and actionable.

---

# 10. Domain Relationships

## 10.1 Workspace to OperatingMap

```text
CompanyWorkspace 1 → many OperatingMaps
```

MVP simplification:

```text
CompanyWorkspace 1 → 1 active OperatingMap
```

## 10.2 OperatingMap to Function

```text
OperatingMap → many Functions
```

Functions may be created from map recommendations.

## 10.3 OperatingMap to OperatingGap

```text
OperatingMap 1 → many OperatingGaps
```

## 10.4 OperatingGap to Task

```text
OperatingGap → suggested or created Task
```

## 10.5 OperatingGap to Responsibility

```text
OperatingGap may represent missing ownership or unclear responsibility
```

## 10.6 OperatingRecommendation to Runtime Object

```text
OperatingRecommendation → Function / Task / Agent / Process / Decision / MemoryEntry
```

---

# 11. Domain Invariants

The Operating Map Domain must enforce:

```text
OperatingMap must belong to one workspace.
Active OperatingMap must be workspace-scoped.
OperatingGap must belong to an OperatingMap.
OperatingRecommendation must have a source or explicit manual origin.
AI-generated map output must be reviewed or confirmed before becoming authoritative.
Resolved gaps should reference the object or action that resolved them.
Archived maps should not be used as active dashboard source.
```

---

# 12. AI Generation Rules

AI may generate:

- draft operating map;
- suggested functions;
- detected gaps;
- recommended tasks;
- suggested agents;
- process suggestions.

AI may not automatically:

- confirm the official operating map;
- assign final human accountability;
- delete functions;
- hide gaps;
- mark risk as resolved;
- bypass audit.

MVP rule:

```text
AI generates structure. Human confirms operating meaning.
```

---

# 13. Operating Map Creation Flow

```text
Workspace created
↓
Business intake completed
↓
Workspace context assembled
↓
AI generates draft operating map
↓
Operating gaps detected
↓
Recommendations created
↓
User reviews map
↓
Functions, tasks or agents are confirmed
↓
Audit events recorded
↓
Memory entries created
↓
Dashboard updated
```

---

# 14. Operating Map Events

Domain events:

```text
operating_map.generated
operating_map.reviewed
operating_map.confirmed
operating_map.updated
operating_map.archived
operating_gap.detected
operating_gap.accepted
operating_gap.resolved
operating_recommendation.created
operating_recommendation.confirmed
operating_recommendation.rejected
```

These events support audit, memory and dashboard updates.

---

# 15. Audit Requirements

Audited actions:

```text
operating_map.generated
operating_map.confirmed
operating_map.updated
operating_gap.detected
operating_gap.resolved
operating_recommendation.confirmed
operating_recommendation.rejected
```

Audit must answer:

```text
Who generated or confirmed the operating structure, what changed, and which workspace was affected?
```

---

# 16. Memory Requirements

Operating Map Domain may create memory from:

- confirmed operating map summary;
- detected operating gaps;
- accepted recommendations;
- resolved gaps;
- operating structure changes;
- map review notes.

Memory types:

```text
operating_map_summary
operating_gap
operating_recommendation
operating_structure_change
```

---

# 17. Dashboard Requirements

Dashboard should show:

- active operating map status;
- confirmed functions;
- open operating gaps;
- ownership gaps;
- suggested tasks;
- suggested agents;
- recently resolved gaps;
- next recommended actions.

Dashboard question:

```text
How is the company structured, what is missing, and what should happen next?
```

---

# 18. Security Requirements

Security requirements:

```text
OperatingMap belongs to one workspace.
Only authorized workspace users may view or modify it.
AI-generated map context must be workspace-scoped.
Map exports require authorization.
Archived maps cannot be edited through normal flows.
Recommendations that create runtime objects require confirmation.
```

---

# 19. MVP Domain Behavior

MVP should support:

```text
Generate operating map from workspace context
Store active operating map
Detect operating gaps
Create recommendations
Confirm suggested functions
Create suggested tasks
Show map summary on dashboard
Create audit events
Create memory entries from confirmed map
```

---

# 20. Out of Scope for MVP

The Operating Map Domain does not need in MVP:

- complex graph editor;
- drag-and-drop process modeling;
- multi-version branching;
- advanced dependency visualization;
- real-time collaborative editing;
- automated reorganization;
- enterprise capability heatmaps;
- simulation of operating models.

---

# 21. Data Model Implications

Future Data Model should include tables or collections for:

```text
operating_maps
operating_map_nodes
operating_gaps
operating_recommendations
```

Recommended indexes later:

```text
operating_maps.workspace_id
operating_maps.status
operating_gaps.workspace_id
operating_gaps.operating_map_id
operating_gaps.status
operating_recommendations.workspace_id
operating_recommendations.status
```

MVP simplification:

```text
operating_map_nodes may be postponed if function and gap lists are enough.
```

---

# 22. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/operating-map/generate
GET /workspaces/{workspace_id}/operating-map
PATCH /workspaces/{workspace_id}/operating-map
POST /workspaces/{workspace_id}/operating-map/confirm
GET /workspaces/{workspace_id}/operating-gaps
PATCH /workspaces/{workspace_id}/operating-gaps/{gap_id}
POST /workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/confirm
POST /workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/reject
```

---

# 23. Traceability Pattern

Operating Map traceability chain:

```text
Workspace Context
↓
OperatingMap
↓
OperatingGap
↓
OperatingRecommendation
↓
Function / Task / Agent / Process / Decision
↓
Runtime Event
↓
Audit Event
↓
Memory Entry
↓
Dashboard Metric
```

---

# 24. Acceptance Criteria

Operating Map Domain is ready when:

- OperatingMap is defined as aggregate root;
- OperatingGap is defined;
- OperatingRecommendation is defined;
- lifecycle states are clear;
- AI generation rules are defined;
- confirmation rules are explicit;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 25. Architecture Alignment

| Operating Map Domain Area | Reference |
|---|---|
| OperatingMap | 01_RUNTIME_ARCHITECTURE.md |
| OperatingGap | 02_CORE_RUNTIME_COMPONENTS.md |
| Recommendations | AI Orchestration Runtime |
| Function Suggestions | Function Registry Runtime |
| Task Suggestions | Task Runtime |
| Agent Suggestions | Agent Runtime |
| Map Events | Event Runtime |
| Map Audit | Audit Runtime |
| Map Memory | Memory Runtime |
| Map Dashboard | Core User Journey |

---

# 26. Final Operating Map Domain Statement

```text
Operating Map Domain defines how Bizzi transforms workspace context into a structured operating model, identifies gaps, creates recommendations and connects operating clarity to execution through functions, tasks, agents, decisions, memory, audit and dashboard visibility.
```

This domain is the bridge between business understanding and operational execution.