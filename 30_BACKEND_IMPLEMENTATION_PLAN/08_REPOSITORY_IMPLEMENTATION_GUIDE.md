# 08_REPOSITORY_IMPLEMENTATION_GUIDE.md

# Bizzi Platform

## Repository Implementation Guide

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 07_SERVICE_IMPLEMENTATION_GUIDE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the repository implementation guide for Bizzi Platform backend.

It translates the data model, database migration plan and service implementation guide into practical rules for implementing repositories with Prisma, PostgreSQL, workspace-scoped queries, transactions, pagination, filtering, sorting and safe persistence behavior.

Core question:

```text
How should Bizzi repositories be implemented so that database access remains workspace-scoped, testable, transaction-aware and isolated from business logic?
```

---

# 2. Repository Implementation Thesis

```text
Bizzi repositories are persistence adapters. They should hide Prisma details from services, enforce workspace-aware query patterns, support transaction context and return persistence records without owning business decisions.
```

Repositories protect:

```text
workspace scoping
query consistency
transaction participation
pagination discipline
database abstraction
future ORM replacement option
```

---

# 3. Repository Responsibilities

A repository is responsible for:

```text
creating records
finding records by id and workspace_id
listing records by workspace_id
updating records by id and workspace_id
archiving records by id and workspace_id
executing persistence queries
applying pagination, filtering and sorting
using transaction client when supplied
returning database records to services
```

A repository is not responsible for:

```text
authorization decisions
business lifecycle rules
audit event decisions
runtime event decisions
HTTP response mapping
AI authority validation
cross-module orchestration
```

---

# 4. Canonical Repository Method Shape

Recommended method shape:

```typescript
async findByIdAndWorkspace(
  db: PrismaClientOrTransaction,
  id: string,
  workspaceId: string,
): Promise<TaskRecord | null> {
  return db.task.findFirst({
    where: {
      id,
      workspaceId,
    },
  });
}
```

Rule:

```text
Workspace-scoped repository methods must include workspace_id in the query, not only in service validation.
```

---

# 5. Transaction Client Pattern

Repositories should support both normal Prisma client and transaction client.

Recommended type concept:

```typescript
type DbClient = PrismaClient | Prisma.TransactionClient;
```

Repository method pattern:

```typescript
async create(db: DbClient, data: CreateTaskData): Promise<TaskRecord> {
  return db.task.create({ data });
}
```

Rule:

```text
Services pass transaction client into repositories during mutations.
```

---

# 6. Workspace Scope Pattern

Workspace-scoped entities must use methods like:

```text
findByIdAndWorkspace(id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(id, workspace_id, patch)
archiveByIdAndWorkspace(id, workspace_id, archive_data)
```

Examples of workspace-scoped entities:

```text
tasks
decisions
memory_entries
audit_events
runtime_events
workspace_settings
export_jobs
integrations
functions
responsibilities
```

Rule:

```text
Never implement findById(id) for workspace-scoped records unless it is internal and clearly protected.
```

---

# 7. Create Pattern

Create methods should:

```text
accept prepared data from service
not invent business status unless repository is explicitly responsible for defaults
not perform authorization
not emit audit or runtime events
return created record
```

Example:

```typescript
async createTask(db: DbClient, data: CreateTaskData): Promise<TaskRecord> {
  return db.task.create({ data });
}
```

Rule:

```text
Services decide what to create; repositories persist it.
```

---

# 8. Update Pattern

Update methods should include workspace scope.

Recommended safe approach:

```text
use updateMany with id + workspace_id and verify count
or find first then update by primary key inside transaction
```

Example:

```typescript
async updateByIdAndWorkspace(
  db: DbClient,
  id: string,
  workspaceId: string,
  patch: UpdateTaskData,
): Promise<TaskRecord | null> {
  const existing = await this.findByIdAndWorkspace(db, id, workspaceId);
  if (!existing) return null;

  return db.task.update({
    where: { id },
    data: patch,
  });
}
```

Rule:

```text
Update operations must not allow cross-workspace writes.
```

---

# 9. Archive Pattern

Bizzi prefers archival over hard delete for business records.

Archive method pattern:

```typescript
async archiveByIdAndWorkspace(
  db: DbClient,
  id: string,
  workspaceId: string,
  data: ArchiveData,
): Promise<TaskRecord | null> {
  return this.updateByIdAndWorkspace(db, id, workspaceId, {
    status: 'archived',
    archivedAt: data.archivedAt,
  });
}
```

Rule:

```text
Hard delete should not be used for confirmed business evidence in normal service flows.
```

---

# 10. List Pattern

List methods should support:

```text
workspace_id
filters
pagination
sorting
```

Canonical shape:

```typescript
async listByWorkspace(
  db: DbClient,
  workspaceId: string,
  filters: TaskFilters,
  pagination: PaginationInput,
): Promise<PaginatedResult<TaskRecord>> {
  const where = this.buildWhere(workspaceId, filters);
  const orderBy = this.buildOrderBy(pagination.sort);

  const [items, total] = await Promise.all([
    db.task.findMany({ where, orderBy, skip: pagination.skip, take: pagination.take }),
    db.task.count({ where }),
  ]);

  return { items, total };
}
```

