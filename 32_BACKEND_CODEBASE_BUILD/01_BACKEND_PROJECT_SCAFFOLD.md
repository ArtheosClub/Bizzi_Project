# 01_BACKEND_PROJECT_SCAFFOLD.md

# Bizzi Platform

## Backend Project Scaffold

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the physical backend project structure that will be created in the repository.

### Target Stack

- NestJS
- TypeScript
- Prisma ORM
- PostgreSQL
- pnpm
- Docker Compose

### Repository Structure

```text
backend/
 ├── src/
 │   ├── app.module.ts
 │   ├── main.ts
 │   ├── shared/
 │   ├── infrastructure/
 │   ├── modules/
 │   │    ├── identity/
 │   │    ├── workspace/
 │   │    ├── task/
 │   │    ├── decision/
 │   │    ├── memory/
 │   │    ├── audit/
 │   │    └── dashboard/
 │   └── common/
 ├── prisma/
 ├── test/
 ├── package.json
 ├── tsconfig.json
 └── nest-cli.json
```

### Initial Deliverables

1. Backend bootstrap.
2. Health endpoint.
3. Configuration module.
4. Logging.
5. Environment loading.
6. Prisma integration.
7. Global validation.
8. Exception filters.
9. Request context.
10. OpenAPI bootstrap.

### Acceptance Criteria

- Project builds.
- `pnpm dev` starts successfully.
- `/health` returns HTTP 200.
- Prisma connects.
- Global validation is enabled.
- OpenAPI endpoint is available.

### Outcome

This scaffold becomes the foundation for all subsequent backend source code implementation.