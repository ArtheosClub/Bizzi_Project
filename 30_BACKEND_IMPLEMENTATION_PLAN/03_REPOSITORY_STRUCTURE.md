# 03_REPOSITORY_STRUCTURE.md

# Bizzi Platform

## Repository Structure

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 02_MVP_VERTICAL_SLICE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the recommended repository structure for Bizzi Platform implementation.

It translates the accepted backend implementation stack and MVP vertical slice into a concrete folder, module, package, configuration, testing and documentation layout.

Core question:

```text
How should the Bizzi repository be organized so that backend implementation remains modular, testable, workspace-safe, AI-readable and aligned with the architecture layers?
```

---

# 2. Repository Structure Thesis

```text
Bizzi should use a structured monorepo that keeps architecture documents, backend implementation, frontend implementation, shared packages, infrastructure configuration and tests in one coordinated repository while preserving strict module boundaries.
```

The repository must support:

```text
architecture-first development
backend MVP implementation
future frontend implementation
future agent orchestration
shared contracts
local development
CI/CD
AI-assisted coding
```

---

# 3. Monorepo Decision

Recommended approach:

```text
Monorepo
```

Reason:

```text
Bizzi is a platform product with tightly connected architecture documents, backend services, frontend UI, shared types, API contracts, deployment configuration and AI orchestration assets.
```

Benefits:

```text
single source of truth
shared contracts between backend and frontend
simpler early-stage development
better architecture traceability
simpler AI-assisted navigation
coordinated commits across docs and code
```

Risks:

```text
repository growth
unclear boundaries if not enforced
large CI jobs later
```

Mitigation:

```text
Use clear top-level directories, package boundaries and module ownership rules.
```

---

# 4. Top-Level Repository Layout

Canonical top-level layout:

```text
/
├── README.md
├── docs/
├── backend/
├── frontend/
├── packages/
├── infra/
├── scripts/
├── tools/
├── .github/
├── .env.example
├── docker-compose.yml
├── package.json
├── pnpm-workspace.yaml
└── tsconfig.base.json
```

Current architecture documents may remain in numbered folders at repository root during architecture phase, but implementation should introduce `docs/` as the long-term documentation home.

---

# 5. Documentation Layout

Recommended documentation structure:

```text
docs/
├── architecture/
├── product/
├── api-contracts/
├── backend-design/
├── implementation-plan/
├── decisions/
└── audits/
```

Mapping from existing architecture layers:

```text
24_PRODUCTIZATION_AND_IMPLEMENTATION → docs/product/
25_RUNTIME_PLATFORM → docs/architecture/runtime/
26_DOMAIN_MODEL → docs/architecture/domain-model/
27_DATA_MODEL → docs/architecture/data-model/
28_API_CONTRACTS → docs/api-contracts/
29_BACKEND_SERVICE_DESIGN → docs/backend-design/
30_BACKEND_IMPLEMENTATION_PLAN → docs/implementation-plan/
```

MVP rule:

```text
Do not move existing numbered folders until a migration plan is created. New implementation code can coexist with current architecture folders.
```

---

# 6. Backend Layout

Recommended backend layout:

```text
backend/
├── README.md
├── package.json
├── tsconfig.json
├── nest-cli.json
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── config/
│   ├── database/
│   ├── shared/
│   ├── modules/
│   └── jobs/
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── scripts/
```

Backend rule:

```text
All business behavior must live under backend/src/modules or backend/src/shared. Controllers must not directly access Prisma.
```

---

# 7. Backend Source Layout

Recommended `backend/src` layout:

```text
backend/src/
├── main.ts
├── app.module.ts
├── config/
│   ├── config.module.ts
│   ├── env.schema.ts
│   └── configuration.ts
├── database/
│   ├── database.module.ts
│   ├── prisma.service.ts
│   └── transaction.manager.ts
├── shared/
│   ├── context/
│   ├── errors/
│   ├── dto/
│   ├── pagination/
│   ├── constants/
│   └── utils/
├── modules/
│   ├── identity/
│   ├── workspace/
│   ├── authorization/
│   ├── validation/
│   ├── task/
│   ├── decision/
│   ├── memory/
│   ├── audit/
│   ├── event/
│   ├── dashboard/
│   └── export/
└── jobs/
    ├── jobs.module.ts
    └── processors/
```

---

# 8. Module Folder Pattern

Each backend module should follow a consistent pattern.

Example:

