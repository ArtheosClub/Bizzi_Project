# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD  
**Component Type:** Codebase Build Specification  
**Previous Document:** 13_TEST_IMPLEMENTATION.md  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete CI implementation for the Bizzi backend codebase.

The goal is to create a repeatable GitHub Actions workflow that validates the backend on every pull request and main branch update.

---

# 2. CI Scope

The CI implementation covers:

```text
checkout
pnpm setup
Node.js setup
dependency install
Prisma validation
Prisma client generation
database migration validation
lint
typecheck
unit tests
integration tests
e2e tests
build
```

---

# 3. Target Workflow File

```text
.github/workflows/backend-ci.yml
```

---

# 4. Runtime Stack

```text
GitHub Actions
ubuntu-latest
Node.js LTS
pnpm
PostgreSQL test service
Prisma
Jest
Supertest
```

---

# 5. Workflow Triggers

```yaml
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
```

---

# 6. Required CI Environment

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

Rules:

```text
CI must not use production secrets.
CI must not depend on local developer state.
CI must use a disposable test database.
```

---

# 7. Required Commands

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

# 8. Acceptance Criteria

CI Implementation is accepted when:

- backend CI workflow file is defined;
- workflow runs on PR and main branch updates;
- PostgreSQL test service is available;
- Prisma schema validates;
- migrations apply cleanly;
- lint passes;
- typecheck passes;
- all test suites pass;
- backend build passes;
- no production secrets are required.

---

# 9. Final Statement

```text
Bizzi CI Implementation defines the automated backend quality gate for the codebase build layer.
```

This workflow protects the backend from regressions before the project moves into runnable source implementation.