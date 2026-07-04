# 05_CREATE_IDENTITY_AUTH_SOURCE.md

# Bizzi Platform

## Create Identity Auth Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the source-code implementation task for creating the Identity and Auth modules in the Bizzi backend.

The goal is to move from codebase build specifications into actual backend source files that provide:

```text
development authentication
current actor resolution
request context creation
/api/v1/me endpoint
safe user response DTO
provider-neutral auth boundary
```

---

# 2. Source Files To Create

Identity module files:

```text
backend/src/modules/identity/identity.module.ts
backend/src/modules/identity/identity.controller.ts
backend/src/modules/identity/identity.service.ts
backend/src/modules/identity/repositories/user.repository.ts
backend/src/modules/identity/dto/current-user.response.dto.ts
backend/src/modules/identity/mappers/user.mapper.ts
```

Auth module files:

```text
backend/src/modules/auth/auth.module.ts
backend/src/modules/auth/guards/auth.guard.ts
backend/src/modules/auth/services/dev-auth.service.ts
backend/src/modules/auth/services/auth-context.service.ts
backend/src/modules/auth/decorators/current-context.decorator.ts
```

Shared dependencies:

```text
backend/src/shared/context/actor-context.ts
backend/src/shared/context/request-context.ts
backend/src/shared/context/service-context.ts
backend/src/shared/context/correlation-context.ts
backend/src/shared/errors/service-error.ts
backend/src/shared/errors/error-codes.ts
```

---

# 3. Identity Module Implementation

`identity.module.ts` must register:

```text
IdentityController
IdentityService
UserRepository
```

It should export:

```text
IdentityService
UserRepository
```

Rule:

```text
Identity module owns user lookup and safe user DTO mapping.
```

---

# 4. Auth Module Implementation

`auth.module.ts` must register:

```text
AuthGuard
DevAuthService
AuthContextService
```

It should export:

```text
AuthGuard
AuthContextService
```

Rule:

```text
Auth module owns request authentication and context creation, not business user profile behavior.
```

---

# 5. Development Auth Mode

MVP development mode is controlled by:

```text
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
```

Behavior:

```text
if DEV_AUTH_MODE=true:
  resolve or create deterministic development user
  attach ActorContext to request
  allow /api/v1/me

if DEV_AUTH_MODE=false and no provider is configured:
  fail closed with unauthenticated
```

Security rule:

```text
Development auth must be explicit and must never silently become production auth.
```

---

# 6. User Repository

`UserRepository` must implement:

```text
findById(id: string)
findByEmail(email: string)
create(data)
findOrCreateDevUser(data)
```

Rules:

```text
repositories return persistence records
services map records to DTOs
user lookup is not workspace-scoped
```

---

# 7. Identity Service

`IdentityService` must implement:

```text
getCurrentUser(context: ServiceContext)
```

Behavior:

```text
validate actor context
load user by actor_id
throw unauthenticated if actor is missing
throw not_found if user does not exist
return CurrentUserResponseDto
```

---

# 8. Identity Controller

Route:

```text
GET /api/v1/me
```

Controller method:

```text
getMe(@CurrentContext() context: RequestContext)
```

Response DTO:

```json
{
  "id": "uuid",
  "email": "dev@bizzi.local",
  "name": "Bizzi Developer",
  "status": "active",
  "created_at": "iso-date"
}
```

---

# 9. Auth Guard

`AuthGuard` must:

```text
read request
resolve development user when enabled
create request context
attach context to request
reject missing identity in production mode
```

Canonical failure:

```text
unauthenticated
```

---

# 10. Auth Context Service

`AuthContextService` must create:

```text
ActorContext
RequestContext
ServiceContext
```

It must ensure:

```text
request_id exists
correlation_id exists or is preserved
actor_id exists
actor_type=user for MVP
```

---

# 11. Current Context Decorator

`CurrentContext` decorator must extract the request context attached by `AuthGuard`.

Rule:

```text
Controllers should not manually parse identity from request headers.
```

---

# 12. DTO Mapping

`CurrentUserResponseDto` includes:

```text
id
email
name
status
created_at
```

It must not include:

```text
password_hash
provider_tokens
session_tokens
internal metadata
```

---

# 13. Tests To Create

Unit tests:

```text
identity.service.spec.ts
user.repository.spec.ts
dev-auth.service.spec.ts
auth-context.service.spec.ts
auth.guard.spec.ts
```

E2E tests:

```text
identity.e2e-spec.ts
```

Required assertions:

```text
GET /api/v1/me returns dev user when DEV_AUTH_MODE=true
GET /api/v1/me fails closed when auth disabled and no provider configured
IdentityService returns safe DTO
AuthContextService creates request_id and correlation_id
UserRepository finds or creates dev user
```

---

# 14. Acceptance Criteria

Identity Auth Source implementation is accepted when:

- Identity module files are created;
- Auth module files are created;
- `/api/v1/me` works in development auth mode;
- ActorContext is created;
- RequestContext and ServiceContext are available;
- current user response is safe;
- unauthenticated failures use canonical error format;
- unit and e2e tests are defined and ready to implement.

---

# 15. Final Statement

```text
Identity Auth Source creates the first executable authentication boundary for Bizzi backend source code.
```

This prepares the source implementation for workspace ownership, authorization, audit attribution and all workspace-scoped backend behavior.