# 02_DATABASE_SCHEMA_EXECUTION.md

# Bizzi Platform

## Database Schema Execution

**Layer:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Component Type:** Execution Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Previous Document:** 01_BACKEND_SCAFFOLD_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the database schema execution plan for Bizzi Platform backend MVP.

It converts the accepted data model and database migration plan into practical instructions for creating the first `backend/prisma/schema.prisma`, MVP tables, enums, relations, indexes, seed data and migration verification workflow.

Core question:

```text
What database schema must be implemented first so Bizzi can run the MVP workspace execution loop safely and auditably?
```

---

# 2. Database Execution Thesis

```text
Bizzi database execution should implement only the MVP persistence surface first, while preserving workspace isolation, lifecycle statuses, audit evidence, runtime events, timestamps, indexes and future expansion fields.
```

The schema must prove:

```text
identity persistence
workspace ownership
workspace settings
task lifecycle
decision confirmation
memory activation
audit event evidence
runtime event coordination
dashboard-readable state
```

---

# 3. Target Files

Primary files:

```text
backend/prisma/schema.prisma
backend/prisma/migrations/
backend/prisma/seed.ts
backend/prisma/README.md optional
```

Supporting files:

```text
backend/src/database/prisma.service.ts
backend/src/database/transaction.manager.ts
backend/.env.example
docker-compose.yml
```

---

# 4. Database Platform

Canonical database:

```text
PostgreSQL
```

ORM / migration layer:

```text
Prisma
Prisma Migrate
```

Rule:

```text
All schema changes must be represented in Prisma schema and committed migrations.
```

---

# 5. MVP Schema Scope

Required MVP models:

```text
User
CompanyWorkspace
WorkspaceSettings
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
```

Optional early model:

```text
WorkspaceAccess
```

Deferred models:

```text
OperatingMap
Function
Responsibility
Agent
Process
Integration
SecurityPolicy
ExportJob
ExportFile
DashboardMetric
```

---

# 6. Naming Rules

Prisma model names:

```text
PascalCase
```

Database table names:

```text
snake_case plural
```

Example:

```text
CompanyWorkspace → company_workspaces
MemoryEntry → memory_entries
AuditEvent → audit_events
RuntimeEvent → runtime_events
```

Database columns:

```text
snake_case
```

TypeScript-facing Prisma fields may use camelCase with `@map`.

---

# 7. UUID Strategy

All primary identifiers should use UUID.

Recommended Prisma pattern:

```prisma
id String @id @default(uuid()) @db.Uuid
```

Foreign keys:

```prisma
workspaceId String @map("workspace_id") @db.Uuid
```

Rule:

```text
Do not use incremental integer IDs for workspace-scoped business entities.
```

---

# 8. Timestamp Strategy

Standard fields:

```prisma
createdAt DateTime @default(now()) @map("created_at")
updatedAt DateTime @updatedAt @map("updated_at")
```

Lifecycle fields:

```text
archived_at
completed_at
confirmed_at
processed_at
failed_at
```

Rule:

```text
Every mutable core table should have created_at and updated_at.
```

---

# 9. Enum Strategy

Stable MVP enums should be implemented as Prisma enums.

Required enums:

```text
UserStatus
WorkspaceStatus
WorkspaceOnboardingStatus
TaskStatus
TaskPriority
DecisionStatus
DecisionType
MemoryStatus
MemoryType
ActorType
AuditSeverity
RuntimeEventStatus
```

Rule:

```text
Enum values must align with 27_DATA_MODEL/11_ENUMS_AND_STATUSES.md.
```

---

# 10. Recommended MVP Enums

