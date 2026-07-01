# 06_FUNCTION_RESPONSIBILITY_SERVICE_DESIGN.md

# Bizzi Platform

## Function Responsibility Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 05_PROCESS_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 05_FUNCTION_RESPONSIBILITY_API.md  
**Previous Document:** 05_OPERATING_MAP_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for function and responsibility behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, transaction patterns, audit events and runtime events required to implement the Function Responsibility API.

Core question:

```text
How should Bizzi backend services create business functions, assign ownership and resolve responsibility gaps safely and consistently?
```

---

# 2. Service Scope

This design covers:

```text
FunctionService
ResponsibilityService
OwnershipGapService
```

Primary API references:

```text
GET /api/v1/workspaces/{workspace_id}/functions
POST /api/v1/workspaces/{workspace_id}/functions
GET /api/v1/workspaces/{workspace_id}/functions/{function_id}
PATCH /api/v1/workspaces/{workspace_id}/functions/{function_id}
POST /api/v1/workspaces/{workspace_id}/functions/{function_id}/archive
GET /api/v1/workspaces/{workspace_id}/responsibilities
POST /api/v1/workspaces/{workspace_id}/responsibilities
GET /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}
POST /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}/reassign
POST /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}/archive
GET /api/v1/workspaces/{workspace_id}/ownership-gaps
POST /api/v1/workspaces/{workspace_id}/ownership-gaps/{ownership_gap_id}/resolve
POST /api/v1/workspaces/{workspace_id}/ownership-gaps/{ownership_gap_id}/archive
```

Primary data references:

```text
functions
responsibilities
ownership_gaps
workspace_access
audit_events
runtime_events
```

---

# 3. Module Ownership

Function and responsibility behavior belongs to:

```text
FunctionResponsibilityModule
```

Supporting modules:

```text
WorkspaceModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
OperatingMapModule via gaps
TaskModule later
ProcessModule later
TransactionModule
```

Rule:

```text
FunctionResponsibilityModule owns business function records, accountability assignments and ownership gap lifecycle.
```

---

# 4. Service Responsibilities

## FunctionService

Responsibilities:

```text
list functions
get function
create function
update function
archive function
validate function hierarchy
validate function category and risk_level
preserve function source traceability
emit function audit events
emit function runtime events
```

## ResponsibilityService

Responsibilities:

```text
list responsibilities
get responsibility
assign responsibility
reassign responsibility
archive responsibility
validate responsibility target object
validate owner user
prevent duplicate active ownership where required
emit responsibility audit events
emit responsibility runtime events
```

## OwnershipGapService

Responsibilities:

```text
list ownership gaps
create ownership gaps from detection workflows
resolve ownership gaps
archive ownership gaps
validate resolution responsibility
preserve ownership gap traceability
emit ownership gap audit events
emit ownership gap runtime events
```

---

# 5. Repository Responsibilities

## FunctionRepository

Methods:

```text
createFunction(data)
findByIdAndWorkspace(function_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(function_id, workspace_id, patch)
archiveByIdAndWorkspace(function_id, workspace_id, archive_data)
findChildren(function_id, workspace_id)
nameExistsInWorkspace(workspace_id, name, parent_function_id optional)
```

## ResponsibilityRepository

Methods:

```text
createResponsibility(data)
findByIdAndWorkspace(responsibility_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
findActiveByObject(workspace_id, object_type, object_id, responsibility_type)
updateByIdAndWorkspace(responsibility_id, workspace_id, patch)
reassignByIdAndWorkspace(responsibility_id, workspace_id, reassignment_data)
archiveByIdAndWorkspace(responsibility_id, workspace_id, archive_data)
```

## OwnershipGapRepository

Methods:

```text
createGap(data)
findByIdAndWorkspace(ownership_gap_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
resolveByIdAndWorkspace(ownership_gap_id, workspace_id, resolution_data)
archiveByIdAndWorkspace(ownership_gap_id, workspace_id, archive_data)
findOpenGapForObject(workspace_id, object_type, object_id, gap_type)
```

---

