# 08_DECISION_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Decision Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Decision module, responsible for capturing, validating and confirming business decisions within a workspace.

### Module Scope

The Decision module records structured business decisions, links them to tasks when needed and preserves confirmation evidence through audit events.

### Directory Structure

```text
backend/src/modules/decision/
 ├── decision.module.ts
 ├── decision.controller.ts
 ├── decision.service.ts
 ├── decision-confirmation.service.ts
 ├── decision.repository.ts
 ├── dto/
 │   ├── create-decision.dto.ts
 │   ├── update-decision.dto.ts
 │   ├── confirm-decision.dto.ts
 │   └── decision-response.dto.ts
 ├── mappers/
 │   └── decision.mapper.ts
 └── policies/
     └── decision-status.policy.ts
```

### API Routes

```text
POST /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
PATCH /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/archive
```

### Responsibilities

- Create workspace-scoped decisions.
- Link decisions to tasks where applicable.
- Validate decision lifecycle transitions.
- Confirm decisions with actor attribution.
- Preserve decision evidence through audit events.
- Enforce workspace authorization.

### Lifecycle

```text
draft → confirmed → archived
```

### Repository Methods

```text
createDecision()
findByIdAndWorkspace()
listByWorkspace()
updateDecision()
confirmDecision()
archiveDecision()
```

### Service Methods

```text
createDecision(context, workspaceId, dto)
listDecisions(context, workspaceId, query)
getDecision(context, workspaceId, decisionId)
updateDecision(context, workspaceId, decisionId, dto)
confirmDecision(context, workspaceId, decisionId, dto)
archiveDecision(context, workspaceId, decisionId)
```

### Validation Rules

- Decision title is required.
- Decision type must be canonical.
- Task reference must belong to the same workspace.
- Confirmed decisions cannot be confirmed again.
- Archived decisions are immutable.

### Audit Events

```text
decision.created
decision.updated
decision.confirmed
decision.archived
```

### Acceptance Criteria

- Decisions are workspace-scoped.
- Decisions can be created and confirmed.
- Cross-workspace task references are rejected.
- Confirmation records actor and timestamp.
- Audit events are emitted transactionally.
- Unit and e2e tests cover lifecycle behavior.

### Outcome

The Decision module creates the official business decision layer of Bizzi Platform and provides the evidence trail needed for AI-assisted enterprise governance.