# 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md

# Bizzi Platform

## Function Responsibility Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 02_CORE_RUNTIME_COMPONENTS.md  
**Domain Reference:** 26_DOMAIN_MODEL / 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Function and Responsibility Data Model for Bizzi Platform.

It translates the Function and Responsibility Domain into database tables, columns, relationships, constraints and indexing rules that support business function structure, human accountability, ownership gaps and governance visibility.

Core question:

```text
How does Bizzi persist business functions and responsibility assignments so that every operating area can be owned, traced and governed?
```

---

# 2. Data Model Role

The Function and Responsibility Data Model stores the organizational operating structure of a workspace.

It supports:

- business function definition;
- function classification;
- function confirmation;
- responsibility assignment;
- ownership visibility;
- ownership gap tracking;
- accountability audit;
- dashboard ownership indicators;
- task and process routing;
- future RACI expansion.

---

# 3. Tables in Scope

MVP tables:

```text
functions
responsibilities
```

Near-MVP tables:

```text
ownership_gaps
```

Expansion tables:

```text
responsibility_assignments
function_categories
responsibility_scopes
```

Recommended MVP implementation:

```text
functions
responsibilities
```

---

# 4. Workspace Scope Rule

All Function and Responsibility tables must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This ensures that functions, ownership and accountability records are isolated by workspace and safe for AI context, dashboard queries, audit records and exports.

---

# 5. functions Table

## Purpose

Stores business functions or operating areas inside a workspace.

## Domain Entity

```text
Function
```

## Table

```text
functions
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
category TEXT NULL
description TEXT NULL
purpose TEXT NULL
parent_function_id UUID NULL REFERENCES functions(id)
status TEXT NOT NULL
priority TEXT NULL
risk_level TEXT NULL
maturity_level TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial values:

```text
suggested
active
archived
```

Expansion values:

```text
draft
confirmed
reviewed
```

## Category Values

Initial MVP categories:

```text
operations
sales
finance
administration
risk
```

Expansion categories:

```text
strategy
marketing
legal
hr
procurement
logistics
customer_support
technology
compliance
```

## Notes

Functions may be created manually, suggested by Operating Map, or generated from AI-assisted business intake.

---

# 6. responsibilities Table

## Purpose

Stores ownership and accountability assignments for domain objects.

## Domain Entity

```text
Responsibility
```

## Table

```text
responsibilities
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
object_type TEXT NOT NULL
object_id UUID NOT NULL
owner_user_id UUID NULL REFERENCES users(id)
responsibility_type TEXT NOT NULL
status TEXT NOT NULL
scope TEXT NULL
assigned_by UUID NULL REFERENCES users(id)
assigned_at TIMESTAMPTZ NULL
review_date DATE NULL
escalation_rule TEXT NULL
notes TEXT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Object Types

Initial object types:

```text
function
process
task
decision
```

Expansion object types:

```text
agent
integration
export
memory_entry
```

## Responsibility Types

MVP value:

```text
owner
```

Expansion values:

```text
accountable
reviewer
approver
operator
observer
```

## Status Values

Initial values:

```text
unassigned
assigned
archived
```

Expansion values:

```text
suggested
reviewed
changed
```

## Notes

The pair `object_type + object_id` provides polymorphic responsibility assignment across functions, processes, tasks and decisions.

Service logic must verify that the referenced object exists and belongs to the same workspace.

---

# 7. ownership_gaps Table

## Purpose

Stores explicit ownership gaps where accountability is missing or unclear.

## Domain Entity

```text
OwnershipGap
```

## MVP Status

```text
Priority 2 / Near-MVP
```

## Table

