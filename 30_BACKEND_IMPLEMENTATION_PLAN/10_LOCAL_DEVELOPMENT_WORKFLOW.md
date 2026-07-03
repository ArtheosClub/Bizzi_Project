# 10_LOCAL_DEVELOPMENT_WORKFLOW.md

# Bizzi Platform

## Local Development Workflow

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 09_TESTING_STRATEGY.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the local development workflow for Bizzi Platform backend implementation.

It describes how a developer or AI-assisted engineering agent should set up, run, test, reset, debug and validate the Bizzi backend locally using the selected stack: TypeScript, NestJS, PostgreSQL, Prisma and Docker Compose.

Core question:

```text
How should Bizzi be run locally so that development is repeatable, safe, fast and aligned with backend architecture guarantees?
```

---

# 2. Local Development Thesis

```text
Bizzi local development should be reproducible with a small set of commands: install, configure, start database, run migrations, seed data, start backend, run tests and reset state when needed.
```

The workflow must support:

```text
fast onboarding
repeatable database setup
safe environment configuration
local test execution
migration validation
audit/runtime event visibility
debug-friendly backend startup
```

---

# 3. Required Local Tools

Required tools:

```text
Node.js LTS
pnpm
Docker Desktop or compatible Docker runtime
Git
PostgreSQL client optional
```

Recommended tools:

```text
VS Code or WebStorm
Prisma extension
REST client / HTTP client
GitHub CLI optional
```

Rule:

```text
Local workflow should not require production cloud credentials for MVP development.
```

---

# 4. Repository Setup

Initial setup:

```bash
git clone https://github.com/ArtheosClub/Bizzi_Project.git
cd Bizzi_Project
pnpm install
```

If backend is implemented as package-local project:

```bash
cd backend
pnpm install
```

Rule:

```text
The repository README should eventually expose the canonical setup command sequence.
```

---

# 5. Environment Files

Required files:

```text
.env.example
backend/.env.example
backend/.env.local
```

Rules:

```text
.env.local must not be committed
.env.example must not contain real secrets
all required environment variables must be documented
application startup should validate required config
```

