# 12_LOCAL_RUNBOOK.md

# Bizzi Platform

## Local Runbook

**Layer:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Component Type:** Execution Runbook  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Previous Document:** 11_CI_WORKFLOW_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the local runbook for Bizzi Platform backend MVP execution.

It gives a practical local workflow for setting up the backend, starting the database, applying migrations, seeding data, running the application, executing tests, checking API routes and troubleshooting common failures.

Core question:

```text
How should a developer or AI-assisted implementation agent run, verify and reset the Bizzi backend MVP locally?
```

---

# 2. Local Runbook Thesis

```text
Local execution must be reproducible, boring and safe. Any developer should be able to clone the repository, install dependencies, start PostgreSQL, apply migrations, run tests and execute the MVP vertical slice without hidden manual state.
```

This runbook protects:

```text
local reproducibility
database safety
migration confidence
test reliability
MVP smoke testing
AI-assisted implementation discipline
troubleshooting speed
```

---

# 3. Required Local Tools

Required tools:

```text
Git
Node.js LTS
pnpm
Docker Desktop or compatible Docker runtime
PostgreSQL client optional
curl or HTTP client
```

Optional tools:

```text
Prisma Studio
VS Code
Postman / Insomnia
GitHub CLI
```

Rule:

```text
Local backend execution should not require production cloud services.
```

---

# 4. Repository Setup

Clone repository:

```bash
git clone https://github.com/ArtheosClub/Bizzi_Project.git
cd Bizzi_Project
```

Install dependencies:

```bash
pnpm install
```

Backend-only fallback:

```bash
cd backend
pnpm install
```

Rule:

```text
Use the lockfile. Do not casually regenerate dependencies during normal setup.
```

---

# 5. Environment Files

Create local backend env file:

```bash
cp backend/.env.example backend/.env.local
```

Expected local values:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
JWT_SECRET=local-dev-only-change-later
```

Test values:

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5433/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

Rules:

```text
never commit .env.local
never use production secrets locally
keep dev and test database URLs separate
```

---

# 6. Start Local Databases

Start Docker services:

```bash
docker compose up -d postgres_dev postgres_test
```

Check status:

```bash
docker compose ps
```

Expected services:

```text
postgres_dev running on 5432
postgres_test running on 5433
```

Rule:

```text
Development and test databases must not share the same port or database name.
```

---

# 7. Prisma Workflow

From backend directory:

```bash
cd backend
pnpm prisma format
pnpm prisma validate
pnpm prisma generate
```

Apply development migration:

```bash
pnpm prisma migrate dev
```

Apply migrations in deploy mode:

```bash
pnpm prisma migrate deploy
```

Open Prisma Studio optional:

```bash
pnpm prisma studio
```

Rule:

```text
Migration commands should run against the intended database only.
```

---

# 8. Seed Local Data

Run seed:

```bash
cd backend
pnpm db:seed
```

Expected seed data:

```text
development user
development workspace optional
default workspace settings optional
sample task optional
sample decision optional
sample memory entry optional
```

Rules:

```text
seed data is local-only
seed data must not contain real secrets
seed should be repeatable or reset-aware
```

---

# 9. Run Backend Locally

Start development server:

```bash
cd backend
pnpm dev
```

Expected default URL:

```text
http://localhost:3000
```

Health check:

```bash
curl http://localhost:3000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 10. Identity Smoke Test

Run:

```bash
curl http://localhost:3000/api/v1/me
```

Expected development response:

```json
{
  "id": "<uuid>",
  "email": "dev@bizzi.local",
  "name": "Bizzi Developer",
  "status": "active"
}
```

Rule:

```text
If DEV_AUTH_MODE=false and no provider is configured, /me should fail closed.
```

---

# 11. MVP Smoke Sequence

Recommended manual flow:

```text
1. GET /api/v1/me
2. POST /api/v1/workspaces
3. GET /api/v1/workspaces
4. POST /api/v1/workspaces/{workspace_id}/tasks
5. POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
6. POST /api/v1/workspaces/{workspace_id}/decisions
7. POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
8. POST /api/v1/workspaces/{workspace_id}/memory-entries
9. POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
10. GET /api/v1/workspaces/{workspace_id}/audit-events
11. GET /api/v1/workspaces/{workspace_id}/dashboard
```

Expected result:

```text
audit events exist for meaningful mutations
dashboard counts reflect task, decision and memory state
```

---

# 12. Run Tests Locally

Run all tests:

```bash
cd backend
pnpm test
```

Run by category:

```bash
pnpm test:unit
pnpm test:integration
pnpm test:e2e
```

Reset test database:

```bash
pnpm db:test:reset
```

Rule:

```text
Integration and e2e tests must use test database, not development database.
```

---

# 13. Quality Checks

Run typecheck:

```bash
cd backend
pnpm typecheck
```

Run lint:

```bash
pnpm lint
```

Run build:

```bash
pnpm build
```

Local acceptance:

```text
install passes
typecheck passes
lint passes
tests pass
build passes
```

---

# 14. Database Reset

Reset development database:

```bash
cd backend
pnpm prisma migrate reset
```

Reset test database:

```bash
pnpm db:test:reset
```

Full Docker reset:

```bash
docker compose down -v
docker compose up -d postgres_dev postgres_test
cd backend
pnpm prisma migrate dev
pnpm db:seed
```

Warning:

```text
Full Docker reset deletes local database volumes.
```

---

# 15. Debugging Checklist

If backend does not start:

```text
check Node version
check pnpm install completed
check backend/.env.local exists
check DATABASE_URL
check PostgreSQL container is running
check Prisma client generated
check port 3000 is free
```

If migrations fail:

```text
check DATABASE_URL points to dev database
check PostgreSQL is healthy
run prisma validate
inspect migration history
reset local dev database if safe
```

If tests fail:

```text
check NODE_ENV=test
check test DATABASE_URL points to test DB
reset test database
ensure migrations are applied
check factory data uniqueness
```

---

# 16. Common Local Commands

```bash
pnpm install
cd backend
pnpm dev
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e
pnpm build
pnpm prisma validate
pnpm prisma generate
pnpm prisma migrate dev
pnpm db:seed
```

Docker:

```bash
docker compose up -d postgres_dev postgres_test
docker compose ps
docker compose logs postgres_dev
docker compose down
```

---

# 17. AI-assisted Local Workflow

AI-assisted implementation should follow:

```text
read relevant execution document
make small scoped change
run typecheck
run targeted tests
run full tests when behavior changes
run build
commit only passing work
```

Rules:

```text
AI-generated code must not skip tests
AI-generated code must not invent fields or routes
AI-generated code must preserve workspace_id scoping
AI-generated code must not commit secrets
```

---

# 18. Local Acceptance Criteria

Local backend is accepted when:

```text
[ ] dependencies install
[ ] Docker databases start
[ ] environment files are configured
[ ] Prisma validates
[ ] migrations apply
[ ] seed runs
[ ] backend starts
[ ] /health works
[ ] /api/v1/me works
[ ] MVP smoke sequence works
[ ] test suite passes
[ ] typecheck passes
[ ] lint passes
[ ] build passes
```

---

# 19. Risks and Controls

## Risk 1 — Hidden Local State

Mitigation:

```text
Use documented reset commands and repeatable seeds.
```

## Risk 2 — Wrong Database Used

Mitigation:

```text
Keep dev and test URLs separate; test setup must fail if not using test environment.
```

## Risk 3 — Local Secrets Committed

Mitigation:

```text
Only commit .env.example; never commit .env.local.
```

## Risk 4 — Manual Smoke Tests Drift

Mitigation:

```text
Keep smoke sequence aligned with MVP vertical slice e2e test.
```

---

# 20. Acceptance Criteria

Local Runbook is accepted when:

- required tools are defined;
- repository setup is documented;
- environment files are defined;
- local database startup is documented;
- Prisma workflow is documented;
- seed workflow is documented;
- backend startup is documented;
- health and identity smoke tests are documented;
- MVP smoke sequence is defined;
- test commands are documented;
- quality checks are documented;
- reset workflow is documented;
- debugging checklist is documented;
- AI-assisted local workflow is documented;
- local acceptance checklist is provided;
- risks and controls are documented.

Status:

```text
Accepted for Backend Execution Milestone
```

---

# 21. Final Statement

```text
Bizzi Local Runbook defines the repeatable developer workflow for running, testing, resetting and verifying the backend MVP locally.
```

This runbook ensures Bizzi backend execution can be reproduced by human developers and AI-assisted implementation agents before CI and milestone acceptance.