Rule:

```text
List queries must always be bounded by pagination defaults.
```

---

# 11. Pagination Rules

Pagination must include:

```text
page_size default
page_size maximum
page_token or offset/page approach
stable sorting
```

MVP approach:

```text
offset pagination with page and page_size is acceptable
```

Future approach:

```text
cursor pagination for high-volume event tables
```

Rule:

```text
Do not return unbounded lists from repositories.
```

---

# 12. Filtering Rules

Filters should be explicit and typed.

Example filters:

```text
status
owner_user_id
object_type
object_id
from_timestamp
to_timestamp
event_type
action
```

Rules:

```text
ignore or reject unknown filters according to API contract
validate filter values before repository query
build where clauses from allowed fields only
never pass raw unvalidated filter objects directly from request to Prisma
```

---

# 13. Sorting Rules

Sorting should be controlled.

Allowed sort fields should be explicit per repository.

Example:

```text
tasks: created_at, updated_at, due_date, status
decisions: created_at, confirmed_at, decision_date
audit_events: timestamp, action
runtime_events: timestamp, event_type, status
```

Rule:

```text
Do not allow arbitrary client-provided sort fields to flow into Prisma orderBy.
```

---

# 14. Error Handling in Repositories

Repositories should not expose raw Prisma errors to controllers.

Repository options:

```text
return null for not found
let known persistence errors bubble to service error mapper
wrap low-level errors in PersistenceError where useful
```

Rule:

```text
Services are responsible for mapping not found and business errors to canonical service errors.
```

---

# 15. Record Naming Pattern

Repository return types should be named clearly.

Examples:

```text
TaskRecord
DecisionRecord
MemoryEntryRecord
AuditEventRecord
RuntimeEventRecord
WorkspaceRecord
```

Rule:

```text
Record types represent persistence shape, not API response shape.
```

---

# 16. DTO Boundary

Repositories return records.

Services map records to DTOs.

Forbidden pattern:

```text
repository returns API response DTO directly
```

Preferred flow:

```text
Repository Record → Service Mapper → Response DTO
```

---

# 17. Query Builder Helpers

Repositories may use private helpers for:

```text
buildWhere
buildOrderBy
buildPagination
mapDatabaseRecord optional
```

Rules:

```text
helpers remain repository-local unless shared safely
shared query helpers must not hide workspace_id requirements
```

---

# 18. Audit and Runtime Event Repositories

AuditEventRepository and RuntimeEventRepository are special persistence repositories.

Rules:

```text
audit_events are append-oriented
runtime_events may update status fields
audit event normal flows should not update or delete events
runtime event status updates should be controlled
payloads must be sanitized before repository call
```

---

# 19. Index-Aware Repository Design

Repository queries should align with indexes from `04_DATABASE_MIGRATION_PLAN.md`.

Common indexed query patterns:

```text
workspace_id + status
workspace_id + created_at
workspace_id + timestamp
workspace_id + object_type + object_id
workspace_id + correlation_id
```

Rule:

```text
If a repository adds a common query pattern, check whether a supporting index exists or is needed.
```

---

# 20. Test Data Pattern

Repository tests should use:

```text
test database
factory helpers
unique workspace ids
clean database per test or transaction rollback
```

Required tests:

```text
create record
find by id and workspace
reject cross-workspace lookup
list by workspace with filters
pagination behavior
sorting behavior
archive behavior when applicable
```

---

# 21. MVP Repositories

MVP repositories:

```text
UserRepository
WorkspaceRepository
WorkspaceSettingsRepository
TaskRepository
DecisionRepository
MemoryRepository
AuditEventRepository
RuntimeEventRepository
```

Optional early:

```text
WorkspaceAccessRepository
ExportJobRepository
```

---

# 22. Repository Completion Checklist

A repository is complete when:

```text
required methods are implemented
workspace-scoped methods include workspace_id
list methods are paginated
filters are explicit
sort fields are controlled
transaction client is supported
records are returned without DTO coupling
repository tests cover workspace isolation
repository tests cover pagination and filters
```

---

# 23. Anti-Patterns

Avoid:

```text
findById for workspace-scoped data
unbounded findMany
raw request filters passed to Prisma
business rules inside repositories
repositories emitting audit events
repositories calling services
repositories returning API DTOs
hard deletes for business evidence
missing workspace_id in update queries
```

---

# 24. Acceptance Criteria

Repository Implementation Guide is accepted when:

- repository responsibilities are defined;
- transaction client pattern is documented;
- workspace scope pattern is documented;
- create, update, archive and list patterns are defined;
- pagination, filtering and sorting rules are documented;
- error handling expectations are defined;
- record and DTO boundaries are defined;
- audit and runtime event repository rules are defined;
- index-aware query guidance is included;
- repository testing expectations are documented;
- MVP repository list is defined;
- completion checklist and anti-patterns are documented.

Status:

```text
Accepted for Testing Strategy
```

---

# 25. Final Statement

```text
Bizzi Repository Implementation Guide defines the persistence discipline required to keep backend data access workspace-scoped, transaction-aware, testable and isolated from business logic.
```

This guide ensures that repository implementation supports the service layer without weakening Bizzi's architecture, auditability or security guarantees.