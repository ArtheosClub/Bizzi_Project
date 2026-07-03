# 04_IDENTITY_AUTH_EXECUTION.md

# Bizzi Platform

## Identity Auth Execution

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
**Previous Document:** 03_SHARED_KERNEL_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Identity and Authentication execution plan for Bizzi Platform backend MVP.

It specifies how the backend should implement the first identity layer, development authentication mode, authenticated actor context, `/api/v1/me` endpoint, user repository, request context creation and future provider-neutral authentication boundary.

Core question:

```text
How should Bizzi create a minimal but safe identity and authentication foundation for the MVP workspace execution loop?
```

---

# 2. Identity Auth Thesis

```text
Bizzi MVP should implement a provider-neutral authentication boundary with a development identity mode first, so backend modules can receive stable ActorContext and ServiceContext without hard-coding a future auth provider.
```

This layer proves:

```text
current actor is available
/me route works
User persistence is available
development auth mode is explicit
future JWT/provider auth can replace the stub
workspace ownership can rely on actor_id
services do not read raw request identity directly
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/modules/identity/
├── identity.module.ts
├── controllers/
│   └── identity.controller.ts
├── services/
│   └── identity.service.ts
├── repositories/
│   └── user.repository.ts
├── dto/
│   └── user.response.dto.ts
└── tests/
    ├── identity.service.spec.ts
    └── identity.e2e-spec.ts

backend/src/modules/auth/
├── auth.module.ts
├── guards/
│   └── auth.guard.ts
├── services/
│   ├── auth-context.service.ts
│   └── dev-auth.service.ts
├── decorators/
│   └── current-context.decorator.ts
└── tests/
    ├── auth-context.service.spec.ts
    └── auth.guard.spec.ts
```

---

# 4. Execution Non-Scope

This execution step does not implement:

```text
full registration
password login
OAuth
SAML
multi-factor authentication
refresh tokens
session storage
production identity provider
full RBAC
workspace permissions beyond actor context
```

These are later security and product expansion concerns.

---

# 5. MVP Auth Mode

MVP authentication mode:

```text
DEV_AUTH_MODE=true
```

Development mode behavior:

```text
request receives deterministic development user
user is loaded or created through seed data
actor context is attached to request
/me returns development user
```

Rule:

```text
Development auth must be explicit and must not silently behave as production authentication.
```

---

# 6. Environment Variables

Required variables:

```text
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local optional
DEV_USER_NAME=Bizzi Developer optional
JWT_SECRET=local-dev-only-change-later
```

Future variables:

```text
AUTH_PROVIDER
AUTH_ISSUER_URL
AUTH_AUDIENCE
AUTH_JWKS_URL
SESSION_SECRET
```

Rule:

```text
Production auth must fail closed if no valid provider configuration exists.
```

---

# 7. User Repository

`UserRepository` owns persistence access for users.

Required methods:

```text
findById(id)
findByEmail(email)
create(data)
findOrCreateDevUser(data)
```

Rules:

```text
UserRepository may query users by id or email because users are not workspace-scoped.
Workspace-scoped data must still use workspace_id in feature repositories.
```

---

# 8. User Response DTO

`UserResponseDto` should include:

```text
id
email
name
status
created_at optional
updated_at optional
```

Must not include:

```text
password hashes
provider tokens
session tokens
raw metadata containing secrets
```

MVP note:

```text
The current User model does not store credentials. That is intentional for provider-neutral MVP auth.
```

---

# 9. Auth Context Service

`AuthContextService` creates RequestContext and ServiceContext from the authenticated user.

Responsibilities:

```text
resolve actor
create request_id
create or preserve correlation_id
attach actor context
attach workspace_id later when route requires it
```

Required output:

```text
RequestContext
ServiceContext
```

Rule:

```text
All downstream services should use ServiceContext, not raw authentication payloads.
```

---

# 10. Auth Guard

`AuthGuard` should:

```text
verify request has identity
use DevAuthService when DEV_AUTH_MODE=true
use future provider validator when production auth is configured
attach RequestContext
reject unauthenticated requests
```

MVP behavior:

```text
DEV_AUTH_MODE=true allows development actor.
DEV_AUTH_MODE=false without provider config returns unauthenticated.
```

---

# 11. Current Context Decorator

`current-context.decorator.ts` should expose RequestContext to controllers.

Example usage:

