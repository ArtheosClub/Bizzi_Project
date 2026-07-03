# 11_CI_CD_READINESS_PLAN.md

# Bizzi Platform

## CI/CD Readiness Plan

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 10_LOCAL_DEVELOPMENT_WORKFLOW.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the CI/CD readiness plan for Bizzi Platform backend implementation.

It specifies how Bizzi should prepare GitHub Actions, quality gates, test gates, migration checks, build validation, artifact handling, branch rules and deployment readiness without prematurely overbuilding production infrastructure.

Core question:

```text
How should Bizzi introduce CI/CD so that every backend change is automatically checked for quality, safety, testability and architecture alignment?
```

---

# 2. CI/CD Readiness Thesis

```text
Bizzi CI/CD should start as a quality gate before it becomes a deployment pipeline. The first goal is to prevent broken, untested or unsafe backend changes from entering main.
```

CI/CD must protect:

```text
install reproducibility
lint quality
type safety
test reliability
database migration validity
workspace isolation regressions
audit/runtime event behavior
build readiness
secret safety
```

---

# 3. Initial CI Scope

Initial CI scope:

```text
backend install
backend lint
backend typecheck
backend unit tests
backend repository tests
backend API/e2e tests
backend build
migration validation
```

Out of initial scope:

```text
production deployment
cloud infrastructure provisioning
blue/green deployments
advanced observability
load testing
release automation
```

---

# 4. GitHub Actions Decision

Recommended CI runner:

```text
GitHub Actions
```

Initial workflow:

```text
.github/workflows/backend-ci.yml
```

Optional workflows later:

```text
.github/workflows/docs-check.yml
.github/workflows/migration-check.yml
.github/workflows/release.yml
.github/workflows/deploy-staging.yml
```

Rule:

```text
Start with backend-ci.yml before adding deployment workflows.
```

---

# 5. Trigger Strategy

Initial triggers:

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
      - 'package.json'
      - 'pnpm-lock.yaml'
      - '.github/workflows/backend-ci.yml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - 'package.json'
      - 'pnpm-lock.yaml'
      - '.github/workflows/backend-ci.yml'