```prisma
enum UserStatus {
  active
  disabled
  archived
}

enum WorkspaceStatus {
  active
  archived
}

enum WorkspaceOnboardingStatus {
  draft
  in_progress
  completed
}

enum TaskStatus {
  open
  in_progress
  completed
  archived
}

enum TaskPriority {
  low
  medium
  high
  urgent
}

enum DecisionStatus {
  draft
  confirmed
  archived
}

enum DecisionType {
  operational
  financial
  legal
  strategic
  technical
  other
}

enum MemoryStatus {
  candidate
  active
  archived
}

enum MemoryType {
  fact
  rule
  decision
  preference
  process_note
  other
}

enum ActorType {
  user
  agent
  system
}

enum AuditSeverity {
  info
  warning
  critical
}

enum RuntimeEventStatus {
  pending
  processed
  failed
  ignored
}
```

---

# 11. User Model

Purpose:

```text
Represents authenticated human identity for MVP owner-only workspace access.
```

Required fields:

```text
id
email
name
status
created_at
updated_at
```

Recommended Prisma model:

```prisma
model User {
  id        String     @id @default(uuid()) @db.Uuid
  email     String     @unique
  name      String?
  status    UserStatus @default(active)
  createdAt DateTime   @default(now()) @map("created_at")
  updatedAt DateTime   @updatedAt @map("updated_at")

  ownedWorkspaces CompanyWorkspace[]

  @@map("users")
}
```

---

# 12. CompanyWorkspace Model

Purpose:

```text
Represents a company workspace and primary tenant boundary.
```

Required fields:

```text
id
owner_user_id
name
slug
status
onboarding_status
description
created_at
updated_at
archived_at
```

Recommended Prisma model:

```prisma
model CompanyWorkspace {
  id               String                    @id @default(uuid()) @db.Uuid
  ownerUserId      String                    @map("owner_user_id") @db.Uuid
  name             String
  slug             String                    @unique
  status           WorkspaceStatus           @default(active)
  onboardingStatus WorkspaceOnboardingStatus @default(draft) @map("onboarding_status")
  description      String?
  createdAt        DateTime                  @default(now()) @map("created_at")
  updatedAt        DateTime                  @updatedAt @map("updated_at")
  archivedAt       DateTime?                 @map("archived_at")

  owner            User                      @relation(fields: [ownerUserId], references: [id])
  settings         WorkspaceSettings?
  tasks            Task[]
  decisions        Decision[]
  memoryEntries    MemoryEntry[]
  auditEvents      AuditEvent[]
  runtimeEvents    RuntimeEvent[]

  @@index([ownerUserId])
  @@index([status])
  @@map("company_workspaces")
}
```

---

# 13. WorkspaceSettings Model

Purpose:

```text
Stores workspace-level runtime and localization settings.
```

Recommended Prisma model:

```prisma
model WorkspaceSettings {
  id                  String           @id @default(uuid()) @db.Uuid
  workspaceId         String           @unique @map("workspace_id") @db.Uuid
  timezone            String           @default("UTC")
  locale              String           @default("en")
  aiAssistanceEnabled Boolean          @default(true) @map("ai_assistance_enabled")
  memoryEnabled       Boolean          @default(true) @map("memory_enabled")
  auditEnabled        Boolean          @default(true) @map("audit_enabled")
  createdAt           DateTime         @default(now()) @map("created_at")
  updatedAt           DateTime         @updatedAt @map("updated_at")

  workspace           CompanyWorkspace @relation(fields: [workspaceId], references: [id])

  @@map("workspace_settings")
}
```

---

# 14. Task Model

Purpose:

```text
Represents actionable work inside a workspace.
```

Recommended Prisma model:

```prisma
model Task {
  id               String           @id @default(uuid()) @db.Uuid
  workspaceId      String           @map("workspace_id") @db.Uuid
  ownerUserId      String?          @map("owner_user_id") @db.Uuid
  title            String
  description      String?
  status           TaskStatus       @default(open)
  priority         TaskPriority     @default(medium)
  dueDate          DateTime?        @map("due_date")
  completedAt      DateTime?        @map("completed_at")
  sourceObjectType String?          @map("source_object_type")
  sourceObjectId   String?          @map("source_object_id") @db.Uuid
  metadata         Json?
  createdAt        DateTime         @default(now()) @map("created_at")
  updatedAt        DateTime         @updatedAt @map("updated_at")
  archivedAt       DateTime?        @map("archived_at")

  workspace        CompanyWorkspace @relation(fields: [workspaceId], references: [id])
  decisions        Decision[]
  memoryEntries    MemoryEntry[]

  @@index([workspaceId])
  @@index([workspaceId, status])
  @@index([workspaceId, ownerUserId])
  @@index([workspaceId, dueDate])
  @@index([workspaceId, createdAt])
  @@map("tasks")
}
```

---

# 15. Decision Model

Purpose:

```text
Represents official decision evidence inside a workspace.
```

Recommended Prisma model:

```prisma
model Decision {
  id               String           @id @default(uuid()) @db.Uuid
  workspaceId      String           @map("workspace_id") @db.Uuid
  taskId           String?          @map("task_id") @db.Uuid
  ownerUserId      String?          @map("owner_user_id") @db.Uuid
  title            String
  description      String?
  decisionType     DecisionType     @default(other) @map("decision_type")
  status           DecisionStatus   @default(draft)
  decisionDate     DateTime?        @map("decision_date")
  confirmedBy      String?          @map("confirmed_by") @db.Uuid
  confirmedAt      DateTime?        @map("confirmed_at")
  sourceObjectType String?          @map("source_object_type")
  sourceObjectId   String?          @map("source_object_id") @db.Uuid
  metadata         Json?
  createdAt        DateTime         @default(now()) @map("created_at")
  updatedAt        DateTime         @updatedAt @map("updated_at")
  archivedAt       DateTime?        @map("archived_at")

  workspace        CompanyWorkspace @relation(fields: [workspaceId], references: [id])
  task             Task?            @relation(fields: [taskId], references: [id])
  memoryEntries    MemoryEntry[]

  @@index([workspaceId])
  @@index([workspaceId, status])
  @@index([workspaceId, taskId])
  @@index([workspaceId, confirmedAt])
  @@index([workspaceId, createdAt])
  @@map("decisions")
}
```

---

# 16. MemoryEntry Model

Purpose:

```text
Stores reusable business memory records and candidate knowledge.
```

Recommended Prisma model:

```prisma
model MemoryEntry {
  id               String           @id @default(uuid()) @db.Uuid
  workspaceId      String           @map("workspace_id") @db.Uuid
  taskId           String?          @map("task_id") @db.Uuid
  decisionId       String?          @map("decision_id") @db.Uuid
  memoryType       MemoryType       @default(other) @map("memory_type")
  title            String
  summary          String?
  content          String
  status           MemoryStatus     @default(candidate)
  confidence       Float?
  sourceObjectType String?          @map("source_object_type")
  sourceObjectId   String?          @map("source_object_id") @db.Uuid
  validFrom        DateTime?        @map("valid_from")
  validUntil       DateTime?        @map("valid_until")
  confirmedBy      String?          @map("confirmed_by") @db.Uuid
  confirmedAt      DateTime?        @map("confirmed_at")
  metadata         Json?
  createdAt        DateTime         @default(now()) @map("created_at")
  updatedAt        DateTime         @updatedAt @map("updated_at")
  archivedAt       DateTime?        @map("archived_at")

  workspace        CompanyWorkspace @relation(fields: [workspaceId], references: [id])
  task             Task?            @relation(fields: [taskId], references: [id])
  decision         Decision?        @relation(fields: [decisionId], references: [id])

  @@index([workspaceId])
  @@index([workspaceId, status])
  @@index([workspaceId, memoryType])
  @@index([workspaceId, sourceObjectType, sourceObjectId])
  @@index([workspaceId, decisionId])
  @@index([workspaceId, taskId])
  @@map("memory_entries")
}
```

---

# 17. AuditEvent Model

Purpose:

```text
Stores append-oriented evidence for meaningful state changes.
```

