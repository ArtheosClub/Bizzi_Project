# 11_ENUMS_AND_STATUSES.md

# Bizzi Platform

## Enums and Statuses

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md, 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md, 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md, 09_INTEGRATION_SECURITY_DATA_MODEL.md, 10_DASHBOARD_EXPORT_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the initial enum and status value catalog for Bizzi Platform data model.

It establishes controlled values for core entity lifecycle states, categories, severity levels, priority levels and runtime classifications.

Core question:

```text
Which controlled values should Bizzi use to keep database state consistent, queryable and implementation-ready?
```

---

# 2. Role of Enums and Statuses

Enums and statuses provide:

- lifecycle consistency;
- validation rules;
- dashboard filtering;
- API contract stability;
- backend service rules;
- audit clarity;
- data model discipline;
- prevention of arbitrary status text.

---

# 3. Implementation Recommendation

For MVP, Bizzi may begin with:

```text
TEXT columns with application-level validation
```

Near implementation or production hardening may use:

```text
PostgreSQL ENUM
CHECK constraints
reference tables
```

Recommended staged approach:

```text
Document values first
↓
Validate in services
↓
Add database constraints where stable
↓
Promote selected statuses to PostgreSQL ENUM if useful
```

---

# 4. General Status Pattern

Common lifecycle pattern:

```text
suggested
↓
draft
↓
active
↓
paused
↓
archived
```

Not every entity uses every value.

Core principle:

```text
Statuses should describe lifecycle state, not replace domain relationships.
```

---

# 5. Identity Enums

## user_status

Used by:

```text
users.status
```

Values:

```text
active
inactive
blocked
archived
```

## session_status

Used by:

```text
sessions.status
```

Values:

```text
active
expired
revoked
```

---

# 6. Workspace Enums

## workspace_status

Used by:

```text
company_workspaces.status
```

Values:

```text
created
onboarding
active
paused
archived
```

## onboarding_status

Used by:

```text
company_workspaces.onboarding_status
```

Values:

```text
not_started
in_progress
completed
skipped
```

## workspace_access_status

Used by:

```text
workspace_access.status
```

Values:

```text
active
invited
revoked
archived
```

## workspace_role

Used by:

```text
workspace_access.role
```

MVP value:

```text
owner
```

Expansion values:

```text
admin
manager
member
viewer
consultant
auditor
```

---

# 7. Operating Map Enums

## operating_map_status

Used by:

```text
operating_maps.status
```

Values:

```text
generated
confirmed
active
archived
```

Expansion values:

```text
draft
reviewed
updated
```

## operating_gap_status

Used by:

```text
operating_gaps.status
```

Values:

```text
detected
accepted
resolved
archived
```

Expansion values:

```text
reviewed
in_progress
rejected
```

## operating_gap_type

Used by:

```text
operating_gaps.gap_type
```

Values:

```text
missing_function
missing_owner
missing_process
missing_task
operational_risk
```

Expansion values:

```text
missing_decision
missing_agent_support
unclear_responsibility
memory_gap
audit_gap
integration_gap
```

## operating_recommendation_status

Used by:

```text
operating_recommendations.status
```

Values:

```text
created
confirmed
rejected
applied
archived
```

## operating_recommendation_type

Used by:

```text
operating_recommendations.recommendation_type
```

Values:

```text
create_function
assign_owner
create_task
create_process
suggest_agent
log_decision
create_memory
review_risk
```

---

# 8. Function and Responsibility Enums

## function_status

Used by:

```text
functions.status
```

Values:

```text
suggested
active
archived
```

Expansion values:

```text
draft
confirmed
reviewed
```

## function_category

Used by:

```text
functions.category
```

MVP values:

```text
operations
sales
finance
administration
risk
```

Expansion values:

```text
strategy
marketing
legal
hr
procurement
logistics
customer_support
technology
compliance
```

## responsibility_status

Used by:

```text
responsibilities.status
```

Values:

```text
unassigned
assigned
archived
```

Expansion values:

```text
suggested
reviewed
changed
```

## responsibility_type

Used by:

```text
responsibilities.responsibility_type
```

MVP value:

```text
owner
```

Expansion values:

```text
accountable
reviewer
approver
operator
observer
```

