# 05_OPERATING_MAP_DATA_MODEL.md

# Bizzi Platform

## Operating Map Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 01_RUNTIME_ARCHITECTURE.md  
**Domain Reference:** 26_DOMAIN_MODEL / 03_OPERATING_MAP_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Operating Map Data Model for Bizzi Platform.

It translates the Operating Map Domain into database tables, columns, relationships, constraints and indexing rules that support operating map generation, gap detection, recommendations and first-hour business visibility.

Core question:

```text
How does Bizzi persist the company operating map, operating gaps and recommendations as structured, workspace-scoped and traceable data?
```

---

# 2. Data Model Role

The Operating Map Data Model stores the first structured representation of how a workspace operates.

It supports:

- AI-generated operating maps;
- user-confirmed operating structure;
- operating gaps;
- suggested actions;
- source traceability;
- dashboard visibility;
- audit and event linkage;
- future map nodes and graph representation.

---

# 3. Tables in Scope

MVP tables:

```text
operating_maps
operating_gaps
```

Near-MVP tables:

```text
operating_recommendations
```

Expansion tables:

```text
operating_map_nodes
```

Recommended MVP implementation:

```text
operating_maps
operating_gaps
```

Optional if AI recommendations are persisted separately:

```text
operating_recommendations
```

---

# 4. Workspace Scope Rule

All Operating Map tables must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This ensures that operating map data is isolated by workspace and can be safely used for dashboard, memory, audit, export and AI context assembly.

---

# 5. operating_maps Table

## Purpose

Stores the structured operating map for a workspace.

## Domain Entity

```text
OperatingMap
```

## Table

```text
operating_maps
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
summary TEXT NULL
status TEXT NOT NULL
version INTEGER NOT NULL DEFAULT 1
generated_by_ai BOOLEAN NOT NULL DEFAULT false
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
source_context_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial values:

```text
generated
confirmed
active
archived
```

Expansion values:

```text
draft
reviewed
updated
```

## Notes

MVP may enforce one active operating map per workspace at service level.

Later versions may support historical maps and version comparison.

---

# 6. operating_gaps Table

## Purpose

Stores missing, weak or unclear parts of the workspace operating model.

## Domain Entity

```text
OperatingGap
```

## Table

```text
operating_gaps
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
operating_map_id UUID NULL REFERENCES operating_maps(id)
function_id UUID NULL REFERENCES functions(id)
gap_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
severity TEXT NULL
status TEXT NOT NULL
recommended_action TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
resolved_by_object_type TEXT NULL
resolved_by_object_id UUID NULL
resolved_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Gap Type Values

Initial values:

```text
missing_function
missing_owner
missing_process
missing_task
operational_risk
```

Expansion values:

```text
missing_decision
missing_agent_support
unclear_responsibility
memory_gap
audit_gap
integration_gap
```

## Status Values

Initial values:

```text
detected
accepted
resolved
archived
```

Expansion values:

```text
reviewed
in_progress
rejected
```

## Severity Values

Initial values:

```text
low
medium
high
critical
```

---

# 7. operating_recommendations Table

## Purpose

Stores suggested actions generated from an operating map or operating gap.

## Domain Entity

```text
OperatingRecommendation
```

## MVP Status

```text
Priority 2 / Near-MVP
```

## Table

```text
operating_recommendations
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
operating_map_id UUID NULL REFERENCES operating_maps(id)
source_gap_id UUID NULL REFERENCES operating_gaps(id)
recommendation_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
suggested_object_type TEXT NULL
suggested_object_payload JSONB NULL
confidence TEXT NULL
created_by_agent_id UUID NULL REFERENCES agents(id)
reviewed_by UUID NULL REFERENCES users(id)
reviewed_at TIMESTAMPTZ NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
rejected_at TIMESTAMPTZ NULL
result_object_type TEXT NULL
result_object_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Recommendation Type Values

Initial values:

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

## Status Values

Initial values:

```text
created
confirmed
rejected
applied
archived
```

## Notes

MVP may create suggested functions or tasks directly with `status = suggested` instead of using this table.

This table becomes useful when Bizzi needs to preserve AI recommendation review history.

---

# 8. operating_map_nodes Table

## Purpose

Stores graph-like operating map nodes for future advanced visualization.

## Domain Entity

```text
OperatingMapNode
```

## MVP Status

```text
Expansion
```

## Table

```text
operating_map_nodes
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
operating_map_id UUID NOT NULL REFERENCES operating_maps(id)
parent_node_id UUID NULL REFERENCES operating_map_nodes(id)
node_type TEXT NOT NULL
title TEXT NOT NULL
status TEXT NOT NULL
linked_object_type TEXT NULL
linked_object_id UUID NULL
position JSONB NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Do not implement this table in the first MVP unless a visual operating map graph becomes required.

Use:

```text
operating_maps
operating_gaps
functions
responsibilities
tasks
```

as the first structured operating model.

---

# 9. Relationships

## Workspace to Operating Map

```text
company_workspaces.id → operating_maps.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many OperatingMaps
```

MVP rule:

```text
CompanyWorkspace 1 → 1 active OperatingMap
```

## Operating Map to Gap

```text
operating_maps.id → operating_gaps.operating_map_id
```

Relationship:

