# 15_CREATE_CI_AND_DOCKER_FILES.md

# Bizzi Platform

## Create CI and Docker Files

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Task  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the implementation task for creating CI and Docker files required to build, test and run the Bizzi backend in a repeatable local and GitHub Actions environment.

Core question:

```text
Which concrete CI and Docker files must exist so Bizzi backend can be installed, tested, built and run consistently?
```

---

# 2. Target Files

Required files:

```text
.github/workflows/backend-ci.yml
Dockerfile
docker-compose.yml
backend/Dockerfile
backend/.dockerignore
backend/.env.example
backend/scripts/wait-for-db.sh
```

Optional later files:

```text
.github/workflows/backend-release.yml
.github/dependabot.yml
backend/docker-compose.test.yml
```

---

# 3. Docker Compose Scope

`docker-compose.yml` should define local services:

```text
postgres_dev
postgres_test
backend optional
```

Required ports:

```text
postgres_dev → 5432
postgres_test → 5433
backend → 3000
```

Rules:

```text
dev and test databases must be separate
no production secrets in compose files
volumes may be used for local database persistence
```

---

# 4. Backend Dockerfile Scope

`backend/Dockerfile` should support:

```text
install dependencies
copy source
run prisma generate
build backend
start backend
```

Recommended approach:

```text
multi-stage build
non-root runtime user where practical
NODE_ENV controlled by environment
```

---

# 5. Environment Example

`backend/.env.example` should include:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
JWT_SECRET=local-dev-only-change-later
```

Test database example:

```text
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5433/bizzi_test
```

---

# 6. GitHub Actions Workflow

`backend-ci.yml` should run:

```text
checkout
setup pnpm
setup Node.js
install dependencies
start PostgreSQL service
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

Rules:

```text
CI must use disposable test database
CI must not require production credentials
CI must fail on test, typecheck or build failure
```

---

# 7. Acceptance Criteria

This implementation task is accepted when:

- backend CI workflow file is defined;
- Docker Compose local database services are defined;
- backend Dockerfile is defined;
- `.dockerignore` is defined;
- `.env.example` is defined;
- test and dev database separation is documented;
- CI quality gates are documented;
- no production secrets are required.

---

# 8. Final Statement

```text
Bizzi CI and Docker file creation establishes the repeatable execution envelope for local development, automated testing and backend build verification.
```
