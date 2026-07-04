# 02_PRISMA_SCHEMA_IMPLEMENTATION.md

# Bizzi Platform

## Prisma Schema Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the implementation of the first production `schema.prisma` for the Bizzi backend.

### Objectives

- Create the initial Prisma schema.
- Configure PostgreSQL datasource.
- Define generator configuration.
- Implement canonical entities.
- Preserve workspace isolation.
- Prepare initial migrations.

### Initial Models

- User
- CompanyWorkspace
- WorkspaceSettings
- Task
- Decision
- MemoryEntry
- AuditEvent
- RuntimeEvent

### Mandatory Conventions

- UUID primary keys.
- `workspace_id` on every workspace-scoped entity.
- `created_at`, `updated_at` timestamps.
- Soft-delete fields where applicable.
- Foreign keys with explicit relations.
- Canonical enum types.

### Migration Strategy

1. Initial schema.
2. Generate Prisma client.
3. Create first migration.
4. Apply migration to development database.
5. Verify clean deployment.
6. Validate against test database.

### Acceptance Criteria

- `schema.prisma` compiles.
- Prisma client is generated.
- Initial migration succeeds.
- Database schema matches Layer 27.
- Workspace isolation constraints are preserved.

### Outcome

This document defines the first executable persistence layer for the Bizzi backend and becomes the basis for all repositories and services.