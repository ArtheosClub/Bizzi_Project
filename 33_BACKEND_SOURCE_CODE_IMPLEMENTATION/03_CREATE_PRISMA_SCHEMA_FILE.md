# 03_CREATE_PRISMA_SCHEMA_FILE.md

# Bizzi Platform

## Create Prisma Schema File

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Task  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Previous Document Reference:** 32_BACKEND_CODEBASE_BUILD/02_PRISMA_SCHEMA_IMPLEMENTATION.md  
**Product:** Bizzi Platform  
**Implementation Phase:** Backend Source Code Build

---

# 1. Purpose

This document defines the implementation task for creating the real Prisma schema file for the Bizzi backend.

Target file:

```text
backend/prisma/schema.prisma
```

Core question:

```text
What exact source file must be created to establish the first executable database schema for Bizzi Platform?
```

---

# 2. Implementation Goal

Create a valid Prisma schema that defines the first backend persistence model for Bizzi MVP.

The schema must support:

```text
identity
workspace ownership
workspace settings
tasks
decisions
memory entries
audit events
runtime events
workspace-scoped queries
future dashboard aggregation
```

---

# 3. Target File Path

```text
backend/prisma/schema.prisma
```

Required directory:

```text
backend/prisma/
```

---

# 4. Generator and Datasource

The file must start with Prisma generator and PostgreSQL datasource configuration:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

---

# 5. Required Enums

The first schema must define canonical enums for MVP lifecycle and attribution.

Required enums:

```prisma
enum UserStatus {
  active
  disabled
}

enum WorkspaceStatus {
  active
  archived
}

enum TaskStatus {
  open
  in_progress
  completed
  archived
}

enum DecisionStatus {
  draft
  confirmed
  archived
}

enum MemoryStatus {
  candidate
  active
  archived
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
}
```

---

# 6. Required Models

The schema must include:

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

These models are the minimum persistence foundation for the backend MVP.

---

# 7. User Model

Required fields:

```prisma
model User {
  id         String     @id @default(uuid()) @db.Uuid
  email      String     @unique
  name       String?
  status     UserStatus @default(active)
  created_at DateTime   @default(now())
  updated_at DateTime   @updatedAt

  workspaces CompanyWorkspace[]
  tasks      Task[]
  decisions  Decision[]

  @@map("users")
}
```

Rule:

```text
User does not store credentials in MVP. Authentication provider integration remains outside this schema version.
```

---

# 8. CompanyWorkspace Model

Required fields:

```prisma
model CompanyWorkspace {
  id                String          @id @default(uuid()) @db.Uuid
  owner_user_id     String          @db.Uuid
  name              String
  slug              String          @unique
  status            WorkspaceStatus @default(active)
  onboarding_status String          @default("not_started")
  description       String?
  created_at        DateTime        @default(now())
  updated_at        DateTime        @updatedAt
  archived_at       DateTime?

  owner             User              @relation(fields: [owner_user_id], references: [id])
  settings          WorkspaceSettings?
  tasks             Task[]
  decisions         Decision[]
  memory_entries    MemoryEntry[]
  audit_events      AuditEvent[]
  runtime_events    RuntimeEvent[]

  @@index([owner_user_id])
  @@index([status])
  @@map("company_workspaces")
}
```

Rule:

```text
CompanyWorkspace is the primary tenant boundary of Bizzi Platform.
```

---

# 9. WorkspaceSettings Model

Required fields:

```prisma
model WorkspaceSettings {
  id                    String   @id @default(uuid()) @db.Uuid
  workspace_id          String   @unique @db.Uuid
  timezone              String   @default("UTC")
  locale                String   @default("en")
  ai_assistance_enabled Boolean  @default(true)
  memory_enabled        Boolean  @default(true)
  audit_enabled         Boolean  @default(true)
  created_at            DateTime @default(now())
  updated_at            DateTime @updatedAt

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])

  @@map("workspace_settings")
}
```

Rule:

```text
Workspace settings are created transactionally with workspace creation.
```

---

# 10. Task Model

Required fields:

```prisma
model Task {
  id                 String     @id @default(uuid()) @db.Uuid
  workspace_id       String     @db.Uuid
  owner_user_id      String?    @db.Uuid
  title              String
  description        String?
  status             TaskStatus @default(open)
  priority           String?
  due_date           DateTime?
  completed_at       DateTime?
  source_object_type String?
  source_object_id   String?
  metadata           Json?
  created_at         DateTime   @default(now())
  updated_at         DateTime   @updatedAt
  archived_at        DateTime?

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])
  owner     User?            @relation(fields: [owner_user_id], references: [id])
  decisions Decision[]

  @@index([workspace_id])
  @@index([workspace_id, status])
  @@index([owner_user_id])
  @@map("tasks")
}
```

---

# 11. Decision Model

Required fields:

