# 11_AUTHORIZATION_VALIDATION_SERVICES.md

# Bizzi Platform

## Authorization Validation Services

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 12_RUNTIME_SECURITY.md  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL / 11_ENUMS_AND_STATUSES.md, 12_INDEXING_STRATEGY.md  
**API Contracts Reference:** 28_API_CONTRACTS / 10_ERROR_AND_VALIDATION_CONTRACTS.md, 11_PAGINATION_FILTERING_SORTING.md  
**Previous Document:** 10_DASHBOARD_EXPORT_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for authorization and validation services in Bizzi Platform.

It specifies how backend services should enforce workspace access, role permissions, agent authority, object reference validation, status transition validation, business rule validation and canonical error mapping.

Core question:

```text
How should Bizzi centralize authorization and validation so that every backend operation remains workspace-scoped, safe, consistent and auditable?
```

---

# 2. Service Scope

This design covers:

```text
AuthorizationService
WorkspacePermissionService
RoleResolutionService
AgentAuthorityService
ExportPermissionService
AuditVisibilityService
RuntimeEventVisibilityService
ValidationService
ObjectReferenceValidator
SourceObjectValidator
StatusTransitionValidator
BusinessRuleValidator
InputValidationService
IdempotencyValidationService
```

Primary API references:

```text
28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md
28_API_CONTRACTS/11_PAGINATION_FILTERING_SORTING.md
```

Primary data references:

```text
users
company_workspaces
workspace_access
agents
agent_authority_scopes
security_policies
audit_events
runtime_events
```

---

# 3. Module Ownership

Authorization and validation behavior belongs to:

```text
AuthorizationModule
ValidationModule
SecurityModule
```

Supporting modules:

```text
WorkspaceModule
AgentModule
AuditModule
EventModule
IdempotencyModule
SharedKernelModule
```

Rule:

```text
Feature services own business intent. Authorization and validation services provide reusable enforcement decisions and canonical failure behavior.
```

---

# 4. Design Principles

Authorization and validation services follow:

```text
server-side enforcement
workspace context first
least privilege
deny by default
explicit permissions
canonical error mapping
structured validation details
auditability for sensitive failures
AI governance enforcement
MVP simplicity with enterprise expansion path
```

Rule:

```text
No feature service should rely on frontend checks as the source of truth for permission or business validity.
```

---

# 5. AuthorizationService Responsibilities

AuthorizationService is the central entry point for permission checks.

Responsibilities:

```text
require authenticated actor
require workspace access
require workspace owner
require role permission
require manager permission
require auditor permission
require integration manager permission
require security manager permission
require export permission
require internal service actor for internal-only operations
return structured authorization decisions
raise canonical AuthorizationError when denied
```

Recommended method style:

```text
AuthorizationService.requirePermission(context, permission, resource optional)
AuthorizationService.can(context, permission, resource optional)
```

---

# 6. WorkspacePermissionService Responsibilities

WorkspacePermissionService evaluates workspace access.

Responsibilities:

```text
load workspace by workspace_id
validate workspace visibility
validate active workspace access
validate owner_user_id in MVP
validate workspace_access record in expansion
validate workspace archived behavior
protect cross-workspace access
```

MVP rule:

```text
actor_id must equal company_workspaces.owner_user_id for mutations unless explicitly internal service.
```

Expansion rule:

```text
actor must have active workspace_access with role that grants the requested permission.
```

---

# 7. RoleResolutionService Responsibilities

RoleResolutionService converts workspace access records into effective roles and permissions.

Responsibilities:

```text
resolve actor role in workspace
resolve inherited or derived permissions later
map role to permission set
support owner/admin/manager/member/auditor/export_manager/integration_manager/security_manager
support future custom roles
```

MVP roles:

```text
owner
```

Expansion roles:

```text
owner
admin
manager
member
auditor
integration_manager
security_manager
export_manager
```

Rule:

```text
Role resolution must be deterministic and testable.
```

---

# 8. AgentAuthorityService Responsibilities

AgentAuthorityService validates whether an AI agent may recommend, draft or apply an action.

Responsibilities:

```text
load agent by workspace
load agent authority scopes
validate action_type
validate object_type
validate authority_level
validate security policy restrictions
require human confirmation when required
return authority decision
```

Authority decision fields:

```text
allowed
requires_human_confirmation
reason_code
matched_scope_id optional
policy_id optional
```

Rule:

```text
AI outputs cannot become official state unless AgentAuthorityService and confirmation policy allow it.
```

---

# 9. ExportPermissionService Responsibilities

ExportPermissionService validates export access.

Responsibilities:

```text
validate actor can create export
validate export_scope sections
validate sensitive sections such as audit summary
validate download permission
validate auditor access when export includes audit evidence
```

