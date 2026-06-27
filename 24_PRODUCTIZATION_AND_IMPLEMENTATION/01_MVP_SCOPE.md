# 01_MVP_SCOPE.md

# Bizzi Platform

## MVP Scope

**Layer:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Component Type:** Product Definition  
**Foundation:** Art of Business Canonical Release v1.0  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Architecture Reference:** Art of Business v1.0  
**Previous Document:** 00_PRODUCT_VISION.md  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Minimum Viable Product scope for Bizzi Platform.

The MVP translates the Product Vision into the smallest working product that proves the core thesis of Bizzi:

```text
A business can be modeled, organized, delegated, monitored and improved as an AI-orchestrated operating system.
```

---

# 2. MVP Objective

The MVP must prove that a business owner can use Bizzi to:

- create a business workspace;
- describe the company structure;
- define core functions;
- assign responsibilities;
- register AI agents;
- create basic processes;
- route tasks;
- record decisions;
- preserve memory;
- view operational status;
- produce a basic audit trail.

---

# 3. MVP Success Statement

The MVP is successful if the first user can say:

```text
Bizzi helped me see how my business works, what is missing, who is responsible and what needs to happen next.
```

---

# 4. Target User for MVP

Primary MVP user:

```text
Owner or managing director of a small or medium business who personally coordinates too many tasks and wants to turn the company into a visible, structured and manageable operating system.
```

Secondary MVP users:

- operations manager;
- chief of staff;
- business analyst;
- department owner;
- consultant helping a business organize operations.

---

# 5. Core MVP Problem

The MVP solves the following problem:

```text
The business owner does not have a single operating view of functions, responsibilities, tasks, decisions, agents and memory.
```

Current reality:

- work is spread across chats, email, spreadsheets and memory;
- responsibilities are unclear;
- recurring processes are informal;
- tasks are lost;
- decisions are not preserved;
- AI is used outside the business structure;
- the owner remains the central bottleneck.

---

# 6. MVP Product Promise

Bizzi MVP promises:

```text
In the first hour, Bizzi creates a basic operating map of the company and helps the owner see responsibilities, gaps, tasks and next actions.
```

---

# 7. In-Scope MVP Capabilities

The MVP includes the following product capabilities:

## 7.1 Company Workspace

Create and manage one company workspace.

Minimum fields:

- company name;
- business type;
- industry;
- number of people;
- operating pain points;
- owner profile.

## 7.2 Business Operating Map

Generate a first operating map from onboarding inputs.

The map includes:

- core functions;
- suggested responsibilities;
- detected gaps;
- recommended agents;
- priority processes.

## 7.3 Function Registry

Create and manage core business functions.

Examples:

- Strategy;
- Sales;
- Marketing;
- Operations;
- Finance;
- Legal;
- HR;
- Customer Support;
- Procurement;
- Risk and Compliance.

## 7.4 Responsibility Assignment

Assign ownership to functions, tasks and processes.

Ownership types:

- human owner;
- AI agent owner;
- shared owner;
- unassigned.

## 7.5 Agent Registry

Register initial AI agents.

Minimum agent fields:

- agent name;
- role;
- assigned function;
- allowed actions;
- escalation rule;
- human owner.

## 7.6 Process Registry

Create simple business processes.

Minimum process fields:

- process name;
- purpose;
- owner;
- steps;
- inputs;
- outputs;
- related function;
- related agent.

## 7.7 Task Routing

Create and route tasks based on function, owner and agent assignment.

Minimum task fields:

- task title;
- description;
- owner;
- function;
- status;
- priority;
- due date;
- linked decision or process.

## 7.8 Decision Log

Record important business decisions.

Minimum decision fields:

- decision title;
- decision owner;
- context;
- options considered;
- final decision;
- rationale;
- date;
- linked function or process.

## 7.9 Enterprise Memory

Store structured knowledge from functions, tasks, decisions and processes.

Minimum memory types:

- decision memory;
- process memory;
- task memory;
- operating context;
- lessons learned.

## 7.10 Operating Dashboard

Show a basic operating view.

Dashboard includes:

- functions created;
- open tasks;
- unassigned responsibilities;
- recent decisions;
- active agents;
- process coverage;
- memory entries;
- risk or governance gaps.

## 7.11 Audit Trail

Capture basic audit events.

Events include:

- workspace created;
- function created;
- owner assigned;
- agent created;
- process created;
- task created;
- decision recorded;
- memory entry created;
- status changed.

---

# 8. Out-of-Scope for MVP

The MVP does not include:

- full ERP functionality;
- full CRM replacement;
- accounting automation;
- payroll;
- complex workflow engine;
- autonomous financial execution;
- multi-company ecosystem orchestration;
- marketplace;
- SDK;
- public API;
- advanced AI model training;
- complex permissions matrix;
- enterprise SSO;
- mobile app;
- billing system;
- multi-tenant enterprise administration.

