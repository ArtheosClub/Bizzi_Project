# 04_IDENTITY_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Identity Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the backend Identity module.

### Module Scope

The Identity module provides authenticated user identity, actor context creation and the `/api/v1/me` endpoint.

### Directory Structure

```text
backend/src/modules/identity/
 ├── identity.module.ts
 ├── identity.controller.ts
 ├── identity.service.ts
 ├── identity.repository.ts
 ├── dto/
 │   └── current-user.dto.ts
 └── mappers/
     └── user.mapper.ts
```

### API Routes

```text
GET /api/v1/me
```

### Responsibilities

- Resolve current authenticated user.
- Return safe user profile DTO.
- Provide user lookup by ID and email.
- Support development authentication mode.
- Create ActorContext for downstream services.

### Repository Methods

```text
findById(id)
findByEmail(email)
createUser(data)
ensureDevUser()
```

### Service Methods

```text
getCurrentUser(context)
resolveActorContext(request)
```

### DTO Contract

```text
CurrentUserDto
 ├── id
 ├── email
 ├── name
 ├── status
 └── created_at
```

### Security Rules

- Do not expose password hashes.
- Do not expose provider tokens.
- Do not expose internal metadata.
- Fail closed when authentication context is missing.

### Acceptance Criteria

- `/api/v1/me` returns current user.
- User lookup works by ID.
- Dev user can be created in local mode.
- ActorContext is available to workspace services.
- Identity module has unit and e2e tests.

### Outcome

The Identity module becomes the foundation for ownership, authorization, audit attribution and all workspace-scoped operations.