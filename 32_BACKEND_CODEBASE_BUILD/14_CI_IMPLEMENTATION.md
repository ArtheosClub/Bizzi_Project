# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of continuous integration for the Bizzi backend codebase.

### Scope

The CI implementation covers:

- dependency installation
- TypeScript validation
- linting
- Prisma schema validation
- Prisma client generation
- test database startup
- migrations
- unit tests
- integration tests
- e2e tests
- production build verification

### Target Workflow File

```text
.github/workflows/backend-ci.yml
```

### CI Runtime

```text
GitHub Actions
Ubuntu latest
Node.js LTS
pnpm
PostgreSQL service container
```

### Workflow Triggers

```text
pull_request
push to main
manual workflow_dispatch
```

### Required Job

```text
backend-ci
```

### Backend CI Steps

```text
checkout repository
setup Node.js
setup pnpm
install dependencies
start PostgreSQL service
validate Prisma schema
generate Prisma client
run migrations
run lint
run typecheck
run unit tests
run integration tests
run e2e tests
run build
```

### CI Environment

The CI environment must use test-only configuration values.

Required variables:

```text
NODE_ENV=test
DATABASE_URL points to disposable PostgreSQL test database
DEV_AUTH_MODE=true
JWT secret value must be test-only and never production
```

### PostgreSQL Service

```text
PostgreSQL version: 16
Database role: bizzi
Database name: bizzi_test
```

### Quality Gates

CI must fail if any of the following fail:

```text
install
lint
typecheck
Prisma validation
migration execution
unit tests
integration tests
e2e tests
build
```

### Security Rules

- No production secrets in CI.
- CI uses test-only credentials.
- Workflow permissions are minimal.
- Logs must not expose secrets.

### Acceptance Criteria

- CI workflow exists.
- CI runs on pull requests.
- CI runs on main branch pushes.
- PostgreSQL test database starts.
- Migrations run successfully.
- All tests pass.
- Backend build passes.
- Failed tests block merge.

### Outcome

The CI Implementation makes Bizzi backend changes verifiable, repeatable and protected by automated quality gates before merge.