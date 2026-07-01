# 05_OPERATING_MAP_SERVICE_DESIGN.md

# Bizzi Platform

## Operating Map Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 05_PROCESS_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 03_OPERATING_MAP_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 05_OPERATING_MAP_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 04_OPERATING_MAP_API.md  
**Previous Document:** 04_WORKSPACE_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for operating map behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, transaction patterns, audit events and runtime events required to implement the Operating Map API.

Core question:

```text
How should Bizzi backend services generate, confirm, archive and improve workspace operating maps safely and consistently?
```

---

# 2. Service Scope

This design covers:

```text
OperatingMapService
OperatingGapService
OperatingRecommendationService
```

Primary API references:

```text
GET /api/v1/workspaces/{workspace_id}/operating-maps
POST /api/v1/workspaces/{workspace_id}/operating-maps/generate
GET /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/confirm
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/archive
GET /api/v1/workspaces/{workspace_id}/operating-gaps
GET /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/accept
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/resolve
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/archive
GET /api/v1/workspaces/{workspace_id}/operating-recommendations
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/confirm
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/apply
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/reject
```

Primary data references:

```text
operating_maps
operating_gaps
operating_recommendations
functions
responsibilities
audit_events
runtime_events
```

---

# 3. Module Ownership

Operating map behavior belongs to:

```text
OperatingMapModule
```

Supporting modules:

```text
WorkspaceModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
FunctionResponsibilityModule
AgentModule later
DashboardModule via runtime event
TransactionModule
```

Rule:

```text
OperatingMapModule owns operating map and gap lifecycle. Other modules own the records created as resolution results.
```

---

# 4. Service Responsibilities

## OperatingMapService

Responsibilities:

```text
list operating maps
get operating map
generate operating map
confirm operating map
archive operating map
validate map lifecycle transitions
coordinate map generation
emit operating map audit events
emit operating map runtime events
```

## OperatingGapService

Responsibilities:

```text
list operating gaps
get operating gap
create detected gaps during generation
accept operating gaps
resolve operating gaps
archive operating gaps
validate resolution object compatibility
emit gap audit events
emit gap runtime events
```

## OperatingRecommendationService

Responsibilities:

```text
list operating recommendations
create recommendations during map analysis
confirm recommendations
apply recommendations through target module services
reject recommendations
track result objects
preserve AI and human confirmation traceability
```

---

# 5. Repository Responsibilities

## OperatingMapRepository

Methods:

```text
createMap(data)
findByIdAndWorkspace(operating_map_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
findActiveMap(workspace_id)
updateByIdAndWorkspace(operating_map_id, workspace_id, patch)
archiveByIdAndWorkspace(operating_map_id, workspace_id, archive_data)
getNextVersion(workspace_id)
```

## OperatingGapRepository

Methods:

```text
createGap(data)
createManyGaps(gaps)
findByIdAndWorkspace(operating_gap_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(operating_gap_id, workspace_id, patch)
resolveByIdAndWorkspace(operating_gap_id, workspace_id, resolution_data)
archiveByIdAndWorkspace(operating_gap_id, workspace_id, archive_data)
```

## OperatingRecommendationRepository

Methods:

```text
createRecommendation(data)
createManyRecommendations(recommendations)
findByIdAndWorkspace(recommendation_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(recommendation_id, workspace_id, patch)
markConfirmed(recommendation_id, workspace_id, confirmation_data)
markApplied(recommendation_id, workspace_id, result_data)
markRejected(recommendation_id, workspace_id, rejection_data)
```

---

# 6. Service Context

