# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD  
**Component Type:** Codebase Build Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete CI implementation for the Bizzi backend codebase.

The CI implementation converts the CI workflow execution plan into repository files, package scripts and automated GitHub quality gates.

Core question:

```text
How should Bizzi verify every backend change automatically before it is accepted into the main branch?
```

---

# 2. CI Thesis

```text
CI is the first automated guardian of Bizzi architecture. It must verify install, schema, type safety, tests, migrations and build before code is trusted.
```

The CI implementation must prove:

```text
reproducible dependency install
Prisma schema validity
migration deployability
TypeScript correctness
lint correctness
unit tests
integration tests
e2e tests
backend build
no production secrets required
```

---

# 3. Target Files

Primary workflow file:

```text
.github/workflows/backend-ci.yml
```

Supporting backend files:

```text
backend/package.json
backend/prisma/schema.prisma
backend/jest.config.ts
backend/jest.e2e.config.ts
backend/.env.example
backend/test/setup/test-database.ts
backend/test/setup/test-app.ts
```

---

# 4. GitHub Actions Workflow

Workflow name:

```text
Backend CI
```

Workflow file:

```text
.github/workflows/backend-ci.yml
```

Recommended triggers:

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
      - 'package.json'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
      - 'package.json'
```

---

# 5. Runtime Environment

Runner:

```text
ubuntu-latest
```

Node:

```text
Node.js LTS
```

Package manager:

```text
pnpm
```

Database service:

```text
PostgreSQL 16
```

---

# 6. CI Environment Variables

Required CI values:

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
DEV_USER_EMAIL=ci@bizzi.local
DEV_USER_NAME=Bizzi CI User
JWT_SECRET=ci-test-only
```

Rules:

```text
CI must not require production credentials.
CI must not require cloud services.
CI must use a disposable test database.
CI must not print secrets.
```

---

# 7. PostgreSQL Service

Required GitHub Actions service:

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

Rule:

```text
CI must wait for PostgreSQL health before running Prisma or tests.
```

---

# 8. Required Package Scripts

Backend `package.json` must provide:

```json
{
  "scripts": {
    "lint": "eslint \"src/**/*.ts\" \"test/**/*.ts\"",
    "typecheck": "tsc --noEmit",
    "build": "nest build",
    "test": "jest",
    "test:unit": "jest --config jest.config.ts",
    "test:integration": "jest --config jest.integration.config.ts",
    "test:e2e": "jest --config jest.e2e.config.ts",
    "db:test:reset": "prisma migrate reset --force --skip-seed"
  }
}
```

Rule:

```text
Scripts may be adapted to actual NestJS/Jest setup, but CI command names should remain stable.
```

---

# 9. CI Job Stages

Required stages:

```text
checkout repository
setup pnpm
setup Node.js
install dependencies
validate Prisma schema
generate Prisma client
apply migrations
lint
typecheck
unit tests
integration tests
e2e tests
build
```

Every stage is a quality gate.

---

# 10. Workflow Skeleton

```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
      - 'package.json'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'pnpm-lock.yaml'
      - 'package.json'

permissions:
  contents: read

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

    env:
      NODE_ENV: test
      DATABASE_URL: postgresql://bizzi:bizzi@localhost:5432/bizzi_test
      DEV_AUTH_MODE: 'true'
      DEV_USER_EMAIL: ci@bizzi.local
      DEV_USER_NAME: Bizzi CI User
      JWT_SECRET: ci-test-only

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Prisma validate
        run: cd backend && pnpm prisma validate

      - name: Prisma generate
        run: cd backend && pnpm prisma generate

      - name: Prisma migrate deploy
        run: cd backend && pnpm prisma migrate deploy

      - name: Lint
        run: cd backend && pnpm lint

      - name: Typecheck
        run: cd backend && pnpm typecheck

      - name: Unit tests
        run: cd backend && pnpm test:unit

      - name: Integration tests
        run: cd backend && pnpm test:integration

      - name: E2E tests
        run: cd backend && pnpm test:e2e

      - name: Build
        run: cd backend && pnpm build
```

---

# 11. Branch Protection Readiness

After CI is stable, the `main` branch may require:

```text
Backend CI success
pull request before merge
no force pushes
conversation resolution optional
linear history optional
```

Rule:

```text
Do not enable strict branch protection until the first CI workflow is reliable.
```

---

# 12. Failure Handling

Common failures:

```text
missing package script
lockfile mismatch
PostgreSQL unavailable
wrong DATABASE_URL
Prisma migration failure
Prisma client not generated
lint failure
typecheck failure
flaky tests
build failure
```

Expected response:

```text
fix the root cause, do not disable CI to bypass failure.
```

---

# 13. Secret Safety

Rules:

```text
no production credentials in workflow YAML
no cloud secrets for MVP CI
no raw tokens in logs
use test-only local values
use minimal workflow permissions
```

---

# 14. Acceptance Criteria

CI Implementation is accepted when:

- backend CI workflow file is defined;
- workflow triggers are defined;
- PostgreSQL service is defined;
- test environment variables are defined;
- install, Prisma, lint, typecheck, test and build gates are defined;
- required package scripts are defined;
- minimal permissions are defined;
- branch protection readiness is documented;
- failure handling is documented;
- secret safety is documented.

Status:

```text
Accepted for Backend Codebase Milestone
```

---

# 15. Final Statement

```text
Bizzi CI Implementation defines the automated backend quality gate for source code construction.
```

This CI layer ensures that the future executable Bizzi backend can be validated consistently before merge and before deployment automation is introduced.