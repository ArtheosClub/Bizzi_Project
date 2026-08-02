# Module Index

Document ID: MSF-INDEX
Title: Module Specification Index
Version: 1.0
Status: ACTIVE
Document Type: Governance Catalog
Part of: Module Specification Framework
Repository: ArtheosClub/Bizzi_Project

This document SHALL catalog every Module Specification created under
this framework. This document does not itself define module
responsibilities; each module's own specification is authoritative for
its content. This document records status only.

---

## Catalog

| Identifier | Module ID | Name | Purpose | Dependencies | Version | Status | Review | Approval | Implementation | Verification | Gate D |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MS-001 | MOD-001 | Foundation | Provide the shared technical substrate every other module depends upon. | None | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-002 | MOD-002 | Identity | Establish authentication, authorization, and identity lifecycle. | Foundation | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-003 | MOD-003 | Organization | Model tenants, companies, teams, and membership. | Identity | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-004 | MOD-004 | Workspace | Provide the bounded working context and navigation for users. | Organization | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-005 | MOD-005 | Documents | Manage document and file storage, versioning, and metadata. | Workspace | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-006 | MOD-006 | Workflow | Model and execute business processes and state transitions. | Documents | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-007 | MOD-007 | AI | Orchestrate AI-assisted capability atop platform processes. | Workflow | 1.0 | **Deferred — post-MVP** | Not Started | Pending | Not Started | Not Started | Pending |
| MS-008 | MOD-008 | Notification | Deliver information across communication channels. | Workflow; AI | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-009 | MOD-009 | API | Expose module capability through public interfaces. | Identity; Organization; Workspace; Documents; Workflow; AI; Notification; Administration | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-010 | MOD-010 | Frontend | Present platform capability to human users. | API | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-011 | MOD-011 | Administration | Provide operational configuration and oversight. | Identity; Organization | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |
| MS-012 | MOD-012 | Integrations | Connect the platform to external systems and services. | API | 1.0 | Draft | Not Started | Pending | Not Started | Not Started | Pending |

---

## Identifier Coexistence

Every module carries two identifiers, which SHALL coexist permanently:

- **Identifier** (`MS-00X`) — the Specification ID, identifying the
  module's specification document.
- **Module ID** (`MOD-00X`) — the permanent engineering identifier.
  Future ADRs, Issues, Pull Requests, and Tests MAY reference the Module
  ID.

Neither identifier SHALL be removed in favor of the other.

---

## MVP Scope Note

**MS-007 (AI) is deferred out of MVP scope** by Project Owner decision
(2026-07-28), pending resolution of Outstanding Item OI-001 (the
unapproved Provider/Model catalog-scope proposal and the unwritten
ADW-05 domain workshop). It is deferred, not cancelled — its
specification is retained in full. No other module's MVP delivery SHALL
be made dependent on it. See `MS-007_AI/README.md` for the full
rationale.

The remaining eleven modules are unaffected by that deferral.

---

## Status Field Definitions

- **Version**: the Specification Version of the module's specification
  document, per its own Module Metadata section.
- **Status**: the module specification's own lifecycle status —
  `Draft` until it has completed Architecture Review and Approval.
- **Review**: `Not Started` until the module's specification has
  undergone Architecture Review, per `README.md` §7.
- **Approval**: `Pending` until the module's specification has completed
  Approval, per `README.md` §7.
- **Implementation**: `Not Started` until implementation of the module
  has commenced under an approved Module Specification.
- **Verification**: `Not Started` until the module's implementation has
  been verified, per `README.md` §7.
- **Gate D**: `Pending` until the module has been presented to, and
  certified by, Gate D Certification — a future certification checkpoint
  not yet established.

All status fields above carry their initial value for every module. No
status field in this catalog authorizes implementation, approval, or
certification by itself; each requires the corresponding governance act
recorded elsewhere.
