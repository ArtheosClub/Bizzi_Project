# 00_BACKEND_SERVICE_DESIGN_VISION.md

# Bizzi Platform

## Backend Service Design Vision

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Previous Layer:** 28_API_CONTRACTS / 13_API_CONTRACTS_AUDIT.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the vision for the `29_BACKEND_SERVICE_DESIGN` layer of Bizzi Platform.

It establishes how backend services should implement the API contracts, enforce business rules, coordinate data access, validate workspace boundaries, emit audit and runtime events, and support AI-safe platform execution.

Core question:

```text
How should Bizzi backend services be designed so that API contracts become reliable, secure, auditable and implementation-ready platform behavior?
```

---

# 2. Backend Service Design Layer Role

The Backend Service Design layer translates API contracts into service responsibilities.

It defines:

- backend module boundaries;
- service ownership;
- controller-to-service flow;
- repository responsibilities;
- transaction boundaries;
- validation responsibilities;
- authorization enforcement;
- audit event emission;
- runtime event emission;
- AI authority enforcement;
- integration service responsibilities;
- export job coordination;
- dashboard computation responsibilities;
- implementation sequencing.

This layer does not yet implement code. It defines how code should be structured.

---

# 3. Position in Architecture

Canonical flow:

```text
Product Definition
↓
Runtime Platform
↓
Domain Model
↓
Data Model
↓
API Contracts
↓
Backend Service Design
↓
Backend Implementation
↓
Frontend Application
↓
Agent Orchestration
```

Backend Service Design must preserve:

```text
workspace isolation
domain meaning
data integrity
API contract stability
auditability
AI safety
security controls
implementation clarity
```

---

# 4. Backend Thesis

```text
Bizzi backend services must act as the governed execution layer that turns workspace-scoped API requests into validated, authorized, transactional, auditable and AI-safe business operations.
```

---

# 5. Backend Consumers

Backend services are consumed by:

```text
API controllers
web frontend
AI orchestration runtime
integration adapters
export workers
dashboard workers
background job processors
future mobile clients
future public API layer
```

The first consumers are expected to be:

```text
REST API controllers
Bizzi web application
AI-assisted internal service calls
```

---

# 6. Core Backend Responsibilities

Backend services are responsible for:

```text
accepting validated API input
loading authorized workspace context
enforcing domain rules
executing transactional changes
persisting data through repositories
emitting audit events
emitting runtime events
coordinating background jobs
returning stable response DTOs
preventing cross-workspace access
protecting raw secrets
requiring human confirmation where needed
```

---

# 7. Service Design Principles

## 7.1 Workspace Context First

Every operating service method must receive or derive workspace context.

Rule:

```text
No workspace context, no operating service action.
```

## 7.2 Services Own Business Rules

Controllers should not contain core business logic.

Rule:

```text
Controllers route requests. Services enforce behavior.
```

## 7.3 Repositories Own Persistence Details

Services should use repositories to access data.

Rule:

```text
Services express business intent. Repositories implement database access.
```

## 7.4 Transactions Wrap Meaningful State Changes

Important mutations must happen in controlled transaction boundaries.

Rule:

```text
State change, audit event and runtime event intent should be consistent within the same operation.
```

## 7.5 Audit Is Not Optional

Important business changes must create audit evidence.

Rule:

```text
If a change matters to the business, it must be auditable.
```

## 7.6 Runtime Events Coordinate Behavior

Runtime events should coordinate downstream behavior such as dashboard refresh, memory candidates, export jobs and integration sync.

Rule:

```text
Runtime events are coordination signals, not substitutes for audit evidence.
```

## 7.7 AI Is Governed by Backend Services

AI-generated actions must be enforced server-side.

Rule:

```text
The backend must enforce confirmation, authority scope and auditability for AI-assisted actions.
```

---

# 8. Recommended Backend Module Families

Initial backend module families:

```text
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
SharedKernel
```

These modules map directly to API resource families and Data Model table groups.

---

# 9. Backend Layering Model

Recommended internal layering:

```text
Controller Layer
↓
Application Service Layer
↓
Domain Service / Policy Layer
↓
Repository Layer
↓
Database
```

Supporting services:

```text
AuthorizationService
ValidationService
AuditService
RuntimeEventService
IdempotencyService
TransactionManager
SecretReferenceService
JobQueueService
```

---

# 10. Controller Responsibilities

Controllers should:

```text
parse API request
extract authenticated actor
extract workspace_id
call application service
map service result to API response
map service errors to API error contract
```

Controllers should not:

```text
contain domain rules
perform direct database writes
emit audit events directly unless very simple
bypass service authorization
apply AI recommendations directly
```

---

# 11. Application Service Responsibilities

Application services should:

```text
enforce workspace scope
check authorization
validate business rules
coordinate repositories
open transactions
call audit service
call runtime event service
return service DTOs
```

Examples:

```text
WorkspaceService.createWorkspace
OperatingMapService.generateOperatingMap
FunctionService.createFunction
ResponsibilityService.assignResponsibility
TaskService.completeTask
DecisionService.confirmDecision
MemoryService.activateMemory
IntegrationService.triggerSync
ExportService.requestExport
```

---

# 12. Repository Responsibilities

Repositories should:

```text
encapsulate database queries
apply workspace_id filters
load records by id and workspace_id
persist records
support list filters
support pagination
avoid business decision logic
```

Rule:

```text
Repositories may enforce workspace filters, but services remain responsible for business meaning.
```

---

# 13. Transaction Boundary Vision

State-changing operations should use transaction boundaries where needed.

Examples:

```text
create task + audit event + runtime event
confirm decision + audit event + memory candidate event
apply agent recommendation + create result object + audit event + runtime event
request export + create export job + runtime event
```