```prisma
model Decision {
  id                 String         @id @default(uuid()) @db.Uuid
  workspace_id       String         @db.Uuid
  task_id            String?        @db.Uuid
  owner_user_id      String?        @db.Uuid
  title              String
  description        String?
  decision_type      String?
  status             DecisionStatus @default(draft)
  decision_date      DateTime?
  confirmed_by       String?        @db.Uuid
  confirmed_at       DateTime?
  source_object_type String?
  source_object_id   String?
  metadata           Json?
  created_at         DateTime       @default(now())
  updated_at         DateTime       @updatedAt
  archived_at        DateTime?

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])
  task      Task?            @relation(fields: [task_id], references: [id])
  owner     User?            @relation(fields: [owner_user_id], references: [id])

  @@index([workspace_id])
  @@index([workspace_id, status])
  @@index([task_id])
  @@map("decisions")
}
```

Rule:

```text
If task_id is present, service-level validation must ensure the task belongs to the same workspace.
```

---

# 12. MemoryEntry Model

Required fields:

```prisma
model MemoryEntry {
  id                 String       @id @default(uuid()) @db.Uuid
  workspace_id       String       @db.Uuid
  task_id            String?      @db.Uuid
  decision_id        String?      @db.Uuid
  memory_type        String?
  title              String
  summary            String?
  content            String
  status             MemoryStatus @default(candidate)
  confidence         Float?
  source_object_type String?
  source_object_id   String?
  valid_from         DateTime?
  valid_until        DateTime?
  confirmed_by       String?      @db.Uuid
  confirmed_at       DateTime?
  metadata           Json?
  created_at         DateTime     @default(now())
  updated_at         DateTime     @updatedAt
  archived_at        DateTime?

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])

  @@index([workspace_id])
  @@index([workspace_id, status])
  @@map("memory_entries")
}
```

Rule:

```text
Memory activation is a lifecycle transition, not a simple update.
```

---

# 13. AuditEvent Model

Required fields:

```prisma
model AuditEvent {
  id              String        @id @default(uuid()) @db.Uuid
  workspace_id    String        @db.Uuid
  timestamp       DateTime      @default(now())
  actor_type      ActorType
  actor_id        String?
  agent_id        String?
  action          String
  object_type     String
  object_id       String?
  source_event_id String?       @db.Uuid
  before_state    Json?
  after_state     Json?
  ai_assisted     Boolean       @default(false)
  human_confirmed Boolean       @default(true)
  severity        AuditSeverity @default(info)
  correlation_id  String
  metadata        Json?

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])

  @@index([workspace_id])
  @@index([workspace_id, action])
  @@index([workspace_id, object_type, object_id])
  @@index([correlation_id])
  @@index([timestamp])
  @@map("audit_events")
}
```

Rule:

```text
Audit events are append-oriented business evidence. Normal business flows must not update or delete them.
```

---

# 14. RuntimeEvent Model

Required fields:

```prisma
model RuntimeEvent {
  id             String             @id @default(uuid()) @db.Uuid
  workspace_id   String             @db.Uuid
  event_type     String
  status         RuntimeEventStatus @default(pending)
  payload        Json?
  correlation_id String
  created_at     DateTime           @default(now())
  processed_at   DateTime?
  failed_at      DateTime?
  error_message  String?

  workspace CompanyWorkspace @relation(fields: [workspace_id], references: [id])

  @@index([workspace_id])
  @@index([workspace_id, event_type])
  @@index([workspace_id, status])
  @@index([correlation_id])
  @@map("runtime_events")
}
```

Rule:

```text
Runtime events coordinate internal behavior and must not replace audit events.
```

---

# 15. Implementation Steps

Create the file:

```bash
mkdir -p backend/prisma
touch backend/prisma/schema.prisma
```

Insert the schema content.

Then run:

```bash
cd backend
pnpm prisma format
pnpm prisma validate
pnpm prisma generate
```

After validation succeeds, create the first migration:

```bash
pnpm prisma migrate dev --name init
```

---

# 16. Validation Requirements

The schema is accepted only when:

```text
Prisma format succeeds
Prisma validate succeeds
Prisma client generates successfully
initial migration can be created
migration can be applied to a clean database
workspace-scoped indexes exist
relations compile correctly
```

---

# 17. Acceptance Criteria

This implementation task is accepted when:

- `backend/prisma/schema.prisma` exists;
- datasource and generator are defined;
- all MVP enums are defined;
- all MVP models are defined;
- workspace relations are defined;
- workspace-scoped indexes are defined;
- audit and runtime event models exist;
- Prisma validation commands are documented;
- initial migration path is documented.

Status:

```text
Ready for source implementation
```

---

# 18. Final Statement

```text
The Prisma schema file establishes the executable persistence foundation of Bizzi Platform.
```

This file is the first true backend source artifact required before repositories, services, controllers and tests can become runnable.