# 6. Service Context

Every service method must receive:

```text
workspace_id
actor_id
actor_type
correlation_id
request_id
idempotency_key optional
```

Rule:

```text
Function and responsibility services must always load records by both object id and workspace_id.
```

---

# 7. Create Function Flow

## Service Method

```text
FunctionService.createFunction(context, input)
```

## Input

```text
name
description optional
category optional
parent_function_id optional
risk_level optional
source_object_type optional
source_object_id optional
metadata optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check create function permission
validate name
validate category if provided
validate risk_level if provided
validate parent_function_id belongs to workspace if provided
validate source object if provided
check duplicate name rule if enabled
begin transaction
create function with active status
record function.created audit event
emit function.created runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return function DTO
```

---

# 8. Create Function Validation

Validation rules:

```text
workspace must exist
workspace must be active
name is required
name must not be empty
category must be valid if supplied
risk_level must be valid if supplied
parent_function_id must belong to same workspace if supplied
parent_function_id must not create a hierarchy cycle
source_object_type must be valid if supplied
source_object_id must exist if supplied
source object must belong to same workspace when workspace-scoped
```

Error mappings:

```text
missing name → validation_error
invalid category → validation_error
invalid risk_level → validation_error
invalid parent_function_id → invalid_object_reference
hierarchy cycle → business_rule_violation
workspace archived → workspace_archived
forbidden actor → forbidden
```

---

# 9. List and Get Function Flows

## List Method

```text
FunctionService.listFunctions(context, filters, pagination)
```

Flow:

```text
validate authenticated actor
check workspace access
validate filters
call FunctionRepository.listByWorkspace
return paginated function DTOs
```

Supported filters:

```text
status
category
parent_function_id
risk_level
```

Default sort:

```text
name:asc
```

## Get Method

```text
FunctionService.getFunction(context, function_id)
```

Flow:

```text
validate authenticated actor
check workspace access
load function by id and workspace_id
return function DTO
```

---

# 10. Update Function Flow

## Service Method

```text
FunctionService.updateFunction(context, function_id, input)
```

## Mutable Fields

```text
name
description
category
parent_function_id
risk_level
metadata
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check update function permission
load function by id and workspace_id
check function is not archived
validate mutable fields
validate hierarchy if parent changes
capture before_state
begin transaction
update function
record function.updated audit event
emit function.updated runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return function DTO
```

---

# 11. Archive Function Flow

## Service Method

```text
FunctionService.archiveFunction(context, function_id, input)
```

## Input

```text
archive_reason optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check archive function permission
load function by id and workspace_id
check function is not already archived
check active dependent responsibilities, processes or tasks according to policy
capture before_state
begin transaction
set function status archived
set archived_at
record function.archived audit event
emit function.archived runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return archived function DTO
```

## Rule

```text
Archiving a function must preserve responsibility and operating history.
```

---

# 12. Assign Responsibility Flow

## Service Method

```text
ResponsibilityService.assignResponsibility(context, input)
```

## Input

```text
object_type
object_id
responsibility_type
owner_user_id
source_object_type optional
source_object_id optional
metadata optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check assign responsibility permission
validate target object_type and object_id
validate target object belongs to workspace
validate responsibility_type
validate owner_user_id exists
validate owner has workspace access when workspace_access is enabled
check duplicate active responsibility rule
validate source object if provided
begin transaction
create responsibility with assigned status
record responsibility.assigned audit event
emit responsibility.assigned runtime event
emit dashboard.refresh_requested runtime event
optionally emit operating_gap.resolution_candidate runtime event
commit transaction
return responsibility DTO
```

---

# 13. Responsibility Target Validation

Supported object types may include:

```text
function
process
task
decision
operating_gap later
```

MVP target:

```text
function
```

Validation rules:

```text
object_type must be valid
object_id must exist
object must belong to workspace
object must not be archived unless policy allows historical assignment
responsibility_type must be valid
owner_user_id must exist
owner_user_id should have workspace access when access model is enabled
```

---

# 14. List and Get Responsibility Flows