Every operating map service method must receive:

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
Operating map services must not accept workspace_id from request body when path context already defines it.
```

---

# 7. Generate Operating Map Flow

## Service Method

```text
OperatingMapService.generateMap(context, input)
```

## Input

```text
source_object_type optional
source_object_id optional
generation_mode optional
include_recommendations optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check generate map permission
validate source object if provided
resolve generation context
compute next map version
run map generation strategy
identify operating gaps
optionally create operating recommendations
begin transaction
create operating_map with generated status
create operating_gaps
create operating_recommendations if enabled
record operating_map.generated audit event
emit operating_map.generated runtime event
emit operating_gaps.detected runtime event if gaps created
emit operating_recommendations.created runtime event if recommendations created
commit transaction
return generated map DTO
```

## Generation Strategy

MVP generation may use:

```text
workspace context
onboarding answers later
existing functions
existing responsibilities
existing tasks
existing decisions
manual input
```

AI-assisted generation must preserve:

```text
generated_by_agent_id if applicable
source_object_type/source_object_id
human confirmation before active status
```

---

# 8. Generate Operating Map Validation

Validation rules:

```text
workspace must exist
workspace must be active
actor must have map generation permission
generation_mode must be valid if supplied
source_object_type must be valid if supplied
source_object_id must exist if supplied
source object must belong to same workspace when workspace-scoped
include_recommendations must be boolean if supplied
```

Error mappings:

```text
workspace missing → not_found
workspace archived → workspace_archived
invalid generation_mode → validation_error
invalid source object → invalid_source_object
forbidden actor → forbidden
```

---

# 9. List Operating Maps Flow

## Service Method

```text
OperatingMapService.listMaps(context, filters, pagination)
```

## Flow

```text
validate authenticated actor
check workspace access
validate filters
call OperatingMapRepository.listByWorkspace
return paginated map DTOs
```

Default sort:

```text
created_at:desc
```

---

# 10. Get Operating Map Flow

## Service Method

```text
OperatingMapService.getMap(context, operating_map_id)
```

## Flow

```text
validate authenticated actor
check workspace access
load operating map by id and workspace_id
return map DTO
```

---

# 11. Confirm Operating Map Flow

## Service Method

```text
OperatingMapService.confirmMap(context, operating_map_id, input)
```

## Input

```text
confirmation_note optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check confirm map permission
load operating map by id and workspace_id
validate map status allows confirmation
capture before_state
begin transaction
optionally mark previous active map as superseded later
set map status active
set confirmed_by
set confirmed_at
record operating_map.confirmed audit event
emit operating_map.confirmed runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return confirmed map DTO
```

## Rule

```text
Generated operating maps must not become active without confirmation.
```

---

# 12. Archive Operating Map Flow

## Service Method

```text
OperatingMapService.archiveMap(context, operating_map_id, input)
```

## Input

```text
archive_reason optional
```

## Flow

```text
validate authenticated actor
load workspace
check archive permission
load operating map by id and workspace_id
check map is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record operating_map.archived audit event
emit operating_map.archived runtime event
commit transaction
return archived map DTO
```

---

# 13. Operating Gap Creation During Generation

Operating gaps should be created by `OperatingGapService` or an internal gap detector.

Gap types may include:

```text
missing_function
missing_owner
missing_process
missing_task
unclear_decision
operational_risk
```

Gap creation should preserve:

```text
workspace_id
operating_map_id
function_id optional
gap_type
title
description
severity
status detected
source_object_type
source_object_id
```

Rule:

```text
Detected gaps are reviewable records, not automatically resolved state.
```

---

# 14. List Operating Gaps Flow

## Service Method

```text
OperatingGapService.listGaps(context, filters, pagination)
```

## Flow

```text
validate authenticated actor
check workspace access
validate filters
call OperatingGapRepository.listByWorkspace
return paginated gap DTOs
```

Supported filters:

```text
status
gap_type
severity
operating_map_id
function_id
```

---

# 15. Accept Operating Gap Flow

## Service Method

```text
OperatingGapService.acceptGap(context, operating_gap_id, input)
```

## Input

```text
acceptance_note optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check gap review permission
load gap by id and workspace_id
validate gap is not resolved or archived
capture before_state
begin transaction
set gap status accepted
record operating_gap.accepted audit event
emit operating_gap.accepted runtime event
commit transaction
return accepted gap DTO
```

---

# 16. Resolve Operating Gap Flow

## Service Method

```text
OperatingGapService.resolveGap(context, operating_gap_id, input)
```

## Input

```text
resolved_by_object_type
resolved_by_object_id
resolution_note optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check gap resolution permission
load gap by id and workspace_id
validate gap is not resolved or archived
validate resolved_by_object_type
validate resolved_by_object_id exists
validate resolution object belongs to workspace
validate resolution object is compatible with gap_type
capture before_state
begin transaction
set gap status resolved
set resolved_by_object_type
set resolved_by_object_id
set resolved_at
record operating_gap.resolved audit event
emit operating_gap.resolved runtime event
emit dashboard.refresh_requested runtime event
optionally emit memory.candidate_created runtime event
commit transaction
return resolved gap DTO
```

## Compatibility Examples

```text
missing_owner → responsibility
missing_function → function
missing_process → process
missing_task → task
unclear_decision → decision
operational_risk → task or decision
```

---

# 17. Archive Operating Gap Flow

## Service Method

```text
OperatingGapService.archiveGap(context, operating_gap_id, input)
```

## Flow

```text
validate authenticated actor
load workspace
check archive permission
load gap by id and workspace_id
check gap is not already archived
begin transaction
set status archived
set archived_at
record operating_gap.archived audit event
emit operating_gap.archived runtime event
commit transaction
return archived gap DTO
```

---

# 18. Operating Recommendation Flow

Operating recommendations are P2 / near-MVP.

## Confirm Recommendation

```text
OperatingRecommendationService.confirmRecommendation(context, recommendation_id, input)
```

Flow:

```text
check workspace access
load recommendation
validate recommendation is confirmable
set status confirmed
set confirmed_by
set confirmed_at
record operating_recommendation.confirmed audit event
emit operating_recommendation.confirmed runtime event
```

## Apply Recommendation

```text
OperatingRecommendationService.applyRecommendation(context, recommendation_id, input)
```

Flow:

```text
check apply permission
load recommendation
validate recommendation is confirmed or application-compatible
validate human confirmation or automation authority
call target module service to create/update result object
record result_object_type and result_object_id
set status applied
record operating_recommendation.applied audit event
emit operating_recommendation.applied runtime event
```

## Reject Recommendation

```text
OperatingRecommendationService.rejectRecommendation(context, recommendation_id, input)
```

Flow:

```text
check review permission
load recommendation
validate recommendation is not already applied or rejected
set status rejected
record operating_recommendation.rejected audit event
emit operating_recommendation.rejected runtime event
```

---

# 19. Authorization Rules

Operating map service authorization matrix:

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List maps | workspace owner | active workspace access |
| Generate map | workspace owner | owner/admin/manager |
| Get map | workspace owner | active workspace access |
| Confirm map | workspace owner | owner/admin |
| Archive map | workspace owner | owner/admin |
| List gaps | workspace owner | active workspace access |
| Accept gap | workspace owner | owner/admin/manager |
| Resolve gap | workspace owner | owner/admin/manager |
| Archive gap | workspace owner | owner/admin/manager |
| Confirm recommendation | workspace owner | owner/admin/manager |
| Apply recommendation | workspace owner | owner/admin/manager + authority |
| Reject recommendation | workspace owner | owner/admin/manager |

---

# 20. Audit Events

Operating map services should emit:

```text
operating_map.generated
operating_map.confirmed
operating_map.archived
operating_gap.detected
operating_gap.accepted
operating_gap.resolved
operating_gap.archived
operating_recommendation.created
operating_recommendation.confirmed
operating_recommendation.applied
operating_recommendation.rejected
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
ai_assisted
human_confirmed
correlation_id
```

---

# 21. Runtime Events

Operating map services should emit:

```text
operating_map.generated
operating_map.confirmed
operating_map.archived
operating_gaps.detected
operating_gap.accepted
operating_gap.resolved
operating_gap.archived
operating_recommendation.created
operating_recommendation.confirmed
operating_recommendation.applied
operating_recommendation.rejected
dashboard.refresh_requested
memory.candidate_created optional
```

Runtime events may trigger:

```text
dashboard refresh
memory candidate creation
ownership gap creation later
notification later
agent follow-up later
```

---

# 22. DTOs

Operating Map DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "version": 1,
  "status": "active",
  "title": "Operating Map v1",
  "summary": "Confirmed operating map",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T10:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

Operating Gap DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "operating_map_id": "uuid",
  "gap_type": "missing_owner",
  "title": "Missing owner for finance function",
  "severity": "high",
  "status": "detected",
  "resolved_by_object_type": null,
  "resolved_by_object_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

Operating Recommendation DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "operating_map_id": "uuid",
  "source_gap_id": "uuid",
  "recommendation_type": "assign_owner",
  "title": "Assign owner for finance function",
  "status": "created",
  "result_object_type": null,
  "result_object_id": null,
  "created_at": "2026-07-01T09:00:00Z"
}
```

