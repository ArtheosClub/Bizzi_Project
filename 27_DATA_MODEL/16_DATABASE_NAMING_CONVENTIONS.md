# 16_DATABASE_NAMING_CONVENTIONS.md

# Bizzi Platform

## Database Naming Conventions

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Standard Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md through 15_DATA_DICTIONARY.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines database naming conventions for Bizzi Platform.

It standardizes how database tables, columns, indexes, constraints, foreign keys, enums, events and migration objects should be named across the `27_DATA_MODEL` layer and future implementation layers.

Core question:

```text
How should Bizzi name database objects so that the schema remains consistent, readable, maintainable and implementation-ready?
```

---

# 2. Naming Convention Role

Naming conventions provide:

- database readability;
- predictable ORM mapping;
- consistent API field design;
- easier migrations;
- easier debugging;
- clearer audit and event records;
- reduced ambiguity between domain entities and tables;
- long-term maintainability for engineering teams.

---

# 3. General Naming Principles

## 3.1 Use English Internal Names

All database object names should use English.

Reason:

```text
Database, API, ORM and infrastructure tools are easier to standardize with English identifiers.
```

## 3.2 Use snake_case

All physical database object names should use:

```text
snake_case
```

Examples:

```text
company_workspaces
workspace_settings
source_object_type
created_at
idx_tasks_workspace_status
```

## 3.3 Avoid Spaces and Special Characters

Do not use:

```text
spaces
hyphens
camelCase
PascalCase
localized characters
punctuation
```

## 3.4 Prefer Clarity Over Abbreviation

Use:

```text
workspace_id
created_at
source_object_type
integration_sync_jobs
```

Avoid unclear abbreviations:

```text
ws_id
crt_at
src_obj_tp
int_sync
```

---

# 4. Table Naming

## 4.1 Table Names

Tables should use:

```text
snake_case_plural
```

Examples:

```text
users
sessions
company_workspaces
workspace_settings
operating_maps
operating_gaps
functions
responsibilities
tasks
decisions
memory_entries
audit_events
runtime_events
```

## 4.2 Aggregate Root Tables

Aggregate root entities should map to clear primary tables.

Examples:

```text
CompanyWorkspace → company_workspaces
OperatingMap → operating_maps
Task → tasks
Decision → decisions
MemoryEntry → memory_entries
```

## 4.3 Join Tables

Join tables should name both joined concepts in logical order.

Pattern:

```text
<left_entity>_<right_entity>
```

Examples:

```text
role_permissions
workspace_access
responsibility_assignments
```

## 4.4 History and Event Tables

History, event and audit tables should make their purpose explicit.

Examples:

```text
audit_events
runtime_events
task_history
event_failures
integration_sync_jobs
```

---

# 5. Column Naming

## 5.1 Column Names

Columns should use:

```text
snake_case
```

Examples:

```text
id
workspace_id
owner_user_id
source_object_type
created_at
updated_at
confirmed_by
confirmed_at
```

## 5.2 Primary Key Column

Primary key column should be:

```text
id
```

Standard pattern:

```text
id UUID PRIMARY KEY
```

Avoid:

```text
task_id as primary key inside tasks
workspace_uuid
pk_id
```

## 5.3 Foreign Key Columns

Foreign key columns should use:

```text
<referenced_entity_singular>_id
```

Examples:

```text
workspace_id
user_id
owner_user_id
function_id
process_id
task_id
decision_id
agent_id
integration_id
```

## 5.4 User Role Columns

When referencing users, column names must communicate meaning.

Examples:

```text
owner_user_id
created_by
assigned_by
confirmed_by
reviewed_by
requested_by
resolved_by
```

Rule:

```text
Do not use user_id when a more specific responsibility meaning exists.
```

---

# 6. Timestamp Naming

Timestamp columns should end with:

```text
_at
```

Examples:

```text
created_at
updated_at
archived_at
confirmed_at
reviewed_at
completed_at
revoked_at
processed_at
```

Date-only fields should end with:

```text
_date
```

Examples:

```text
due_date
decision_date
review_date
```

Use:

```text
created_at TIMESTAMPTZ
```

not:

```text
created_on
creation_time
createdDate
```

---

# 7. Boolean Naming

Boolean fields should be named as readable flags.

Recommended prefixes:

```text
is_
has_
can_
should_
requires_
```

Existing Bizzi-compatible examples:

```text
ai_assistance_enabled
memory_enabled
audit_enabled
generated_by_ai
ai_assisted
human_confirmed
review_required
automation_candidate
agent_assist_allowed
```

Rule:

```text
Boolean names should be understandable when read as true or false.
```

---

# 8. Status and Type Naming

## 8.1 Status Columns

Lifecycle columns should be named:

```text
status
```

Examples:

```text
tasks.status
decisions.status
memory_entries.status
integrations.status
export_jobs.status
```

## 8.2 Type Columns

Classification columns should use:

```text
<concept>_type
```

Examples:

```text
gap_type
memory_type
recommendation_type
export_type
event_type
policy_type
sync_type
metric_type
```

## 8.3 Category Columns

Higher-level groupings may use:

```text
category
```

or:

```text
<concept>_category
```

Examples:

```text
functions.category
dashboard_metrics.category
permissions.category
```

---

# 9. Polymorphic Reference Naming

Bizzi uses polymorphic references for source, target, result and resolution links.

Standard pairs:

```text
source_object_type
source_object_id
object_type
object_id
result_object_type
result_object_id
resolved_by_object_type
resolved_by_object_id
suggested_object_type
suggested_object_payload
used_by_object_type
used_by_object_id
```