```text
backend/src/modules/task/
├── task.module.ts
├── controllers/
│   └── task.controller.ts
├── services/
│   ├── task.service.ts
│   └── task-lifecycle.service.ts
├── repositories/
│   └── task.repository.ts
├── dto/
│   ├── create-task.dto.ts
│   ├── update-task.dto.ts
│   └── task.response.dto.ts
├── policies/
│   └── task-status.policy.ts
├── constants/
│   └── task-status.constants.ts
└── tests/
    ├── task.service.spec.ts
    └── task.repository.spec.ts
```

Rule:

```text
Every feature module must separate controllers, services, repositories and DTOs.
```

---

# 9. MVP Backend Modules

Initial backend modules:

```text
identity
workspace
authorization
validation
task
decision
memory
audit
event
dashboard
```

Optional early modules:

```text
export
health
jobs
```

Deferred modules:

```text
operating-map
function-responsibility
agent
process
integration
security
advanced-export
```

---

# 10. Shared Kernel Layout

Recommended shared layout:

```text
backend/src/shared/
├── context/
│   ├── actor-context.ts
│   ├── workspace-context.ts
│   ├── request-context.ts
│   └── correlation-context.ts
├── errors/
│   ├── service-error.ts
│   ├── error-codes.ts
│   └── error-mapper.ts
├── dto/
│   ├── error-response.dto.ts
│   ├── pagination.dto.ts
│   └── base-response.dto.ts
├── pagination/
│   ├── pagination.types.ts
│   └── pagination.utils.ts
├── constants/
│   ├── object-types.ts
│   ├── audit-actions.ts
│   └── runtime-events.ts
└── utils/
```

Rule:

```text
Shared kernel may contain cross-cutting primitives, but not feature-specific business logic.
```

---

# 11. Database Layout

Recommended database layout:

```text
backend/prisma/
├── schema.prisma
├── migrations/
├── seed.ts
└── README.md
```

Additional optional layout for SQL-heavy evolution:

```text
backend/database/
├── sql/
├── views/
├── indexes/
└── fixtures/
```

MVP rule:

```text
Use Prisma schema and migrations first. Keep raw SQL isolated if introduced later.
```

---

# 12. Test Layout

Recommended test layout:

```text
backend/test/
├── unit/
├── integration/
├── e2e/
├── fixtures/
├── factories/
└── helpers/
```

Module-local tests are allowed:

```text
backend/src/modules/task/tests/
```

Preferred approach:

```text
Use module-local unit tests and central integration/e2e tests.
```

Rule:

```text
Every module must have service tests and repository tests before it is considered complete.
```

---

# 13. Frontend Layout

Frontend is not implemented in the first backend slice, but repository structure should reserve space.

Recommended future layout:

```text
frontend/
├── README.md
├── package.json
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── api/
│   ├── state/
│   └── styles/
└── test/
```

Recommended future stack:

```text
Next.js or React/Vite
TypeScript
API client generated from OpenAPI later
```

---

# 14. Shared Packages Layout

Recommended packages layout:

```text
packages/
├── api-types/
├── domain-types/
├── config/
├── eslint-config/
└── tsconfig/
```

MVP may start without shared packages.

Rule:

```text
Introduce packages only when duplication appears or frontend implementation begins.
```

---

# 15. Infrastructure Layout

Recommended infra layout:

```text
infra/
├── docker/
├── terraform/
├── environments/
│   ├── local/
│   ├── staging/
│   └── production/
└── README.md
```

MVP infra requirement:

```text
docker-compose.yml for local PostgreSQL and Redis later
```

Do not overbuild cloud infrastructure before MVP backend passes.

---

# 16. Scripts Layout

Recommended scripts layout:

```text
scripts/
├── dev.sh
├── test.sh
├── db-migrate.sh
├── db-seed.sh
├── lint.sh
└── generate-openapi.sh
```

Backend-local scripts may also exist:

```text
backend/scripts/
```

Rule:

```text
Common developer tasks should be executable by simple documented commands.
```

---

# 17. GitHub Workflow Layout

Recommended GitHub workflow layout:

```text
.github/
├── workflows/
│   ├── backend-ci.yml
│   ├── docs-check.yml
│   └── release.yml later
├── pull_request_template.md
└── ISSUE_TEMPLATE/
```

MVP workflow:

```text
backend-ci.yml
```

CI checks:

```text
install
lint
typecheck
test
build
```

---

# 18. Environment Files

Recommended environment files:

```text
.env.example
backend/.env.example
backend/.env.local ignored
```

Rules:

```text
.env files with secrets must not be committed
.env.example must not contain real secrets
configuration must validate required variables at startup
```

