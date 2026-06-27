# 04_CORE_USER_JOURNEY.md

# Bizzi Platform

## Core User Journey

**Layer:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Component Type:** Product Definition  
**Foundation:** Art of Business Canonical Release v1.0  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Architecture Reference:** Art of Business v1.0  
**Previous Documents:** 00_PRODUCT_VISION.md, 01_MVP_SCOPE.md, 02_USER_PERSONAS.md, 03_VALUE_PROPOSITION.md  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the core user journey for the Bizzi Platform MVP.

It answers the product question:

```text
How does the first user receive value from Bizzi from registration to the first operating dashboard?
```

---

# 2. Journey Goal

The core journey must guide the user from business chaos to first operating clarity.

Journey transformation:

```text
Scattered Business Context
↓
Guided Intake
↓
Business Operating Map
↓
Confirmed Functions
↓
Assigned Responsibilities
↓
Suggested Agents
↓
First Tasks
↓
Operating Dashboard
```

---

# 3. Primary User

The journey is optimized for:

```text
P01 — The Overloaded Business Owner
```

Secondary users supported:

- Operations Manager;
- Business Analyst / Consultant;
- Chief of Staff;
- Department Owner.

---

# 4. Core Journey Principle

The user must receive visible value before complex configuration.

```text
Value First
↓
Configuration Later
```

Bizzi must not ask the user to build the system manually before showing insight.

---

# 5. Journey Entry Point

The user arrives with one of the following intents:

- I want to organize my company;
- I want fewer lost tasks;
- I want to understand who is responsible;
- I want AI to help manage operations;
- I want to reduce dependence on myself;
- I want a better operating system for my business.

The product must meet the user at this practical level, not with technical architecture language.

---

# 6. Stage 1 — Registration

## User Action

User creates an account and starts a company workspace.

## Required Inputs

- name;
- email;
- company name;
- role;
- company size;
- business type.

## Product Output

```text
Company Workspace Created
```

## Success Condition

User enters the workspace without friction.

---

# 7. Stage 2 — Business Intake

## User Action

User answers guided questions about the company.

## Intake Questions

- What does your company do?
- How many people work in it?
- What are the main functions?
- Where do tasks get lost?
- What depends too much on you personally?
- Which areas feel chaotic?
- What do you want to control better?
- Do you already use AI tools?

## Product Output

```text
Structured Business Context
```

## Success Condition

User feels the questions are relevant and not too heavy.

---

# 8. Stage 3 — Operating Map Generation

## System Action

Bizzi analyzes intake answers and generates the first Business Operating Map.

## Output Includes

- suggested core functions;
- responsibility gaps;
- high-risk operating gaps;
- suggested AI agents;
- suggested first processes;
- suggested first tasks.

## User Feeling

```text
Bizzi understands my business enough to show me something useful.
```

---

# 9. Stage 4 — Function Confirmation

## User Action

User confirms, edits or removes suggested functions.

## Product Output

```text
Initial Function Registry
```

## Required UX

- simple cards;
- plain language;
- edit-in-place;
- suggested defaults;
- no complex hierarchy at MVP stage.

## Success Condition

User confirms at least three business functions.

---

# 10. Stage 5 — Responsibility Assignment

## User Action

User assigns owners to functions or marks them as unassigned.

## Ownership Types

- human owner;
- AI agent support;
- shared owner;
- unassigned.

## Product Output

```text
Responsibility Map
```

## Success Condition

User sees at least one responsibility gap clearly.

---

# 11. Stage 6 — Agent Suggestions

## System Action

Bizzi suggests AI agents based on confirmed functions and pain points.

## Example Agent Suggestions

- Operations Coordinator Agent;
- Sales Support Agent;
- Finance Assistant Agent;
- Risk Monitor Agent;
- Process Analyst Agent;
- Executive Summary Agent.

## User Action

User accepts, edits or ignores suggested agents.

## Product Output

```text
Initial Agent Registry
```

## Governance Rule

All suggested agents must have a human owner and limited authority.

---

# 12. Stage 7 — First Tasks Created

## System Action

Bizzi creates suggested first tasks from gaps, functions and responsibilities.

## Example Tasks