## ownership_gap_status

Used by:

```text
ownership_gaps.status
```

Values:

```text
detected
accepted
resolved
archived
```

Expansion values:

```text
reviewed
rejected
in_progress
```

## ownership_gap_type

Used by:

```text
ownership_gaps.gap_type
```

Values:

```text
missing_owner
unclear_owner
owner_inactive
responsibility_conflict
```

---

# 9. Agent Enums

## agent_status

Used by:

```text
agents.status
```

Values:

```text
suggested
active
paused
archived
```

Expansion values:

```text
draft
configured
```

## agent_authority_scope_status

Used by:

```text
agent_authority_scopes.status
```

Values:

```text
draft
active
paused
archived
```

## agent_recommendation_status

Used by:

```text
agent_recommendations.status
```

Values:

```text
created
reviewed
confirmed
applied
rejected
archived
```

## agent_action_draft_status

Used by:

```text
agent_action_drafts.status
```

Values:

```text
draft
reviewed
confirmed
rejected
applied
archived
```

## autonomy_level

Used by:

```text
agent_authority_scopes.max_autonomy_level
```

Values:

```text
assist_only
suggest
prepare_draft
execute_with_confirmation
```

Future value:

```text
limited_autonomous
```

---

# 10. Process Enums

## process_status

Used by:

```text
processes.status
```

Values:

```text
suggested
draft
active
archived
```

Expansion values:

```text
defined
reviewed
improved
```

## process_step_status

Used by:

```text
process_steps.status
```

Values:

```text
active
removed
```

Expansion values:

```text
draft
changed
```

## process_frequency

Used by:

```text
processes.frequency
```

Suggested values:

```text
ad_hoc
daily
weekly
monthly
quarterly
annually
triggered
```

---

# 11. Task Enums

## task_status

Used by:

```text
tasks.status
```

Values:

```text
suggested
open
in_progress
blocked
completed
archived
```

MVP minimum:

```text
suggested
open
in_progress
completed
archived
```

## task_priority

Used by:

```text
tasks.priority
```

Values:

```text
low
normal
high
urgent
```

Default:

```text
normal
```

---

# 12. Decision Enums

## decision_status

Used by:

```text
decisions.status
```

Values:

```text
draft
confirmed
implemented
archived
```

MVP minimum:

```text
draft
confirmed
archived
```

Expansion values:

```text
proposed
reviewed
```

## risk_level

Used by:

```text
functions.risk_level
processes.risk_level
decisions.risk_level
```

Values:

```text
low
medium
high
critical
```

---

# 13. Memory Enums

## memory_status

Used by:

```text
memory_entries.status
```

Values:

```text
candidate
active
archived
```

Expansion values:

```text
draft
confirmed
reviewed
updated
rejected
```

## memory_confidence

Used by:

```text
memory_entries.confidence
```

MVP values:

```text
manual
ai_suggested
confirmed
```

Expansion values:

```text
low
medium
high
verified
```

## memory_type

Used by:

```text
memory_entries.memory_type
```

MVP values:

```text
company_context
operating_gap
function_context
process_definition
task_outcome
decision_context
decision_rationale
agent_recommendation
```

Expansion values:

```text
owner_goal
operating_pain_point
workspace_profile
operating_map_summary
responsibility_context
process_lesson
task_context
decision_outcome
audit_summary
integration_context
dashboard_insight
export_summary
```

---

# 14. Audit and Event Enums

## actor_type

Used by:

```text
audit_events.actor_type
```

Values:

```text
user
agent
system
integration
```

## audit_severity

Used by:

```text
audit_events.severity
```

Values:

```text
info
warning
critical
```

Expansion value:

```text
notice
```

## runtime_event_status

Used by:

```text
runtime_events.status
```

Values:

```text
emitted
processed
failed
```

Expansion values:

```text
processing
ignored
```

## runtime_event_severity

Used by:

```text
runtime_events.severity
```

Values:

```text
info
warning
critical
```

---

# 15. Integration and Security Enums

## integration_status

Used by:

```text
integrations.status
```

Values:

```text
configured
active
paused
revoked
error
```

Expansion values:

```text
available
requested
connected
archived
```

## integration_sync_type

Used by:

```text
integration_sync_jobs.sync_type
```

