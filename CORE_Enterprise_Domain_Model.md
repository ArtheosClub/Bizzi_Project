# CORE Enterprise Domain Model

Version: 1.0
Status: Architecture Closure Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Object_Registry.md
- CORE_Enterprise_Taxonomy.md
- CORE_Canonical_Data_Model.md
- CORE_Simplicity_and_Usability_Principles.md

Primary Owner:
- AG009 Enterprise Architect

Business Owner:
- AG002 Chief Orchestrator

Data Owner:
- AG065 Data Engineer

Knowledge Owner:
- AG053 Knowledge Curator

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Enterprise Domain Model defines the business entities Bizzi must understand in simple enterprise language.

This model is not a technical database schema. It is the shared business vocabulary that connects Bizzi architecture to real companies, customers, suppliers, employees, contracts, products, projects, assets, documents, transactions, and operations.

Core principle:

```text
Bizzi should remain understandable to business users before it becomes complex for engineers.
```

---

## 01. Purpose

This document defines:

- core business domains;
- canonical business entities;
- entity relationships;
- boundary between business domain model and platform object model;
- simplification rules for future implementation.

---

## 02. Domain Model vs Object Model

| Model | Purpose |
|---|---|
| Enterprise Domain Model | Describes real business entities and relationships |
| Enterprise Object Model | Describes managed platform objects and metadata |
| Canonical Data Model | Describes implementation-ready data structures |
| Knowledge Graph Model | Connects objects, entities, evidence, and relationships |

The Domain Model answers: what does the business talk about?
The Object Model answers: what does Bizzi manage?
The Data Model answers: what does software store?

---

## 03. Core Business Domains

| Domain | Purpose |
|---|---|
| Organization | Company, business units, teams, roles, governance bodies |
| People | employees, contractors, customers, suppliers, partners |
| Commercial | products, services, offers, prices, deals, contracts |
| Operations | processes, workflows, tasks, cases, work orders |
| Finance | invoices, payments, budgets, costs, revenue, ROI |
| Risk and Compliance | obligations, controls, risks, incidents, audits |
| Knowledge | documents, policies, SOPs, lessons, patterns, memory |
| Technology | systems, tools, integrations, APIs, configurations |
| Assets | physical, digital, financial, and knowledge assets |
| Projects | initiatives, milestones, deliverables, portfolios |

---

## 04. Core Domain Entities

| Entity | Meaning |
|---|---|
| Company | Legal or operating enterprise using Bizzi |
| Business Unit | Organizational subdivision |
| Team | Group of people or agents working together |
| Role | Responsibility or authority position |
| Person | Human individual |
| Agent | AI or hybrid operational role |
| Customer | Buyer or recipient of value |
| Supplier | Provider of goods or services |
| Partner | External collaborator |
| Product | Item or digital offering sold or managed |
| Service | Work or capability delivered to customer |
| Contract | Formal agreement with obligations |
| Invoice | Financial request for payment |
| Payment | Money movement or settlement |
| Budget | Planned financial allocation |
| Project | Temporary initiative with objective and deliverables |
| Process | Repeatable business flow |
| Task | Unit of work |
| Case | Business issue or service request |
| Asset | Managed resource of value |
| Document | Controlled information artifact |
| Policy | Governance rule or standard |
| Risk | Potential negative exposure |
| Control | Preventive or detective safeguard |
| Incident | Realized issue or failure |
| KPI | Performance measure |
| Decision | Governed choice |
| Event | Something meaningful that happened |

---

## 05. Core Entity Relationships

Examples:

```text
Company has Business Units
Business Unit owns Processes
Team executes Processes
Person fills Role
Agent executes Task
Customer signs Contract
Supplier provides Service
Product generates Revenue
Invoice requests Payment
Payment settles Invoice
Project delivers Artifact
Risk affects Process
Control mitigates Risk
KPI measures Process
Decision approves Change
Event records Activity
Document describes Policy
```

---

## 06. Domain Entity Classification

Each domain entity should be classified by:

- business domain;
- owner function;
- data sensitivity;
- lifecycle;
- related processes;
- related documents;
- related KPIs;
- related risks;
- implementation priority.

---

## 07. Simplicity Rules

To protect usability:

- start with fewer entities, not more;
- avoid modeling rare exceptions too early;
- prefer business names over technical names;
- do not turn every noun into a platform object;
- only promote an entity to managed object if Bizzi must govern, track, audit, or automate it;
- domain entities should be easy to explain to a non-technical founder or manager.

---

## 08. MVP Domain Scope

Initial MVP should focus on:

- Company;
- Person;
- Agent;
- Role;
- Process;
- Task;
- Decision;
- Event;
- KPI;
- Document;
- Memory Entry;
- Risk;
- Alert;
- Project / Initiative.

Commercial, finance, HR, logistics, and domain-specific entities can be expanded later through domain playbooks.

---

## 09. Governance Rules

Domain model governance rules:

- new core domain entities require architecture review;
- domain terms must align with Enterprise Taxonomy;
- technical implementation must not rename business entities without mapping;
- deprecated domain terms remain as aliases;
- domain expansion should follow real business need, not theoretical completeness.

---

## 10. Success Criteria

This model is successful if Bizzi can:

- describe real business entities clearly;
- map business language to platform objects;
- keep implementation understandable;
- avoid over-modeling;
- support future business domains without breaking core simplicity.

---

## 11. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-09 | Initial Enterprise Domain Model architecture closure specification |