```

Rule:

```text
CI should run on pull requests and on pushes to main.
```

---

# 6. CI Environment

Required services:

```text
PostgreSQL test database
```

Future services:

```text
Redis for BullMQ tests
MinIO for export storage tests
```

Environment variables:

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

Rule:

```text
CI must not use production secrets.
```

---

# 7. Backend CI Job Stages

Recommended job stages:

```text
checkout
setup Node.js
setup pnpm
install dependencies
start PostgreSQL service
validate Prisma schema
run migrations
run lint
run typecheck
run unit tests
run integration/repository tests
run API/e2e tests
run build
upload test artifacts optional
```

Rule:

```text
Failure in any quality gate should fail the workflow.
```

---

# 8. Dependency Installation Gate

CI must verify:

```text
lockfile consistency
dependency install succeeds
no missing packages
```

Recommended command:

```bash
pnpm install --frozen-lockfile
```

Rule:

```text
CI should not mutate lockfiles.
```

---

# 9. Lint Gate

Recommended command:

```bash
pnpm lint
```

Purpose:

```text
prevent obvious style, unused code and unsafe patterns
```

Rule:

```text
Lint should be required before merge once backend implementation begins.
```

---

# 10. Typecheck Gate

Recommended command:

```bash
pnpm typecheck
```

Purpose:

```text
verify TypeScript compile-time correctness
```

Rule:

```text
Type errors must block merge.
```

---

# 11. Test Gates

Required test gates:

```bash
pnpm test:unit
pnpm test:integration
pnpm test:e2e
```

MVP rule:

```text
At minimum, all P1 route tests and repository workspace isolation tests must run in CI.
```

Future optional gate:

```bash
pnpm test:coverage
```

---

# 12. Migration Gate

Migration gate verifies:

```text
Prisma schema is valid
Prisma client can generate
migrations can apply to empty database
```

Recommended commands:

```bash
pnpm prisma validate
pnpm prisma generate
pnpm prisma migrate deploy
```

Rule:

```text
A migration that cannot apply from a clean database must block merge.
```

---

# 13. Build Gate

Recommended command:

```bash
pnpm build
```

Purpose:

```text
verify backend compiles into deployable artifact
```

Rule:

```text
Build failure blocks merge.
```

---

# 14. Secret Safety Gate

Initial checks:

```text
no .env.local committed
no obvious secret names with real values
no production credentials in repo
```

Possible tools later:

```text
gitleaks
GitHub secret scanning
trufflehog
```

Rule:

```text
Secrets must be injected through environment variables or secret manager, not committed.
```

---

# 15. Branch Protection Readiness

Recommended branch protection for `main` after CI is stable:

```text
require pull request before merge
require backend-ci success
require linear history optional
require conversation resolution optional
restrict force pushes
```

Rule:

```text
Branch protection should be enabled only after CI workflow is reliable enough not to block development unnecessarily.
```

---

# 16. Artifact Strategy

Initial artifacts:

```text
test reports optional
coverage reports optional
build output optional
```

MVP rule:

```text
Do not overbuild artifact publishing before deployment target exists.
```

Future artifacts:

```text
Docker image
OpenAPI spec
coverage report
migration report
release package
```

---

# 17. Deployment Readiness Phases

Phases:

```text
Phase 1 — CI quality gates only
Phase 2 — build artifact generation
Phase 3 — Docker image build
Phase 4 — staging deployment
Phase 5 — production deployment
```

Current target:

```text
Phase 1
```

---

# 18. Docker Image Readiness Later

Future Docker requirements:

```text
backend Dockerfile
.dockerignore
non-root runtime user
production build step
healthcheck
environment variable injection
```

Rule:

```text
Docker image build should be added after local backend MVP runs reliably.
```

---

# 19. Staging Deployment Readiness Later

Before staging deployment, Bizzi needs:

```text
hosting target selected
managed PostgreSQL selected
environment variable strategy
migration deployment process
health and readiness endpoints
rollback strategy
logging strategy
```

Rule:

```text
Do not deploy before migrations, health checks and test gates are stable.
```

---

# 20. CI/CD Security Rules

Rules:

```text
CI secrets should be scoped minimally
pull requests from untrusted contexts must not expose secrets
test database must be disposable
logs must not print secrets
production deploy requires explicit environment protection later
```

---

# 21. Pull Request Quality Checklist

Each backend PR should answer:

```text
Does it pass lint?
Does it pass typecheck?
Does it pass tests?
Does it add/update tests for changed behavior?
Does it preserve workspace isolation?
Does it preserve audit/runtime events for mutations?
Does it avoid raw secrets?
Does it update docs when behavior changes?
```

---

# 22. AI-Assisted CI Rules

AI-generated code must pass the same gates.

Rules:

```text
no bypass for AI-generated commits
tests must be included or updated
architecture docs must be referenced when implementing major modules
human review remains required before production deployment
```

---

# 23. Initial Workflow Skeleton

Illustrative `backend-ci.yml` skeleton:

```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'

jobs:
  backend-ci:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: bizzi
          POSTGRES_PASSWORD: bizzi
          POSTGRES_DB: bizzi_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: cd backend && pnpm prisma validate
      - run: cd backend && pnpm prisma generate
      - run: cd backend && pnpm prisma migrate deploy
      - run: cd backend && pnpm lint
      - run: cd backend && pnpm typecheck
      - run: cd backend && pnpm test
      - run: cd backend && pnpm build
```

Rule:

```text
The skeleton is illustrative and should be adjusted to actual package scripts once backend scaffold exists.
```

---

# 24. CI/CD Readiness Checklist

CI/CD is ready for MVP when:

```text
backend-ci.yml exists
CI uses test database
install gate passes
Prisma validation passes
migrations apply in CI
lint passes
typecheck passes
tests pass
build passes
no production secrets are required
main branch protection can require CI
```

---

# 25. Anti-Patterns

Avoid:

```text
adding deployment before tests exist
using production database in CI
committing .env.local
allowing failing tests on main
skipping migration validation
CI that only checks formatting
secrets in workflow YAML
unreviewed AI-generated code bypassing CI
```

---

# 26. Acceptance Criteria

CI/CD Readiness Plan is accepted when:

- GitHub Actions is selected;
- initial CI scope is defined;
- triggers are defined;
- CI environment is defined;
- backend job stages are documented;
- install, lint, typecheck, test, migration and build gates are defined;
- secret safety gate is defined;
- branch protection readiness is documented;
- artifact strategy is defined;
- deployment readiness phases are defined;
- PR quality checklist is included;
- AI-assisted CI rules are documented;
- illustrative workflow skeleton is provided;
- anti-patterns are documented.

Status:

```text
Accepted for Implementation Risk Register
```

---

# 27. Final Statement

```text
Bizzi CI/CD Readiness Plan defines the transition from local backend development into automated quality enforcement, ensuring that every backend change is installable, typed, tested, migration-safe and ready for controlled deployment evolution.
```

This plan prepares Bizzi for reliable team and AI-assisted engineering without prematurely committing to production infrastructure.