---

# 23. Error Mapping

Operating map service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
OperatingMapNotFound → not_found
OperatingGapNotFound → not_found
RecommendationNotFound → not_found
AccessDenied → forbidden
InvalidGenerationMode → validation_error
InvalidSourceObject → invalid_source_object
InvalidStatusTransition → invalid_status_transition
InvalidResolutionObject → invalid_object_reference
ResolutionObjectIncompatible → business_rule_violation
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
```

---

# 24. MVP Simplifications

MVP may simplify by:

```text
one generated operating map per workspace
simple generated → active → archived lifecycle
operating gaps without full recommendations
manual or rules-based gap detection before AI expansion
owner-only authorization
simple map versioning
synchronous map generation for small workspaces
```

MVP must preserve:

```text
workspace scope
confirmation before active map
audit events
runtime events
source traceability
gap resolution traceability
no hard-delete of operating history
```

---

# 25. Future Expansion

Future service expansion may add:

```text
operating map versions
map comparison service
map node service
operating health scoring
bulk gap resolution
AI-generated recommendations
collaborative map review
operating map export
map quality scoring
ownership gap synchronization
```

---

# 26. Testing Expectations

Service tests should cover:

```text
generate map creates map and gaps
generate map validates source object workspace
confirm map requires valid status
confirm map records confirmed_by and confirmed_at
archive map preserves history
accept gap rejects resolved gaps
resolve gap validates compatible resolution object
resolve gap emits dashboard refresh event
recommendation apply requires confirmation or authority
all mutations emit audit events
all mutations emit runtime events
workspace archived blocks mutations
```

Repository tests should cover:

```text
list maps by workspace
get map by id and workspace
get next map version
list gaps by workspace and filters
resolve gap by id and workspace
list recommendations by workspace
pagination and sorting behavior
```

---

# 27. Acceptance Criteria

Operating Map Service Design is accepted when:

- OperatingMapService responsibilities are defined;
- OperatingGapService responsibilities are defined;
- OperatingRecommendationService responsibilities are defined;
- repository methods are identified;
- generate, confirm and archive map flows are documented;
- gap accept, resolve and archive flows are documented;
- recommendation confirm, apply and reject flows are documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- DTOs and error mappings are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Function Responsibility Service Design
```

---

# 28. Final Statement

```text
Bizzi Operating Map Service Design defines how backend services generate, review, confirm and improve workspace operating structure through transactional, auditable and AI-safe service behavior.
```

This service layer turns workspace context into governed operating clarity.