```text
OperatingMap 1 → many OperatingGaps
```

## Function to Gap

```text
functions.id → operating_gaps.function_id
```

Relationship:

```text
Function 1 → many OperatingGaps
```

## Gap to Recommendation

```text
operating_gaps.id → operating_recommendations.source_gap_id
```

Relationship:

```text
OperatingGap 1 → many OperatingRecommendations
```

---

# 10. Source Traceability

Operating gaps and recommendations should support:

```text
source_object_type
source_object_id
```

Examples:

```text
source_object_type = 'operating_map'
source_object_type = 'function'
source_object_type = 'agent_recommendation'
source_object_type = 'user_input'
```

Resolution traceability should use:

```text
resolved_by_object_type
resolved_by_object_id
```

Examples:

```text
resolved_by_object_type = 'task'
resolved_by_object_type = 'responsibility'
resolved_by_object_type = 'process'
resolved_by_object_type = 'function'
```

---

# 11. Indexing Requirements

## operating_maps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, version)
```

Optional later:

```text
UNIQUE(workspace_id, version)
PARTIAL UNIQUE(workspace_id) WHERE status = 'active'
```

## operating_gaps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, gap_type)
INDEX(operating_map_id)
INDEX(function_id)
INDEX(source_object_type, source_object_id)
INDEX(resolved_by_object_type, resolved_by_object_id)
```

## operating_recommendations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, recommendation_type)
INDEX(operating_map_id)
INDEX(source_gap_id)
INDEX(result_object_type, result_object_id)
```

---

# 12. Data Integrity Rules

Recommended database-level rules:

```text
operating_maps.workspace_id IS NOT NULL
operating_maps.title IS NOT NULL
operating_maps.status IS NOT NULL
operating_gaps.workspace_id IS NOT NULL
operating_gaps.gap_type IS NOT NULL
operating_gaps.title IS NOT NULL
operating_gaps.status IS NOT NULL
```

Service-level rules:

```text
Only one active operating map per workspace.
AI-generated operating map must be confirmed before becoming authoritative.
Resolved gap should reference resolved_by_object_type and resolved_by_object_id.
Archived maps cannot be modified through normal flows.
Rejected recommendations cannot create runtime objects.
```

---

# 13. AI Generation Persistence

AI-generated operating map data should preserve:

```text
generated_by_ai
source_context_id
confirmed_by
confirmed_at
metadata
```

AI-generated recommendations should preserve:

```text
created_by_agent_id
confidence
suggested_object_type
suggested_object_payload
status
reviewed_by
confirmed_by
confirmed_at
```

Rule:

```text
AI may generate draft structure, but confirmed operating meaning must be traceable to human confirmation.
```

---

# 14. Audit Requirements

Operating Map actions that should create audit records:

```text
operating_map.generated
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

Audit target examples:

```text
object_type = 'operating_map'
object_id = operating_maps.id
```

```text
object_type = 'operating_gap'
object_id = operating_gaps.id
```

---

# 15. Runtime Event Requirements

Runtime event types:

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

Event source pattern:

```text
source_object_type = 'operating_map'
source_object_id = operating_maps.id
```

or:

```text
source_object_type = 'operating_gap'
source_object_id = operating_gaps.id
```

---

# 16. Dashboard Requirements

Dashboard should query Operating Map data for:

- active operating map status;
- number of open gaps;
- gaps by severity;
- gaps by type;
- ownership gaps;
- recommended next actions;
- recently resolved gaps;
- operating map confirmation status.

Core dashboard queries should be supported by:

```text
operating_maps.workspace_id, status
operating_gaps.workspace_id, status
operating_gaps.workspace_id, gap_type
```

---

# 17. Memory Requirements

Memory may be created from:

- confirmed operating map summary;
- accepted operating gaps;
- resolved operating gaps;
- confirmed recommendations;
- operating structure changes.

Memory source references should point back to:

```text
operating_maps.id
operating_gaps.id
operating_recommendations.id
```

---

# 18. MVP Simplifications

For MVP, Bizzi may simplify by:

- storing one active operating map per workspace;
- postponing `operating_map_nodes`;
- creating suggested functions and tasks directly rather than through `operating_recommendations`;
- using text statuses before formal PostgreSQL ENUM migration;
- using service-level enforcement for active map uniqueness.

These simplifications must preserve workspace scope and source traceability.

---

# 19. Future Expansion

Future Operating Map Data Model may add:

```text
operating_map_nodes
operating_map_versions
operating_recommendations
operating_map_reviews
operating_map_snapshots
operating_map_edges
```

These should be introduced when product behavior requires advanced visualization, versioning or recommendation review.

---

# 20. Acceptance Criteria

Operating Map Data Model is ready when:

- operating_maps table is defined;
- operating_gaps table is defined;
- operating_recommendations expansion path is defined;
- operating_map_nodes expansion path is defined;
- workspace scoping is explicit;
- source and resolution traceability are defined;
- indexes are identified;
- audit and event requirements are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 21. Final Operating Map Data Model Statement

```text
Bizzi Operating Map Data Model defines how the platform persists the workspace operating structure, detected gaps and recommended actions as traceable, auditable and workspace-scoped database records.
```

This model enables Bizzi to turn business context into durable operating visibility and actionable next steps.