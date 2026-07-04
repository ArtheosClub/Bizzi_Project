# 02_CREATE_PACKAGE_AND_CONFIG_FILES.md

# Bizzi Platform

## Create Package and Config Files

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the source-code implementation step for creating the backend package and configuration files required to run the Bizzi backend as a real NestJS application.

Core question:

```text
Which package, TypeScript, NestJS, environment, linting, formatting and runtime configuration files must be created before backend source modules can be implemented?
```

---

# 2. Target Files

This step creates or verifies the following files:

```text
backend/package.json
backend/tsconfig.json
backend/tsconfig.build.json
backend/nest-cli.json
backend/.env.example
backend/.gitignore
backend/.eslintrc.cjs
backend/.prettierrc
backend/jest.config.ts
backend/jest.e2e.config.ts
backend/prisma/schema.prisma placeholder
```

Optional repository-level files:

```text
pnpm-workspace.yaml
package.json
docker-compose.yml
```

---

# 3. package.json Requirements

`backend/package.json` must define:

```text
name
version
private flag
scripts
dependencies
devDependencies
package manager expectation
```

Required scripts:

```text
dev
build
start
lint
typecheck
format
test
test:unit
test:integration
test:e2e
prisma:validate
prisma:generate
prisma:migrate:dev
prisma:migrate:deploy
db:seed
db:test:reset
```

---

# 4. Core Dependencies

Required runtime dependencies:

```text
@nestjs/common
@nestjs/core
@nestjs/platform-express
@nestjs/config
@nestjs/swagger
reflect-metadata
rxjs
@prisma/client
class-validator
class-transformer
uuid
```

Required development dependencies:

```text
typescript
ts-node
tsx
@nestjs/cli
@nestjs/testing
prisma
jest
ts-jest
supertest
eslint
prettier
@types/node
@types/jest
@types/supertest
```

---

# 5. TypeScript Configuration

`tsconfig.json` must support:

```text
strict TypeScript
NestJS decorators
module resolution
source maps
incremental builds
path aliases
```

Required path aliases:

```text
@shared/* → src/shared/*
@modules/* → src/modules/*
@infrastructure/* → src/infrastructure/*
@test/* → test/*
```

---

# 6. Nest CLI Configuration

`nest-cli.json` must define:

```text
sourceRoot: src
entryFile: main
compilerOptions
asset handling if needed later
```

Rule:

```text
Nest CLI config must match the physical backend/src structure.
```

---

# 7. Environment Example

`backend/.env.example` must include safe non-secret defaults:

```text
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://bizzi:bizzi@localhost:5432/bizzi_dev
DEV_AUTH_MODE=true
DEV_USER_EMAIL=dev@bizzi.local
DEV_USER_NAME=Bizzi Developer
JWT_SECRET=local-dev-only-change-later
```

Test values may be documented separately:

```text
TEST_DATABASE_URL=postgresql://bizzi:bizzi@localhost:5433/bizzi_test
```

Rules:

```text
Do not commit real secrets.
.env.example is documentation, not a secret store.
```

---

# 8. Lint and Format Configuration

ESLint must enforce:

```text
TypeScript correctness
no unused variables where practical
consistent imports
safe async patterns later
```

Prettier must enforce:

```text
stable formatting
consistent line width
consistent quotes and trailing commas
```

Rule:

```text
Linting should guide implementation without becoming a blocker before source code exists.
```

---

# 9. Jest Configuration

Jest configs must support:

```text
unit tests
integration tests
e2e tests
TypeScript transpilation
path aliases
test setup files
```

Required test setup path:

```text
test/setup
```

---

# 10. Prisma Placeholder

A minimal `backend/prisma/schema.prisma` placeholder may be created in this step if the full schema is implemented in the next step.

Placeholder must include:

```text
generator client
datasource db
```

Rule:

```text
Do not create incomplete production models unless this step explicitly includes full schema implementation.
```

---

# 11. Acceptance Criteria

This step is accepted when:

- backend package file is defined;
- TypeScript configs are defined;
- Nest CLI config is defined;
- environment example is defined;
- lint and format configs are defined;
- Jest configs are defined;
- Prisma placeholder strategy is defined;
- required scripts are documented;
- dependency groups are documented;
- configuration supports the future source tree.

---

# 12. Final Statement

```text
This step creates the package and configuration foundation required before real Bizzi backend source files can compile, run, test and build.
```