These may be considered in later versions.

---

# 9. MVP User Journey

## Step 1 — Sign Up

User creates an account and company workspace.

## Step 2 — Business Intake

Bizzi asks structured questions:

- What does your company do?
- How many people work in it?
- What functions exist?
- Where do tasks get lost?
- What depends too much on the owner?
- What do you want to control better?

## Step 3 — Operating Map Generated

Bizzi generates an initial Business Operating Map.

## Step 4 — User Confirms Functions

User confirms or edits suggested functions.

## Step 5 — Responsibilities Assigned

User assigns owners or marks gaps.

## Step 6 — Agents Suggested

Bizzi suggests AI agents for key functions.

## Step 7 — First Tasks Created

Bizzi creates first recommended tasks.

## Step 8 — Dashboard Opens

User sees the first operating dashboard.

---

# 10. First-Hour MVP Experience

Within the first hour, the user should complete:

```text
Workspace Created
↓
Business Intake Completed
↓
Operating Map Generated
↓
Functions Confirmed
↓
Responsibilities Assigned
↓
First Agents Suggested
↓
First Tasks Created
↓
Dashboard Visible
```

The user must feel:

```text
I can finally see my business as a system.
```

---

# 11. MVP Data Objects

Minimum MVP data objects:

```text
User
CompanyWorkspace
Function
Responsibility
Agent
Process
Task
Decision
MemoryEntry
AuditEvent
DashboardMetric
```

---

# 12. MVP Runtime Components

Minimum runtime components:

```text
Onboarding Engine
Operating Map Generator
Function Registry
Agent Registry
Process Registry
Task Router
Decision Logger
Memory Store
Audit Logger
Dashboard
```

---

# 13. MVP AI Capabilities

MVP AI features:

- analyze onboarding answers;
- suggest functions;
- suggest responsibilities;
- suggest agents;
- suggest first processes;
- suggest first tasks;
- summarize decisions;
- generate operating map;
- identify missing ownership;
- identify operating gaps.

AI must not execute irreversible actions in the MVP.

---

# 14. Governance Constraints

The MVP must preserve Art of Business governance principles:

- human accountability;
- explicit ownership;
- traceability;
- auditability;
- no hidden autonomous execution;
- memory governance;
- controlled agent authority.

---

# 15. MVP Non-Functional Requirements

Minimum requirements:

- simple onboarding;
- reliable data persistence;
- clear UI;
- fast first value;
- auditable events;
- basic access control;
- readable exports;
- safe AI recommendations;
- low operational complexity.

---

# 16. MVP Success Metrics

Product metrics:

- workspace creation completion rate;
- onboarding completion rate;
- operating map generation rate;
- functions confirmed per workspace;
- tasks created per workspace;
- decisions logged per workspace;
- memory entries created;
- day-1 return rate;
- week-1 return rate.

Qualitative success:

```text
The owner understands the business better after using Bizzi than before using it.
```

---

# 17. MVP Exports

The MVP should generate simple exports:

- Business Operating Map;
- Function Registry;
- Responsibility Map;
- Task List;
- Decision Log;
- Basic Audit Trail.

Exports may initially be Markdown, PDF or CSV.

---

# 18. MVP Release Boundary

The MVP release boundary is:

```text
One company
One workspace
One owner account
Basic functions
Basic agents
Basic tasks
Basic decisions
Basic memory
Basic dashboard
Basic audit trail
```

---

# 19. MVP Architecture Alignment

MVP maps to Art of Business v1.0 as follows:

| MVP Component | Art of Business Reference |
|---|---|
| Company Workspace | Enterprise Foundation |
| Function Registry | Enterprise Function Registry |
| Agent Registry | Agent Library |
| Process Registry | Process Architecture |
| Task Router | Operating Model |
| Decision Log | Decision Routing |
| Memory Store | Enterprise Memory |
| Audit Logger | Observability and Intelligence |
| Dashboard | Enterprise Operations |
| Governance Constraints | Governance Baseline |

---

# 20. MVP Definition of Done

The MVP is done when:

- a user can create a workspace;
- onboarding produces an operating map;
- functions can be created and edited;
- responsibilities can be assigned;
- agents can be registered;
- tasks can be created and routed;
- decisions can be logged;
- memory entries are preserved;
- audit events are recorded;
- dashboard shows operating status;
- user can export core operating information.

---

# 21. Final MVP Scope Statement

```text
Bizzi MVP is the smallest working product that helps a business owner transform company chaos into a visible operating system of functions, responsibilities, agents, tasks, decisions, memory and auditability.
```

This document defines the initial build boundary for Bizzi Platform.