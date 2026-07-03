# 03_SHARED_KERNEL_EXECUTION.md

# Bizzi Platform

## Shared Kernel Execution

**Layer:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Component Type:** Execution Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Previous Document:** 02_DATABASE_SCHEMA_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the shared kernel execution plan for Bizzi Platform backend MVP.

It specifies the common backend primitives that must be created before feature modules are implemented: request context, service context, actor context, workspace context, canonical errors, response DTOs, pagination, constants, correlation identifiers and shared utility boundaries.

Core question:

```text
Which shared backend primitives must exist so Bizzi modules can implement workspace-scoped, auditable, testable and consistent behavior without duplicating infrastructure logic?
```

---

# 2. Shared Kernel Thesis

```text
Bizzi Shared Kernel must provide only cross-cutting primitives required by all modules. It must not become a dumping ground for feature-specific business logic.
```

The Shared Kernel protects:

```text
context consistency
canonical error handling
response consistency
workspace isolation patterns
correlation_id propagation
pagination standards
audit/runtime naming consistency
AI-safe implementation discipline
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/shared/
├── shared.module.ts
├── context/
│   ├── actor-context.ts
│   ├── request-context.ts
│   ├── service-context.ts
│   ├── workspace-context.ts
│   └── correlation-context.ts
├── errors/
│   ├── error-codes.ts
│   ├── service-error.ts
│   ├── error-details.ts
│   └── error-mapper.ts
├── dto/
│   ├── base-response.dto.ts
│   ├── error-response.dto.ts
│   ├── paginated-response.dto.ts
│   └── pagination-query.dto.ts
├── pagination/
│   ├── pagination.types.ts
│   ├── pagination.constants.ts
│   └── pagination.utils.ts
├── constants/
│   ├── object-types.ts
│   ├── actor-types.ts
│   ├── audit-actions.ts
│   ├── runtime-events.ts
│   └── http.constants.ts
└── utils/
    ├── assert-never.ts
    ├── sanitize-payload.ts
    └── date.util.ts
```

---

# 4. Shared Kernel Non-Scope

The Shared Kernel must not contain:

```text
workspace business logic
task lifecycle logic
decision confirmation logic
memory activation logic
repository queries
Prisma model-specific behavior
agent decision logic
integration provider logic
```

Rule:

```text
If a function knows a specific feature's business rule, it belongs in that feature module, not in Shared Kernel.
```

---

# 5. SharedModule

`shared.module.ts` should expose shared providers only if NestJS injection is required.

Initial role:

```text
provide shared utilities and constants
export common context/error helpers when necessary
```

MVP rule:

```text
Most shared files can be plain TypeScript exports. Do not overuse injectable providers for simple constants and types.
```

---

# 6. Actor Context

`actor-context.ts` defines the authenticated actor.

Recommended shape:

```typescript
export type ActorType = 'user' | 'agent' | 'system';

export interface ActorContext {
  actorId: string;
  actorType: ActorType;
  agentId?: string;
  email?: string;
  roles?: string[];
}
```

Rules:

```text
actorId is required for user-facing operations
actorType must be explicit
agentId is optional for AI-assisted operations
services must not reconstruct actor identity from raw request objects
```

---

# 7. Request Context

`request-context.ts` represents request-level metadata.

Recommended shape:

```typescript
export interface RequestContext {
  requestId: string;
  correlationId: string;
  actor: ActorContext;
  workspaceId?: string;
}
```

Rules:

```text
request_id identifies the HTTP request
correlation_id groups related operations/events
workspace_id may be attached from route path
```

---

# 8. Service Context

`service-context.ts` converts request context into service-safe context.

Recommended shape:

```typescript
export interface ServiceContext {
  requestId: string;
  correlationId: string;
  actorId: string;
  actorType: ActorType;
  agentId?: string;
  workspaceId?: string;
  aiAssisted?: boolean;
  humanConfirmed?: boolean;
}
```

Required helper:

```typescript
export function withWorkspace(
  context: ServiceContext,
  workspaceId: string,
): ServiceContext {
  return { ...context, workspaceId };
}
```

Rule:

```text
Feature services should accept ServiceContext, not raw HTTP request objects.
```

---

# 9. Workspace Context

`workspace-context.ts` defines workspace-safe helpers.

Recommended content:

```typescript
export interface WorkspaceContext {
  workspaceId: string;
  status?: 'active' | 'archived';
  ownerUserId?: string;
}

export function requireWorkspaceId(context: ServiceContext): string;
```

Rule:

```text
Workspace-scoped service methods must fail early if workspaceId is missing.
```

---

# 10. Correlation Context

`correlation-context.ts` standardizes correlation values.

Required behavior:

```text
generate correlation_id if absent
preserve incoming correlation_id if valid
attach correlation_id to service context
audit events and runtime events must reuse it
```

Recommended helper names:

```text
createCorrelationId
normalizeCorrelationId
```

---

# 11. Error Codes

`error-codes.ts` defines canonical API/service error codes.

Required codes:

```text
unauthenticated
forbidden
not_found
workspace_archived
validation_error
invalid_object_reference
invalid_status_transition
business_rule_violation
conflict
internal_error
```

Rule:

```text
Error code strings must align with 28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md.
```

---

# 12. Service Error Base Class

`service-error.ts` defines structured application errors.

Recommended shape:

```typescript
export class ServiceError extends Error {
  constructor(
    public readonly code: ErrorCode,
    message: string,
    public readonly statusCode: number,
    public readonly details?: unknown,
  ) {
    super(message);
  }
}
```

Specialized errors:

