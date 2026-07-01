# 07_AGENT_PROCESS_TASK_DECISION_SERVICE_DESIGN.md

# Bizzi Platform

## Agent Process Task Decision Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 06_AGENT_PROCESS_TASK_DECISION_API.md  
**Previous Document:** 06_FUNCTION_RESPONSIBILITY_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for agent, process, task and decision behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, transaction patterns, audit events and runtime events required to implement the Agent Process Task Decision API.

Core question:

```text
How should Bizzi backend services govern AI assistance, repeatable processes, actionable tasks and accountable decisions safely and consistently?
```

---

# 2. Service Scope

This design covers:

```text
AgentService
AgentAuthorityService
AgentRecommendationService
AgentActionDraftService
ProcessService
ProcessStepService
TaskService
TaskLifecycleService
DecisionService
DecisionConfirmationService
```

Primary API families:

```text
agents
agent-authority-scopes
agent-recommendations
agent-action-drafts
processes
process-steps
tasks
decisions
```

Primary data references:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
tasks
decisions
functions
responsibilities
memory_entries
audit_events
runtime_events
```

---

# 3. Module Ownership

Execution behavior is distributed across:

```text
AgentModule
ProcessModule
TaskModule
DecisionModule
```

Supporting modules:

```text
WorkspaceModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
FunctionResponsibilityModule
MemoryModule via runtime events
DashboardModule via runtime events
TransactionModule
IdempotencyModule optional
```

Rule:

```text
TaskModule and DecisionModule own MVP execution. AgentModule and ProcessModule add governed runtime depth.
```

---

# 4. MVP Priority

MVP backend priority:

```text
P1 — TaskService
P1 — DecisionService
P1 — Audit and runtime event emission for tasks and decisions
P2 — Agent recommendations and action drafts
P2 — Process and process steps
P2 — Agent authority scopes
```

MVP may implement AgentModule and ProcessModule as minimal stubs if full behavior is not yet needed.

---

# 5. Service Responsibilities

## AgentService

Responsibilities:

```text
list agents
create agents
update agent configuration
archive agents
validate agent_type and authority_level
preserve agent lifecycle auditability
```

## AgentAuthorityService

Responsibilities:

```text
validate whether an agent may recommend, draft or apply an action
check workspace policy
check restricted action types
require human confirmation when needed
return authority decision result
```

## AgentRecommendationService

Responsibilities:

```text
list recommendations
create recommendations from AI or analysis flows
confirm recommendations
apply recommendations through target services
reject recommendations
record result object references
preserve AI traceability
```

## AgentActionDraftService

Responsibilities:

```text
store AI-generated draft actions
validate draft payloads
approve drafts
apply approved drafts through target services
reject drafts
ensure drafts are not official state before application
```

## ProcessService

Responsibilities:

```text
list processes
create processes
update processes
activate processes
archive processes
validate function and owner references
```

## ProcessStepService

Responsibilities:

```text
list process steps
create process steps
update process steps
archive process steps
validate step order
```

## TaskService

Responsibilities:

```text
list tasks
get task
create task
update task
archive task
validate task references
emit task audit and runtime events
```

## TaskLifecycleService

Responsibilities:

```text
start task
complete task
validate task status transitions
set completed_at
trigger dashboard refresh
optionally trigger memory candidate creation
```

## DecisionService

Responsibilities:

```text
list decisions
get decision
create decision
update decision
archive decision
validate decision references
emit decision audit and runtime events
```

## DecisionConfirmationService

Responsibilities:

```text
confirm decision
validate human confirmation requirement
set decision_date
set confirmed_by and confirmed_at
trigger dashboard refresh
optionally trigger memory candidate creation
```

---

# 6. Repository Responsibilities

## AgentRepository

```text
createAgent(data)
findByIdAndWorkspace(agent_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(agent_id, workspace_id, patch)
archiveByIdAndWorkspace(agent_id, workspace_id, archive_data)
```

## AgentAuthorityScopeRepository

```text
listByAgent(agent_id, workspace_id)
findMatchingScope(workspace_id, agent_id, action_type, object_type)
createScope(data)
archiveScope(scope_id, workspace_id, archive_data)
```

## AgentRecommendationRepository

```text
createRecommendation(data)
findByIdAndWorkspace(recommendation_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
markConfirmed(recommendation_id, workspace_id, confirmation_data)
markApplied(recommendation_id, workspace_id, result_data)
markRejected(recommendation_id, workspace_id, rejection_data)
```

## AgentActionDraftRepository

```text
createDraft(data)
findByIdAndWorkspace(draft_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
markApproved(draft_id, workspace_id, approval_data)
markApplied(draft_id, workspace_id, result_data)
markRejected(draft_id, workspace_id, rejection_data)
```

## ProcessRepository

```text
createProcess(data)
findByIdAndWorkspace(process_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(process_id, workspace_id, patch)
activateByIdAndWorkspace(process_id, workspace_id, activation_data)
archiveByIdAndWorkspace(process_id, workspace_id, archive_data)
```

## ProcessStepRepository

```text
createStep(data)
findByIdAndWorkspace(step_id, workspace_id)
listByProcess(workspace_id, process_id, pagination)
updateByIdAndWorkspace(step_id, workspace_id, patch)
archiveByIdAndWorkspace(step_id, workspace_id, archive_data)
getNextStepOrder(workspace_id, process_id)
```

## TaskRepository

```text
createTask(data)
findByIdAndWorkspace(task_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(task_id, workspace_id, patch)
setStatus(task_id, workspace_id, status_data)
archiveByIdAndWorkspace(task_id, workspace_id, archive_data)
```

## DecisionRepository

```text
createDecision(data)
findByIdAndWorkspace(decision_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(decision_id, workspace_id, patch)
confirmByIdAndWorkspace(decision_id, workspace_id, confirmation_data)
archiveByIdAndWorkspace(decision_id, workspace_id, archive_data)
```

---

# 7. Service Context

Every service method must receive:

```text
workspace_id
actor_id
actor_type
correlation_id
request_id
idempotency_key optional
```

For AI-assisted operations, context should also carry:

```text
agent_id optional
ai_assisted boolean
human_confirmed boolean
source_event_id optional
```

Rule:

```text
Agent, process, task and decision services must load all records by id and workspace_id.
```

---

# 8. Agent Create and Update Flow

## Create Agent

```text
AgentService.createAgent(context, input)
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check manage agent permission
validate name
validate agent_type
validate authority_level
begin transaction
create agent
record agent.created audit event
emit agent.created runtime event
commit transaction
return agent DTO
```

## Update Agent

```text
AgentService.updateAgent(context, agent_id, input)
```

Flow:

```text
load agent by id and workspace_id
check update permission
validate mutable fields
capture before_state
begin transaction
update agent
record agent.updated audit event
emit agent.updated runtime event
commit transaction
return agent DTO
```

---

# 9. Agent Recommendation Flow

## Confirm Recommendation

```text
AgentRecommendationService.confirmRecommendation(context, recommendation_id, input)
```

Flow:

```text
validate authenticated actor
check workspace access
load recommendation by id and workspace_id
validate recommendation is confirmable
begin transaction
set status confirmed
set confirmed_by
set confirmed_at
record agent_recommendation.confirmed audit event
emit agent_recommendation.confirmed runtime event
commit transaction
return recommendation DTO
```

## Apply Recommendation

```text
AgentRecommendationService.applyRecommendation(context, recommendation_id, input)
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
load recommendation
validate status is confirmed or application-compatible
validate agent authority
validate human confirmation unless automation authority allows direct application
resolve target service by recommendation_type
begin transaction
create or update result object through target service or controlled internal operation
mark recommendation applied
record result_object_type and result_object_id
record agent_recommendation.applied audit event
emit agent_recommendation.applied runtime event
commit transaction
return recommendation DTO
```

## Reject Recommendation

```text
AgentRecommendationService.rejectRecommendation(context, recommendation_id, input)
```

Flow:

```text
load recommendation
validate not already applied or rejected
begin transaction
set status rejected
record agent_recommendation.rejected audit event
emit agent_recommendation.rejected runtime event
commit transaction
return recommendation DTO
```

Rule:

```text
Recommendations are not official business state until applied by backend service under policy.
```

---

# 10. Agent Action Draft Flow

Drafts represent proposed state changes.

## Apply Draft

```text
AgentActionDraftService.applyDraft(context, draft_id, input)
```

Flow:

```text
load draft by id and workspace_id
validate draft is approved or apply-compatible
validate draft payload against target operation schema
validate agent authority
validate human confirmation unless automation authority allows direct application
begin transaction
execute target operation
mark draft applied
record result_object_type and result_object_id
record agent_action_draft.applied audit event
emit agent_action_draft.applied runtime event
commit transaction
return draft DTO
```

Rule:

```text
Draft payloads must be revalidated before application.
```

---

# 11. Process Create and Activate Flow

## Create Process

```text
ProcessService.createProcess(context, input)
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check create process permission
validate name
validate function_id belongs to workspace if provided
validate owner_user_id exists if provided
validate source object if provided
begin transaction
create process with draft status
record process.created audit event
emit process.created runtime event
commit transaction
return process DTO
```

## Activate Process

```text
ProcessService.activateProcess(context, process_id, input)
```

Flow:

```text
load process by id and workspace_id
validate status allows activation
check activation permission
begin transaction
set status active
record process.activated audit event
emit process.activated runtime event
commit transaction
return process DTO
```

---

# 12. Process Step Flow

## Create Step

```text
ProcessStepService.createStep(context, process_id, input)
```

Flow:

```text
validate authenticated actor
load process by id and workspace_id
check process is not archived
check manage process permission
validate title
assign step_order if omitted
begin transaction
create process step
record process_step.created audit event
emit process_step.created runtime event
commit transaction
return step DTO
```

Rule:

```text
Process steps belong to the same workspace as their parent process.
```

---

# 13. Create Task Flow

## Service Method

```text
TaskService.createTask(context, input)
```

## Input

```text
title
description optional
function_id optional
process_id optional
owner_user_id optional
agent_id optional
priority optional
due_date optional
source_object_type optional
source_object_id optional
metadata optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check create task permission
validate title
validate priority if provided
validate due_date if provided
validate function_id belongs to workspace if provided
validate process_id belongs to workspace if provided
validate owner_user_id exists and has access when required
validate source object if provided
begin transaction
create task with open status
record task.created audit event
emit task.created runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return task DTO
```

---

# 14. Update Task Flow

```text
TaskService.updateTask(context, task_id, input)
```

Mutable fields:

```text
title
description
function_id
process_id
owner_user_id
priority
due_date
metadata
```

Flow:

```text
load task by id and workspace_id
check task is not archived
check update task permission
validate mutable fields
capture before_state
begin transaction
update task
record task.updated audit event
emit task.updated runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return task DTO
```

---

# 15. Start Task Flow

```text
TaskLifecycleService.startTask(context, task_id, input)
```

Flow:

```text
load task by id and workspace_id
check start permission
validate task status allows start
capture before_state
begin transaction
set status in_progress
record task.started audit event
emit task.status_changed runtime event
commit transaction
return task DTO
```

Allowed MVP transition:

```text
open → in_progress
```

---

# 16. Complete Task Flow

```text
TaskLifecycleService.completeTask(context, task_id, input)
```

Input:

```text
completion_note optional
result_summary optional
```

Flow:

```text
load task by id and workspace_id
check complete permission
validate task status allows completion
capture before_state
begin transaction
set status completed
set completed_at
record task.completed audit event
emit task.completed runtime event
emit dashboard.refresh_requested runtime event
optionally emit memory.candidate_created runtime event
commit transaction
return task DTO
```

Allowed MVP transitions:

```text
open → completed
in_progress → completed
```

---

# 17. Archive Task Flow

```text
TaskService.archiveTask(context, task_id, input)
```

Flow:

```text
load task by id and workspace_id
check archive permission
check task is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record task.archived audit event
emit task.archived runtime event
emit dashboard.refresh_requested runtime event
commit transaction
return task DTO
```

Rule:

```text
Archiving a task preserves execution history.
```

---

# 18. Create Decision Flow

```text
DecisionService.createDecision(context, input)
```

Input:

```text
title
description optional
decision_type optional
task_id optional
function_id optional
owner_user_id optional
agent_id optional
source_object_type optional
source_object_id optional
metadata optional
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check create decision permission
validate title
validate decision_type if provided
validate task_id belongs to workspace if provided
validate function_id belongs to workspace if provided
validate owner_user_id exists if provided
validate source object if provided
begin transaction
create decision with draft status
record decision.created audit event
emit decision.created runtime event
commit transaction
return decision DTO
```

---

# 19. Confirm Decision Flow

```text
DecisionConfirmationService.confirmDecision(context, decision_id, input)
```

Input:

```text
confirmation_note optional
decision_date optional
```

Flow:

```text
load decision by id and workspace_id
check confirm permission
validate decision is not archived
validate status allows confirmation
if AI-generated, validate human confirmation or automation authority
capture before_state
begin transaction
set status confirmed
set decision_date
set confirmed_by
set confirmed_at
record decision.confirmed audit event with human_confirmed flag
emit decision.confirmed runtime event
emit dashboard.refresh_requested runtime event
optionally emit memory.candidate_created runtime event
commit transaction
return decision DTO
```

Rule:

```text
Confirmed decisions become official business evidence and must be auditable.
```

---

# 20. Archive Decision Flow

```text
DecisionService.archiveDecision(context, decision_id, input)
```

Flow:

```text
load decision by id and workspace_id
check archive permission
check decision is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record decision.archived audit event
emit decision.archived runtime event
commit transaction
return decision DTO
```

---

# 21. Authorization Rules

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| Manage agents | workspace owner | owner/admin |
| Confirm recommendation | workspace owner | owner/admin/manager |
| Apply recommendation | workspace owner | role + agent authority + confirmation |
| Manage processes | workspace owner | owner/admin/manager |
| Create task | workspace owner | owner/admin/manager/member with permission |
| Update task | workspace owner | owner/admin/assigned user |
| Start task | workspace owner | owner/admin/assigned user |
| Complete task | workspace owner | owner/admin/assigned user |
| Archive task | workspace owner | owner/admin/manager |
| Create decision | workspace owner | owner/admin/manager |
| Confirm decision | workspace owner | owner/admin/authorized decision owner |
| Archive decision | workspace owner | owner/admin/manager |

---

# 22. Validation Rules

Common validation rules:

```text
workspace must exist
workspace must be active for mutations
referenced function must belong to workspace
referenced process must belong to workspace
referenced task must belong to workspace
referenced decision must belong to workspace
owner_user_id must exist
agent_id must belong to workspace when supplied
source object must belong to workspace when workspace-scoped
status transition must be allowed
AI-generated official actions require confirmation or authority
```

---

# 23. Audit Events

Services should emit:

```text
agent.created
agent.updated
agent.archived
agent_recommendation.created
agent_recommendation.confirmed
agent_recommendation.applied
agent_recommendation.rejected
agent_action_draft.created
agent_action_draft.approved
agent_action_draft.applied
agent_action_draft.rejected
process.created
process.updated
process.activated
process.archived
process_step.created
process_step.updated
process_step.archived
task.created
task.updated
task.started
task.completed
task.archived
decision.created
decision.updated
decision.confirmed
decision.archived
```

Audit payload should include:

```text
workspace_id
actor_id
actor_type
agent_id optional
action
object_type
object_id
source_object_type optional
source_object_id optional
before_state optional
after_state optional
ai_assisted
human_confirmed
correlation_id
```

---

# 24. Runtime Events

Services should emit:

```text
agent.created
agent.updated
agent.archived
agent_recommendation.confirmed
agent_recommendation.applied
agent_recommendation.rejected
process.created
process.activated
process.archived
task.created
task.updated
task.status_changed
task.completed
task.archived
decision.created
decision.confirmed
decision.archived
dashboard.refresh_requested
memory.candidate_created optional
```

Runtime events may trigger:

```text
dashboard refresh
memory candidate generation
agent follow-up
notification later
process analytics later
```

---

# 25. DTOs

Task DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "function_id": "uuid",
  "process_id": "uuid",
  "owner_user_id": "uuid",
  "agent_id": "uuid",
  "title": "Review supplier contract",
  "status": "open",
  "priority": "normal",
  "due_date": "2026-07-15",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

Decision DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "task_id": "uuid",
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "agent_id": "uuid",
  "title": "Approve supplier contract",
  "decision_type": "approval",
  "status": "confirmed",
  "decision_date": "2026-07-01",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T12:00:00Z"
}
```

Agent Recommendation DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "agent_id": "uuid",
  "recommendation_type": "create_task",
  "title": "Create task to review finance ownership",
  "status": "created",
  "confidence": "medium",
  "result_object_type": null,
  "result_object_id": null
}
```

---

# 26. Error Mapping

Service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
AgentNotFound → not_found
ProcessNotFound → not_found
TaskNotFound → not_found
DecisionNotFound → not_found
RecommendationNotFound → not_found
AccessDenied → forbidden
InvalidObjectReference → invalid_object_reference
InvalidSourceObject → invalid_source_object
InvalidStatusTransition → invalid_status_transition
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
DuplicateApplication → conflict
InvalidTaskPriority → validation_error
InvalidDecisionType → validation_error
```

---

# 27. MVP Simplifications

MVP may simplify by:

```text
implementing tasks and decisions before agents and processes
owner-only authorization
simple task statuses
simple decision statuses
no task comments or history table
no process engine
agent recommendations stored but not automatically applied
all AI-generated official state requires human confirmation
synchronous service operations for small workloads
```

MVP must preserve:

```text
workspace scope
auditability
runtime event emission
AI confirmation rules
source traceability
status transition validation
structured error mapping
```

---

# 28. Future Expansion

Future service expansion may add:

```text
task comments
task history
task dependencies
automated assignment
decision options
decision outcomes
decision review workflow
process versioning
process execution runs
agent run logs
agent performance metrics
authority simulations
bulk task creation
```

---

# 29. Testing Expectations

Service tests should cover:

```text
create task validates references
start task validates status transition
complete task emits audit and dashboard event
archive task preserves history
create decision validates source object
confirm decision requires human confirmation when AI-assisted
apply recommendation requires authority and confirmation
apply recommendation records result object
create process validates function reference
activate process validates lifecycle
agent update emits audit event
workspace archived blocks mutations
all mutations emit audit and runtime events
```

Repository tests should cover:

```text
list tasks by workspace and filters
find task by id and workspace
list decisions by workspace and filters
confirm decision by id and workspace
list recommendations by workspace
mark recommendation applied
list processes and steps by workspace
pagination and sorting behavior
```

---

# 30. Acceptance Criteria

Agent Process Task Decision Service Design is accepted when:

- Agent services are defined;
- Process services are defined;
- Task services are defined;
- Decision services are defined;
- repository methods are identified;
- task lifecycle flows are documented;
- decision confirmation flow is documented;
- AI recommendation and draft flows are documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- DTOs and error mappings are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Memory Audit Event Service Design
```

---

# 31. Final Statement

```text
Bizzi Agent Process Task Decision Service Design defines how backend services turn AI assistance, repeatable processes, actionable work and confirmed decisions into governed, auditable and AI-safe platform execution.
```

This service layer is the execution core of Bizzi Platform.