Values:

```text
import
export
validation
```

Expansion values:

```text
full_sync
incremental_sync
webhook_event
```

## integration_sync_status

Used by:

```text
integration_sync_jobs.status
```

Values:

```text
queued
running
completed
failed
cancelled
```

## security_policy_status

Used by:

```text
security_policies.status
```

Values:

```text
draft
active
paused
archived
```

## security_policy_type

Used by:

```text
security_policies.policy_type
```

Values:

```text
workspace_access
ai_context
integration_access
export_control
audit_policy
```

---

# 16. Dashboard and Export Enums

## dashboard_metric_status

Used by:

```text
dashboard_metrics.status
```

Values:

```text
calculated
visible
stale
archived
```

Expansion values:

```text
refreshing
error
```

## dashboard_severity

Used by:

```text
dashboard_metrics.severity
dashboard_alerts.severity
```

Values:

```text
info
warning
critical
```

## export_status

Used by:

```text
export_jobs.status
```

Values:

```text
requested
generating
completed
failed
```

Expansion values:

```text
queued
expired
cancelled
```

## export_type

Used by:

```text
export_jobs.export_type
```

Values:

```text
workspace_summary
operating_map_export
task_list_export
decision_log_export
```

Expansion values:

```text
memory_export
audit_export
implementation_brief
```

## export_format

Used by:

```text
export_jobs.format
```

Values:

```text
markdown
pdf
```

Expansion values:

```text
csv
json
```

---

# 17. Shared Severity and Priority Values

## severity_level

Used across gaps, audit, events, dashboard and alerts.

Values:

```text
low
medium
high
critical
```

## display_severity

Used for dashboard and audit visibility.

Values:

```text
info
warning
critical
```

## priority_level

Used for tasks and future routing.

Values:

```text
low
normal
high
urgent
```

---

# 18. Object Type Values

Polymorphic object references may use controlled object type strings.

Common values:

```text
company_workspace
operating_map
operating_gap
function
responsibility
ownership_gap
agent
agent_recommendation
agent_action_draft
process
process_step
task
decision
memory_entry
audit_event
runtime_event
integration
integration_sync_job
security_policy
dashboard_metric
export_job
user_input
system
```

These values may appear in:

```text
source_object_type
object_type
resolved_by_object_type
result_object_type
suggested_object_type
used_by_object_type
```

---

# 19. Status Transition Notes

Service layer should enforce valid transitions.

Examples:

```text
task: suggested → open → in_progress → completed → archived
memory: candidate → active → archived
decision: draft → confirmed → implemented → archived
export_job: requested → generating → completed
export_job: requested → generating → failed
integration: configured → active → paused → revoked
```

Database may validate allowed values, but service logic should validate transitions.

---

# 20. Database Constraint Strategy

Recommended MVP strategy:

```text
Use TEXT columns.
Validate through backend services.
Centralize enum definitions in code.
```

Recommended hardening strategy:

```text
Add CHECK constraints for stable statuses.
Use PostgreSQL ENUM for highly stable values.
Use reference tables for values that may be managed by admin UI.
```

Potential PostgreSQL ENUM candidates:

```text
task_status
task_priority
decision_status
memory_status
runtime_event_status
export_status
```

Potential reference table candidates:

```text
function_category
memory_type
export_type
integration_provider
```

---

# 21. Anti-Patterns to Avoid

Avoid:

```text
arbitrary status strings
multiple names for same state
mixing lifecycle status with category
using status to represent ownership
using status to hide errors
changing enum values without migration plan
storing UI labels instead of stable internal values
```

---

# 22. Acceptance Criteria

Enums and Statuses are ready when:

- core entity statuses are defined;
- MVP values are separated from expansion values;
- shared severity and priority values are defined;
- object type values are listed;
- database constraint strategy is documented;
- service-level transition responsibility is clear.

Status:

```text
Accepted for Indexing Strategy and Implementation Planning
```

---

# 23. Final Statement

```text
Bizzi Enums and Statuses define the controlled vocabulary of the data model, ensuring that lifecycle state, priority, severity, object references and runtime classifications remain consistent, queryable and implementation-ready.
```

This catalog becomes the reference for database constraints, API validation and backend service logic.