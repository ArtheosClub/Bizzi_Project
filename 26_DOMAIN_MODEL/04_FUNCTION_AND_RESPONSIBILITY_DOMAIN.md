# 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md

# Bizzi Platform

## Function and Responsibility Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 02_CORE_RUNTIME_COMPONENTS.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Function and Responsibility Domain for Bizzi Platform.

The domain describes how Bizzi represents business functions, ownership, accountability gaps and responsibility assignments inside a company workspace.

Core question:

```text
How does Bizzi define what work areas exist in a company and who is accountable for them?
```

---

# 2. Domain Role

The Function and Responsibility Domain connects operating structure to governance.

It provides:

- business function structure;
- ownership visibility;
- responsibility assignment;
- accountability gaps;
- escalation foundation;
- links to agents, processes, tasks and decisions;
- dashboard indicators;
- audit and memory traceability.

---

# 3. Domain Principle

```text
Every Function Needs Ownership
```

Bizzi must make it visible when a business function exists without a clear accountable owner.

The system should not hide responsibility gaps. It should surface them and convert them into actions.

---

# 4. Aggregate Boundaries

Primary aggregate roots:

```text
Function
Responsibility
```

Supporting entities:

```text
FunctionCategory
FunctionStatus
ResponsibilityAssignment
OwnershipGap
ResponsibilityScope
```

Related external entities:

