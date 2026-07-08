# CORE Enterprise Metadata Standard

Version: 1.0
Status: Information Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Object_Registry.md
- CORE_Versioning_Framework.md
- CORE_Configuration_Management_Framework.md

Primary Owner:
- AG009 Enterprise Architect

Data Owner:
- AG065 Data Engineer

Governance Owner:
- AG002 Chief Orchestrator

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Enterprise Metadata Standard defines the minimum metadata required for all managed Bizzi objects, documents, playbooks, agents, workflows, decisions, events, KPIs, patterns, simulations, and knowledge entries.

Metadata is the control layer that makes Bizzi searchable, governable, auditable, versionable, and machine-readable.

Core principle:

```text
No managed object without metadata.
No metadata without ownership, status, version, and traceability.
```

---

## 01. Purpose

This document defines:

- mandatory metadata fields;
- recommended metadata fields;
- metadata quality rules;
- metadata lifecycle;
- ownership expectations;
- relationship metadata;
- governance and audit requirements.

---

## 02. Universal Metadata Block

Every managed object should include:

```yaml
id:
object_type:
title:
description:
version:
status:
owner_agent:
created_by:
created_at:
updated_by:
updated_at:
related_capabilities:
related_functions:
related_agents:
related_playbooks:
source_objects:
dependent_objects:
decision_level:
risk_rating:
confidence_level:
audit_required:
human_override_required:
```

---

## 03. Required Fields

Minimum required fields:

- id
- object_type
- title
- version
- status
- owner_agent
- created_at
- related_capabilities, where applicable
- source_objects, where applicable

---

## 04. Metadata Categories

| Category | Purpose |
|---|---|
| Identity Metadata | ID, title, object type, description |
| Ownership Metadata | owner, creator, updater, responsible agent |
| Lifecycle Metadata | status, version, created/updated dates |
| Relationship Metadata | related capabilities, agents, functions, source objects |
| Governance Metadata | decision level, audit required, human override |
| Risk Metadata | risk rating, sensitivity, confidence |
| Operational Metadata | priority, SLA, workflow state, next action |

---

## 05. Status Values

Recommended common statuses:

- Draft
- Under Review
- Approved
- Active
- Superseded
- Deprecated
- Archived
- Rejected
- Failed
- Closed

Domain-specific statuses are allowed but must map to common status values.

---

## 06. Confidence Levels

| Level | Meaning |
|---|---|
| Low | Weak or incomplete evidence |
| Medium | Usable but with known uncertainty |
| High | Strong evidence and stable interpretation |
| Verified | Audited or empirically confirmed |

---

## 07. Metadata Quality Rules

High-quality metadata is:

- complete;
- consistent;
- owned;
- current;
- traceable;
- machine-readable;
- aligned with object registry;
- not duplicated;
- not contradictory.

Objects with missing metadata may not be used for governance-critical decisions.

---

## 08. Governance Rules

Metadata governance requirements:

- every object must have an owner;
- every object must have a lifecycle status;
- every object must have a version;
- high-impact objects must have decision_level;
- audit-critical objects must have source_objects;
- deprecated objects must not be used as active guidance;
- metadata changes should be versioned or traceable.

---

## 09. Integration

This standard supports:

- Object Registry;
- Enterprise Taxonomy;
- Versioning Framework;
- Configuration Management;
- Enterprise Memory;
- Workflow Framework;
- Decision Framework;
- KPI Framework.

---

## 10. Success Criteria

This specification is successful if Bizzi can:

- search objects reliably;
- route objects by ownership;
- audit object history;
- identify stale or deprecated objects;
- connect objects into an enterprise graph;
- prepare for machine-readable registry and API layers.

---

## 11. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Enterprise Metadata Standard foundation specification |
