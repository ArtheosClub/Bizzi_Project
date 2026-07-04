# 13_CREATE_API_BOOTSTRAP_SOURCE.md

# Bizzi Platform

## Create API Bootstrap Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the source-code implementation task for creating the Bizzi backend API bootstrap.

The API bootstrap is the runtime entry point that starts the NestJS application, wires global middleware, configures validation, exception handling, OpenAPI documentation, CORS, logging, request context and graceful shutdown.

Core question:

```text
Which actual backend source files must be created so the Bizzi API can start, validate requests, expose documentation and provide a stable runtime foundation for all modules?
```

---

# 2. Source Files To Create

Required files:

```text
backend/src/main.ts
backend/src/app.module.ts
backend/src/health/health.module.ts
backend/src/health/health.controller.ts
backend/src/config/app-config.module.ts
backend/src/config/app-config.service.ts
backend/src/shared/filters/http-exception.filter.ts
backend/src/shared/interceptors/request-logging.interceptor.ts
backend/src/shared/middleware/request-context.middleware.ts
backend/src/shared/context/request-context.ts
backend/src/shared/context/correlation-id.ts
```

Optional later files:

```text
backend/src/openapi/openapi.config.ts
backend/src/shared/pipes/validation.pipe.ts
backend/src/shared/filters/domain-exception.filter.ts
backend/src/shared/interceptors/response-shape.interceptor.ts
```

---

# 3. `main.ts` Responsibilities

`main.ts` must:

```text
create NestJS application
load configuration
register global validation pipe
register global exception filter
register global interceptors
configure CORS
configure OpenAPI docs
start HTTP server
enable shutdown hooks
```

Recommended implementation behavior:

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api/v1', {
    exclude: ['health'],
  });

  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  app.useGlobalFilters(new HttpExceptionFilter());
  app.enableCors();
  app.enableShutdownHooks();

  setupOpenApi(app);

  const port = process.env.PORT || 3000;
  await app.listen(port);
}

bootstrap();
```

---

# 4. `AppModule` Responsibilities

`AppModule` must import foundational modules first.

Initial module imports:

```text
AppConfigModule
HealthModule
PrismaModule later
IdentityModule later
WorkspaceModule later
AuthorizationModule later
AuditModule later
TaskModule later
DecisionModule later
MemoryModule later
DashboardModule later
```

Rule:

```text
AppModule should wire modules; it must not contain business logic.
```

---

# 5. Health Endpoint

Health route:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "service": "bizzi-backend"
}
```

Purpose:

```text
local smoke test
CI smoke test
container readiness later
simple runtime verification
```

---

# 6. Configuration Source

`AppConfigService` should expose:

```text
NODE_ENV
PORT
DATABASE_URL
DEV_AUTH_MODE
JWT_SECRET
CORS_ORIGIN
LOG_LEVEL
```

Rules:

```text
configuration is read from environment
missing required configuration fails early
production must not use development defaults
secrets must not be logged
```

---

# 7. Request Context Middleware

The request context middleware must create or preserve:

```text
request_id
correlation_id
started_at
```

Headers:

```text
x-request-id
x-correlation-id
```

Rules:

```text
preserve incoming correlation_id when present
generate correlation_id when absent
attach request_id and correlation_id to request object
make correlation_id available to logs, audit and runtime events
```

---

# 8. Global Validation

Global validation must enforce:

```text
whitelist true
forbidNonWhitelisted true
transform true
```

Purpose:

```text
reject unknown fields
normalize DTO values
protect API contracts
support typed controller inputs
```

---

# 9. Exception Handling

The HTTP exception filter must map errors to canonical response shape:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request",
    "details": []
  },
  "request_id": "req_...",
  "correlation_id": "corr_..."
}
```

Rules:

```text
raw stack traces must not leak
Prisma errors must not leak
unknown errors become internal_error
request_id and correlation_id should be included when available
```

---

# 10. OpenAPI Setup

OpenAPI must be exposed at:

```text
/api/docs
```

Recommended title:

```text
Bizzi Platform API
```

Recommended version:

```text
v1
```

Rules:

```text
OpenAPI must reflect /api/v1 route prefix
health route remains outside /api/v1
schemas should be generated from DTOs later
```

---

# 11. CORS

MVP CORS behavior:

```text
allow localhost frontend origin
allow configured CORS_ORIGIN
avoid wildcard in production
```

Rules:

```text
production CORS must be explicit
credentials support must be intentional
```

---

# 12. Logging

Request logging should include:

```text
method
path
status_code
duration_ms
request_id
correlation_id
```

Rules:

```text
never log secrets
never log raw authorization headers
never log full sensitive payloads
```

---

# 13. Graceful Shutdown

Bootstrap must enable shutdown hooks.

Future shutdown responsibilities:

```text
close Prisma connection
flush logs
stop background workers
close queue connections
```

MVP requirement:

```text
app.enableShutdownHooks()
```

---

# 14. Verification Commands

Expected local checks:

```bash
cd backend
pnpm dev
curl http://localhost:3000/health
curl http://localhost:3000/api/docs
pnpm typecheck
pnpm test
pnpm build
```

Expected health response:

```json
{
  "status": "ok",
  "service": "bizzi-backend"
}
```

---

# 15. Acceptance Criteria

API Bootstrap Source is accepted when:

- `main.ts` is created;
- `AppModule` is created;
- health module and controller are created;
- configuration module and service are created;
- global validation is enabled;
- global exception filter is wired;
- request context middleware is defined;
- correlation ID handling is defined;
- OpenAPI docs are available;
- CORS is configured safely;
- graceful shutdown hooks are enabled;
- local verification commands are documented;
- no business logic is placed in bootstrap files.

---

# 16. Final Statement

```text
The API Bootstrap Source creates the runtime entry point for Bizzi backend source code.
```

This implementation step makes the backend startable, observable, validated and ready for module wiring.