MVP variables:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
JWT_SECRET=local-dev-only-change-later
```

Test variables:

```text
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5433/bizzi_test
NODE_ENV=test
```

---

# 6. Docker Compose Services

MVP Docker Compose should include:

```text
postgres_dev
postgres_test
```

Optional later:

```text
redis
minio
mailpit
```

Recommended local ports:

```text
PostgreSQL dev: 5432
PostgreSQL test: 5433
Redis later: 6379
MinIO later: 9000 / 9001
```

Rule:

```text
Development and test databases should be separate.
```

---

# 7. Start Local Infrastructure

Command:

```bash
docker compose up -d postgres_dev postgres_test
```

Check running containers:

```bash
docker compose ps
```

Stop infrastructure:

```bash
docker compose down
```

Full reset including volumes:

```bash
docker compose down -v
```

Rule:

```text
Use volume reset only when local data loss is acceptable.
```

---

# 8. Database Migration Workflow

Run migrations:

```bash
cd backend
pnpm prisma migrate dev
```

Generate Prisma client:

```bash
pnpm prisma generate
```

Reset local development database:

```bash
pnpm prisma migrate reset
```

Rules:

```text
migration files must be committed
applied migrations should not be edited casually
schema changes should be verified with migrate reset before sharing
```

---

# 9. Seed Workflow

Run seed:

```bash
cd backend
pnpm db:seed
```

Seed should create:

```text
development user
development workspace
default workspace settings
sample task
sample decision optional
sample memory entry optional
```

Rules:

```text
seed data must be deterministic or reset-aware
seed data must not include real secrets
seed data must be safe to run locally multiple times where possible
```

---

# 10. Start Backend Locally

Development command:

```bash
cd backend
pnpm dev
```

Expected local URL:

```text
http://localhost:3000
```

Health check later:

```text
GET http://localhost:3000/health
```

Identity check:

```text
GET http://localhost:3000/api/v1/me
```

---

# 11. Local Developer Commands

Recommended root commands:

```text
pnpm install
pnpm dev
pnpm test
pnpm lint
pnpm typecheck
pnpm build
```

Recommended backend commands:

```text
pnpm dev
pnpm build
pnpm test
pnpm test:unit
pnpm test:integration
pnpm test:e2e
pnpm lint
pnpm typecheck
pnpm db:migrate
pnpm db:reset
pnpm db:seed
pnpm prisma:generate
```

Rule:

```text
Commands should be documented and stable before MVP implementation begins.
```

---

# 12. API Smoke Test Workflow

Manual smoke test sequence:

```text
GET /api/v1/me
POST /api/v1/workspaces
GET /api/v1/workspaces
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/runtime-events
GET /api/v1/workspaces/{workspace_id}/dashboard
```

Rule:

```text
The smoke flow should match 02_MVP_VERTICAL_SLICE.md and 05_API_ROUTE_IMPLEMENTATION_PLAN.md.
```

---

# 13. Test Workflow

Run all tests:

```bash
cd backend
pnpm test
```

Run unit tests:

```bash
pnpm test:unit
```

Run integration tests:

```bash
pnpm test:integration
```

Run e2e tests:

```bash
pnpm test:e2e
```

Rules:

```text
tests must use test database
tests must not use development database
tests must not require real external services
```

---

# 14. Debug Workflow

Debugging should support:

```text
NestJS watch mode
source maps
structured logs
correlation_id in logs
request_id in logs
workspace_id when available
actor_id when available
```

Recommended debug flow:

```text
start backend in watch mode
send HTTP request
copy correlation_id from response/log
trace service, repository, audit and runtime event records
```

Rule:

```text
Every meaningful operation should be traceable by correlation_id.
```

---

# 15. Local Data Inspection

Options:

```text
Prisma Studio
psql
TablePlus / DBeaver / DataGrip
```

Prisma Studio:

```bash
cd backend
pnpm prisma studio
```

Inspection targets:

```text
company_workspaces
workspace_settings
tasks
decisions
memory_entries
audit_events
runtime_events
```

---

# 16. Reset Workflow

Common reset sequence:

```bash
docker compose down -v
docker compose up -d postgres_dev postgres_test
cd backend
pnpm prisma migrate dev
pnpm db:seed
pnpm dev
```

Test reset sequence:

```bash
cd backend
pnpm db:test:reset
pnpm test
```

Rule:

```text
Reset workflows should be safe for local development only and clearly documented.
```

---

# 17. Branch Workflow

Recommended branch naming:

```text
feature/backend-scaffold
feature/workspace-module
feature/task-module
feature/decision-module
fix/workspace-isolation
chore/migrations
```

Commit style:

```text
Add backend scaffold
Add workspace migrations
Implement TaskService
Add task repository tests
Fix workspace isolation check
```

Rule:

```text
Each branch should keep changes reviewable and aligned with one implementation stage.
```

---

# 18. Local Security Rules

Local development must still protect:

```text
no real production secrets
no committed .env.local
no raw tokens in logs
no raw secrets in audit events
no raw secrets in runtime events
```

MVP local auth may use development mode, but must be clearly marked:

```text
DEV_AUTH_MODE=true
```

Rule:

```text
Development shortcuts must not silently become production behavior.
```

---

# 19. AI-Assisted Development Workflow

AI-assisted coding should use:

```text
architecture docs as source of truth
implementation plan docs as coding plan
small file-level tasks
tests as acceptance criteria
Git diffs for review
```

Recommended prompt pattern:

```text
Implement TaskRepository according to 30_BACKEND_IMPLEMENTATION_PLAN/08_REPOSITORY_IMPLEMENTATION_GUIDE.md and 27_DATA_MODEL conventions. Add repository tests for workspace isolation.
```

Rule:

```text
AI-generated code must be tested and reviewed like human-written code.
```

---

# 20. Documentation Workflow

When implementation changes architecture assumptions:

```text
update relevant implementation plan document
update API contract if route behavior changes
update data model if schema meaning changes
update audit document when layer is complete
```

Rule:

```text
Code and architecture documents should not intentionally diverge without an explicit decision record.
```

---

# 21. Troubleshooting

Common issues:

```text
Docker not running
PostgreSQL port already in use
DATABASE_URL points to wrong database
Prisma client not generated
migrations out of sync
.env.local missing
DEV_AUTH_MODE disabled unexpectedly
tests accidentally using dev database
```

Recommended first checks:

```bash
docker compose ps
cat backend/.env.local
cd backend && pnpm prisma validate
cd backend && pnpm prisma migrate status
```

---

# 22. Local Workflow Acceptance Criteria

Local Development Workflow is accepted when:

- required local tools are defined;
- repository setup is documented;
- environment file rules are defined;
- Docker Compose services are identified;
- database migration workflow is documented;
- seed workflow is documented;
- backend start workflow is defined;
- developer commands are listed;
- API smoke workflow is defined;
- test workflow is defined;
- debug and data inspection workflows are defined;
- reset workflow is defined;
- branch workflow is documented;
- local security rules are defined;
- AI-assisted development workflow is documented;
- troubleshooting guidance is included.

Status:

```text
Accepted for CI/CD Readiness Plan
```

---

# 23. Final Statement

```text
Bizzi Local Development Workflow defines the repeatable developer path for running, testing, resetting and debugging the backend MVP locally while preserving workspace scope, auditability and implementation discipline.
```

This workflow prepares Bizzi for consistent human and AI-assisted backend development.