```text
ownership_gaps
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
object_type TEXT NOT NULL
object_id UUID NOT NULL
gap_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
severity TEXT NULL
status TEXT NOT NULL
recommended_owner_id UUID NULL REFERENCES users(id)
recommended_action TEXT NULL
resolved_by_responsibility_id UUID NULL REFERENCES responsibilities(id)
resolved_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Gap Type Values

Initial values:

```text
missing_owner
unclear_owner
owner_inactive
responsibility_conflict
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
rejected
in_progress
```

## Notes

Ownership gaps may also be represented as `operating_gaps` with `gap_type = missing_owner`.

This table becomes useful when ownership management needs its own lifecycle and dashboard.

---

# 8. responsibility_assignments Table

## Purpose

Stores historical ownership assignment actions.

## Domain Entity

```text
ResponsibilityAssignment
```

## MVP Status

```text
Expansion
```

## Table

```text
responsibility_assignments
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
responsibility_id UUID NOT NULL REFERENCES responsibilities(id)
owner_user_id UUID NOT NULL REFERENCES users(id)
assigned_by UUID NULL REFERENCES users(id)
assigned_at TIMESTAMPTZ NOT NULL DEFAULT now()
assignment_reason TEXT NULL
status TEXT NOT NULL
metadata JSONB NULL
```

## MVP Simplification

Do not implement this table in the first MVP unless detailed assignment history is required.

Use:

```text
responsibilities.assigned_by
responsibilities.assigned_at
audit_events
```

for initial traceability.

---

# 9. Relationships

## Workspace to Function

```text
company_workspaces.id → functions.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many Functions
```

## Function to Parent Function

```text
functions.id → functions.parent_function_id
```

Relationship:

```text
Function 1 → many child Functions
```

MVP note:

```text
Function hierarchy can be optional in the first release.
```

## Workspace to Responsibility

```text
company_workspaces.id → responsibilities.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many Responsibilities
```

## Responsibility to User

```text
users.id → responsibilities.owner_user_id
```

Relationship:

```text
User 1 → many Responsibilities
```

## Responsibility to Object

```text
responsibilities.object_type + responsibilities.object_id → target object
```

Target examples:

```text
functions.id
processes.id
tasks.id
decisions.id
```

---

# 10. Source Traceability

Functions should support:

```text
source_object_type
source_object_id
```

Examples:

```text
source_object_type = 'operating_map'
source_object_type = 'operating_gap'
source_object_type = 'agent_recommendation'
source_object_type = 'user_input'
```

Responsibilities may be traceable through:

```text
assigned_by
assigned_at
audit_events
metadata
```

Ownership gaps should identify the affected object through:

```text
object_type
object_id
```

---

# 11. Indexing Requirements

## functions

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, category)
INDEX(parent_function_id)
INDEX(source_object_type, source_object_id)
```

Optional later:

```text
UNIQUE(workspace_id, name)
```

This unique constraint should be considered carefully because different business functions may share similar names across versions or imports.

## responsibilities

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, object_type, object_id)
INDEX(owner_user_id)
INDEX(assigned_by)
```

Optional later:

```text
UNIQUE(workspace_id, object_type, object_id, responsibility_type)
```

This may be appropriate when only one owner is allowed per object and responsibility type.

## ownership_gaps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, gap_type)
INDEX(workspace_id, object_type, object_id)
INDEX(recommended_owner_id)
INDEX(resolved_by_responsibility_id)
```

---

# 12. Data Integrity Rules

Recommended database-level rules:

```text
functions.workspace_id IS NOT NULL
functions.name IS NOT NULL
functions.status IS NOT NULL
responsibilities.workspace_id IS NOT NULL
responsibilities.object_type IS NOT NULL
responsibilities.object_id IS NOT NULL
responsibilities.responsibility_type IS NOT NULL
responsibilities.status IS NOT NULL
```

Service-level rules:

```text
Active function should have owner responsibility or explicit ownership gap.
Assigned responsibility should have owner_user_id.
Responsibility target object must belong to the same workspace.
AI-suggested function must be confirmed before becoming authoritative.
Ownership gap should be resolved by a responsibility assignment.
Archived functions cannot be modified through normal flows.
```

---