Recommended Prisma model:

```prisma
model AuditEvent {
  id            String           @id @default(uuid()) @db.Uuid
  workspaceId   String           @map("workspace_id") @db.Uuid
  timestamp     DateTime         @default(now())
  actorType     ActorType        @map("actor_type")
  actorId       String           @map("actor_id") @db.Uuid
  agentId       String?          @map("agent_id") @db.Uuid
  action        String
  objectType    String           @map("object_type")
  objectId      String           @map("object_id") @db.Uuid
  sourceEventId String?          @map("source_event_id") @db.Uuid
  beforeState   Json?            @map("before_state")
  afterState    Json?            @map("after_state")
  aiAssisted    Boolean          @default(false) @map("ai_assisted")
  humanConfirmed Boolean         @default(true) @map("human_confirmed")
  severity      AuditSeverity    @default(info)
  correlationId String           @map("correlation_id")
  metadata      Json?

  workspace     CompanyWorkspace @relation(fields: [workspaceId], references: [id])

  @@index([workspaceId, timestamp])
  @@index([workspaceId, action])
  @@index([workspaceId, objectType, objectId])
  @@index([workspaceId, actorId])
  @@index([workspaceId, correlationId])
  @@map("audit_events")
}
```

Rule:

```text
Audit events are append-oriented and must not be updated in normal service flows.
```

---

# 18. RuntimeEvent Model

Purpose:

```text
Stores internal coordination events for runtime processing and visibility.
```

Recommended Prisma model:

```prisma
model RuntimeEvent {
  id               String             @id @default(uuid()) @db.Uuid
  workspaceId      String             @map("workspace_id") @db.Uuid
  eventType        String             @map("event_type")
  status           RuntimeEventStatus @default(pending)
  sourceObjectType String?            @map("source_object_type")
  sourceObjectId   String?            @map("source_object_id") @db.Uuid
  actorType        ActorType          @map("actor_type")
  actorId          String             @map("actor_id") @db.Uuid
  agentId          String?            @map("agent_id") @db.Uuid
  payload          Json?
  correlationId    String             @map("correlation_id")
  causationId      String?            @map("causation_id") @db.Uuid
  timestamp        DateTime           @default(now())
  processedAt      DateTime?          @map("processed_at")
  failedAt         DateTime?          @map("failed_at")
  failureReason    String?            @map("failure_reason")
  attemptCount     Int                @default(0) @map("attempt_count")

  workspace        CompanyWorkspace   @relation(fields: [workspaceId], references: [id])

  @@index([workspaceId, timestamp])
  @@index([workspaceId, eventType])
  @@index([workspaceId, status])
  @@index([workspaceId, sourceObjectType, sourceObjectId])
  @@index([workspaceId, correlationId])
  @@map("runtime_events")
}
```

---

# 19. Workspace Isolation Execution

Every workspace-scoped table must have:

```text
workspace_id
workspace relation
workspace_id index
repository methods requiring workspace_id
cross-workspace tests
```

Workspace-scoped MVP tables:

```text
workspace_settings
tasks
decisions
memory_entries
audit_events
runtime_events
```

Rule:

```text
No user-facing read or write for workspace data may rely only on object id.
```

---

# 20. Relation Strategy

Use direct foreign keys for stable relations:

```text
workspace_settings.workspace_id → company_workspaces.id
tasks.workspace_id → company_workspaces.id
decisions.workspace_id → company_workspaces.id
memory_entries.workspace_id → company_workspaces.id
audit_events.workspace_id → company_workspaces.id
runtime_events.workspace_id → company_workspaces.id
```

Use polymorphic references for flexible source/object links:

```text
source_object_type
source_object_id
object_type
object_id
```

Rule:

```text
Polymorphic references require service-level validation.
```

---

# 21. Index Strategy

Required index groups:

