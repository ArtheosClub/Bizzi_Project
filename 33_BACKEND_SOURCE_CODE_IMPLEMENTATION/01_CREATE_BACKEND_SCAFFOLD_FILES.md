# 01_CREATE_BACKEND_SCAFFOLD_FILES.md

# Bizzi Platform

## Create Backend Scaffold Files

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Step  
**Foundation:** Art of Business Canonical Release v1.0  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

# 1. Purpose

This document defines the first source-code implementation step for the Bizzi backend.

It describes the actual backend scaffold files that must be created in the repository before Prisma schema, shared kernel and feature modules are implemented.

---

# 2. Implementation Goal

Create a runnable NestJS backend scaffold with TypeScript, package configuration, application bootstrap, health endpoint, environment loading and initial project structure.

Target result:

```text
backend can install, start, typecheck and expose /health
```

---

# 3. Files To Create

Initial backend files:

```text
backend/package.json
backend/tsconfig.json
backend/tsconfig.build.json
backend/nest-cli.json
backend/.env.example
backend/src/main.ts
backend/src/app.module.ts
backend/src/health/health.module.ts
backend/src/health/health.controller.ts
backend/src/health/health.service.ts
backend/src/shared/README.md
backend/src/modules/README.md
backend/prisma/README.md
backend/test/README.md
```

---

# 4. Backend Directory Structure

Target scaffold:

```text
backend/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── health/
│   │   ├── health.module.ts
│   │   ├── health.controller.ts
│   │   └── health.service.ts
│   ├── shared/
│   └── modules/
├── prisma/
├── test/
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── nest-cli.json
└── .env.example
```

---

# 5. Package Scripts

Required scripts:

```json
{
  "dev": "nest start --watch",
  "build": "nest build",
  "start": "node dist/main.js",
  "typecheck": "tsc --noEmit",
  "lint": "eslint \"src/**/*.ts\" \"test/**/*.ts\"",
  "test": "jest",
  "test:e2e": "jest --config ./test/jest-e2e.json"
}
```

---

# 6. Required Dependencies

Runtime dependencies:

```text
@nestjs/common
@nestjs/core
@nestjs/platform-express
@nestjs/config
reflect-metadata
rxjs
```

Development dependencies:

```text
@nestjs/cli
@nestjs/testing
@types/jest
@types/node
jest
ts-jest
typescript
eslint
prettier
supertest
```

---

# 7. Health Endpoint

Route:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

Purpose:

```text
prove backend process is running and route wiring works
```

---

# 8. Bootstrap Requirements

`main.ts` must:

```text
create Nest application
load configuration
set global API prefix /api/v1 later where appropriate
start server on configured PORT
log startup message
```

MVP port:

```text
PORT=3000
```

---

# 9. AppModule Requirements

`AppModule` must import:

```text
ConfigModule
HealthModule
```

Future modules:

```text
IdentityModule
WorkspaceModule
AuthorizationModule
TaskModule
DecisionModule
MemoryModule
AuditModule
DashboardModule
```

---

# 10. Environment Example

`.env.example` should include:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
JWT_SECRET=local-dev-only-change-later
```

---

# 11. Verification Commands

Expected commands:

```bash
cd backend
pnpm install
pnpm typecheck
pnpm build
pnpm dev
```

Smoke check:

```bash
curl http://localhost:3000/health
```

Expected:

```text
HTTP 200 with { "status": "ok" }
```

---

# 12. Acceptance Criteria

This step is accepted when:

- backend directory exists;
- package configuration exists;
- TypeScript configuration exists;
- NestJS bootstrap exists;
- AppModule exists;
- HealthModule exists;
- `/health` endpoint is defined;
- environment example exists;
- project can typecheck;
- project can build;
- project can start locally.

---

# 13. Final Statement

```text
The backend scaffold files create the first runnable source-code foundation for Bizzi Platform.
```

This step prepares the repository for Prisma schema implementation, shared kernel implementation and feature module source-code creation.
