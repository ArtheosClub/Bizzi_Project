# CORE Object Registry

Version: 1.0
Status: Information Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Enterprise_Metadata_Standard.md
- CORE_Enterprise_Taxonomy.md

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

The CORE Object Registry defines the canonical registry of managed Bizzi object types.

It standardizes object prefixes, ownership, purpose, lifecycle expectations, and governance requirements.

Core principle:

```text
Every object type must be registered before it becomes part of the Bizzi platform language.
```

---

## 01. Purpose

This registry defines:

- object type names;
- ID prefixes;
- object purpose;
- primary owners;
- lifecycle expectations;
- governance relevance;
- relationship to other architecture documents.

---

## 02. Registry Rules

Rules:

- Every managed object type must have a unique prefix.
- Prefixes must not be reused for unrelated object types.
- Object types must have an owner agent.
- Object types must define minimum metadata.
- Deprecated object types remain in registry as retired.
- New object types require architecture review.

---

## 03. Core Object Types

| Prefix | Object Type | Purpose | Primary Owner |
|---|---|---|---|
| CAP | Capability | Enterprise capability area | AG002 |
| FUNC | Function | Enterprise function or responsibility | AG002 |
| AG | Agent | AI or human/AI role agent | AG002 |
| PB | Playbook | Execution or governance playbook | AG002 |
| PROC | Process | Business or operational process | AG047 |
| PROCV | Process Version | Versioned process definition | AG047 |
| WF | Workflow | Managed state machine or work path | AG009 |
| EVT | Event | Timestamped enterprise event | AG065 |
| DEC | Decision | Governance decision record | AG002 |
| KPI | KPI / Metric | Governed performance measure | AG066 |
| RISK | Risk | Risk object or exposure | AG005 |
| AUD | Audit Report | Audit or validation artifact | AG003 |
| KNOW | Knowledge Entry | Enterprise Memory item | AG054 |
| PAT | Optimization Pattern | Reusable improvement pattern | AG053 |
| TWIN | Digital Twin | Simulation-ready process model | AG009 |
| SCN | Scenario | Proposed future-state option | AG047 |
| SIM | Simulation Run | Simulation execution result | AG067 |
| ECON | Economic Evaluation | Economic impact object | AG016 |
| CFG | Configuration | Managed platform or process configuration | AG009 |
| API | API / Integration | Managed interface or integration | AG009 |
| DOC | Document | Controlled documentation artifact | AG053 |
| ART | Artifact | Output or generated work product | AG053 |
| PORT | Portfolio Item | Initiative or portfolio tracking object | AG007 |

---

## 04. Object Registration Template

New object types should be registered using:

```yaml
prefix:
object_type:
description:
primary_owner:
supporting_agents:
required_metadata:
lifecycle:
related_objects:
governance_relevance:
audit_required:
status:
```

---

## 05. Lifecycle Mapping

Each object type must map to a generic lifecycle:

```text
Proposed -> Draft -> Reviewed -> Approved -> Active -> Superseded -> Deprecated -> Archived
```

Domain-specific lifecycle extensions are allowed if mapped to the generic model.

---

## 06. Governance Classes

| Class | Meaning |
|---|---|
| G0 | Low governance relevance |
| G1 | Operational relevance |
| G2 | Cross-functional relevance |
| G3 | Financial, legal, compliance, risk, or strategic relevance |
| G4 | Human Board / executive-level relevance |

Object types with G2 or higher require explicit ownership and audit path.

---

## 07. Registry Maintenance

The registry should be reviewed when:

- a new object type appears;
- an existing object type changes meaning;
- an ID prefix conflict occurs;
- a playbook introduces new artifacts;
- the platform architecture changes;
- a deprecated object type is retired.

---

## 08. Integration

The Object Registry supports:

- Metadata Standard;
- Enterprise Taxonomy;
- Versioning Framework;
- Configuration Management;
- Enterprise Object Model;
- API and Integration Framework;
- Enterprise Memory.

---

## 09. Success Criteria

This registry is successful if Bizzi can:

- identify object types consistently;
- prevent prefix conflicts;
- assign object ownership;
- support metadata enforcement;
- build enterprise graph relationships;
- govern object lifecycle and reuse.

---

## 10. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Core Object Registry foundation specification |