```text
workspace_id + status
workspace_id + created_at
workspace_id + timestamp
workspace_id + object_type + object_id
workspace_id + source_object_type + source_object_id
workspace_id + correlation_id
```

Dashboard-supporting indexes:

```text
tasks.workspace_id + status
decisions.workspace_id + status
memory_entries.workspace_id + status
audit_events.workspace_id + timestamp
runtime_events.workspace_id + timestamp
```

---

# 22. Migration Execution Workflow

Recommended first migration name:

```text
001_mvp_workspace_execution_schema
```

Commands:

```bash
cd backend
pnpm prisma format
pnpm prisma validate
pnpm prisma migrate dev --name 001_mvp_workspace_execution_schema
pnpm prisma generate
```

Verification:

```bash
pnpm prisma migrate reset
pnpm prisma migrate status
```

Rule:

```text
Generated migration files must be committed.
```

---

# 23. Seed Execution

`backend/prisma/seed.ts` should create:

```text
development user
development workspace
default workspace settings
sample task optional
sample draft decision optional
sample memory entry optional
```

Seed constraints:

```text
no real secrets
repeatable or reset-aware
safe for local development only
clearly separated from migrations
```

---

# 24. Transaction Readiness

The database schema must support transactional creation of:

```text
workspace + settings + audit event + runtime event
task + audit event + runtime event
decision + audit event + runtime event
memory entry + audit event + runtime event
```

Rule:

```text
No meaningful mutation should commit without required audit evidence.
```

---

# 25. Data Safety Rules

Schema execution must protect:

```text
no raw secrets in metadata
no raw secrets in audit states
no raw secrets in runtime payloads
archival over hard delete for business evidence
workspace_id required for workspace data
bounded list queries supported by indexes
```

---

# 26. Verification Checklist

Database schema execution is complete when:

```text
[ ] schema.prisma contains MVP enums
[ ] schema.prisma contains User model
[ ] schema.prisma contains CompanyWorkspace model
[ ] schema.prisma contains WorkspaceSettings model
[ ] schema.prisma contains Task model
[ ] schema.prisma contains Decision model
[ ] schema.prisma contains MemoryEntry model
[ ] schema.prisma contains AuditEvent model
[ ] schema.prisma contains RuntimeEvent model
[ ] workspace-scoped indexes exist
[ ] relations compile
[ ] prisma format passes
[ ] prisma validate passes
[ ] migration is generated
[ ] migration applies to clean database
[ ] prisma generate succeeds
[ ] seed script exists or is planned
```

---

# 27. Risks and Controls

## Risk 1 — Schema Too Broad

Mitigation:

```text
Implement only MVP tables first.
```

## Risk 2 — Workspace Scope Missing

Mitigation:

```text
Require workspace_id and indexes on all workspace-scoped tables.
```

## Risk 3 — Prisma Schema Drift

Mitigation:

```text
Validate schema against 27_DATA_MODEL and 30_BACKEND_IMPLEMENTATION_PLAN.
```

## Risk 4 — Unsafe Metadata Usage

Mitigation:

```text
Use metadata as extension only, not as replacement for canonical fields.
```

---

# 28. Acceptance Criteria

Database Schema Execution is accepted when:

- target files are defined;
- PostgreSQL and Prisma execution path is confirmed;
- MVP schema scope is defined;
- naming, UUID, timestamp and enum strategies are defined;
- MVP models are specified;
- workspace isolation rules are defined;
- relations and indexes are defined;
- migration workflow is documented;
- seed workflow is documented;
- transaction readiness is documented;
- data safety rules are defined;
- verification checklist is provided;
- risks and controls are documented.

Status:

```text
Accepted for Shared Kernel Execution
```

---

# 29. Final Statement

```text
Bizzi Database Schema Execution defines the first real persistence foundation for the backend MVP: identity, workspace, task, decision, memory, audit events and runtime events implemented through PostgreSQL and Prisma.
```

This schema prepares Bizzi for shared kernel implementation, repository creation and the first runnable workspace execution loop.