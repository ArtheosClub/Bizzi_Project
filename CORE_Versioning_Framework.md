# CORE Versioning Framework

Version: 1.0
Status: Information Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Enterprise_Metadata_Standard.md
- CORE_Configuration_Management_Framework.md

Primary Owner:
- AG009 Enterprise Architect

Governance Owner:
- AG002 Chief Orchestrator

Audit Owner:
- AG003 AI Auditor

Knowledge Owner:
- AG053 Knowledge Curator

---

## 00. Executive Summary

The CORE Versioning Framework defines how Bizzi versions documents, playbooks, objects, processes, agents, configurations, schemas, patterns, simulations, and platform specifications.

Versioning is required so Bizzi can evolve without losing traceability, confusing active guidance with historical guidance, or weakening audit history.

Core principle:

```text
Every managed change must be versioned or traceable.
Every active version must be distinguishable from draft, superseded, and archived versions.
```

---

## 01. Purpose

This document defines:

- version format;
- version meaning;
- major and minor change rules;
- version lifecycle;
- compatibility rules;
- dependency rules;
- archive and supersession rules;
- governance requirements.

---

## 02. Standard Version Format

Default version format:

```text
vMAJOR.MINOR
```

Examples:

```text
v1.0
v1.1
v2.0
```

Optional patch notation may be used for technical artifacts:

```text
vMAJOR.MINOR.PATCH
```

---

## 03. Version Meaning

| Version Change | Meaning |
|---|---|
| Patch | Typo, formatting, non-substantive correction |
| Minor | Clarification, extension, new section, compatible change |
| Major | Structural, governance, schema, authority, or lifecycle change |

---

## 04. Versioned Object Types

Objects that should be versioned:

- Playbooks;
- Core architecture documents;
- Process versions;
- Agent specifications;
- Function definitions;
- Digital Twins;
- Simulation models;
- KPI definitions;
- Pattern Cards;
- API schemas;
- Configuration baselines;
- Governance rules;
- Templates;
- controlled documents.

---

## 05. Version Lifecycle

```text
Draft
  -> Review
  -> Approved
  -> Active
  -> Superseded
  -> Deprecated
  -> Archived
```

Only one version should be marked Active for operational use unless parallel versions are explicitly allowed.

---

## 06. Major Change Criteria

A major version update is required when a change modifies:

- object meaning;
- required metadata;
- decision authority;
- lifecycle states;
- API or schema compatibility;
- process execution logic;
- agent responsibility;
- governance or audit expectations;
- dependent references.

---

## 07. Compatibility Rules

Each new major version should define:

- what it replaces;
- what remains compatible;
- what migration is needed;
- what references must be updated;
- whether old versions remain usable;
- rollback option if relevant.

---

## 08. Dependency Rules

Versioned objects may depend on other versioned objects.

Dependency metadata should include:

```yaml
depends_on:
  - object_id:
    version:
    compatibility:
```

Major updates must review dependent objects.

---

## 09. Governance

Versioning governance requirements:

- active versions must be explicit;
- superseded versions must not be deleted;
- major changes require review;
- governance-impacting changes require approval;
- version history must be maintained;
- rollback path should exist where feasible.

---

## 10. Version History Standard

Every controlled document should include:

```markdown
## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | YYYY-MM-DD | Initial version |
```

---

## 11. Success Criteria

This specification is successful if Bizzi can:

- distinguish active and historical versions;
- manage major changes;
- preserve audit history;
- update dependencies safely;
- prevent stale guidance from being reused as current truth;
- support future release management.

---

## 12. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Versioning Framework foundation specification |
