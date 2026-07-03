# 01_BACKEND_SCAFFOLD_EXECUTION.md

# Bizzi Platform

## Backend Scaffold Execution

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
**Previous Document:** 00_EXECUTION_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the backend scaffold execution plan for Bizzi Platform.

It specifies the first concrete backend assets to create in the repository so the project can move from implementation planning into a runnable TypeScript/NestJS backend foundation.

Core question:

```text
What exact backend scaffold must exist before Bizzi can implement database schema, shared kernel, modules, tests and CI?
```

---

# 2. Scaffold Thesis

```text
Bizzi backend scaffold must be small, clean and architecture-aligned: enough to start, build, typecheck and host future modules, but not overloaded with business behavior before database and shared kernel execution are ready.
```

The scaffold proves:

```text
backend directory exists
TypeScript project exists
NestJS application can boot
configuration pattern exists
database module placeholder exists
shared module placeholder exists
testing foundation exists
scripts are defined
local environment contract exists
```

---

# 3. Target Directory Structure

The initial scaffold should create:

```text
backend/
├── README.md
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── nest-cli.json
├── jest.config.ts
├── .env.example
├── prisma/
│   └── schema.prisma
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── config/
│   │   ├── config.module.ts
│   │   ├── configuration.ts
│   │   └── env.schema.ts
│   ├── database/
│   │   ├── database.module.ts
│   │   ├── prisma.service.ts
│   │   └── transaction.manager.ts
│   ├── shared/
│   │   ├── shared.module.ts
│   │   ├── context/
│   │   ├── errors/
│   │   ├── dto/
│   │   └── constants/
│   └── modules/
│       └── health/
│           ├── health.module.ts
│           ├── health.controller.ts
│           └── health.service.ts
└── test/
    └── app.e2e-spec.ts
```

Repository root should also include or prepare:

```text
docker-compose.yml
.env.example
```

---

# 4. Scaffold Non-Scope

The scaffold should not yet implement:

```text
full Prisma data model
real database migrations
workspace business logic
task business logic
decision business logic
audit event persistence
runtime event persistence
full authentication provider
CI workflow
production deployment
```

These are handled in later execution documents.

---

# 5. Package Configuration

`backend/package.json` should define scripts:

```text
start
dev
build
lint
typecheck
test
test:unit
test:e2e
prisma:generate
db:migrate
db:reset
db:seed
```

Recommended runtime dependencies:

```text
@nestjs/common
@nestjs/core
@nestjs/platform-express
@nestjs/config
reflect-metadata
rxjs
@prisma/client
zod optional
```

Recommended development dependencies:

```text
typescript
ts-node
@nestjs/cli
@nestjs/testing
jest
ts-jest
supertest
eslint
prettier
prisma
```

Rule:

```text
The scaffold must support install, typecheck, test and build before feature modules are added.
```

---

# 6. TypeScript Configuration

TypeScript config should support:

```text
strict mode
source maps
module resolution
decorators
emit decorator metadata
incremental builds optional
```

Required principles:

```text
no implicit any
strict null checks preferred
consistent path aliases optional but not required for first scaffold
```

MVP rule:

```text
Avoid complex path aliasing until repository structure stabilizes.
```

---

# 7. NestJS Application Entry

`src/main.ts` should:

```text
create Nest application
load AppModule
apply global validation pipe later
listen on configured port
log startup message
```

MVP placeholder behavior:

```text
Application boots and exposes health route.
```

Rule:

```text
main.ts should remain thin and not contain business logic.
```

---

# 8. AppModule

`src/app.module.ts` should import initial infrastructure modules:

```text
ConfigModule
DatabaseModule
SharedModule
HealthModule
```

Future imports:

```text
IdentityModule
WorkspaceModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
TaskModule
DecisionModule
MemoryModule
DashboardModule
```

Rule:

```text
AppModule composes modules; it does not own business behavior.
```

---

# 9. Config Scaffold

Config scaffold should provide:

```text
validated environment variables
typed configuration access
clear .env.example
startup failure on missing required configuration
```

Initial variables:

```text
NODE_ENV
PORT
DATABASE_URL
DEV_AUTH_MODE
JWT_SECRET
```

Rule:

