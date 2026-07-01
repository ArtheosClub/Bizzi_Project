# 02_BACKEND_MODULE_CATALOG.md

# Bizzi Platform

## Backend Module Catalog

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Previous Document:** 01_BACKEND_ARCHITECTURE_PRINCIPLES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend module catalog for Bizzi Platform.

It identifies the canonical backend modules, their service responsibilities, repository boundaries, dependency rules and implementation priority for the `29_BACKEND_SERVICE_DESIGN` layer.

Core question:

```text
Which backend modules must Bizzi define so that API contracts can be implemented as secure, workspace-scoped, auditable and AI-safe services?
```

---

# 2. Module Catalog Role

The Backend Module Catalog is the bridge between:

```text
API Contracts
↓
Backend services
↓
Repositories
↓
Database tables
↓
Runtime behavior
```

It provides a single reference for:

- backend module naming;
- service grouping;
- repository grouping;
- dependency direction;
- MVP priority;
- audit and runtime event responsibility;
- future implementation planning.

---

# 3. Backend Module Naming Rules

Backend modules should use clear singular domain names.

Recommended pattern:

```text
<DomainName>Module
```

Examples:

```text
WorkspaceModule
TaskModule
DecisionModule
MemoryModule
AuditModule
EventModule
IntegrationModule
ExportModule
```

Services should use:

```text
<DomainName>Service
```

Repositories should use:

```text
<DomainName>Repository
```

---

# 4. Module Priority Levels

Priority levels:

```text
P1 — MVP core backend module
P2 — governed runtime module
P3 — expansion and enterprise module
```

Definitions:

```text
P1 supports the first runnable Bizzi vertical slice.
P2 supports governed AI, integrations, access control and deeper execution.
P3 supports enterprise hardening, advanced collaboration, analytics and public API expansion.
```

---

# 5. Canonical Backend Modules

Initial backend modules:

```text
SharedKernelModule
IdentityModule
WorkspaceModule
OperatingMapModule
FunctionResponsibilityModule
AgentModule
ProcessModule
TaskModule
DecisionModule
MemoryModule
AuditModule
EventModule
IntegrationModule
SecurityModule
DashboardModule
ExportModule
```

Supporting modules:

```text
AuthorizationModule
ValidationModule
TransactionModule
IdempotencyModule
JobQueueModule
SecretReferenceModule
NotificationModule later
ObservabilityModule later
```

---

# 6. Module Catalog Summary

| Module | Priority | Main API Families | Main Data Tables |
|---|---:|---|---|
| SharedKernelModule | P1 | all | shared types only |
| IdentityModule | P1 | me | users, sessions |
| WorkspaceModule | P1 | workspaces, workspace-settings | company_workspaces, workspace_settings, workspace_access |
| OperatingMapModule | P1 | operating-maps, operating-gaps | operating_maps, operating_gaps |
| FunctionResponsibilityModule | P1 | functions, responsibilities | functions, responsibilities, ownership_gaps |
| TaskModule | P1 | tasks | tasks |
| DecisionModule | P1 | decisions | decisions |
| MemoryModule | P1 | memory-entries | memory_entries |
| AuditModule | P1 | audit-events | audit_events |
| EventModule | P1 | runtime-events | runtime_events |
| DashboardModule | P1 | dashboard, dashboard-metrics | dashboard_metrics |
| ExportModule | P1/P2 | export-jobs | export_jobs |
| AgentModule | P2 | agents, recommendations, drafts | agents, agent_recommendations, agent_action_drafts |
| ProcessModule | P2 | processes, process-steps | processes, process_steps |
| IntegrationModule | P2 | integrations, sync jobs | integrations, integration_sync_jobs |
| SecurityModule | P2 | security-policies, workspace-access | security_policies, workspace_access |

---

# 7. SharedKernelModule

## Purpose

Provide shared backend primitives that are used across modules.

## Contains

```text
ActorContext
WorkspaceContext
CorrelationContext
ServiceError types
Result types
Pagination types
Filter types
Sort types
Audit action constants
Runtime event constants
Object reference types
Status value constants
```

## Rule

```text
SharedKernelModule should contain stable cross-cutting primitives, not feature business logic.
```

## Priority

```text
P1
```

---

# 8. IdentityModule

## Purpose

Manage authenticated user identity and session-related backend behavior.

## Services

```text
IdentityService
SessionService later
```

## Repositories

```text
UserRepository
SessionRepository
```

## Responsibilities

```text
load current user
validate user status
provide actor context
support /me endpoint
support workspace discovery with WorkspaceModule
```

## Priority

```text
P1
```

---

# 9. WorkspaceModule

## Purpose

Manage workspace lifecycle, settings and workspace access entry points.

## Services

```text
WorkspaceService
WorkspaceSettingsService
WorkspaceAccessService
```

## Repositories

```text
WorkspaceRepository
WorkspaceSettingsRepository
WorkspaceAccessRepository
```

## Responsibilities

