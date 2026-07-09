# CORE Simplicity and Usability Principles

Version: 1.0
Status: Architecture Closure Specification

Related Architecture:
- CORE_Enterprise_Domain_Model.md
- CORE_Canonical_Data_Model.md
- CORE_Architecture_Traceability_Matrix.md
- PB050_Bizzi_Reference_Implementation_Architecture.md

Primary Owner:
- AG009 Enterprise Architect

Product Owner:
- AG002 Chief Orchestrator

User Experience Owner:
- AG083 Dashboard Manager

Governance Owner:
- AG010 Governance Agent

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Simplicity and Usability Principles define how Bizzi protects itself from becoming too complex to understand, implement, operate, or sell.

Bizzi is architecturally powerful, but its value depends on being usable by real business owners, managers, operators, and teams.

Core principle:

```text
Enterprise power must feel simple at the point of use.
```

---

## 01. Purpose

This document defines:

- simplicity principles;
- usability principles;
- architecture closure rules;
- MVP constraints;
- product experience rules;
- anti-complexity guardrails;
- future expansion discipline.

---

## 02. Simplicity Principles

| Principle | Meaning |
|---|---|
| Start Small | Implement the smallest useful vertical slice first |
| One Concept, One Name | Avoid duplicate names for the same idea |
| Business First | Use business language before technical language |
| Progressive Disclosure | Hide complexity until needed |
| Defaults Before Configuration | Provide good defaults before exposing settings |
| Guided Workflows | Users should be guided through tasks, not exposed to raw architecture |
| Traceability Without Burden | Capture metadata automatically where possible |
| No Architecture Theater | Do not create documents or modules without operational use |

---

## 03. Usability Principles

Bizzi should be usable by:

- founder / owner;
- operations manager;
- analyst;
- accountant / finance user;
- sales or service team;
- process owner;
- technical administrator;
- AI agent supervisor.

Users should not need to understand all architecture layers to complete daily work.

---

## 04. Product Experience Rules

Product experience rules:

- show tasks, decisions, alerts, and outcomes first;
- hide technical graph complexity unless requested;
- show clear next action;
- explain why a recommendation exists;
- show confidence and risk simply;
- provide business-friendly names;
- avoid overwhelming dashboards;
- prioritize guided workflows over open-ended configuration.

---

## 05. MVP Simplicity Constraints

The MVP should not attempt to implement everything.

MVP should focus on:

- creating objects;
- creating tasks;
- running basic agent sessions;
- building context packages;
- recording events;
- recording decisions;
- storing memory entries;
- showing command center basics;
- preserving audit trail.

MVP should avoid:

- full multi-tenant complexity;
- advanced simulation;
- marketplace features;
- complex domain modules;
- excessive configuration screens;
- fully automated governance decisions;
- large-scale enterprise integrations before product fit.

---

## 06. Anti-Complexity Guardrails

Bizzi should reject or defer complexity when:

- it does not help the first real users;
- it requires too much explanation;
- it creates configuration burden;
- it duplicates existing concepts;
- it weakens implementation speed;
- it adds architecture without reducing risk;
- it blocks MVP delivery;
- it cannot be tested or observed.

---

## 07. Architecture Closure Rules

After Architecture v1.0 closure:

- new architecture files should be exceptional;
- new documents must map to implementation or usability need;
- implementation should be prioritized over speculative modeling;
- broad new layers should not be added before MVP;
- architecture updates should improve clarity, not expand scope;
- product simplicity has priority over theoretical completeness.

---

## 08. User-Facing Simplification

Architecture terms should be translated for users.

Examples:

| Architecture Term | User-Facing Term |
|---|---|
| Runtime Session | Agent work session |
| Context Package | Information used for this task |
| Knowledge Graph | Connected company knowledge |
| Decision Intelligence | Decision support |
| Human-in-the-Loop | Needs your approval |
| Event Bus | Activity log / system signals |
| Canonical Data Model | Standard data structure |
| Command Center | Control panel |

---

## 09. Success Criteria

This specification is successful if Bizzi:

- remains understandable;
- can be explained simply;
- avoids unnecessary architecture expansion;
- supports fast MVP implementation;
- feels useful before it feels powerful;
- protects business users from internal complexity;
- keeps architecture as an enabler, not a burden.

---

## 10. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-09 | Initial Simplicity and Usability Principles architecture closure specification |