- Assign owner for Sales function;
- Document customer onboarding process;
- Review unpaid invoice responsibility;
- Define weekly operations review;
- Create decision log for pricing decisions.

## Product Output

```text
Initial Task List
```

## Success Condition

User sees actionable next steps.

---

# 13. Stage 8 — Decision Log Setup

## User Action

User records or imports the first important decision.

## Product Output

```text
Decision Memory Started
```

## Success Condition

User understands that important decisions will no longer disappear into chat history.

---

# 14. Stage 9 — Memory Creation

## System Action

Bizzi creates initial memory entries from onboarding, operating map, functions, tasks and decisions.

## Memory Types

- company context;
- function memory;
- decision memory;
- task memory;
- process memory;
- lessons learned.

## Product Output

```text
Enterprise Memory Initialized
```

---

# 15. Stage 10 — Operating Dashboard

## User Action

User opens the first operating dashboard.

## Dashboard Includes

- confirmed functions;
- unassigned responsibilities;
- open tasks;
- suggested agents;
- recent decisions;
- memory entries;
- operating gaps;
- next recommended actions.

## Product Output

```text
First Operating Dashboard
```

## Success Condition

User can answer:

```text
What is happening?
Who is responsible?
What should happen next?
```

---

# 16. First Five Minutes Journey

Within the first five minutes:

```text
Registration
↓
Business Intake Started
↓
Basic Company Context Captured
↓
First Operating Map Preview Generated
```

The user must see early proof that Bizzi creates clarity.

---

# 17. First Hour Journey

Within the first hour:

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
Agents Suggested
↓
First Tasks Created
↓
Dashboard Opened
```

The user must feel:

```text
I finally see my business as a system.
```

---

# 18. First Day Journey

Within the first day, user should:

- revisit dashboard;
- edit functions;
- assign missing owners;
- create more tasks;
- record first decision;
- review agent suggestions;
- export operating map.

---

# 19. First Week Journey

Within the first week, Bizzi should help user:

- establish weekly operating rhythm;
- maintain task status;
- log decisions;
- create process drafts;
- build memory entries;
- identify recurring gaps;
- reduce manual follow-up.

---

# 20. Journey Success Metrics

Activation metrics:

- registration completed;
- intake completed;
- operating map generated;
- functions confirmed;
- at least one owner assigned;
- at least one task created;
- dashboard opened.

Retention metrics:

- day-1 return;
- week-1 return;
- tasks updated;
- decisions logged;
- memory entries created;
- dashboard revisits.

---

# 21. Journey Failure Points

The journey fails if:

- onboarding feels too long;
- outputs feel generic;
- user cannot edit suggestions;
- no visible value appears quickly;
- terminology is too architectural;
- AI suggestions feel unsafe or unrealistic;
- dashboard is empty;
- user does not know what to do next.

---

# 22. UX Requirements

Bizzi MVP UX must be:

- guided;
- calm;
- simple;
- business-language first;
- editable;
- transparent;
- low-friction;
- focused on next action.

Avoid:

- complex setup screens;
- technical configuration first;
- excessive hierarchy;
- abstract architecture terminology;
- empty dashboards.

---

# 23. Journey Outputs

The core journey must create these outputs:

```text
Company Workspace
Structured Business Context
Business Operating Map
Function Registry
Responsibility Map
Agent Registry
Initial Task List
Decision Log
Enterprise Memory
Operating Dashboard
Audit Trail
```

---

# 24. Architecture Alignment

The core journey maps to Art of Business v1.0:

| Journey Output | Architecture Reference |
|---|---|
| Business Operating Map | Capability Map / Function Registry |
| Function Registry | Enterprise Function Registry |
| Responsibility Map | Governance / Decision Routing |
| Agent Registry | Agent Library |
| Task List | Operating Model |
| Decision Log | Decision Routing / Enterprise Memory |
| Memory Entries | Enterprise Memory |
| Dashboard | Observability and Intelligence |
| Audit Trail | Governance / Audit Model |

---

# 25. Final Core Journey Statement

```text
Bizzi’s core user journey transforms an overloaded business owner from scattered operational context to a visible operating dashboard in the first hour.
```

This journey becomes the product backbone for the Bizzi MVP.