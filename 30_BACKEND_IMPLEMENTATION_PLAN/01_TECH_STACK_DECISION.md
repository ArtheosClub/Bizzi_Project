# 01_TECH_STACK_DECISION.md

# Bizzi Platform

## Tech Stack Decision

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 00_IMPLEMENTATION_PLAN_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the recommended backend technology stack for Bizzi Platform MVP implementation.

It converts architectural requirements into concrete technology decisions for backend language, framework, database, ORM/query layer, migrations, validation, testing, local development, jobs, storage and observability.

Core question:

```text
Which technology stack gives Bizzi the fastest, safest and most maintainable path from backend architecture into a working MVP?
```

---

# 2. Decision Summary

Recommended MVP stack:

```text
Language: TypeScript
Runtime: Node.js LTS
Backend Framework: NestJS
API Style: REST JSON first
Database: PostgreSQL
ORM / Query Layer: Prisma for MVP
Migrations: Prisma Migrate
Validation: Zod or class-validator with DTO discipline
Authentication: JWT/session abstraction with provider-neutral boundary
Authorization: custom AuthorizationService owner-first, RBAC-ready
Testing: Jest + Supertest
Local Development: Docker Compose for PostgreSQL and Redis
Job Queue: BullMQ with Redis when async jobs are needed
Object Storage: S3-compatible abstraction, local MinIO later
Logging: structured JSON logging with Pino or Nest logger adapter
Observability: correlation_id first, OpenTelemetry later
API Docs: OpenAPI generated from controllers or maintained from contracts
```

Decision result:

```text
Use TypeScript + NestJS + PostgreSQL + Prisma for MVP backend implementation.
```

---

# 3. Selection Criteria

The stack is selected against these criteria:

```text
speed of MVP delivery
clear module boundaries
strong TypeScript DTO discipline
PostgreSQL compatibility
transaction support
testability
API contract implementation clarity
workspace isolation enforceability
audit/event implementation simplicity
AI orchestration integration readiness
future enterprise expansion path
```

---

# 4. Why TypeScript

TypeScript is recommended because Bizzi requires:

```text
shared DTO discipline
clear service interfaces
fast API implementation
strong developer ecosystem
AI-friendly code generation and review
frontend/backend type alignment later
large ecosystem for validation and testing
```

Benefits:

```text
faster MVP iteration
fewer schema drift errors than plain JavaScript
clearer service contracts
better compatibility with modern AI-assisted engineering workflows
```

---

# 5. Why NestJS

NestJS is recommended because it naturally supports Bizzi backend architecture:

```text
modules
controllers
services
providers
dependency injection
guards
pipes
interceptors
testing utilities
OpenAPI integration
```

This maps directly to:

```text
29_BACKEND_SERVICE_DESIGN/02_BACKEND_MODULE_CATALOG.md
29_BACKEND_SERVICE_DESIGN/03_CONTROLLER_SERVICE_REPOSITORY_PATTERN.md
```

Decision:

```text
NestJS is the preferred backend framework for the MVP.
```

---

# 6. Why PostgreSQL

PostgreSQL is recommended because Bizzi needs:

```text
relational integrity
workspace-scoped queries
UUID primary keys
JSONB metadata fields
indexed filtering and sorting
transaction consistency
audit and runtime event persistence
future full-text search
future vector search extension path
```

Decision:

```text
PostgreSQL is the canonical Bizzi database for MVP and beyond.
```

---

# 7. ORM / Query Layer Decision

Recommended MVP choice:

```text
Prisma
```

Why Prisma:

```text
fast schema iteration
clear generated types
simple migrations
strong TypeScript integration
good developer experience
sufficient for MVP CRUD and transactional services
```

Known limitation:

```text
advanced query optimization may require raw SQL or future query builder patterns.
```

Mitigation:

```text
Use repositories to isolate Prisma implementation details so the persistence layer can evolve later.
```

---

# 8. Migration Tool Decision