Rule:

```text
Export authorization must consider not only the export job but also the data included in export_scope.
```

---

# 10. Visibility Services

## AuditVisibilityService

Responsibilities:

```text
validate audit event list access
validate audit event detail access
restrict audit reads to owner/admin/auditor in expansion
optionally audit sensitive reads
```

## RuntimeEventVisibilityService

Responsibilities:

```text
validate runtime event list access
validate runtime event detail access
restrict operational event visibility
hide or redact sensitive payloads
```

Rule:

```text
Audit and runtime visibility may be stricter than ordinary workspace access.
```

---

# 11. ValidationService Responsibilities

ValidationService is the shared entry point for service-level validation.

Responsibilities:

```text
validate workspace active state
validate required business fields not covered by schema
validate object references
validate source object references
validate status transitions
validate business rules
validate pagination and sorting
validate idempotency where applicable
return structured validation details
raise canonical validation errors
```

Rule:

```text
ValidationService complements schema validation and database constraints; it does not replace either.
```

---

# 12. InputValidationService Responsibilities

InputValidationService validates common request input patterns.

Responsibilities:

```text
validate UUID format
validate date format
validate timestamp format
validate enum values
validate non-empty strings
validate page_size range
validate sort syntax
validate filter names
validate include parameters
```

Common errors:

```text
validation_error
invalid_request
```

---

# 13. ObjectReferenceValidator Responsibilities

ObjectReferenceValidator validates direct object references.

Responsibilities:

```text
validate referenced object exists
validate referenced object belongs to workspace
validate referenced object is not archived unless allowed
validate object_type is supported
validate object_id matches object_type
```

Common object types:

```text
workspace
operating_map
operating_gap
function
responsibility
agent
process
task
decision
memory_entry
integration
export_job
```

Rule:

```text
If object_id is supplied for a polymorphic reference, object_type should also be supplied unless endpoint context makes the type unambiguous.
```

---

# 14. SourceObjectValidator Responsibilities

SourceObjectValidator validates traceability fields.

Fields:

```text
source_object_type
source_object_id
result_object_type
result_object_id
resolved_by_object_type
resolved_by_object_id
```

Responsibilities:

```text
validate source object type
validate source object exists
validate source object belongs to workspace when workspace-scoped
validate result object compatibility
validate resolution object compatibility
```

Rule:

```text
Traceability references must not create cross-workspace links unless explicitly designed.
```

---

# 15. StatusTransitionValidator Responsibilities

StatusTransitionValidator enforces lifecycle rules.

Responsibilities:

```text
validate current status
validate requested transition
validate terminal statuses
validate archived state restrictions
validate confirmation requirements
```

Example transitions:

```text
task: open → in_progress → completed
decision: draft → confirmed → archived
memory: candidate → active → archived
operating_map: generated → active → archived
export_job: queued → processing → completed
integration: active → revoked
```

Rule:

```text
Lifecycle transition validation belongs in service/policy layer, not only in database constraints.
```

---

# 16. BusinessRuleValidator Responsibilities

BusinessRuleValidator enforces cross-field and cross-object business rules.

Examples:

```text
last workspace owner cannot be revoked
function hierarchy cannot contain cycles
responsibility owner must exist
ownership gap resolution must match object
export scope must be allowed
raw credentials must be rejected
AI-generated official state requires confirmation
archived memory cannot be activated
revoked integration cannot sync
```

Common errors:

```text
business_rule_violation
conflict
human_confirmation_required
invalid_agent_authority
```

---

# 17. IdempotencyValidationService Responsibilities

IdempotencyValidationService protects retryable mutations.

Responsibilities:

```text
validate idempotency key format
check existing idempotency record
compare request fingerprint
return stored result when same request completed
reject same key with different payload
record operation result reference
```

Candidate operations:

```text
operating map generation
integration sync trigger
export job creation
AI recommendation application
```

Rule:

```text
Idempotency must prevent duplicate business effects without hiding conflicting payloads.
```

---

# 18. Authorization Flow

Canonical authorization flow:

```text
controller builds context
↓
service loads workspace or target resource
↓
AuthorizationService.requireAuthenticated
↓
WorkspacePermissionService.requireWorkspaceAccess
↓
RoleResolutionService resolves effective role
↓
AuthorizationService checks required permission
↓
feature service continues or fails with forbidden
```

Rule:

```text
Authorization must run before mutation and before exposing sensitive resource details.
```

---

# 19. Validation Flow

Canonical validation flow:

```text
API schema validation
↓
service input validation
↓
workspace state validation
↓
object reference validation
↓
status transition validation
↓
business rule validation
↓
transactional mutation
```

Rule:

```text
Validation failures should return structured details that match 28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md.
```

---

