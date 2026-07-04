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

# 2. CI Thesis

```text
CI is the automated guardian of Bizzi backend integrity.
```

Every backend change must prove:

```text
installability
type safety
lint safety
schema validity
migration validity
test correctness
build correctness
no production secret dependency
```

---

# 3. Target Workflow File

Primary file:

```text
.github/workflows/backend-ci.yml
```

Supporting files:

```text
backend/package.json
backend/prisma/schema.prisma
backend/jest.config.ts
backend/.env.example
backend/test/setup/test-database.ts
docker-compose.yml
```

---

# 4. Workflow Triggers

The workflow should run on:

```text
pull_request to main
push to main
manual workflow_dispatch
```

Path filters should include:

```text
backend/**
.github/workflows/backend-ci.yml
package.json
pnpm-lock.yaml
docker-compose.yml
```

---

# 5. Runtime Environment

Recommended CI runtime:

```text
ubuntu-latest
Node.js LTS
pnpm
PostgreSQL 16
```

Environment variables:

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
JWT_SECRET=ci-test-only
```

---

# 6. PostgreSQL Service

The workflow must start a disposable PostgreSQL service.

Required service configuration:

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
CI must never connect to development or production databases.
```

---

# 7. Quality Gates

Required gates:

```text
checkout
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

Failure rule:

```text
Any failed gate fails the workflow.
```

---

# 8. Command Sequence

Expected commands:

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

# 9. Required package.json Scripts

Backend package should expose:

```json
{
  "scripts": {
    "dev": "nest start --watch",
    "build": "nest build",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "test:unit": "jest --config jest.unit.config.ts",
    "test:integration": "jest --config jest.integration.config.ts",
    "test:e2e": "jest --config jest.e2e.config.ts",
    "db:test:reset": "tsx test/setup/reset-test-db.ts"
  }
}
```

---

# 10. Workflow Skeleton

```yaml
name: Backend CI

on:
  pull_request:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'
      - 'docker-compose.yml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
      - 'package.json'
      - 'pnpm-lock.yaml'
      - 'docker-compose.yml'
  workflow_dispatch:

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
      DEV_USER_EMAIL: dev@bizzi.local
      DEV_USER_NAME: Bizzi Developer
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

# 11. Secret Safety

CI must not require production secrets.

Rules:

```text
use test-only values
never print secrets
never store real provider credentials in workflow YAML
use GitHub Secrets only for later deployment workflows
keep permissions minimal
```

---

# 12. Branch Protection Readiness

After CI stabilizes, `main` may require:

```text
Backend CI must pass
pull request required before merge
no force pushes
conversation resolution optional
linear history optional
```

Rule:

```text
Do not enable strict branch protection until workflow is stable.
```

---

# 13. Acceptance Criteria

CI Implementation is accepted when:

- backend CI workflow path is defined;
- triggers are defined;
- PostgreSQL test service is defined;
- environment variables are defined;
- quality gates are documented;
- command sequence is documented;
- required package scripts are documented;
- workflow skeleton is provided;
- secret safety rules are defined;
- branch protection readiness is defined.

Status:

```text
Accepted for Backend Codebase Milestone
```

---

# 14. Final Statement

```text
Bizzi CI Implementation defines the automated verification gate for backend codebase construction.
```

This workflow ensures that backend changes can be installed, migrated, typed, tested and built before they are accepted into the main codebase.