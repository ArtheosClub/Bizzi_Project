# 12_API_BOOTSTRAP_IMPLEMENTATION.md

# Bizzi Platform

## API Bootstrap Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the implementation of the backend bootstrap responsible for starting the NestJS application, configuring global middleware and exposing the Bizzi API.

### Scope

The bootstrap configures:

- `main.ts`
- `AppModule`
- configuration loading
- logging
- global validation
- exception filters
- request context
- CORS
- OpenAPI
- graceful shutdown

### Entry Files

```text
backend/src/main.ts
backend/src/app.module.ts
backend/src/config/
backend/src/shared/filters/
backend/src/shared/interceptors/
backend/src/shared/middleware/
```

### Bootstrap Pipeline

1. Load environment.
2. Initialize configuration.
3. Initialize logger.
4. Register global ValidationPipe.
5. Register global exception filter.
6. Register request context middleware.
7. Configure CORS.
8. Configure OpenAPI.
9. Start HTTP server.
10. Enable graceful shutdown.

### Global Middleware

- Request ID generation
- Correlation ID propagation
- Request logging
- Actor context initialization

### OpenAPI

Expose documentation at:

```text
/api/docs
```

### Health Endpoint

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```

### Acceptance Criteria

- Application starts successfully.
- Global validation is active.
- OpenAPI documentation is available.
- Health endpoint returns HTTP 200.
- Correlation IDs propagate through requests.
- Graceful shutdown works correctly.

### Outcome

The API bootstrap becomes the runtime entry point for the Bizzi backend and provides a consistent execution environment for all modules.