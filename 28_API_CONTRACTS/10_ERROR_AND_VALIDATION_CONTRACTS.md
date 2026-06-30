# 10_ERROR_AND_VALIDATION_CONTRACTS.md

# Bizzi Platform

## Error and Validation Contracts

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Standard  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**Previous Document:** 09_DASHBOARD_EXPORT_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the canonical error and validation contracts for Bizzi Platform APIs.

It standardizes how API failures, validation issues, authorization problems, state transition errors, workspace scope errors and AI-safety violations are returned to clients.

Core question:

```text
How should Bizzi APIs communicate errors and validation failures consistently, safely and usefully across all resource families?
```

---

# 2. Contract Scope

This document applies to all APIs in `28_API_CONTRACTS`:

```text
Workspace API
Operating Map API
Function Responsibility API
Agent Process Task Decision API
Memory Audit Event API
Integration Security API
Dashboard Export API
Pagination Filtering Sorting contracts
```

It defines:

- common error shape;
- validation error shape;
- error code taxonomy;
- HTTP status mapping;
- field validation rules;
- workspace validation rules;
- authorization validation rules;
- lifecycle transition validation rules;
- AI safety validation rules;
- retry and idempotency error expectations;
- correlation and traceability rules.

---

# 3. Core Error Contract Principles

## 3.1 One Error Shape

All API errors should follow one canonical structure.

Rule:

```text
Clients should not need endpoint-specific parsing for common error classes.
```

## 3.2 Machine-Readable Codes

Every error must include a stable `code`.

Rule:

```text
Do not rely on human-readable messages for program logic.
```

## 3.3 Human-Readable Message

Every error should include a safe human-readable `message`.

Rule:

```text
Messages should be useful but must not leak secrets, private payloads or sensitive implementation details.
```

## 3.4 Correlation Required

Every error should include a `correlation_id` when available.

Rule:

```text
Errors must be traceable through audit, runtime events and backend logs.
```

## 3.5 Validation Details Are Structured

Validation errors should identify fields and issues clearly.

---

# 4. Canonical Error Shape

Recommended error response:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "title",
        "issue": "required",
        "message": "title is required"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

Required fields:

```text
error.code
error.message
error.correlation_id where available
```

Optional fields:

```text
error.details
error.retry_after_seconds
error.documentation_ref
error.source
```

---

# 5. Validation Detail Shape

Validation detail object:

```json
{
  "field": "owner_user_id",
  "issue": "invalid_reference",
  "message": "owner_user_id does not reference a user with workspace access"
}
```

Allowed fields:

```text
field
issue
message
expected
actual
object_type
object_id
```

Example with expected values:

```json
{
  "field": "priority",
  "issue": "invalid_value",
  "expected": ["low", "normal", "high", "urgent"],
  "actual": "critical",
  "message": "priority must be one of the allowed values"
}
```

---

# 6. HTTP Status Mapping

| HTTP Status | Error Code | Meaning |
|---:|---|---|
| 400 | validation_error | Request is syntactically valid but semantically invalid |
| 400 | invalid_request | Malformed or unsupported request |
| 401 | unauthenticated | User is not authenticated |
| 403 | forbidden | User lacks required permission |
| 404 | not_found | Resource does not exist or is not visible to caller |
| 409 | conflict | Request conflicts with current state |
| 409 | invalid_status_transition | Lifecycle transition is not allowed |
| 410 | gone | Resource or file has expired |
| 422 | business_rule_violation | Valid request violates business rule |
| 423 | workspace_archived | Workspace is archived or locked |
| 429 | rate_limited | Too many requests |
| 500 | internal_error | Unexpected server error |
| 503 | service_unavailable | Temporary service outage |

Rule:

```text
The same error code should map to the same HTTP status across APIs unless explicitly justified.
```

---

# 7. Common Error Codes

Canonical API error codes:

```text
unauthenticated
forbidden
not_found
validation_error
invalid_request
conflict
workspace_archived
invalid_status_transition
invalid_object_reference
invalid_source_object
invalid_owner
human_confirmation_required
invalid_agent_authority
invalid_provider
invalid_scope
invalid_policy
invalid_credential_ref
credential_value_not_allowed
integration_revoked
export_not_ready
export_expired
rate_limited
idempotency_conflict
internal_error
service_unavailable
```