```text
CompanyWorkspace
OperatingMap
OperatingGap
User
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

## 5.1 Function

Represents a business function inside a workspace.

Minimum domain attributes:

```text
id
workspace_id
name
category
status
created_at
updated_at
created_by
```

Optional domain attributes:

```text
description
purpose
parent_function_id
priority
risk_level
maturity_level
source_object_type
source_object_id
confirmed_by
confirmed_at
```

Domain responsibility:

```text
Function defines a business capability or operating area that must be visible, structured and governed.
```

---

## 5.2 Responsibility

Represents accountability for a function, process, task or decision.

Minimum domain attributes:

```text
id
workspace_id
object_type
object_id
owner_user_id
responsibility_type
status
created_at
updated_at
```

Optional domain attributes:

```text
scope
assigned_by
assigned_at
review_date
escalation_rule
notes
```

Domain responsibility:

```text
Responsibility connects operating objects to accountable humans.
```

---

## 5.3 ResponsibilityAssignment

Represents a concrete act of assigning ownership.

Potential attributes:

```text
id
workspace_id
responsibility_id
owner_user_id
assigned_by
assigned_at
assignment_reason
status
```

Domain responsibility:

```text
ResponsibilityAssignment preserves the history and rationale of ownership changes.
```

MVP simplification:

```text
ResponsibilityAssignment may be represented through Responsibility fields and AuditEvent history.
```

---

## 5.4 OwnershipGap

Represents a missing or unclear owner.

Minimum domain attributes:

```text
id
workspace_id
object_type
object_id
gap_type
severity
status
created_at
updated_at
```

Optional domain attributes:

```text
description
recommended_owner_id
recommended_action
resolved_by_responsibility_id
resolved_at
```

Domain responsibility:

```text
OwnershipGap makes accountability problems visible and actionable.
```

---

# 6. Function Categories

Initial function categories:

```text
strategy
operations
sales
marketing
finance
legal
risk
hr
procurement
logistics
customer_support
technology
administration
compliance
```

MVP may begin with a smaller set:

```text
operations
sales
finance
administration
risk
```

---

# 7. Responsibility Types

Initial responsibility types:

```text
owner
accountable
reviewer
approver
operator
observer
```

MVP responsibility type:

```text
owner
```

Future expansion can distinguish RACI-style roles.

---

# 8. Function Lifecycle

Recommended lifecycle:

```text
suggested
↓
draft
↓
confirmed
↓
active
↓
reviewed
↓
archived
```

MVP lifecycle:

```text
suggested
active
archived
```

---

# 9. Responsibility Lifecycle

Recommended lifecycle:

```text
unassigned
↓
suggested
↓
assigned
↓
reviewed
↓
changed
↓
archived
```

MVP lifecycle:

```text
unassigned
assigned
archived
```

---

# 10. Domain Relationships

## 10.1 Workspace to Function

```text
CompanyWorkspace 1 → many Functions
```

## 10.2 Function to Responsibility

```text
Function 1 → many Responsibilities
```

MVP simplification:

```text
Function 1 → 0 or 1 Owner Responsibility
```

## 10.3 Function to Process

```text
Function 1 → many Processes
```

## 10.4 Function to Task

```text
Function 1 → many Tasks
```

## 10.5 Function to Agent

```text
Function 1 → many Agents
```

## 10.6 Responsibility to User

```text
Responsibility many → 1 User
```

---

# 11. Domain Invariants

The domain must enforce:

```text
Function must belong to one workspace.
Active Function should have a clear status.
Responsibility must belong to one workspace.
Assigned Responsibility must reference an owner_user_id.
OwnershipGap must reference the object with unclear ownership.
Archived functions cannot receive normal operational updates.
AI-suggested functions require confirmation before becoming authoritative.
Responsibility changes must be auditable.
```

---

# 12. AI Suggestion Rules

AI may suggest:

- missing functions;
- function categories;
- likely owners;
- responsibility gaps;
- next tasks;
- process candidates;
- agent support candidates.

AI may not automatically:

- assign final human accountability;
- remove an owner;
- archive a function;
- mark an ownership gap resolved;
- bypass audit.

MVP rule:

```text
AI may recommend responsibility. Human confirms accountability.
```

---

# 13. Function Creation Flow

```text
Operating map generated
↓
Suggested functions created
↓
User reviews function list
↓
Function confirmed or edited
↓
Owner assigned or ownership gap created
↓
Related tasks or process suggestions generated
↓
Audit event recorded
↓
Memory entry created if useful
↓
Dashboard updated
```

---

# 14. Responsibility Assignment Flow

```text
Function or object requires owner
↓
Responsibility Runtime checks ownership
↓
Owner suggested or selected
↓
User confirms assignment
↓
Responsibility record created
↓
Ownership gap resolved if applicable
↓
Audit event recorded
↓
Dashboard updated
```

---

# 15. Domain Events

Function events:

```text
function.suggested
function.created
function.confirmed
function.updated
function.reviewed
function.archived
```

Responsibility events:

```text
responsibility.required
responsibility.suggested
responsibility.assigned
responsibility.changed
responsibility.removed
ownership_gap.detected
ownership_gap.resolved
```

---

# 16. Audit Requirements

Audited actions:

```text
function.created
function.confirmed
function.updated
function.archived
responsibility.assigned
responsibility.changed
responsibility.removed
ownership_gap.detected
ownership_gap.resolved
```

Audit must answer:

```text
Who created or changed the function or responsibility, what changed, and which workspace object was affected?
```

---

# 17. Memory Requirements

Memory may be created from:

- confirmed functions;
- responsibility assignments;
- ownership gaps;
- function reviews;
- function changes;
- governance lessons.

Memory types:

```text
function_context
responsibility_context
ownership_gap
function_change
governance_lesson
```

---

# 18. Dashboard Requirements

Dashboard should show:

- active functions;
- functions without owners;
- ownership gaps;
- responsibilities by owner;
- suggested functions;
- recently changed responsibilities;
- functions with open tasks;
- functions supported by agents.

Dashboard question:

```text
Which business areas exist, who owns them, and where is accountability missing?
```

---

# 19. Security Requirements

Security requirements:

```text
Function belongs to one workspace.
Responsibility belongs to one workspace.
Only authorized users may create or edit functions.
Only authorized users may assign or change owners.
AI suggestions must not become final ownership without confirmation.
Responsibility changes must be audited.
```

---

# 20. MVP Domain Behavior

MVP should support:

```text
Create function
Confirm suggested function
List functions by workspace
Assign owner to function
Detect function without owner
Create ownership gap
Resolve ownership gap through owner assignment
Show function and ownership status on dashboard
Create audit events for ownership changes
Create memory from confirmed function context
```

---

# 21. Out of Scope for MVP

The domain does not need in MVP:

- full RACI matrix UI;
- multi-owner approval chains;
- complex org chart;
- department hierarchy;
- role inheritance;
- automatic reassignment;
- enterprise delegation workflows;
- performance management.

---

# 22. Data Model Implications

Future Data Model should include tables or collections for:

```text
functions
responsibilities
ownership_gaps
```

Potential later tables:

```text
function_categories
responsibility_assignments
responsibility_scopes
```

Recommended indexes later:

```text
functions.workspace_id
functions.status
functions.category
responsibilities.workspace_id
responsibilities.object_type
responsibilities.object_id
responsibilities.owner_user_id
ownership_gaps.workspace_id
ownership_gaps.status
```

---

# 23. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/functions
GET /workspaces/{workspace_id}/functions
GET /workspaces/{workspace_id}/functions/{function_id}
PATCH /workspaces/{workspace_id}/functions/{function_id}
POST /workspaces/{workspace_id}/functions/{function_id}/archive
POST /workspaces/{workspace_id}/responsibilities
PATCH /workspaces/{workspace_id}/responsibilities/{responsibility_id}
GET /workspaces/{workspace_id}/ownership-gaps
POST /workspaces/{workspace_id}/ownership-gaps/{gap_id}/resolve
```

---

# 24. Traceability Pattern

Function and Responsibility traceability chain:

```text
OperatingMap / OperatingGap
↓
Function
↓
Responsibility / OwnershipGap
↓
Task / Process / Agent / Decision
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

# 25. Acceptance Criteria

Function and Responsibility Domain is ready when:

- Function is defined as a core domain entity;
- Responsibility is defined;
- OwnershipGap is defined;
- lifecycle states are clear;
- ownership invariants are explicit;
- AI suggestion rules are defined;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 26. Architecture Alignment

| Domain Area | Reference |
|---|---|
| Function | Enterprise Function Registry / Core Runtime Components |
| Responsibility | Governance Baseline / Responsibility Runtime |
| OwnershipGap | Operating Map Domain / Task Runtime |
| AI Suggestions | Agent Runtime / AI Orchestration Runtime |
| Audit | Audit Runtime |
| Memory | Memory Runtime |
| Events | Event Runtime |
| Dashboard | Core User Journey |
| Security | Runtime Security |

---

# 27. Final Function and Responsibility Domain Statement

```text
Function and Responsibility Domain defines how Bizzi represents the company’s operating areas and connects them to clear human accountability, making ownership visible, governable, auditable and actionable.
```

This domain ensures Bizzi can show not only what the company does, but who is responsible for making it work.