# 13. Responsibility Validation Pattern

Because `responsibilities.object_type + object_id` is polymorphic, database foreign keys cannot fully enforce all target references.

Backend service validation must enforce:

```text
object exists
object belongs to workspace_id
user has authorization
responsibility_type is valid
status transition is valid
```

Audit should record responsibility changes.

---

# 14. AI Suggestion Persistence

AI may suggest functions or owners.

Function suggestions may be persisted as:

```text
functions.status = 'suggested'
functions.source_object_type = 'agent_recommendation'
functions.source_object_id = agent_recommendations.id
```

Owner suggestions may be persisted as:

```text
ownership_gaps.recommended_owner_id
ownership_gaps.recommended_action
```

or as an Agent Recommendation in later layers.

Rule:

```text
AI may suggest responsibility. Human confirmation must create the official responsibility assignment.
```

---

# 15. Audit Requirements

Function and Responsibility actions that should create audit records:

```text
function.suggested
function.created
function.confirmed
function.updated
function.archived
responsibility.required
responsibility.suggested
responsibility.assigned
responsibility.changed
responsibility.removed
ownership_gap.detected
ownership_gap.resolved
```

Audit target examples:

```text
object_type = 'function'
object_id = functions.id
```

```text
object_type = 'responsibility'
object_id = responsibilities.id
```

---

# 16. Runtime Event Requirements

Runtime event types:

```text
function.suggested
function.created
function.confirmed
function.updated
function.archived
responsibility.required
responsibility.assigned
responsibility.changed
responsibility.removed
ownership_gap.detected
ownership_gap.resolved
```

Event source pattern:

```text
source_object_type = 'function'
source_object_id = functions.id
```

or:

```text
source_object_type = 'responsibility'
source_object_id = responsibilities.id
```

---

# 17. Dashboard Requirements

Dashboard should query Function and Responsibility data for:

- active functions;
- functions by category;
- functions without owners;
- responsibilities by owner;
- ownership gaps;
- recently changed responsibilities;
- functions with open tasks;
- functions supported by agents.

Core dashboard queries should be supported by:

```text
functions.workspace_id, status
functions.workspace_id, category
responsibilities.workspace_id, object_type, object_id
responsibilities.owner_user_id
ownership_gaps.workspace_id, status
```

---

# 18. Memory Requirements

Memory may be created from:

- confirmed function context;
- responsibility assignments;
- ownership gaps;
- function reviews;
- governance lessons.

Memory source references should point back to:

```text
functions.id
responsibilities.id
ownership_gaps.id
```

---

# 19. MVP Simplifications

For MVP, Bizzi may simplify by:

- implementing only `functions` and `responsibilities`;
- representing ownership gaps as `operating_gaps` first;
- using `owner_user_id` on tasks and decisions for direct ownership;
- using audit events instead of `responsibility_assignments`;
- using text statuses before formal PostgreSQL ENUM migration;
- using service-level validation for polymorphic responsibility targets.

These simplifications must preserve accountability visibility.

---

# 20. Future Expansion

Future Function and Responsibility Data Model may add:

```text
ownership_gaps
responsibility_assignments
function_categories
function_reviews
responsibility_scopes
raci_assignments
org_units
escalation_rules
```

These should be introduced when governance and collaboration behavior requires them.

---

# 21. Acceptance Criteria

Function Responsibility Data Model is ready when:

- functions table is defined;
- responsibilities table is defined;
- ownership_gaps expansion path is defined;
- responsibility assignment history path is defined;
- workspace scoping is explicit;
- polymorphic responsibility validation is documented;
- indexes are identified;
- audit and event requirements are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 22. Final Function Responsibility Data Model Statement

```text
Bizzi Function Responsibility Data Model defines how the platform persists business functions, ownership assignments and accountability gaps as workspace-scoped, auditable and dashboard-visible database records.
```

This model ensures Bizzi can show what the company does, who owns it and where accountability is missing.