```text
create workspace
read workspace
update workspace
archive workspace
manage workspace settings
list user workspaces
support workspace access expansion
emit workspace audit events
emit workspace runtime events
```

## API Reference

```text
28_API_CONTRACTS/03_WORKSPACE_API.md
```

## Priority

```text
P1
```

---

# 10. OperatingMapModule

## Purpose

Manage operating maps, operating gaps and operating recommendations.

## Services

```text
OperatingMapService
OperatingGapService
OperatingRecommendationService later
```

## Repositories

```text
OperatingMapRepository
OperatingGapRepository
OperatingRecommendationRepository later
```

## Responsibilities

```text
generate operating map
confirm operating map
archive operating map
list operating gaps
accept operating gaps
resolve operating gaps
archive operating gaps
emit operating map events
emit dashboard refresh events
```

## Priority

```text
P1 for maps and gaps
P2 for recommendations
```

---

# 11. FunctionResponsibilityModule

## Purpose

Manage business functions, responsibilities and ownership gaps.

## Services

```text
FunctionService
ResponsibilityService
OwnershipGapService later
```

## Repositories

```text
FunctionRepository
ResponsibilityRepository
OwnershipGapRepository later
```

## Responsibilities

```text
create function
update function
archive function
assign responsibility
reassign responsibility
archive responsibility
resolve ownership gaps
maintain ownership traceability
emit dashboard refresh events
```

## Priority

```text
P1 for functions and responsibilities
P2 for ownership gaps
```

---

# 12. AgentModule

## Purpose

Manage AI agents, authority scopes, recommendations and action drafts.

## Services

```text
AgentService
AgentAuthorityService
AgentRecommendationService
AgentActionDraftService
```

## Repositories

```text
AgentRepository
AgentAuthorityScopeRepository
AgentRecommendationRepository
AgentActionDraftRepository
```

## Responsibilities

```text
configure agents
validate agent authority
record recommendations
confirm recommendations
apply recommendations under policy
reject recommendations
manage action drafts
preserve AI traceability
```

## Priority

```text
P2
```

---

# 13. ProcessModule

## Purpose

Manage repeatable business processes and ordered process steps.

## Services

```text
ProcessService
ProcessStepService
```

## Repositories

```text
ProcessRepository
ProcessStepRepository
```

## Responsibilities

```text
create processes
activate processes
archive processes
create process steps
reorder process steps later
archive process steps
connect processes to functions and tasks
```

## Priority

```text
P2
```

---

# 14. TaskModule

## Purpose

Manage actionable workspace work items.

## Services

```text
TaskService
TaskLifecycleService
```

## Repositories

```text
TaskRepository
```

## Responsibilities

```text
create task
update task
start task
complete task
archive task
validate task ownership
emit task audit events
emit task runtime events
trigger dashboard refresh
create memory candidates when appropriate
```

## Priority

```text
P1
```

---

# 15. DecisionModule

## Purpose

Manage business decisions and confirmation workflows.

## Services

```text
DecisionService
DecisionConfirmationService
```

## Repositories

```text
DecisionRepository
```

## Responsibilities

```text
create decision
update decision
confirm decision
archive decision
validate decision source objects
require human confirmation for AI decisions
emit decision audit events
emit decision runtime events
create memory candidates when appropriate
```

## Priority

```text
P1
```

---

# 16. MemoryModule

## Purpose

Manage workspace memory entries and active AI context eligibility.

## Services

```text
MemoryService
MemoryActivationService
MemoryContextService later
```

## Repositories

```text
MemoryRepository
MemorySourceRepository later
MemoryUsageRepository later
```

## Responsibilities

```text
create memory entries
update memory entries
activate memory entries
archive memory entries
ensure archived memory is not active AI context
validate source traceability
support memory retrieval
```

## Priority

```text
P1 for memory entries
P3 for semantic context and usage tracking
```

---

# 17. AuditModule

## Purpose

Provide canonical audit event creation and authorized audit reads.

## Services

```text
AuditService
AuditQueryService
AuditExportService later
```

## Repositories

```text
AuditEventRepository
AuditExportRepository later
```

## Responsibilities

```text
create audit events
standardize audit payloads
record actor and object references
record AI flags
record correlation IDs
serve authorized audit event reads
protect audit immutability
```

## Priority

```text
P1
```

---

# 18. EventModule

## Purpose

Manage runtime events used for internal coordination.

## Services

```text
RuntimeEventService
EventDispatchService later
EventHandlerService later
```

## Repositories

```text
RuntimeEventRepository
EventFailureRepository later
EventHandlerRunRepository later
```

## Responsibilities

```text
create runtime events
store event payloads safely
link correlation and causation IDs
dispatch events later
track processing status
serve restricted runtime event reads
```

## Priority

```text
P1 minimal event creation
P2 event handling and retries
```

---

# 19. IntegrationModule

## Purpose

Manage external integrations and sync jobs.

## Services

```text
IntegrationService
IntegrationSyncService
ProviderAdapterService
```

## Repositories

```text
IntegrationRepository
IntegrationSyncJobRepository
```

