# 11_CI_WORKFLOW_EXECUTION.md

# Bizzi Platform

## CI Workflow Execution

**Layer:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Component Type:** Execution Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Previous Document:** 10_TEST_SUITE_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the CI workflow execution plan for Bizzi Platform backend MVP.

It specifies how to implement the first GitHub Actions workflow that verifies install, TypeScript, lint, Prisma schema, migrations, tests and build for the backend.

Core question:

```text
How should Bizzi automate backend quality gates so every change is checked before it becomes part of main?
```

---

# 2. CI Workflow Thesis

```text
Bizzi CI starts as an automated quality gate before it becomes a deployment pipeline.
```

The first CI workflow must prove:

```text
repository can install dependencies
backend can typecheck
backend can lint
Prisma schema validates
migrations apply to a clean test database
unit tests pass
integration tests pass
API/e2e tests pass
backend builds
no production secrets are required
```

---

# 3. Target Files

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
```

---

# 4. Execution Non-Scope

This step does not implement:

```text
production deployment
staging deployment
Docker image publishing
release tagging
blue-green deployment
infrastructure provisioning
cloud secret manager integration
```

These belong to later delivery layers.

---

# 5. Workflow Name

Recommended workflow name:

```text
Backend CI
```

Recommended file:

```text
.github/workflows/backend-ci.yml
```

Rule:

```text
Use one reliable backend CI workflow before adding multiple specialized workflows.
```

---

# 6. Trigger Strategy

Initial triggers:

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

Rule:

```text
CI should run on backend changes, workflow changes and dependency lockfile changes.
```

---

# 7. Runtime Environment

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

Rule:

```text
CI environment should match local development workflow as closely as practical.
```

---

# 8. CI Environment Variables

Required CI variables:

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

Rules:

```text
CI must not require production credentials
CI must not print secrets
CI must use disposable test database
```

---

# 9. PostgreSQL Service

GitHub Actions service:

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
CI should wait for PostgreSQL health before running migrations or tests.
```

---

# 10. Job Stages

Required stages:

```text
checkout repository
setup pnpm
setup Node.js
install dependencies with frozen lockfile
validate Prisma schema
generate Prisma client
apply migrations to clean database
run lint
run typecheck
run unit tests
run integration tests
run e2e tests
run build
```

Rule:

```text
Any failed stage should fail the workflow.
```

---

# 11. Install Gate

Command:

```bash
pnpm install --frozen-lockfile
```

Purpose:

```text
prove lockfile consistency and reproducible install
```

Rule:

```text
CI must not mutate dependency lockfiles.
```

---

# 12. Prisma Gate

Commands:

```bash
cd backend
pnpm prisma validate
pnpm prisma generate
pnpm prisma migrate deploy
```

Purpose:

```text
prove schema validity and migration deployability on clean database
```

Rule:

```text
A migration that cannot apply from a clean database blocks merge.
```

---

# 13. Static Quality Gates

Commands:

```bash
cd backend
pnpm lint
pnpm typecheck
```

Purpose:

```text
prevent style, correctness and typing regressions
```

Rule:

```text
Type errors must block merge.
```

---

# 14. Test Gates

Commands:

```bash
cd backend
pnpm test:unit
pnpm test:integration
pnpm test:e2e
```

Optional combined command:

```bash
cd backend
pnpm test
```

Rule:

```text
CI must run tests that prove workspace isolation, authorization, validation, transactions and audit evidence.
```

---

# 15. Build Gate

Command:

```bash
cd backend
pnpm build
```

Purpose:

```text
prove backend compiles into deployable artifact
```

Rule:

```text
Build failure blocks merge.
```

---

# 16. Recommended Workflow Skeleton

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
      JWT_SECRET: ci-test-only

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

Rule:

```text
The skeleton must be adapted to actual package scripts once backend scaffold exists.
```

---

# 17. Workflow Permissions

Recommended minimal permissions:

```yaml
permissions:
  contents: read
```

Rule:

```text
CI quality checks should not need write permissions.
```

---

# 18. Artifacts

Optional artifacts:

```text
coverage report
JUnit test report
build output
migration report
```

MVP rule:

```text
Do not add artifact complexity until test and build gates are stable.
```

---

# 19. Branch Protection Readiness

After CI is stable, main should require:

```text
Backend CI success
pull request before merge
no force pushes
conversation resolution optional
linear history optional
```

Rule:

```text
Do not enable strict branch protection until CI is reliable enough not to block normal work unnecessarily.
```

---

# 20. Failure Handling

Common failures:

```text
lockfile mismatch
PostgreSQL not ready
DATABASE_URL wrong
Prisma client not generated
migration failure
lint errors
type errors
flaky tests
missing package scripts
```

Expected response:

```text
fix root cause
add missing script or test setup
avoid disabling CI checks to bypass failure
```

---

# 21. Secret Safety

Rules:

```text
no production credentials in workflow YAML
no raw tokens in logs
use test-only local values
avoid write permissions unless needed
GitHub secrets only for future deployment stages
```

---

# 22. Execution Order

Recommended order:

```text
1. Confirm backend scripts exist
2. Confirm test database config exists
3. Create backend-ci.yml
4. Add PostgreSQL service
5. Add install gate
6. Add Prisma gate
7. Add lint and typecheck gates
8. Add test gates
9. Add build gate
10. Run workflow on pull request
11. Stabilize failures
12. Enable branch protection later
```

---

# 23. Verification Checklist

CI Workflow Execution is complete when:

```text
[ ] backend-ci.yml exists
[ ] workflow triggers on PR and main push
[ ] PostgreSQL service starts
[ ] dependencies install with frozen lockfile
[ ] Prisma schema validates
[ ] Prisma client generates
[ ] migrations apply to clean database
[ ] lint passes
[ ] typecheck passes
[ ] unit tests pass
[ ] integration tests pass
[ ] e2e tests pass
[ ] build passes
[ ] no production secrets required
[ ] workflow permissions are minimal
```

---

# 24. Risks and Controls

## Risk 1 — CI Checks Too Weak

Mitigation:

```text
Include migration, test and build gates, not only lint.
```

## Risk 2 — CI Uses Production Secrets

Mitigation:

```text
Use disposable test database and test-only environment values.
```

## Risk 3 — Flaky Test Suite

Mitigation:

```text
Stabilize test database reset and avoid hidden state.
```

## Risk 4 — Branch Protection Too Early

Mitigation:

```text
Enable branch protection only after workflow is stable.
```

---

# 25. Acceptance Criteria

CI Workflow Execution is accepted when:

- target workflow file is defined;
- execution non-scope is documented;
- workflow name and triggers are defined;
- runtime environment is defined;
- CI variables are defined;
- PostgreSQL service is defined;
- job stages are documented;
- install, Prisma, static quality, test and build gates are defined;
- workflow skeleton is provided;
- permissions are documented;
- artifact strategy is defined;
- branch protection readiness is defined;
- failure handling is documented;
- secret safety rules are defined;
- execution order is documented;
- verification checklist is provided;
- risks and controls are documented.

Status:

```text
Accepted for Local Runbook
```

---

# 26. Final Statement

```text
Bizzi CI Workflow Execution defines the first automated quality gate for backend implementation.
```

This workflow ensures every backend change can be installed, migrated, typed, tested and built before Bizzi proceeds toward controlled delivery.