---

# 8. Authentication Errors

## unauthenticated

HTTP status:

```text
401
```

Example:

```json
{
  "error": {
    "code": "unauthenticated",
    "message": "Authentication is required.",
    "correlation_id": "uuid"
  }
}
```

Rule:

```text
Do not reveal whether a protected resource exists when the caller is unauthenticated.
```

---

# 9. Authorization Errors

## forbidden

HTTP status:

```text
403
```

Example:

```json
{
  "error": {
    "code": "forbidden",
    "message": "You do not have permission to perform this action.",
    "correlation_id": "uuid"
  }
}
```

Authorization checks may include:

```text
authenticated user
workspace access
workspace role
resource ownership
agent authority scope
integration scope
export permission
auditor permission
```

Rule:

```text
Authorization failures must be auditable when security-sensitive.
```

---

# 10. Not Found Errors

## not_found

HTTP status:

```text
404
```

Example:

```json
{
  "error": {
    "code": "not_found",
    "message": "Resource not found.",
    "correlation_id": "uuid"
  }
}
```

Rule:

```text
For protected resources, not_found may be returned instead of forbidden to avoid information disclosure.
```

---

# 11. Workspace Scope Errors

## workspace_archived

HTTP status:

```text
423
```

Example:

```json
{
  "error": {
    "code": "workspace_archived",
    "message": "Archived workspaces cannot be modified through this endpoint.",
    "correlation_id": "uuid"
  }
}
```

Workspace validation rules:

```text
workspace_id must exist
workspace must be visible to caller
workspace must be active for state-changing operations
resource must belong to workspace
cross-workspace references are not allowed unless explicitly designed
```

---

# 12. Field Validation Errors

Field validation should use:

```text
validation_error
```

Common issues:

```text
required
invalid_value
invalid_format
invalid_reference
invalid_date_range
too_long
too_short
not_allowed
unsupported
```

Example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "due_date",
        "issue": "invalid_format",
        "message": "due_date must use YYYY-MM-DD format"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

---

# 13. Object Reference Validation

## invalid_object_reference

HTTP status:

```text
400
```

Example:

```json
{
  "error": {
    "code": "invalid_object_reference",
    "message": "Referenced object does not belong to this workspace.",
    "details": [
      {
        "field": "function_id",
        "issue": "cross_workspace_reference"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

Validation rules:

```text
referenced object must exist
referenced object must belong to the same workspace when workspace-scoped
referenced object must not be archived unless explicitly allowed
polymorphic object_type must be valid
polymorphic object_id must resolve to expected object type
```

---

# 14. Source Object Validation

## invalid_source_object

HTTP status:

```text
400
```

Source object fields:

```text
source_object_type
source_object_id
result_object_type
result_object_id
resolved_by_object_type
resolved_by_object_id
```

Rules:

```text
source_object_type must be controlled value
source_object_id must exist when required
source object must belong to same workspace when workspace-scoped
result object must be traceable after application
resolution object must be compatible with gap or issue being resolved
```

---

# 15. Lifecycle Transition Errors

## invalid_status_transition

HTTP status:

```text
409
```

Example:

```json
{
  "error": {
    "code": "invalid_status_transition",
    "message": "Archived tasks cannot be completed.",
    "details": [
      {
        "field": "status",
        "issue": "transition_not_allowed",
        "expected": ["open", "in_progress"],
        "actual": "archived"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

Rule:

```text
Lifecycle transitions must be validated by service layer, not only database constraints.
```

---

# 16. Business Rule Errors

## business_rule_violation

HTTP status:

```text
422
```

Examples:

```text
last owner cannot be revoked
confirmed decision cannot be hard deleted
active integration cannot sync without valid credential reference
export scope is not allowed for current user
AI-generated action requires confirmation
```

Example response:

```json
{
  "error": {
    "code": "business_rule_violation",
    "message": "The last workspace owner cannot be revoked without ownership transfer.",
    "correlation_id": "uuid"
  }
}
```

---

# 17. AI Safety Errors

## human_confirmation_required

HTTP status:

```text
422
```

Example:

```json
{
  "error": {
    "code": "human_confirmation_required",
    "message": "This AI-generated action requires human confirmation before application.",
    "correlation_id": "uuid"
  }
}
```

## invalid_agent_authority

HTTP status:

```text
403
```

Example:

```json
{
  "error": {
    "code": "invalid_agent_authority",
    "message": "Agent authority scope does not allow this action.",
    "correlation_id": "uuid"
  }
}
```

AI validation rules:

```text
AI suggestions must not become official state without confirmation or explicit automation authority
agent authority must match action type
AI-generated memory requires review before active context use
AI draft payload must be validated before application
human confirmation must be recorded for sensitive actions
```

---

# 18. Integration and Secret Errors

## credential_value_not_allowed

HTTP status:

```text
400
```

Example:

```json
{
  "error": {
    "code": "credential_value_not_allowed",
    "message": "Raw credential values are not allowed. Use credential_ref instead.",
    "correlation_id": "uuid"
  }
}
```

## invalid_credential_ref

HTTP status:

```text
400
```

Rules:

```text
raw secrets must not be accepted
credential_ref must point to secure secret storage
revoked credentials cannot be used for sync
credential scope must match integration scope
```

---

# 19. Export Errors

## export_not_ready

HTTP status:

```text
409
```

## export_expired

HTTP status:

```text
410
```

Example:

```json
{
  "error": {
    "code": "export_expired",
    "message": "The export file has expired.",
    "correlation_id": "uuid"
  }
}
```

---

# 20. Rate Limit Errors

## rate_limited

HTTP status:

```text
429
```

Example:

```json
{
  "error": {
    "code": "rate_limited",
    "message": "Too many requests. Try again later.",
    "retry_after_seconds": 60,
    "correlation_id": "uuid"
  }
}
```

---

# 21. Idempotency Errors

## idempotency_conflict

HTTP status:

```text
409
```

Example:

```json
{
  "error": {
    "code": "idempotency_conflict",
    "message": "Idempotency key was reused with a different request payload.",
    "correlation_id": "uuid"
  }
}
```

Candidate idempotent operations:

```text
operating map generation
integration sync trigger
export job creation
AI recommendation application
```

---

# 22. Internal Errors

## internal_error

HTTP status:

```text
500
```

Example:

```json
{
  "error": {
    "code": "internal_error",
    "message": "Unexpected server error.",
    "correlation_id": "uuid"
  }
}
```

Rule:

```text
Internal error messages must not expose stack traces, SQL queries, secrets or infrastructure details.
```

---

# 23. Validation Rule Categories

Bizzi APIs should validate:

```text
required fields
field formats
allowed values
status transitions
workspace ownership
foreign key existence
polymorphic references
authorization scope
agent authority
human confirmation
retention and archive restrictions
export format and scope
integration provider configuration
```

---

# 24. Error Audit Expectations

Not every error needs an audit event.

Audit security-sensitive failures:

```text
forbidden
invalid_agent_authority
credential_value_not_allowed
workspace_access change denied
export access denied
runtime_event_restricted
repeated rate limit abuse
```

Usually do not audit:

```text
simple missing required field
simple invalid date format
normal not_found for read operations
```

---

# 25. Client Behavior Guidance

Clients should:

```text
show error.message to users where appropriate
use error.code for program logic
show field validation details near fields
log correlation_id for support
retry only rate_limited and service_unavailable when safe
not retry validation_error without changing request
not retry idempotency_conflict with same incorrect payload
```

---

# 26. Acceptance Criteria

Error and Validation Contracts are accepted when:

- canonical error shape is defined;
- validation detail shape is defined;
- HTTP status mapping is documented;
- common error codes are standardized;
- workspace, object reference and lifecycle errors are covered;
- AI safety errors are defined;
- integration and credential errors are defined;
- export, rate limit and idempotency errors are defined;
- audit expectations for errors are documented;
- client behavior guidance is included.

Status:

```text
Accepted for Pagination Filtering Sorting Contracts
```

---

# 27. Final Statement

```text
Bizzi Error and Validation Contracts define the shared language for API failure, validation, authorization, AI safety and workspace scope enforcement across all API resources.
```

This standard makes Bizzi APIs predictable, debuggable, secure and implementation-ready.