## Responsibilities

```text
create integrations using credential_ref
update integration configuration
trigger sync jobs
revoke integrations
validate provider scopes
coordinate secret resolution through SecretReferenceModule
emit integration audit and runtime events
```

## Priority

```text
P2
```

---

# 20. SecurityModule

## Purpose

Manage workspace security policies and access governance.

## Services

```text
SecurityPolicyService
WorkspaceAccessService
AccessReviewService later
```

## Repositories

```text
SecurityPolicyRepository
WorkspaceAccessRepository
```

## Responsibilities

```text
manage security policies
validate AI action policies
manage workspace access
protect last owner
support role expansion
emit security audit events
```

## Priority

```text
P2
```

---

# 21. DashboardModule

## Purpose

Compute and expose workspace operational visibility.

## Services

```text
DashboardService
DashboardMetricService
DashboardActivityService
```

## Repositories

```text
DashboardMetricRepository
AuditEventRepository read dependency
RuntimeEventRepository read dependency
TaskRepository read dependency
DecisionRepository read dependency
```

## Responsibilities

```text
compute dashboard summary
read dashboard metrics
refresh metrics
show activity
combine dynamic and persisted values
respect authorization
```

## Priority

```text
P1
```

---

# 22. ExportModule

## Purpose

Manage governed export job lifecycle.

## Services

```text
ExportService
ExportJobService
ExportFileService later
```

## Repositories

```text
ExportJobRepository
ExportFileRepository later
```

## Responsibilities

```text
create export jobs
validate export scope
emit export events
coordinate export workers
create temporary download links
expire export files
preserve export metadata
```

## Priority

```text
P1/P2
```

---

# 23. AuthorizationModule

## Purpose

Centralize authorization decisions.

## Services

```text
AuthorizationService
WorkspacePermissionService
AgentAuthorityPolicyService
ExportPermissionService
```

## Responsibilities

```text
check workspace access
check owner/admin roles
check resource ownership
check agent authority
check integration scope
check export scope
protect restricted audit/runtime visibility
```

## Priority

```text
P1 owner-only authorization
P2 role expansion
```

---

# 24. ValidationModule

## Purpose

Centralize shared validation utilities and policy validators.

## Services

```text
ValidationService
ObjectReferenceValidator
StatusTransitionValidator
SourceObjectValidator
BusinessRuleValidator
```

## Responsibilities

```text
validate required fields not covered by schema
validate object references
validate workspace ownership
validate status transitions
validate source/result/resolution references
validate business rules
```

## Priority

```text
P1
```

---

# 25. Supporting Infrastructure Modules

## TransactionModule

Purpose:

```text
Provide transaction boundaries for meaningful state changes.
```

## IdempotencyModule

Purpose:

```text
Prevent duplicate effects for retryable operations.
```

## SecretReferenceModule

Purpose:

```text
Resolve credential_ref inside secure execution boundaries.
```

## JobQueueModule

Purpose:

```text
Coordinate background work such as exports, sync jobs and AI analysis.
```

---

# 26. Dependency Direction Rules

Recommended dependency direction:

```text
Controllers → Application Services → Repositories
Application Services → Authorization / Validation / Audit / Event services
Feature Services → SharedKernel
Repositories → Database
```

Avoid:

```text
Repositories calling services
Controllers calling repositories directly
Feature modules bypassing authorization
Feature modules writing audit events inconsistently
Circular module dependencies
```

---

# 27. MVP Module Set

Minimum MVP backend module set:

```text
SharedKernelModule
IdentityModule
WorkspaceModule
OperatingMapModule
FunctionResponsibilityModule
TaskModule
DecisionModule
MemoryModule
AuditModule
EventModule
DashboardModule
ExportModule
AuthorizationModule
ValidationModule
TransactionModule
```

P2 modules may be partially stubbed:

```text
AgentModule
ProcessModule
IntegrationModule
SecurityModule
IdempotencyModule
JobQueueModule
SecretReferenceModule
```

---

# 28. Module Anti-Patterns

Avoid:

```text
one giant backend service
repositories with business decisions
controllers with domain logic
cross-module writes without service ownership
shared kernel containing feature logic
feature modules accessing secrets directly
AI recommendation application outside AgentModule policy
runtime events emitted without correlation_id
audit events emitted with inconsistent action names
```

---

# 29. Acceptance Criteria

Backend Module Catalog is accepted when:

- canonical backend modules are listed;
- module priority levels are defined;
- module responsibilities are documented;
- service and repository names are identified;
- dependency direction rules are defined;
- MVP module set is identified;
- supporting infrastructure modules are defined;
- anti-patterns are documented.

Status:

```text
Accepted for Controller Service Repository Pattern
```

---

# 30. Final Statement

```text
Bizzi Backend Module Catalog defines the canonical backend module map that turns API contracts into organized, workspace-scoped, auditable and AI-safe service architecture.
```

This catalog becomes the roadmap for detailed backend service design documents in the `29_BACKEND_SERVICE_DESIGN` layer.