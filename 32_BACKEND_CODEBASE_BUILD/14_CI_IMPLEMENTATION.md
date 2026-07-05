# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD  
**Component Type:** Backend Codebase Build Specification  
**Previous Document:** 13_TEST_IMPLEMENTATION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

# 1. Purpose

This document defines the concrete CI implementation for the Bizzi backend codebase.

It specifies the GitHub Actions workflow, required quality gates, test database service, environment variables, command sequence and acceptance rules required before backend code can be considered safe to merge.

---

# 2. Target Workflow File

```text
.github/workflows/backend-ci.yml
```

The CI workflow belongs at repository root and validates the backend codebase on pull requests and main branch pushes.

---

# 3. CI Responsibilities

The CI workflow must:

```text
checkout repository
install Node.js LTS
install pnpm
install dependencies with lockfile enforcement
start PostgreSQL test service
validate Prisma schema
generate Prisma client
apply migrations to test database
run lint
run typecheck
run unit tests
run integration tests
run e2e tests
build backend
```

---

# 4. Runtime Environment

```text
ubuntu-latest
Node.js LTS
pnpm
PostgreSQL 16
```

---

# 5. Required Environment Variables

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

Rules:

```text
CI must not use production credentials.
CI must use disposable test values only.
CI must not print secrets into logs.
```

---

# 6. Workflow Triggers

Recommended triggers:

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
```

---

# 7. PostgreSQL Service

The workflow must start a disposable PostgreSQL service:

```yaml
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
```

---

# 8. Workflow Gates

Required gates:

```text
install gate
prisma validation gate
migration gate
lint gate
typecheck gate
unit test gate
integration test gate
e2e test gate
build gate
```

Any failed gate must fail the workflow.

---

# 9. Recommended Command Sequence

```bash
pnpm install --frozen-lockfile
cd backend
pnpm prisma validate
pnpm prisma generate
pnpm prisma migrate deploy
pnpm lint
pnpm typecheck
pnpm test:unit
pnpm test:integration
pnpm test:e2e
pnpm build
```

---

# 10. Minimal Permissions

Recommended permissions:

```yaml
permissions:
  contents: read
```

CI does not need write access for the initial quality gate.

---

# 11. Acceptance Criteria

CI Implementation is accepted when:

```text
[ ] backend-ci.yml exists
[ ] workflow runs on pull requests
[ ] workflow runs on main branch pushes
[ ] PostgreSQL service starts successfully
[ ] dependencies install with frozen lockfile
[ ] Prisma schema validates
[ ] Prisma client generates
[ ] migrations apply to test database
[ ] lint passes
[ ] typecheck passes
[ ] unit tests pass
[ ] integration tests pass
[ ] e2e tests pass
[ ] backend build passes
[ ] failed quality gate blocks merge
```

---

# 12. Final Statement

```text
Bizzi CI Implementation defines the automated quality gate for backend codebase changes.
```

This workflow protects the repository before Bizzi proceeds into executable source generation, full module implementation and deployment readiness.