Required MVP variables:

```text
DATABASE_URL
NODE_ENV
PORT
JWT_SECRET or DEV_AUTH_MODE
```

Future variables:

```text
REDIS_URL
S3_ENDPOINT
S3_BUCKET
OPENAI_API_KEY or AI_PROVIDER_KEY
```

---

# 19. Package Manager Decision

Recommended package manager:

```text
pnpm
```

Reason:

```text
fast installs
workspace support
monorepo-friendly
strict dependency management
```

Alternative:

```text
npm is acceptable for very early MVP if simplicity is more important.
```

Decision:

```text
Use pnpm for structured monorepo implementation unless tooling constraints require npm.
```

---

# 20. Import Rules

Import rules:

```text
feature modules may import shared primitives
feature modules should avoid importing other feature repositories directly
cross-module business actions should go through services
repositories must not import services
controllers must not import repositories
shared kernel must not import feature modules
```

Preferred dependency direction:

```text
controller → service → repository
service → authorization / validation / audit / event
repository → database
feature → shared
```

---

# 21. Naming Rules

File naming:

```text
kebab-case for files
PascalCase for classes
camelCase for methods and variables
UPPER_SNAKE_CASE for environment variables
snake_case for database fields
```

Examples:

```text
task-lifecycle.service.ts
TaskLifecycleService
completeTask()
DATABASE_URL
workspace_id
```

---

# 22. Generated Code Policy

Generated code may include:

```text
Prisma client
OpenAPI generated clients later
API types later
```

Rules:

```text
generated code should be clearly separated
do not manually edit generated files
commit generated code only when project policy requires it
prefer reproducible generation commands
```

---

# 23. Documentation Policy

Each implemented module should have:

```text
README or module notes when behavior is non-obvious
service tests as executable documentation
references to architecture documents where useful
```

Architecture docs remain canonical for intent.

Implementation docs clarify how code realizes the intent.

---

# 24. Repository Growth Strategy

Growth phases:

```text
Phase 1 — architecture folders + backend MVP
Phase 2 — backend services expanded
Phase 3 — frontend added
Phase 4 — shared packages introduced
Phase 5 — infra and CI/CD expanded
Phase 6 — agent orchestration assets added
```

Rule:

```text
Do not introduce complex workspace packages before the first backend vertical slice works.
```

---

# 25. Anti-Patterns

Avoid:

```text
single flat src directory
controllers with database access
services without tests
repositories without workspace_id filters
shared folder becoming a dumping ground
committing real .env files
mixing generated code with handwritten business logic
creating frontend before backend contracts are stable enough
adding cloud infra before local MVP works
```

---

# 26. MVP Repository Structure

Minimum MVP structure:

```text
/
├── backend/
│   ├── package.json
│   ├── prisma/
│   │   ├── schema.prisma
│   │   └── migrations/
│   ├── src/
│   │   ├── main.ts
│   │   ├── app.module.ts
│   │   ├── database/
│   │   ├── shared/
│   │   └── modules/
│   │       ├── identity/
│   │       ├── workspace/
│   │       ├── authorization/
│   │       ├── validation/
│   │       ├── task/
│   │       ├── decision/
│   │       ├── memory/
│   │       ├── audit/
│   │       ├── event/
│   │       └── dashboard/
│   └── test/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 27. Migration from Architecture-Only Repository

Current repository contains architecture documents as numbered folders.

Migration rule:

```text
Do not delete or move architecture folders during backend scaffold creation.
```

Recommended approach:

```text
add backend/ alongside existing architecture folders
add docs/ later if documentation migration is planned
keep numbered architecture folders as canonical until migration audit passes
```

---

# 28. Acceptance Criteria

Repository Structure is accepted when:

- monorepo decision is documented;
- top-level layout is defined;
- backend layout is defined;
- backend source layout is defined;
- module folder pattern is defined;
- shared kernel layout is defined;
- database layout is defined;
- test layout is defined;
- frontend, packages and infra placeholders are defined;
- environment file rules are defined;
- package manager decision is documented;
- import and dependency rules are defined;
- naming and generated code rules are documented;
- MVP minimum structure is defined;
- migration from architecture-only repository is addressed.

Status:

```text
Accepted for Database Migration Plan
```

---

# 29. Final Statement

```text
Bizzi Repository Structure defines a modular monorepo layout that keeps architecture, backend implementation, future frontend, shared packages and infrastructure coordinated while preserving backend service boundaries and implementation discipline.
```

This structure gives Bizzi a practical foundation for moving from architecture documentation into real backend code.