# 20. Repository Responsibilities

Authorization and validation services may depend on repositories for read checks.

Required repository access:

```text
WorkspaceRepository
WorkspaceAccessRepository
UserRepository
AgentRepository
AgentAuthorityScopeRepository
SecurityPolicyRepository
FunctionRepository
ProcessRepository
TaskRepository
DecisionRepository
MemoryRepository
IntegrationRepository
ExportJobRepository
```

Rule:

```text
Authorization and validation services should read enough state to decide, but feature services remain responsible for executing the business operation.
```

---

# 21. Error Mapping

Authorization and validation errors map to canonical API errors.

```text
UnauthenticatedActor → unauthenticated
PermissionDenied → forbidden
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
InvalidInput → validation_error
InvalidObjectReference → invalid_object_reference
InvalidSourceObject → invalid_source_object
InvalidStatusTransition → invalid_status_transition
BusinessRuleViolation → business_rule_violation
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
IdempotencyConflict → idempotency_conflict
```

Rule:

```text
Services must raise structured service errors, not raw database, framework or provider errors.
```

---

# 22. Audit Expectations

Authorization and validation failures do not always require audit events.

Audit security-sensitive failures:

```text
forbidden on security policy changes
forbidden on workspace access changes
invalid_agent_authority
credential_value_not_allowed
export access denied
runtime_event_restricted
repeated rate limit or abuse patterns later
```

Usually do not audit:

```text
simple missing required field
invalid date format
normal not_found reads
simple pagination errors
```

Rule:

```text
Security-sensitive denial should be auditable without flooding audit history with ordinary input mistakes.
```

---

# 23. Runtime Events

Authorization and validation services generally do not emit runtime events directly.

Exceptions may include:

```text
security.violation_detected later
agent_authority.denied later
access_review.required later
```

MVP rule:

```text
Feature services emit runtime events after authorized and validated state changes.
```

---

# 24. DTOs and Decision Shapes

Authorization Decision DTO:

```json
{
  "allowed": true,
  "permission": "task.complete",
  "workspace_id": "uuid",
  "actor_id": "uuid",
  "role": "owner",
  "reason_code": null
}
```

Agent Authority Decision DTO:

```json
{
  "allowed": false,
  "action_type": "apply_recommendation",
  "object_type": "task",
  "requires_human_confirmation": true,
  "reason_code": "human_confirmation_required",
  "matched_scope_id": null
}
```

Validation Detail DTO:

```json
{
  "field": "function_id",
  "issue": "invalid_reference",
  "message": "function_id does not belong to this workspace"
}
```

---

# 25. MVP Simplifications

MVP may simplify by:

```text
owner-only authorization
single workspace owner model
simple permission constants
simple enum validation
simple object reference validators
simple status transition maps
basic idempotency only for export and sync operations
no custom roles
no complex policy engine
```

MVP must preserve:

```text
server-side authorization
workspace isolation
workspace archived mutation blocking
structured validation details
AI confirmation enforcement
secret input rejection
canonical error mapping
```

---

# 26. Future Expansion

Future service expansion may add:

```text
custom roles
permission groups
attribute-based access control
policy simulation
access review workflows
resource-level permissions
field-level permissions
rate limit validation
security violation events
admin override workflows
approval policies
organization-level policies
```

---

# 27. Testing Expectations

Authorization service tests should cover:

```text
unauthenticated actor rejected
owner allowed for MVP operations
non-owner denied in MVP
workspace archived blocks mutations
role resolution returns correct permissions
agent authority requires confirmation where configured
audit visibility is stricter than workspace access
export permission validates export_scope
```

Validation service tests should cover:

```text
invalid UUID rejected
invalid enum rejected
cross-workspace object reference rejected
archived object rejected where not allowed
invalid status transition rejected
last owner revocation rejected
raw credential fields rejected
idempotency conflict rejected
structured validation details returned
```

---

# 28. Acceptance Criteria

Authorization Validation Services are accepted when:

- AuthorizationService responsibilities are defined;
- WorkspacePermissionService responsibilities are defined;
- RoleResolutionService responsibilities are defined;
- AgentAuthorityService responsibilities are defined;
- ExportPermissionService responsibilities are defined;
- validation services and validators are defined;
- authorization and validation flows are documented;
- repository dependencies are identified;
- error mapping is defined;
- audit expectations are documented;
- DTOs and decision shapes are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Transaction and Event Emission
```

---

# 29. Final Statement

```text
Bizzi Authorization Validation Services define the shared backend enforcement layer that protects workspace isolation, permission boundaries, object integrity, lifecycle correctness and AI-safe operation.
```

This service layer ensures Bizzi backend behavior is consistently authorized, validated and mapped to canonical API errors before state changes become official.