```text
UnauthenticatedError
ForbiddenError
NotFoundError
WorkspaceArchivedError
ValidationServiceError
InvalidObjectReferenceError
InvalidStatusTransitionError
BusinessRuleViolationError
ConflictServiceError
InternalServiceError
```

---

# 13. Error Mapper

`error-mapper.ts` converts ServiceError to API response shape.

Required output:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request",
    "details": []
  },
  "request_id": "req_...",
  "correlation_id": "corr_..."
}
```

Rules:

```text
raw Prisma errors must not leak
provider stack traces must not leak
unknown errors map to internal_error
```

---

# 14. Base Response DTO

`base-response.dto.ts` standardizes metadata where useful.

Recommended fields:

```text
request_id
correlation_id
```

MVP rule:

```text
Resource DTOs do not need to inherit from a heavy base class; response wrappers can be introduced where API contracts require them.
```

---

# 15. Error Response DTO

`error-response.dto.ts` should reflect canonical error contracts.

Required fields:

```text
error.code
error.message
error.details optional
request_id
correlation_id
```

Rule:

```text
Every API error path should use this response shape.
```

---

# 16. Pagination DTOs

`pagination-query.dto.ts` should support MVP list routes.

Required query fields:

```text
page
page_size
sort
```

Recommended defaults:

```text
page = 1
page_size = 25
max_page_size = 100
```

`paginated-response.dto.ts` should include:

```text
items
total
page
page_size
has_next
```

---

# 17. Pagination Utilities

`pagination.utils.ts` should provide:

```text
normalizePagination
calculateOffset
validatePageSize
buildPaginatedResponse
```

Rules:

```text
list endpoints must not return unbounded collections
unknown sort fields must not flow directly into repositories
```

---

# 18. Object Type Constants

`object-types.ts` defines canonical object names for audit/runtime events.

Required MVP values:

```text
user
workspace
workspace_settings
task
decision
memory_entry
audit_event
runtime_event
dashboard
```

Rule:

```text
Audit and runtime events should use constants instead of hardcoded object type strings in feature services.
```

---

# 19. Actor Type Constants

`actor-types.ts` defines:

```text
user
agent
system
```

Rule:

```text
Actor type values must align with database enum ActorType.
```

---

# 20. Audit Action Constants

`audit-actions.ts` defines MVP audit actions:

```text
workspace.created
workspace.updated
workspace_settings.updated
task.created
task.updated
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
```

Rule:

```text
Audit actions are business evidence identifiers and should remain stable.
```

---

# 21. Runtime Event Constants

`runtime-events.ts` defines MVP runtime events:

```text
workspace.created
task.created
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
dashboard.refresh_requested
```

Rule:

```text
Runtime event names coordinate internal behavior; do not use them as a replacement for audit action names.
```

---

# 22. Payload Sanitizer

`sanitize-payload.ts` removes unsafe fields before logging, audit or runtime event storage.

Default forbidden field names:

```text
password
token
access_token
refresh_token
api_key
secret
private_key
credential
signed_url
```

Rule:

```text
Sanitization is a safety net, not permission to pass raw secrets through services.
```

---

# 23. Date Utility

`date.util.ts` may provide:

```text
nowUtc
isValidDateRange
normalizeDateInput
```

MVP rule:

```text
Keep date utilities minimal until domain logic requires more.
```

---

# 24. Shared Kernel Testing

Required tests:

```text
ServiceError maps to canonical error response
unknown error maps to internal_error
pagination applies default page_size
pagination enforces max page_size
requireWorkspaceId fails when workspaceId is missing
sanitizePayload removes forbidden secret fields
correlation_id is preserved or generated
```

Test file examples:

```text
backend/src/shared/errors/error-mapper.spec.ts
backend/src/shared/pagination/pagination.utils.spec.ts
backend/src/shared/context/workspace-context.spec.ts
backend/src/shared/utils/sanitize-payload.spec.ts
```

---

# 25. Execution Order

Recommended implementation order:

```text
1. shared.module.ts
2. context types and helpers
3. error codes and ServiceError
4. specialized service errors
5. error mapper
6. DTOs
7. pagination constants and utilities
8. object/actor/audit/runtime constants
9. sanitize payload utility
10. tests
```

---

# 26. Verification Commands

Expected commands:

```bash
cd backend
pnpm typecheck
pnpm test
pnpm build
```

Expected result:

```text
shared kernel compiles
shared kernel tests pass
no feature module dependency introduced into shared kernel
```

---

# 27. Risks and Controls

## Risk 1 — Shared Kernel Becomes Dumping Ground

Mitigation:

```text
Allow only cross-cutting primitives; feature-specific logic belongs in modules.
```

## Risk 2 — Error Contract Drift

Mitigation:

```text
Align error codes and response shape with API contracts.
```

## Risk 3 — Correlation IDs Not Propagated

Mitigation:

```text
Require correlation_id in RequestContext and ServiceContext from the start.
```

## Risk 4 — Unsafe Payloads Stored

Mitigation:

```text
Introduce sanitizePayload before audit/runtime event implementation.
```

---

# 28. Acceptance Criteria

Shared Kernel Execution is accepted when:

- target directory structure is defined;
- non-scope is documented;
- context primitives are defined;
- canonical error codes and service errors are defined;
- error mapper is defined;
- response DTOs are defined;
- pagination DTOs and utilities are defined;
- object, actor, audit and runtime constants are defined;
- payload sanitizer is defined;
- shared kernel tests are specified;
- execution order is documented;
- verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Identity Auth Execution
```

---

# 29. Final Statement

```text
Bizzi Shared Kernel Execution defines the common backend primitives required before feature modules can safely implement business behavior.
```

This kernel prepares the backend for identity, workspace, authorization, validation, audit, runtime events and MVP module implementation without duplicating foundational logic.