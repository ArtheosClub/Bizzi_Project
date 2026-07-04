# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD  
**Component Type:** Codebase Build Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Previous Document:** 13_TEST_IMPLEMENTATION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

# 1. Purpose

This document defines the concrete continuous integration implementation for the Bizzi backend codebase.

It specifies the GitHub Actions workflow files, runtime services, quality gates, commands, environment variables and merge-readiness checks required before backend changes are accepted.

---

# 2. Target Workflow Files

```text
.github/workflows/backend-ci.yml
.github/workflows/backend-pr-check.yml optional later
```

MVP rule:

```text
Start with one reliable backend-ci.yml before adding specialized workflows.
```

---

# 3. CI Responsibilities

The backend CI workflow must verify:

```text
dependency installation
TypeScript type safety
lint quality
Prisma schema validity
Prisma client generation
migration deployability on clean PostgreSQL
unit tests
integration tests
e2e tests
backend build
```

---

# 4. Trigger Strategy

Recommended triggers:

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'
```

---

# 5. Runtime Environment

```text
runner: ubuntu-latest
node: Node.js LTS
package manager: pnpm
database: PostgreSQL 16
```

---

# 6. Environment Variables

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-secret
```

Rules:

```text
CI must not require production secrets.
CI must use disposable test infrastructure.
CI must not print sensitive values.
```

---

# 7. PostgreSQL Service

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

# 8. Pipeline Steps

```text
checkout repository
setup pnpm
setup Node.js
install dependencies with frozen lockfile
validate Prisma schema
generate Prisma client
apply migrations
run lint
run typecheck
run unit tests
run integration tests
run e2e tests
run build
```

---

# 9. Required Commands

```bash
pnpm install --frozen-lockfile
cd backend && pnpm prisma validate
cd backend && pnpm prisma generate
cd backend && pnpm prisma migrate deploy
cd backend && pnpm lint
cd backend && pnpm typecheck
cd backend && pnpm test:unit
cd backend && pnpm test:integration
cd backend && pnpm test:e2e
cd backend && pnpm build
```

---

# 10. Workflow Skeleton

```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'

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
      JWT_SECRET: ci-test-secret

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Validate Prisma schema
        run: cd backend && pnpm prisma validate

      - name: Generate Prisma client
        run: cd backend && pnpm prisma generate

      - name: Apply migrations
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

# 11. Quality Gates

The workflow must fail on:

```text
lockfile mismatch
install failure
Prisma validation failure
migration failure
lint failure
typecheck failure
unit test failure
integration test failure
e2e test failure
build failure
```

---

# 12. Branch Protection Readiness

After CI stabilizes, `main` should require:

```text
Backend CI success
pull request before merge
no direct force push
review approval optional for early stage
```

---

# 13. Acceptance Criteria

CI Implementation is accepted when:

- backend CI workflow target file is defined;
- trigger strategy is defined;
- PostgreSQL service is defined;
- environment variables are defined;
- install, Prisma, lint, typecheck, test and build gates are defined;
- workflow skeleton is documented;
- quality gates are documented;
- branch protection readiness is documented;
- no production secrets are required.

Status:

```text
Accepted for Backend Codebase Milestone
```

---

# 14. Final Statement

```text
Bizzi CI Implementation defines the automated quality gate for backend source-code evolution.
```

This workflow protects the backend codebase from regressions and prepares the project for controlled AI-assisted development.