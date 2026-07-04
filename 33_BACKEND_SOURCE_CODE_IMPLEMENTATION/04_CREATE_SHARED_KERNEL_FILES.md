# 04_CREATE_SHARED_KERNEL_FILES.md

# Bizzi Platform

## Create Shared Kernel Files

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Reference:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION/03_CREATE_PRISMA_SCHEMA_FILE.md  
**Upstream Specification:** 32_BACKEND_CODEBASE_BUILD/03_SHARED_KERNEL_IMPLEMENTATION.md  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the source-code creation plan for the Bizzi backend Shared Kernel files.

The Shared Kernel provides the common primitives required by all backend modules before feature implementation begins.

Core question:

```text
Which concrete shared files must be created so all Bizzi backend modules can use consistent context, errors, DTOs, pagination, validation, constants and utilities?
```

---

# 2. Source Directory Target

Target directory:

```text
backend/src/shared/
```

Target structure:

```text
backend/src/shared/
├── context/
├── errors/
├── dto/
├── pagination/
├── constants/
├── validation/
├── transaction/
├── logging/
├── config/
└── utils/
```

---

# 3. Context Files

Create:

```text
backend/src/shared/context/actor-context.ts
backend/src/shared/context/request-context.ts
backend/src/shared/context/service-context.ts
backend/src/shared/context/workspace-context.ts
backend/src/shared/context/correlation-context.ts
```

Responsibilities:

```text
represent authenticated actor
carry request_id
carry correlation_id
carry workspace_id
convert request context into service-safe context
```

Acceptance:

```text
services can receive ServiceContext without depending on HTTP request objects
```

---

# 4. Error Files

Create:

```text
backend/src/shared/errors/error-codes.ts
backend/src/shared/errors/service-error.ts
backend/src/shared/errors/error-details.ts
backend/src/shared/errors/error-mapper.ts
backend/src/shared/errors/http-error.filter.ts
```

Required canonical codes:

```text
unauthenticated
forbidden
not_found
workspace_archived
validation_error
invalid_object_reference
invalid_status_transition
business_rule_violation
conflict
internal_error
```

Acceptance:

```text
all service errors map to canonical API error responses
```

---

# 5. DTO Files

Create:

```text
backend/src/shared/dto/base-response.dto.ts
backend/src/shared/dto/error-response.dto.ts
backend/src/shared/dto/paginated-response.dto.ts
backend/src/shared/dto/pagination-query.dto.ts
```

Responsibilities:

```text
standardize response metadata
standardize error response shape
standardize pagination response shape
```

---

# 6. Pagination Files

Create:

```text
backend/src/shared/pagination/pagination.types.ts
backend/src/shared/pagination/pagination.constants.ts
backend/src/shared/pagination/pagination.utils.ts
```

Required behavior:

```text
normalize page
normalize page_size
enforce max_page_size
calculate offset
build paginated response
```

---

# 7. Constant Files

Create:

```text
backend/src/shared/constants/object-types.ts
backend/src/shared/constants/actor-types.ts
backend/src/shared/constants/audit-actions.ts
backend/src/shared/constants/runtime-events.ts
backend/src/shared/constants/http.constants.ts
```

Rules:

```text
feature modules must import constants instead of hardcoding canonical strings
```

---

# 8. Validation Files

Create:

```text
backend/src/shared/validation/validation-result.ts
backend/src/shared/validation/assertions.ts
backend/src/shared/validation/uuid.validator.ts
backend/src/shared/validation/date-range.validator.ts
```

Purpose:

```text
provide reusable validation primitives before module-level validators are implemented
```

---

# 9. Transaction Files

Create:

```text
backend/src/shared/transaction/transaction-manager.ts
backend/src/shared/transaction/transaction-context.ts
```

Responsibilities:

```text
wrap state mutations
pass transaction client to repositories
allow audit writes inside the same transaction as business mutations
```

---

# 10. Logging Files

Create:

```text
backend/src/shared/logging/logger.ts
backend/src/shared/logging/request-logger.middleware.ts
```

Rules:

```text
logs must include request_id and correlation_id when available
logs must not include secrets
```

---

# 11. Config Files

Create:

```text
backend/src/shared/config/configuration.ts
backend/src/shared/config/env.validation.ts
backend/src/shared/config/config.module.ts
```

Required configuration groups:

```text
app
server
database
auth
dev_auth
logging
```

---

# 12. Utility Files

Create:

```text
backend/src/shared/utils/assert-never.ts
backend/src/shared/utils/sanitize-payload.ts
backend/src/shared/utils/date.util.ts
backend/src/shared/utils/string.util.ts
```

Security rule:

```text
sanitizePayload must remove passwords, tokens, API keys, secrets and credentials before audit or log storage
```

---

# 13. Index Exports

Create barrel exports where useful:

```text
backend/src/shared/context/index.ts
backend/src/shared/errors/index.ts
backend/src/shared/dto/index.ts
backend/src/shared/pagination/index.ts
backend/src/shared/constants/index.ts
backend/src/shared/utils/index.ts
backend/src/shared/index.ts
```

Rule:

```text
avoid circular dependencies between shared subfolders
```

---

# 14. Implementation Order

Recommended order:

```text
1. context files
2. constants
3. error codes and ServiceError
4. error mapper and filter
5. DTOs
6. pagination utilities
7. validation helpers
8. transaction manager
9. sanitizer and utilities
10. logger/config files
11. index exports
12. unit tests
```

---

# 15. Tests To Create

Create tests:

```text
backend/src/shared/errors/error-mapper.spec.ts
backend/src/shared/pagination/pagination.utils.spec.ts
backend/src/shared/utils/sanitize-payload.spec.ts
backend/src/shared/context/workspace-context.spec.ts
backend/src/shared/validation/assertions.spec.ts
```

Required assertions:

```text
canonical errors map correctly
pagination defaults work
max page size is enforced
workspace id is required for scoped operations
secret payload fields are sanitized
```

---

# 16. Acceptance Criteria

Shared Kernel source files are accepted when:

- all required shared directories exist;
- context files are implemented;
- canonical errors are implemented;
- error mapper and filter are implemented;
- DTO files are implemented;
- pagination utilities are implemented;
- constants are implemented;
- validation helpers are implemented;
- transaction manager is defined;
- sanitizer utility is implemented;
- logging/config foundations are defined;
- tests are defined;
- shared code compiles independently;
- no feature-specific business logic exists in the Shared Kernel.

---

# 17. Final Statement

```text
Bizzi Shared Kernel source implementation creates the reusable backend foundation required before Identity, Workspace, Authorization, Task, Decision, Memory, Audit and Dashboard source files are generated.
```

This step prepares the backend codebase for consistent, safe and workspace-scoped module implementation.