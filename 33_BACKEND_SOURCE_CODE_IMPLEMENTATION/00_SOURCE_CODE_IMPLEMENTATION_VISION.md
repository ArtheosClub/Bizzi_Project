# 00_SOURCE_CODE_IMPLEMENTATION_VISION.md

# Bizzi Platform

## Source Code Implementation Vision

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Build Vision  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Execution Reference:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Codebase Build Reference:** 32_BACKEND_CODEBASE_BUILD  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch IV — Source Code Implementation

---

# 1. Purpose

This document opens the `33_BACKEND_SOURCE_CODE_IMPLEMENTATION` layer.

The purpose of this layer is to move from implementation specifications into actual repository source files: backend package configuration, NestJS bootstrap, Prisma schema, shared kernel, modules, tests, Docker support and CI workflow.

Core question:

```text
How do we turn the accepted Bizzi backend specifications into a real, runnable backend codebase in the repository?
```

---

# 2. Layer Thesis

```text
Layer 33 is the materialization layer: every accepted backend specification must now become concrete source code, configuration, tests and runnable infrastructure.
```

This layer is no longer only documentation.

It should produce actual implementation artifacts:

```text
backend/package.json
backend/src/main.ts
backend/src/app.module.ts
backend/prisma/schema.prisma
backend/src/shared/**
backend/src/modules/**
backend/test/**
docker-compose.yml
.github/workflows/backend-ci.yml
```

---

# 3. Source Code Implementation Objectives

The objectives are:

```text
create real backend project scaffold
create executable NestJS application
create Prisma schema and database migrations
implement shared kernel primitives
implement identity/auth foundation
implement workspace module
implement authorization/validation module
implement audit module
implement task and decision modules
implement memory and dashboard modules
implement API bootstrap and health endpoint
implement test suite
implement local Docker workflow
implement GitHub Actions CI
verify MVP vertical slice
```

---

# 4. Implementation Mode

Layer 33 should follow a strict rule:

```text
One implementation step equals one focused commit.
```

Each step should:

```text
create or update concrete source files
preserve architecture from prior layers
avoid scope creep
include or prepare tests
remain runnable or move toward runnable state
```

---

# 5. Canonical Build Sequence

Recommended sequence:

```text
00_SOURCE_CODE_IMPLEMENTATION_VISION.md
01_CREATE_BACKEND_PACKAGE_STRUCTURE.md
02_CREATE_NESTJS_BOOTSTRAP_FILES.md
03_CREATE_PRISMA_SCHEMA_FILE.md
04_CREATE_DOCKER_COMPOSE_LOCAL_DATABASE.md
05_CREATE_SHARED_KERNEL_SOURCE.md
06_CREATE_IDENTITY_AUTH_SOURCE.md
07_CREATE_WORKSPACE_SOURCE.md
08_CREATE_AUTHORIZATION_VALIDATION_SOURCE.md
09_CREATE_AUDIT_SOURCE.md
10_CREATE_TASK_DECISION_SOURCE.md
11_CREATE_MEMORY_DASHBOARD_SOURCE.md
12_CREATE_TEST_SETUP_SOURCE.md
13_CREATE_BACKEND_CI_WORKFLOW.md
14_RUNNABLE_MVP_VERIFICATION.md
15_SOURCE_CODE_IMPLEMENTATION_MILESTONE.md
16_SOURCE_CODE_IMPLEMENTATION_AUDIT.md
```

---

# 6. Source Code Guardrails

Mandatory guardrails:

```text
workspace_id scoping is mandatory
services must not bypass repositories
repositories must not return DTOs
controllers must not contain business logic
mutations requiring evidence must call AuditService
cross-workspace references must be rejected
production secrets must not be committed
tests must use isolated test database
CI must not require production credentials
```

---

# 7. Acceptance Criteria

Layer 33 is accepted when:

- backend source structure exists;
- backend app can start locally;
- Prisma schema exists;
- local PostgreSQL workflow exists;
- shared kernel source exists;
- core modules are implemented at MVP level;
- tests are present for critical paths;
- CI workflow exists;
- MVP vertical slice is documented and verifiable;
- milestone is passed;
- audit is passed.

---

# 8. Final Statement

```text
Layer 33 begins the conversion of Bizzi backend architecture into executable source code.
```

This layer is the transition from canonical specification to real working software.