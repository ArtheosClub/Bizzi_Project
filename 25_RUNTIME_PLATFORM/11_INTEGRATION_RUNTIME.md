# 11_INTEGRATION_RUNTIME.md

# Bizzi Platform

## Integration Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md, 08_MEMORY_RUNTIME.md, 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Integration Runtime for Bizzi Platform.

Integration Runtime is responsible for connecting Bizzi to external systems, tools, data sources and future APIs while preserving workspace boundaries, governance, memory, auditability and security.

Core question:

```text
How does Bizzi connect to external tools and data sources without losing control, traceability, security and architectural coherence?
```

---

# 2. Runtime Role

Integration Runtime is the controlled boundary between Bizzi and the external world.

It connects Bizzi to:

- AI providers;
- email systems;
- calendars;
- file storage;
- CRM tools;
- accounting systems;
- task tools;
- messaging systems;
- webhook sources;
- export destinations;
- future public APIs.

---

# 3. Integration Runtime Principle

```text
Integrate Carefully, Govern Always
```

External integrations should not bypass Bizzi governance.

Every integration should be:

- workspace-scoped;
- permissioned;
- auditable;
- traceable;
- revocable;
- limited by purpose;
- safe for AI context use.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
Integration
IntegrationConnection
IntegrationProvider
IntegrationCredential
IntegrationScope
IntegrationEvent
IntegrationSyncJob
IntegrationMapping
IntegrationStatus
```

Supporting objects:

```text
CompanyWorkspace
User
Agent
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
ExportJob
```

---

# 5. Integration Object

## Purpose

Represents an external system or provider connected to a workspace.

## Minimum Fields

```text
id
workspace_id
provider
name
status
created_by
created_at
updated_at
```

## Optional Fields

```text
connection_type
scopes
last_sync_at
credential_ref
configuration
mapping_rules
rate_limit_policy
error_state
```

---

# 6. Integration Lifecycle

```text
Available
↓
Requested
↓
Configured
↓
Connected
↓
Active
↓
Paused
↓
Revoked
↓
Archived
```

## Available

Integration type exists but is not connected.

## Requested

User initiated connection.

## Configured

Settings and scopes are defined.

## Connected

External connection is established.

## Active

Integration can exchange data under governance rules.

## Paused

Integration is temporarily disabled.

## Revoked

Access was removed.

## Archived

Integration record is retained historically.

---

# 7. Integration States

```text
available
requested
configured
connected
active
paused
revoked
archived
error
```

MVP required states:

```text
configured
active
paused
revoked
error
```

---

# 8. Integration Types for MVP

Initial integration types may include:

```text
AI Provider Integration
File Export Integration
Email Import Integration
Calendar Import Integration
Manual Data Import
Webhook Input
```

The MVP should not attempt to support a large integration marketplace.

---

# 9. Core Operations

## 9.1 Register Integration Provider

Defines an available integration provider or integration type.

## 9.2 Configure Integration

Sets workspace-specific configuration, scopes and purpose.

## 9.3 Connect Integration

Establishes connection or credential reference.

## 9.4 Sync Data

Imports or exports data according to integration rules.

## 9.5 Map External Data

Maps external data into Bizzi runtime objects.

## 9.6 Pause Integration

Temporarily disables integration activity.

## 9.7 Revoke Integration

Removes access to the external system.

## 9.8 Record Integration Event

Creates event and audit evidence for integration activity.

---

# 10. Integration Flow

```text
User selects integration
↓
Integration scope is defined
↓
Authorization or configuration is completed
↓
Connection is validated
↓
Integration becomes active
↓
External data is imported or exported
↓
Runtime events are emitted
↓
Audit records are created
↓
Memory or dashboard updates occur if applicable
```

---

# 11. Data Import Flow

```text
External data received
↓
Integration Runtime validates source
↓
Data is normalized
↓
Mapping rules are applied
↓
Draft runtime objects are created if needed
↓
User confirmation required for sensitive changes
↓
Audit event recorded
↓
Memory updated if useful
↓
Dashboard refreshed
```

---

# 12. Data Export Flow

```text
User requests export or integration sends output
↓
Workspace permissions checked
↓
Export data is prepared
↓
Destination scope validated
↓
Export job executed
↓
Audit event recorded
↓
Integration event emitted
```

---

# 13. Integration Events

Minimum events:

```text
integration.configured
integration.connected
integration.activated
integration.paused
integration.revoked
integration.error
integration.sync_started
integration.sync_completed
integration.sync_failed
integration.data_imported
integration.data_exported
integration.mapping_applied
```

Events must include:

```text
event_id
workspace_id
integration_id
actor_id
event_type
timestamp
payload
```

---

# 14. Integration Audit Requirements

Audit events are required for:

- integration configuration;
- connection activation;
- permission scope changes;
- credential changes;
- data import;
- data export;
- sync failures;
- integration pause;
- integration revocation;
- AI use of imported data.

Audit question:

```text
Which external system was connected, what data moved, under which scope, and who authorized it?
```

---

# 15. Integration Memory Integration

Integration Runtime may create memory from:

- imported business context;
- confirmed external records;
- recurring sync patterns;
- integration errors;
- user-confirmed insights from imported data.

Memory types:

```text
integration_context
imported_context
integration_lesson
external_data_summary
sync_issue
```

Memory must remain linked to integration source and workspace.

---

# 16. Integration Dashboard Integration

Dashboard should show:

- active integrations;
- paused integrations;
- integration errors;
- last sync time;
- imported items pending review;
- exported files;
- data sources connected;
- integration-related audit warnings.

Dashboard question:

```text
Which external systems are connected, what data moved, and are there any integration risks?
```

---

# 17. Integration Security Boundary

Integration Runtime must enforce:

```text
Integration belongs to one workspace.
Integration must reference workspace_id.
Credentials must not be exposed in runtime objects.
Scopes must be explicit.
External data must be normalized before use.
Sensitive imported data should require confirmation before becoming memory or decisions.
AI context use of imported data must respect integration scope.
Revoked integrations cannot sync data.
Integration audit must be scoped to workspace.
```

---

# 18. Integration Context Model

Integration context may include:

- provider;
- workspace id;
- connection status;
- allowed scopes;
- mapping rules;
- last sync status;
- imported object references;
- export job references;
- audit events;
- error state.

This context supports AI orchestration, dashboard visibility and operational trust.

---

# 19. Integration API Boundary

Suggested API group:

```text
/integrations
```

Minimum endpoints:

```text
GET /workspaces/{workspace_id}/integrations
POST /workspaces/{workspace_id}/integrations
GET /workspaces/{workspace_id}/integrations/{integration_id}
PATCH /workspaces/{workspace_id}/integrations/{integration_id}
POST /workspaces/{workspace_id}/integrations/{integration_id}/pause
POST /workspaces/{workspace_id}/integrations/{integration_id}/revoke
POST /workspaces/{workspace_id}/integrations/{integration_id}/sync
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/integrations/{integration_id}/audit
GET /workspaces/{workspace_id}/integrations/{integration_id}/memory
POST /workspaces/{workspace_id}/integrations/{integration_id}/mapping
GET /workspaces/{workspace_id}/integrations/providers
```

---

# 20. Integration Service Responsibilities

`IntegrationRuntimeService` responsibilities:

- register integration providers;
- configure workspace integrations;
- validate scopes;
- manage connection lifecycle;
- normalize imported data;
- map external data to runtime objects;
- trigger user confirmation when required;
- emit integration events;
- trigger audit recording;
- trigger memory creation where useful;
- expose integration status to dashboard.

---

# 21. Integration Data Validation

Required validation:

- workspace_id is required;
- integration provider is required;
- integration status must be valid;
- scopes must be explicit;
- credential references must not expose secrets;
- imported data must identify source provider;
- exported data must identify destination;
- revoked integrations cannot sync;
- failed sync jobs must record error state.

---

# 22. MVP Acceptance Criteria

Integration Runtime is MVP-ready when:

- workspace can register at least one AI provider integration;
- exports can be generated through a controlled export path;
- manual import or simple data import can create draft runtime objects;
- integration activity emits events;
- integration activity creates audit records;
- integration errors are visible;
- dashboard can show active integration status;
- integration data is workspace-scoped.

---

# 23. Out of Scope for MVP

The MVP does not require:

- public integration marketplace;
- complex OAuth support for many providers;
- real-time bidirectional sync;
- accounting system automation;
- CRM replacement integration;
- payment execution;
- external write actions without approval;
- enterprise iPaaS functionality;
- complex data transformation engine.

---

# 24. Architecture Alignment

| Integration Runtime Area | Architecture Reference |
|---|---|
| Integration Object | Runtime Architecture |
| Workspace Scope | Workspace Runtime |
| Integration Events | Event Runtime |
| Integration Audit | Audit Runtime |
| Integration Memory | Memory Runtime |
| Integration Dashboard | Core User Journey |
| Integration Security | Security / Governance Baseline |
| AI Provider Integration | Agent Runtime / AI Governance |
| Export Integration | MVP Scope |

---

# 25. Final Integration Runtime Statement

```text
Integration Runtime is the controlled boundary through which Bizzi connects to external systems, imports and exports data, preserves governance, records audit evidence and protects workspace-scoped operating context.
```

This component prepares Bizzi for real-world tool connectivity without sacrificing trust, structure or control.