## List Method

```text
ResponsibilityService.listResponsibilities(context, filters, pagination)
```

Supported filters:

```text
status
object_type
object_id
owner_user_id
responsibility_type
```

Default sort:

```text
created_at:desc
```

## Get Method

```text
ResponsibilityService.getResponsibility(context, responsibility_id)
```

Flow:

```text
validate authenticated actor
check workspace access
load responsibility by id and workspace_id
return responsibility DTO
```

---

# 15. Reassign Responsibility Flow

## Service Method

```text
ResponsibilityService.reassignResponsibility(context, responsibility_id, input)
```

## Input

```text
owner_user_id
reassignment_reason optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check reassign responsibility permission
load responsibility by id and workspace_id
check responsibility is not archived
validate new owner_user_id exists
validate new owner has workspace access when enabled
capture before_state
begin transaction
update owner_user_id
record responsibility.reassigned audit event
emit responsibility.reassigned runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return responsibility DTO
```

---

# 16. Archive Responsibility Flow

## Service Method

```text
ResponsibilityService.archiveResponsibility(context, responsibility_id, input)
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check archive responsibility permission
load responsibility by id and workspace_id
check responsibility is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record responsibility.archived audit event
emit responsibility.archived runtime event
emit dashboard.refresh_requested runtime event
optionally create ownership_gap if object now has no owner
commit transaction
return archived responsibility DTO
```

---

# 17. Ownership Gap Detection

Ownership gaps may be created by:

```text
operating map analysis
function creation without owner
responsibility archive that leaves object ownerless
periodic ownership audit later
AI recommendation later
```

Detected gaps should preserve:

```text
workspace_id
object_type
object_id
gap_type
title
description
status detected
recommended_owner_id optional
source_object_type optional
source_object_id optional
```

Rule:

```text
Ownership gaps are reviewable records, not automatic assignments.
```

---

# 18. Resolve Ownership Gap Flow

## Service Method

```text
OwnershipGapService.resolveGap(context, ownership_gap_id, input)
```

## Input

```text
resolved_by_responsibility_id
resolution_note optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check ownership gap resolution permission
load ownership gap by id and workspace_id
check gap is not resolved or archived
load responsibility by id and workspace_id
validate responsibility addresses same object or compatible object
capture before_state
begin transaction
set gap status resolved
set resolved_by_responsibility_id
set resolved_at
record ownership_gap.resolved audit event
emit ownership_gap.resolved runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return ownership gap DTO
```

---

# 19. Archive Ownership Gap Flow

## Service Method

```text
OwnershipGapService.archiveGap(context, ownership_gap_id, input)
```

Flow:

```text
validate authenticated actor
load workspace
check archive gap permission
load ownership gap by id and workspace_id
check gap is not already archived
begin transaction
set status archived
set archived_at
record ownership_gap.archived audit event
emit ownership_gap.archived runtime event
commit transaction
return archived ownership gap DTO
```

---

# 20. Authorization Rules

Function responsibility authorization matrix:

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List functions | workspace owner | active workspace access |
| Create function | workspace owner | owner/admin/manager |
| Get function | workspace owner | active workspace access |
| Update function | workspace owner | owner/admin/manager |
| Archive function | workspace owner | owner/admin/manager |
| List responsibilities | workspace owner | active workspace access |
| Assign responsibility | workspace owner | owner/admin/manager |
| Reassign responsibility | workspace owner | owner/admin/manager |
| Archive responsibility | workspace owner | owner/admin/manager |
| List ownership gaps | workspace owner | active workspace access |
| Resolve ownership gap | workspace owner | owner/admin/manager |
| Archive ownership gap | workspace owner | owner/admin/manager |

---

# 21. Audit Events

Function responsibility services should emit:

```text
function.created
function.updated
function.archived
responsibility.assigned
responsibility.reassigned
responsibility.archived
ownership_gap.detected
ownership_gap.resolved
ownership_gap.archived
```

Audit payload should include:

```text
workspace_id
actor_id
actor_type
action
object_type
object_id
source_object_type optional
source_object_id optional
before_state optional
after_state optional
correlation_id
```

---

# 22. Runtime Events

Function responsibility services should emit:

```text
function.created
function.updated
function.archived
responsibility.assigned
responsibility.reassigned
responsibility.archived
ownership_gap.detected
ownership_gap.resolved
ownership_gap.archived
dashboard.refresh_requested
operating_gap.resolution_candidate optional
```

Runtime events may trigger:

```text
dashboard refresh
operating gap resolution suggestions
memory candidate creation later
notification later
ownership review workflow later
```

---

# 23. DTOs

Function DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "parent_function_id": null,
  "name": "Finance",
  "description": "Financial management and reporting function",
  "category": "finance",
  "status": "active",
  "risk_level": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

Responsibility DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "responsibility_type": "owner",
  "owner_user_id": "uuid",
  "status": "assigned",
  "assigned_by": "uuid",
  "assigned_at": "2026-07-01T09:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

Ownership Gap DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "gap_type": "missing_owner",
  "title": "Missing owner for finance function",
  "status": "detected",
  "recommended_owner_id": null,
  "resolved_by_responsibility_id": null,
  "created_at": "2026-07-01T09:00:00Z"
}
```

---

# 24. Error Mapping

Function responsibility service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
FunctionNotFound → not_found
ResponsibilityNotFound → not_found
OwnershipGapNotFound → not_found
AccessDenied → forbidden
InvalidFunctionCategory → validation_error
InvalidRiskLevel → validation_error
InvalidParentFunction → invalid_object_reference
FunctionHierarchyCycle → business_rule_violation
InvalidObjectReference → invalid_object_reference
InvalidOwner → invalid_owner
DuplicateActiveResponsibility → conflict
InvalidStatusTransition → invalid_status_transition
IncompatibleGapResolution → business_rule_violation
```

---

# 25. MVP Simplifications

MVP may simplify by:

```text
flat function list before full hierarchy
function object_type only for responsibilities
owner responsibility type only
owner-only authorization
ownership gaps derived from operating gaps or missing owner checks
simple assigned → archived lifecycle
no dedicated responsibility history table
```

MVP must preserve:

```text
workspace scope
owner traceability
audit events
runtime events
no hard-delete of confirmed responsibility history
structured validation and error mapping
```

---

# 26. Future Expansion

Future service expansion may add:

```text
function hierarchy management
function merge and split flows
RACI responsibility types
responsibility review dates
ownership escalation rules
bulk responsibility assignment
ownership conflict detection
function health scoring
responsibility history table
ownership review workflows
```

---

# 27. Testing Expectations

Service tests should cover:

```text
create function validates workspace and fields
create function rejects hierarchy cycle
update archived function is rejected
archive function preserves history
assign responsibility validates target object workspace
assign responsibility validates owner access
duplicate owner responsibility is prevented where configured
reassign responsibility changes owner and audits change
archive responsibility can create ownership gap
resolve ownership gap requires compatible responsibility
all mutations emit audit events
all mutations emit runtime events
workspace archived blocks mutations
```

Repository tests should cover:

```text
list functions by workspace and filters
find function by id and workspace
find function children
list responsibilities by object and owner
find active responsibility by object
list ownership gaps by workspace
resolve ownership gap by id and workspace
pagination and sorting behavior
```

---

# 28. Acceptance Criteria

Function Responsibility Service Design is accepted when:

- FunctionService responsibilities are defined;
- ResponsibilityService responsibilities are defined;
- OwnershipGapService responsibilities are defined;
- repository methods are identified;
- function create, update and archive flows are documented;
- responsibility assign, reassign and archive flows are documented;
- ownership gap detection and resolution flows are documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- DTOs and error mappings are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Agent Process Task Decision Service Design
```

---

# 29. Final Statement

```text
Bizzi Function Responsibility Service Design defines how backend services turn operating structure into accountable ownership through workspace-scoped, transactional, auditable and implementation-ready service behavior.
```

This service layer makes every business function ownable, reviewable and governable.