```typescript
@Get('/me')
getMe(@CurrentContext() context: RequestContext): Promise<UserResponseDto> {
  return this.identityService.getMe(toServiceContext(context));
}
```

Rule:

```text
Controllers should not parse actor identity manually.
```

---

# 12. Identity Service

`IdentityService` should expose:

```text
getMe(context: ServiceContext)
```

Behavior:

```text
load user by context.actorId
return UserResponseDto
raise not_found if user does not exist
raise forbidden or unauthenticated if actor context is invalid
```

Rule:

```text
IdentityService returns DTOs, not raw persistence records.
```

---

# 13. Identity Controller

Route:

```text
GET /api/v1/me
```

Controller:

```text
IdentityController.getMe
```

Response:

```json
{
  "id": "uuid",
  "email": "dev@bizzi.local",
  "name": "Bizzi Developer",
  "status": "active"
}
```

Required errors:

```text
unauthenticated
not_found
internal_error
```

---

# 14. Request Context Propagation

Every authenticated request should carry:

```text
request_id
correlation_id
actor_id
actor_type
```

Optional later:

```text
agent_id
roles
workspace_access
```

Rule:

```text
correlation_id must be available before audit and runtime events are implemented.
```

---

# 15. Auth Boundary Design

The authentication boundary must be provider-neutral.

Allowed future providers:

```text
JWT provider
Auth0
Clerk
Supabase Auth
custom session provider
enterprise SSO later
```

Boundary rule:

```text
Feature modules should not know which auth provider produced the actor.
```

---

# 16. Security Rules

MVP security rules:

```text
DEV_AUTH_MODE must be explicit
production mode must fail closed without provider config
no raw tokens in logs
no raw tokens in audit events
no raw tokens in runtime events
no credentials in UserResponseDto
```

Rule:

```text
Development shortcuts must be clearly marked and isolated from production behavior.
```

---

# 17. Tests Required

Required tests:

```text
GET /api/v1/me returns development user when DEV_AUTH_MODE=true
GET /api/v1/me rejects unauthenticated request when auth disabled and no provider configured
IdentityService returns UserResponseDto
IdentityService rejects missing actor
UserRepository finds user by email
AuthContextService creates request_id and correlation_id
AuthContextService preserves incoming correlation_id
UserResponseDto excludes secrets
```

---

# 18. Execution Order

Recommended execution order:

```text
1. Create AuthModule
2. Create IdentityModule
3. Create UserRepository
4. Create DevAuthService
5. Create AuthContextService
6. Create AuthGuard
7. Create CurrentContext decorator
8. Create IdentityService
9. Create IdentityController
10. Add /api/v1/me route
11. Add tests
12. Verify typecheck/test/build
```

---

# 19. Verification Commands

Expected commands:

```bash
cd backend
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
pnpm dev
```

Manual smoke check:

```text
GET http://localhost:3000/api/v1/me
```

Expected dev response:

```json
{
  "id": "<uuid>",
  "email": "dev@bizzi.local",
  "name": "Bizzi Developer",
  "status": "active"
}
```

---

# 20. Risks and Controls

## Risk 1 — Dev Auth Becomes Production Auth

Mitigation:

```text
Production mode must fail closed unless real provider config exists.
```

## Risk 2 — Feature Modules Depend on Auth Provider

Mitigation:

```text
Expose only ActorContext and ServiceContext to feature modules.
```

## Risk 3 — Missing Correlation ID

Mitigation:

```text
AuthContextService creates or preserves correlation_id for every request.
```

## Risk 4 — User DTO Leaks Sensitive Data

Mitigation:

```text
Use explicit UserResponseDto mapping and tests.
```

---

# 21. Acceptance Criteria

Identity Auth Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- MVP auth mode is defined;
- environment variables are defined;
- UserRepository is defined;
- UserResponseDto is defined;
- AuthContextService is defined;
- AuthGuard is defined;
- CurrentContext decorator is defined;
- IdentityService is defined;
- IdentityController and /me route are defined;
- request context propagation rules are defined;
- provider-neutral auth boundary is defined;
- security rules are defined;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Workspace Module Execution
```

---

# 22. Final Statement

```text
Bizzi Identity Auth Execution defines the first backend identity boundary: a provider-neutral actor context, explicit development authentication mode and /me route required for workspace ownership and MVP execution.
```

This prepares Bizzi for workspace creation, authorization and all workspace-scoped service behavior.