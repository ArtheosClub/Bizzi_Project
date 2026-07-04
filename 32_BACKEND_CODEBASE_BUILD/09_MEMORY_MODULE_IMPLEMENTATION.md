# 09_MEMORY_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Memory Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Memory module responsible for capturing, activating and maintaining organizational knowledge inside each workspace.

### Module Scope

The Memory module manages memory entries throughout their lifecycle and exposes the active knowledge base used by AI agents and business processes.

### Directory Structure

```text
backend/src/modules/memory/
 ├── memory.module.ts
 ├── memory.controller.ts
 ├── memory.service.ts
 ├── memory-activation.service.ts
 ├── memory.repository.ts
 ├── dto/
 │   ├── create-memory-entry.dto.ts
 │   ├── update-memory-entry.dto.ts
 │   ├── activate-memory-entry.dto.ts
 │   └── memory-entry-response.dto.ts
 ├── mappers/
 │   └── memory.mapper.ts
 └── policies/
     └── memory-status.policy.ts
```

### API Routes

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
PATCH /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/archive
```

### Responsibilities

- Create workspace-scoped memory entries.
- Store structured business knowledge.
- Validate lifecycle transitions.
- Activate approved knowledge.
- Archive obsolete entries.
- Emit audit events for all meaningful changes.
- Enforce workspace authorization.

### Lifecycle

```text
candidate → active → archived
```

### Repository Methods

```text
createMemoryEntry()
findByIdAndWorkspace()
listByWorkspace()
listActiveByWorkspace()
updateMemoryEntry()
activateMemoryEntry()
archiveMemoryEntry()
```

### Service Methods

```text
createMemoryEntry(context, workspaceId, dto)
listMemoryEntries(context, workspaceId, query)
getMemoryEntry(context, workspaceId, memoryEntryId)
updateMemoryEntry(context, workspaceId, memoryEntryId, dto)
activateMemoryEntry(context, workspaceId, memoryEntryId)
archiveMemoryEntry(context, workspaceId, memoryEntryId)
```

### Validation Rules

- Title and content are required.
- Entry type must use canonical values.
- Only candidate entries may be activated.
- Archived entries are immutable.
- Workspace ownership is mandatory.

### Audit Events

```text
memory.created
memory.updated
memory.activated
memory.archived
```

### Acceptance Criteria

- Memory entries are workspace-scoped.
- Active memory is queryable separately.
- Activation is transactional with audit evidence.
- Cross-workspace access is rejected.
- Unit, integration and e2e tests verify lifecycle behavior.

### Outcome

The Memory module provides the canonical organizational knowledge layer that powers AI agents, dashboards and future enterprise reasoning capabilities.