Recommended MVP choice:

```text
Prisma Migrate
```

Rules:

```text
all schema changes must be versioned migrations
migration files must be committed
no manual production schema changes
seed data must be separate from schema migrations
```

Future option:

```text
If migration complexity grows, evaluate dedicated migration tools or SQL-first migrations.
```

---

# 9. Validation Decision

Two acceptable options:

```text
NestJS DTO + class-validator
Zod schemas
```

Recommended MVP approach:

```text
Use NestJS DTO validation for controller boundary and shared ValidationService for business validation.
```

Possible enhancement:

```text
Use Zod for reusable schema definitions where AI/tool contracts benefit from explicit schemas.
```

Rule:

```text
API schema validation does not replace service-level business validation.
```

---

# 10. Authentication Decision

MVP should use an authentication abstraction, not hard-code a provider deeply into services.

Recommended approach:

```text
AuthModule provides authenticated ActorContext
IdentityModule exposes /me behavior
service layer receives actor_id and actor_type
```

Possible providers:

```text
simple local auth for development
JWT auth
Auth0
Clerk
Supabase Auth
custom session provider later
```

MVP decision:

```text
Implement provider-neutral AuthModule with JWT/session-compatible interfaces.
```

---

# 11. Authorization Decision

Authorization is custom platform logic.

MVP authorization:

```text
owner-only workspace authorization
```

Expansion path:

```text
workspace_access roles
permission map
resource-level permissions
agent authority scopes
export scopes
audit visibility roles
```

Decision:

```text
Implement AuthorizationService from the beginning, even if MVP uses owner-only rules.
```

---

# 12. Testing Stack Decision

Recommended testing tools:

```text
Jest
Supertest
Prisma test database
Docker Compose PostgreSQL
```

Test categories:

```text
unit tests for validators and policies
service tests for business rules
repository tests for workspace-scoped queries
API tests for route contracts
transaction tests for audit/runtime event consistency
```

Rule:

```text
No backend module is considered complete without service and repository tests.
```

---

# 13. Local Development Decision

Recommended local tooling:

```text
Docker Compose
PostgreSQL container
Redis container when queues are introduced
.env files for local config
seed scripts
migration scripts
```

Required commands:

```text
npm install
npm run dev
npm run test
npm run lint
npm run typecheck
npm run db:migrate
npm run db:seed
```

---

# 14. Job Queue Decision

MVP can start without a full async queue if all operations are simple.

However, Bizzi needs an expansion path for:

```text
export generation
integration sync
AI analysis
dashboard refresh
runtime event processing
```

Recommended queue when needed:

```text
BullMQ + Redis
```

MVP rule:

```text
Persist runtime events from day one; add BullMQ when background execution becomes necessary.
```

---

# 15. Object Storage Decision

Exports require file storage.

MVP options:

```text
local filesystem for development only
S3-compatible storage abstraction for implementation
MinIO for local development later
AWS S3 or compatible provider for production later
```

Decision:

```text
Create an ExportFileStorage interface before binding to a provider.
```

---

# 16. Logging Decision

Logging must support traceability.

Recommended approach:

```text
structured JSON logs
correlation_id in every request log
request_id in every request log
workspace_id when available
actor_id when available
```

Recommended tools:

```text
NestJS logger adapter
Pino later if needed
```

Rule:

```text
Logs must not contain raw secrets, provider tokens or signed URLs.
```

---

# 17. Observability Decision

MVP observability starts with:

```text
correlation_id
structured logs
audit events
runtime events
basic health endpoint
```

Future observability:

```text
OpenTelemetry
metrics
tracing
error monitoring
runtime event failure dashboards
```

Decision:

```text
Do not overbuild observability first; preserve correlation hooks from the beginning.
```

---

# 18. API Documentation Decision

Bizzi already has Markdown API contracts.

Implementation should later generate or maintain:

```text
OpenAPI YAML
Swagger UI
typed API client later
```

MVP approach:

```text
Implement routes according to 28_API_CONTRACTS and generate OpenAPI from NestJS decorators where practical.
```

Rule:

```text
If implementation diverges from API contracts, update the contract intentionally or fix implementation.
```

---

# 19. Security Baseline

MVP stack must enforce:

```text
server-side authorization
workspace isolation
structured validation
no raw secrets in logs/events/API responses
credential_ref only for integrations
correlation_id propagation
rate limit expansion path
secure environment variable handling
```

---

# 20. Rejected Alternatives

## Express-only Backend

Rejected because:

```text
less structure by default
more custom boilerplate for modules and DI
higher risk of architecture drift
```

## Python FastAPI

Strong alternative, but not selected because:

```text
TypeScript aligns better with frontend and DTO sharing
NestJS maps more directly to module/service architecture
```

## Prisma-free Raw SQL First

Rejected for MVP because:

```text
slower iteration
more boilerplate
less type generation
```

May be revisited for performance-sensitive areas later.

---

# 21. MVP Stack Decision Table

| Area | Decision | Status |
|---|---|---|
| Language | TypeScript | Accepted |
| Runtime | Node.js LTS | Accepted |
| Framework | NestJS | Accepted |
| Database | PostgreSQL | Accepted |
| ORM | Prisma | Accepted for MVP |
| Migrations | Prisma Migrate | Accepted for MVP |
| Validation | NestJS DTO validation + service validators | Accepted |
| Auth | Provider-neutral AuthModule | Accepted |
| Authorization | Custom AuthorizationService | Accepted |
| Testing | Jest + Supertest | Accepted |
| Local DB | Docker Compose PostgreSQL | Accepted |
| Queue | BullMQ + Redis later | Conditional |
| Storage | S3-compatible abstraction | Accepted |
| Logging | Structured logs with correlation_id | Accepted |
| Observability | Correlation first, OpenTelemetry later | Accepted |
| API Docs | OpenAPI from implementation/contracts | Accepted |

---

# 22. Implementation Implications

The selected stack implies:

```text
backend project should be TypeScript-first
modules should map to NestJS modules
controllers should map to API resource families
services should map to 29_BACKEND_SERVICE_DESIGN service classes
repositories should wrap Prisma client
transactions should use Prisma transaction context
validation should be split between DTO validation and service validation
errors should map to canonical API errors
```

---

# 23. Risk Register

## Risk 1 — Prisma Query Limits

Mitigation:

```text
Hide Prisma behind repositories and allow raw SQL for complex queries later.
```

## Risk 2 — NestJS Boilerplate Slows MVP

Mitigation:

```text
Start with limited modules and shared patterns.
```

## Risk 3 — Auth Provider Choice Delays Implementation

Mitigation:

```text
Use provider-neutral AuthModule and development identity stub first.
```

## Risk 4 — Async Jobs Overbuilt Too Early

Mitigation:

```text
Persist runtime events first; add BullMQ when needed.
```

## Risk 5 — OpenAPI Drift

Mitigation:

```text
Use API contracts as canonical source and audit generated docs later.
```

---

# 24. Acceptance Criteria

Tech Stack Decision is accepted when:

- backend language is selected;
- backend framework is selected;
- database is selected;
- ORM/query strategy is selected;
- migration strategy is selected;
- validation approach is selected;
- authentication and authorization approach is defined;
- testing stack is defined;
- local development dependencies are defined;
- queue and storage expansion paths are defined;
- logging and observability baseline is defined;
- rejected alternatives are documented;
- implementation implications are clear.

Status:

```text
Accepted for MVP Vertical Slice
```

---

# 25. Final Statement

```text
Bizzi backend implementation will use TypeScript, NestJS, PostgreSQL and Prisma as the MVP technology foundation, with service boundaries, repository isolation, workspace safety, auditability and AI governance preserved from the first implementation slice.
```

This decision enables practical backend implementation planning without sacrificing the architectural guarantees established in previous layers.