Rule:

```text
A business operation should either complete coherently or fail safely.
```

---

# 14. Authorization Vision

Authorization must be enforced in backend services.

Initial MVP:

```text
workspace owner access
```

Near-MVP:

```text
workspace_access roles
```

Expansion:

```text
role permissions
resource ownership
agent authority scopes
integration scopes
export scopes
auditor roles
```

Rule:

```text
API clients cannot be trusted to enforce authorization.
```

---

# 15. Validation Vision

Validation occurs in layers:

```text
API schema validation
↓
service business validation
↓
repository existence checks
↓
database constraints
```

Service validation should include:

```text
workspace active check
record belongs to workspace
status transition allowed
referenced object exists
AI confirmation present
agent authority allowed
raw credentials prohibited
export scope allowed
```

---

# 16. Audit Service Vision

AuditService should standardize audit event creation.

Responsibilities:

```text
build audit event payload
record actor context
record object reference
record before_state and after_state when needed
record ai_assisted and human_confirmed flags
record correlation_id
persist audit event
```

Rule:

```text
Services should not handcraft inconsistent audit events.
```

---

# 17. Runtime Event Service Vision

RuntimeEventService should standardize runtime event creation.

Responsibilities:

```text
create runtime events
link source object
assign correlation_id and causation_id
queue downstream processing
record processing status
support retries later
```

Runtime events may trigger:

```text
dashboard refresh
memory candidate creation
export generation
integration sync
notifications later
observability later
```

---

# 18. AI Governance Service Vision

AI-related services must enforce:

```text
recommendation review
draft approval
human confirmation
authority scope
restricted action checks
audit evidence
result object traceability
```

Possible services:

```text
AgentAuthorityService
RecommendationService
ActionDraftService
AIConfirmationPolicy
```

Rule:

```text
AI outputs are not official state until backend services make them official under policy.
```

---

# 19. Integration and Secret Handling Vision

Integration services must never expose raw secrets.

Responsibilities:

```text
accept credential_ref only
validate provider configuration
resolve secrets only inside secure execution boundary
trigger sync jobs
record integration audit events
record sync runtime events
handle revoked integrations safely
```

Rule:

```text
Secrets are resolved at execution time, not stored in normal service DTOs.
```

---

# 20. Dashboard and Export Service Vision

DashboardService should:

```text
compute dashboard summaries
read current metrics
request metric refresh
combine dynamic and persisted values
respect workspace authorization
```

ExportService should:

```text
create export jobs
validate export scope
emit export.requested events
coordinate background export workers
create temporary download references
preserve export metadata
```

---

# 21. Error Handling Vision

Backend services should raise structured service errors that map to API error contracts.

Examples:

```text
ValidationError → validation_error
AuthorizationError → forbidden
NotFoundError → not_found
InvalidStatusTransition → invalid_status_transition
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
CredentialValueNotAllowed → credential_value_not_allowed
```

Rule:

```text
Backend errors must map predictably to 28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md.
```

---

# 22. MVP Backend Scope

MVP backend should implement:

```text
WorkspaceService
WorkspaceSettingsService
OperatingMapService minimal
FunctionService
ResponsibilityService
TaskService
DecisionService
MemoryService minimal
AuditService
RuntimeEventService minimal
DashboardService minimal
ExportService minimal
AuthorizationService owner-only
ValidationService basic
```

MVP may defer:

```text
full RBAC
webhooks
public API keys
advanced process engine
semantic memory search
advanced integration adapters
advanced observability
```

---

# 23. Out of Scope

This vision does not define:

```text
specific programming language
specific backend framework
actual source code
OpenAPI YAML
database migration files
frontend implementation
infrastructure deployment
CI/CD pipeline
cloud provider architecture
```

These belong to later layers.

---

# 24. Expected Layer Deliverables

Expected documents for `29_BACKEND_SERVICE_DESIGN`:

```text
00_BACKEND_SERVICE_DESIGN_VISION.md
01_BACKEND_ARCHITECTURE_PRINCIPLES.md
02_BACKEND_MODULE_CATALOG.md
03_CONTROLLER_SERVICE_REPOSITORY_PATTERN.md
04_WORKSPACE_SERVICE_DESIGN.md
05_OPERATING_MAP_SERVICE_DESIGN.md
06_FUNCTION_RESPONSIBILITY_SERVICE_DESIGN.md
07_AGENT_PROCESS_TASK_DECISION_SERVICE_DESIGN.md
08_MEMORY_AUDIT_EVENT_SERVICE_DESIGN.md
09_INTEGRATION_SECURITY_SERVICE_DESIGN.md
10_DASHBOARD_EXPORT_SERVICE_DESIGN.md
11_AUTHORIZATION_VALIDATION_SERVICES.md
12_TRANSACTION_AND_EVENT_EMISSION.md
13_BACKEND_SERVICE_MILESTONE.md
14_BACKEND_SERVICE_AUDIT.md
```

---

# 25. Acceptance Criteria

Backend Service Design Vision is accepted when:

- role of backend service layer is defined;
- relationship to API Contracts is defined;
- service design principles are documented;
- backend module families are identified;
- controller, service and repository responsibilities are separated;
- transaction, authorization, validation, audit and event visions are defined;
- AI governance responsibilities are defined;
- integration and secret handling rules are defined;
- MVP backend scope is identified;
- expected layer deliverables are listed.

Status:

```text
Accepted for Backend Architecture Principles
```

---

# 26. Final Statement

```text
Bizzi Backend Service Design defines the governed execution architecture that turns API contracts into validated, authorized, transactional, auditable and AI-safe platform behavior.
```

This vision begins the transition from API specification into real backend implementation architecture.