```text
Configuration validation must be introduced before database and auth execution depend on runtime variables.
```

---

# 10. Database Scaffold

Database scaffold should include placeholders for:

```text
PrismaService
DatabaseModule
TransactionManager
```

Initial behavior:

```text
PrismaService can be injected
TransactionManager interface exists
real schema and migrations are added in 02_DATABASE_SCHEMA_EXECUTION.md
```

Rule:

```text
Feature services must use TransactionManager once mutations are introduced.
```

---

# 11. Shared Kernel Scaffold

Shared scaffold should prepare folders for:

```text
context
errors
dto
constants
pagination
utils
```

Initial minimal files:

```text
shared.module.ts
errors/service-error.ts
errors/error-codes.ts
dto/error-response.dto.ts
context/request-context.ts
context/service-context.ts
```

Rule:

```text
Shared kernel may contain cross-cutting primitives only, not feature-specific business logic.
```

---

# 12. Health Module

A minimal HealthModule should provide:

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

Future readiness endpoint:

```text
GET /ready
```

Rule:

```text
Health route proves application boot only; database readiness is added after schema execution.
```

---

# 13. Environment Files

`backend/.env.example` should include safe placeholder values only:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
JWT_SECRET=local-dev-only-change-later
```

Rules:

```text
no real secrets
no production credentials
.env.local ignored by git
configuration must fail safely when required values are absent
```

---

# 14. Docker Compose Placeholder

Root `docker-compose.yml` should prepare local services:

```text
postgres_dev
postgres_test
```

Deferred services:

```text
redis
minio
mailpit
```

Rule:

```text
Development and test databases must remain separate.
```

---

# 15. Test Scaffold

Initial tests should prove:

```text
application module compiles
GET /health returns ok
configuration loads in test mode
```

Test structure:

```text
backend/test/app.e2e-spec.ts
backend/src/modules/health/health.service.spec.ts optional
```

Rule:

```text
Even scaffold should have at least one test that proves the backend can boot.
```

---

# 16. README Scaffold

`backend/README.md` should document:

```text
install command
local environment setup
start command
test command
build command
migration command placeholder
```

MVP note:

```text
README should clearly say this is the backend scaffold and not yet the full MVP implementation.
```

---

# 17. Execution Order

Recommended scaffold execution order:

```text
1. Create backend directory
2. Add package.json
3. Add TypeScript and Nest config
4. Add src/main.ts and app.module.ts
5. Add ConfigModule scaffold
6. Add DatabaseModule scaffold
7. Add SharedModule scaffold
8. Add HealthModule
9. Add .env.example
10. Add initial tests
11. Add README
12. Verify install/typecheck/build/test
```

---

# 18. Verification Commands

Expected commands after scaffold exists:

```bash
cd backend
pnpm install
pnpm typecheck
pnpm test
pnpm build
pnpm dev
```

Expected smoke check:

```text
GET http://localhost:3000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 19. Risks and Controls

## Risk 1 — Scaffold Becomes Feature Implementation

Mitigation:

```text
Keep scaffold limited to boot, config, placeholders and health.
```

## Risk 2 — Configuration Is Added Too Late

Mitigation:

```text
Add ConfigModule and .env.example in scaffold stage.
```

## Risk 3 — Feature Code Bypasses Future Architecture

Mitigation:

```text
Create database/shared/module folders before features so code has a correct place to live.
```

## Risk 4 — No Test Proof of Boot

Mitigation:

```text
Add initial health e2e test.
```

---

# 20. Acceptance Criteria

Backend Scaffold Execution is accepted when:

- backend directory structure is defined;
- package scripts are defined;
- TypeScript configuration is defined;
- NestJS entry and AppModule expectations are defined;
- config scaffold is defined;
- database scaffold is defined;
- shared kernel scaffold is defined;
- health module is defined;
- environment files are defined;
- Docker Compose placeholder is defined;
- test scaffold is defined;
- README scaffold is defined;
- execution order is documented;
- verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Database Schema Execution
```

---

# 21. Final Statement

```text
Bizzi Backend Scaffold Execution defines the first real implementation step: creating a clean, runnable and architecture-aligned NestJS backend foundation.
```

This scaffold prepares the repository for database schema execution, shared kernel implementation and MVP module construction.