Rule:

```text
Polymorphic reference pairs must always include both type and id when the reference is expected to be resolvable.
```

---

# 10. JSONB Column Naming

Flexible JSONB columns should use clear purpose names.

Common names:

```text
metadata
payload
configuration
rules
mapping_rules
before_state
after_state
export_scope
scopes
allowed_actions
restricted_actions
```

Rule:

```text
Use metadata for non-core additional information only. Use specific JSONB names when the structure has a clear role.
```

Avoid:

```text
data
json
extra
misc
blob
```

---

# 11. Index Naming

Indexes should use:

```text
idx_<table>_<columns>
```

Examples:

```text
idx_tasks_workspace_status
idx_tasks_workspace_owner_status
idx_memory_entries_workspace_type
idx_audit_events_workspace_timestamp
idx_runtime_events_workspace_status_type
```

For long names, keep the most important columns:

```text
idx_agent_recommendations_workspace_status
```

Avoid opaque names:

```text
idx_1
index_tasks_abc
ix_tmp
```

---

# 12. Unique Constraint Naming

Unique constraints should use:

```text
uq_<table>_<columns>
```

Examples:

```text
uq_users_email
uq_workspace_settings_workspace
uq_workspace_access_workspace_user
uq_process_steps_process_step_order
```

---

# 13. Foreign Key Constraint Naming

Foreign key constraints should use:

```text
fk_<table>_<referenced_table>
```

or when multiple references exist:

```text
fk_<table>_<column>
```

Examples:

```text
fk_tasks_workspaces
fk_tasks_owner_user
fk_decisions_tasks
fk_memory_entries_decisions
fk_audit_events_runtime_events
```

---

# 14. Check Constraint Naming

Check constraints should use:

```text
chk_<table>_<rule>
```

Examples:

```text
chk_tasks_status
chk_tasks_priority
chk_export_jobs_format
chk_memory_entries_status
```

---

# 15. Enum Naming

If PostgreSQL ENUMs are used later, enum type names should use:

```text
<concept>_<field>_enum
```

Examples:

```text
task_status_enum
task_priority_enum
decision_status_enum
memory_status_enum
runtime_event_status_enum
export_status_enum
```

Enum values should use:

```text
snake_case
```

Examples:

```text
in_progress
ai_suggested
execute_with_confirmation
workspace_summary
```

---

# 16. Event and Audit Action Naming

Runtime events and audit actions should use stable dot notation.

Pattern:

```text
<object>.<action>
```

Examples:

```text
workspace.created
operating_map.generated
function.created
responsibility.assigned
task.status_changed
decision.confirmed
memory.created
export.completed
integration.sync_failed
access.denied
```

Rule:

```text
Event and audit names must be stable internal identifiers, not UI labels.
```

---

# 17. Migration Naming

Migration files should use chronological ordering.

Recommended pattern:

```text
YYYYMMDDHHMMSS_<action>_<object>.sql
```

Examples:

```text
20260701090000_create_users.sql
20260701090500_create_company_workspaces.sql
20260701100000_add_workspace_id_to_tasks.sql
20260701110000_create_runtime_events.sql
```

Migration names should be descriptive and irreversible ambiguity should be avoided.

---

# 18. ORM Naming Alignment

ORM models may use PascalCase class names while mapping to snake_case table names.

Examples:

```text
CompanyWorkspace → company_workspaces
WorkspaceSettings → workspace_settings
RuntimeEvent → runtime_events
MemoryEntry → memory_entries
```

Rule:

```text
Physical database names remain snake_case even if application models use PascalCase.
```

---

# 19. API Field Alignment

API fields should generally mirror database field names unless there is a clear product reason not to.

Recommended API field style:

```text
snake_case
```

Examples:

```text
workspace_id
owner_user_id
source_object_type
created_at
updated_at
```

This reduces mapping complexity between API, backend and database.

---

# 20. Reserved Words and Confusing Names

Avoid database reserved words as table or column names.

Avoid:

```text
user
session
order
group
role
permission
function
```

Preferred Bizzi names:

```text
users
sessions
export_jobs
workspace_access
functions
responsibilities
```

Note:

```text
functions is acceptable as a table name in Bizzi context but must be tested against ORM and SQL tooling.
```

---

# 21. File Naming Inside Repository

Data model documents should use numbered uppercase Markdown names:

```text
00_DATA_MODEL_VISION.md
01_DATABASE_PRINCIPLES.md
16_DATABASE_NAMING_CONVENTIONS.md
```

Rule:

```text
Document numbering must preserve layer order and avoid duplicate semantic names with different numbers.
```

---

# 22. Naming Anti-Patterns

Avoid:

```text
mixed casing
camelCase database columns
unclear abbreviations
singular table names
status values as UI labels
metadata used for primary relationships
random index names
duplicate terms for same concept
renaming stable fields without migration plan
```

---

# 23. Acceptance Criteria

Database Naming Conventions are ready when:

- table naming is standardized;
- column naming is standardized;
- foreign key naming is standardized;
- timestamp naming is standardized;
- polymorphic reference naming is standardized;
- index and constraint names are defined;
- enum and event naming rules are defined;
- migration naming is defined;
- ORM and API naming alignment is documented.

Status:

```text
Accepted as Data Model Standard
```

---

# 24. Final Statement

```text
Bizzi Database Naming Conventions define the canonical naming standard for database objects, ensuring that schema, migrations, ORM models, API contracts, audit events and runtime events remain consistent, readable and implementation-ready.
```

This document strengthens the `27_DATA_MODEL` layer as an engineering-grade database specification.