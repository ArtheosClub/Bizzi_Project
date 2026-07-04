# 14_CI_IMPLEMENTATION.md

# Bizzi Platform

## CI Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the GitHub Actions continuous integration workflow for the Bizzi backend.

### Scope

The CI implementation validates that the backend can be installed, checked, tested and built automatically on every relevant change.

### Target Workflow File

```text
.github/workflows/backend-ci.yml
```

### Trigger Strategy

```text
pull_request
push to main
changes under backend/**
changes to workflow files
changes to lockfile
```

### CI Runtime

- Ubuntu runner
- Node.js LTS
- pnpm
- PostgreSQL service
- Prisma CLI
- Jest
- Supertest

### Workflow Jobs

```text
checkout
setup node
setup pnpm
install dependencies
validate Prisma schema
generate Prisma client
run migrations against test database
run lint
run typecheck
run unit tests
run integration tests
run e2e tests
run build
```

### Environment Variables

```text
NODE_ENV=test
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_test
DEV_AUTH_MODE=true
JWT_SECRET=ci-test-only
```

### PostgreSQL Service

CI must provide a disposable PostgreSQL database for migrations and tests.

```text
POSTGRES_USER=bizzi
POSTGRES_PASSWORD=bizzi
POSTGRES_DB=bizzi_test
```

### Required Commands

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

### Security Rules

- CI must not use production secrets.
- CI must use disposable test database.
- Workflow permissions should be read-only where possible.
- Secrets are reserved for future deployment workflows.

### Acceptance Criteria

- Workflow runs on pull requests.
- Workflow runs on main branch pushes.
- Dependencies install from lockfile.
- Prisma validates and migrates.
- Tests pass against test database.
- Build succeeds.
- Failed checks block merge once branch protection is enabled.

### Outcome

The CI implementation establishes an automated quality gate for Bizzi backend development and prepares the repository for reliable AI-assisted and human code contributions.