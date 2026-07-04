# 09_CREATE_DECISION_SOURCE.md

# Bizzi Platform

## Create Decision Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Task  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

# 1. Purpose

This document defines the source-code implementation task for the Bizzi Decision module.

It translates the decision implementation specification into concrete backend source files that should be created under `backend/src/modules/decision`.

---

# 2. Source Files To Create

Target files:

```text
backend/src/modules/decision/decision.module.ts
backend/src/modules/decision/decision.controller.ts
backend/src/modules/decision/decision.service.ts
backend/src/modules/decision/decision-confirmation.service.ts
backend/src/modules/decision/decision.repository.ts
backend/src/modules/decision/dto/create-decision.dto.ts
backend/src/modules/decision/dto/update-decision.dto.ts
backend/src/modules/decision/dto/confirm-decision.dto.ts
backend/src/modules/decision/dto/decision-query.dto.ts
backend/src/modules/decision/dto/decision-response.dto.ts
backend/src/modules/decision/mappers/decision.mapper.ts
backend/src/modules/decision/policies/decision-status.policy.ts
backend/src/modules/decision/__tests__/decision.service.spec.ts
backend/src/modules/decision/__tests__/decision.repository.spec.ts
backend/test/e2e/decision.e2e-spec.ts
```

---

# 3. Module Responsibilities

The Decision module must:

```text
create workspace-scoped decisions
list decisions by workspace
read decision detail by workspace
update draft decisions
confirm decisions
archive decisions
validate lifecycle transitions
reject cross-workspace task references
record audit events transactionally
return canonical DTOs
```

---

# 4. API Routes

Required routes:

```text
POST /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
PATCH /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/archive
```

---

# 5. DTOs

## CreateDecisionDto

Fields:

```text
title required
description optional
decision_type optional
task_id optional
source_object_type optional
source_object_id optional
metadata optional
```

## ConfirmDecisionDto

Fields:

```text
confirmation_note optional
metadata optional
```

## DecisionResponseDto

Fields:

```text
id
workspace_id
task_id
owner_user_id
title
description
decision_type
status
confirmed_by
confirmed_at
source_object_type
source_object_id
metadata
created_at
updated_at
archived_at
```

---

# 6. Repository Contract

`DecisionRepository` must implement:

```text
create(db, data)
findByIdAndWorkspace(db, decisionId, workspaceId)
listByWorkspace(db, workspaceId, filters, pagination)
updateByIdAndWorkspace(db, decisionId, workspaceId, patch)
confirmByIdAndWorkspace(db, decisionId, workspaceId, patch)
archiveByIdAndWorkspace(db, decisionId, workspaceId, patch)
```

Repository rules:

```text
all queries must include workspace_id
repositories return persistence records
repositories do not return API DTOs
repositories accept transaction client
```

---

# 7. Service Contract

`DecisionService` must implement:

```text
createDecision(context, workspaceId, input)
listDecisions(context, workspaceId, query)
getDecision(context, workspaceId, decisionId)
updateDecision(context, workspaceId, decisionId, input)
archiveDecision(context, workspaceId, decisionId)
```

`DecisionConfirmationService` must implement:

```text
confirmDecision(context, workspaceId, decisionId, input)
```

---

# 8. Validation Rules

Required validation:

```text
workspace_id must be valid
decision_id must be valid
title is required for create
task_id must belong to same workspace when provided
only draft decisions can be confirmed
archived decisions cannot be mutated
confirmed decisions cannot be confirmed again
```

---

# 9. Authorization Rules

The module must call:

```text
AuthorizationService.requireWorkspaceOwner(context, workspaceId)
AuthorizationService.requireWorkspaceMutation(context, workspaceId)
```

Rules:

```text
read routes require workspace owner in MVP
mutation routes require active workspace
controllers do not replace service-level authorization
```

---

# 10. Audit Events

Required audit actions:

```text
decision.created
decision.updated
decision.confirmed
decision.archived
```

Audit rules:

```text
audit writes happen inside the same transaction as mutation
audit event includes actor context
audit event includes correlation_id
audit before_state and after_state are sanitized
mutation rolls back if required audit write fails
```

---

# 11. Lifecycle Policy

Allowed transitions:

```text
draft → confirmed
draft → archived
confirmed → archived
```

Forbidden transitions:

```text
confirmed → draft
archived → confirmed
confirmed → confirmed
archived → draft
```

---

# 12. Tests Required

Unit and integration tests must prove:

```text
create decision succeeds
create decision rejects missing title
create decision rejects cross-workspace task_id
list decisions is workspace-scoped
get decision rejects cross-workspace access
confirm decision succeeds from draft
confirm decision rejects already confirmed decision
confirm decision rejects archived decision
archive decision succeeds
mutation records audit events
```

E2E tests must cover:

```text
POST /decisions
GET /decisions
GET /decisions/{decision_id}
POST /decisions/{decision_id}/confirm
non-owner rejection
canonical validation error response
```

---

# 13. Acceptance Criteria

Decision source implementation is accepted when:

- all target source files are created;
- routes compile and are registered;
- repository methods are workspace-scoped;
- service methods enforce authorization and validation;
- decision confirmation lifecycle works;
- audit events are emitted transactionally;
- DTO mapping is explicit;
- unit, integration and e2e tests are defined;
- module integrates into `AppModule`.

---

# 14. Final Statement

```text
Bizzi Decision Source implementation creates the backend source code required to manage official business decisions, confirmation lifecycle and auditable decision evidence inside a workspace.
```