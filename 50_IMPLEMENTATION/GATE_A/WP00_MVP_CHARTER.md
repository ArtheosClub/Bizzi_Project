# WP00 — MVP Charter

Version: 1.0  
Status: Proposed for Retrospective Approval  
Gate: A — Product Definition  
Priority: P0  
Owner: Project Owner  
Product Owner: AG002 Chief Orchestrator  
Architecture Owner: AG009 Enterprise Architect

## 1. Purpose

The Bizzi MVP must prove that a business owner can submit a real operational problem and receive a structured, reviewable recommendation through one governed execution loop.

## 2. MVP Product Statement

Bizzi is an AI-orchestrated business operating platform that converts an unstructured business problem into a traceable task, agent execution, recommendation, human decision, event trail, audit record, and reusable memory entry.

## 3. MVP Scope

The MVP includes one complete scenario:

```text
User Request
→ EnterpriseObject
→ Task
→ ContextPackage
→ AgentDefinition / RuntimeSession
→ Structured Recommendation
→ Human Approval, Rejection, or Rework
→ Decision Record
→ Event and Audit Trail
→ Command Center View
→ Memory Entry
```

The MVP implements:

- one generic agent runtime;
- three required configured roles: Chief Orchestrator, Process Analysis Agent, Reviewer/Auditor;
- one human approver;
- one workspace-scoped execution path;
- one business-process analysis scenario;
- one visible request-to-decision timeline;
- one Docker Compose deployment path.

## 4. Non-Goals

The MVP does not include:

- implementation of the full 83+ agent catalog;
- autonomous execution of strategic or high-impact decisions without human approval;
- marketplace, billing, multi-region deployment, or enterprise federation;
- Kubernetes deployment;
- graph intelligence as a blocking dependency;
- advanced semantic memory retrieval;
- multiple business scenarios before the first vertical slice is proven;
- custom runtime code per agent role.

## 5. Primary Release Definition

The MVP is release-ready when one approved demo scenario can be completed end to end from a clean environment using documented startup instructions, with:

- authenticated request intake;
- workspace isolation;
- persisted task, context, session, result, decision, event, and audit records;
- human approval/rejection/rework;
- visible result and timeline;
- automated integration test coverage;
- no active critical stop condition.

## 6. Governing Constraints

- Backend: Python + FastAPI.
- Database: PostgreSQL with SQLAlchemy and Alembic.
- Frontend: React + TypeScript.
- Architecture: modular monolith.
- Deployment: Docker Compose for MVP.
- Kubernetes is deferred.
- Human override remains mandatory for critical and strategic decisions.
- Workspace isolation, authorization, audit integrity, and CI failures are hard stop conditions.

## 7. Success Boundary

Gate A defines the product and acceptance contract. Gate B may provide infrastructure, Gate C the platform backbone, Gate D the first vertical slice, and Gate E release completion. No later gate may silently expand the MVP beyond this charter.

## 8. Approval Record

This charter is prepared for retrospective Gate A approval because Gate B was implemented before the Gate A artifact set was formally completed. Retrospective approval validates product intent without rewriting or invalidating the already completed engineering foundation.
