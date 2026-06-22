# TASK_ROUTER.md

# Art of Business

## Task Router v1.0

**Status:** Canonical Runtime Orchestration Specification  
**Architecture Layer:** 15_RUNTIME_ORCHESTRATION  
**Owner:** AG002_Chief_Orchestrator  
**Architecture Owner:** AG054_Enterprise_Architect  
**Operational Owner:** AG002_Chief_Orchestrator  
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

Task Router defines how incoming tasks, events, requests, signals, exceptions, and workflow triggers are classified, prioritized, assigned, routed, and tracked within the Art of Business runtime orchestration layer.

---

# 2. Mission

Ensure that every task enters the system with clear ownership, correct priority, proper workflow mapping, traceable routing logic, and controlled execution responsibility.

---

# 3. Architectural Position

```text
Event / Request / Signal
↓
Task Router
↓
Workflow Engine
↓
Agent Runtime
↓
Execution Service
↓
Result
```

Task Router is the entry control point for executable work.

---

# 4. Routing Principle

No task may be executed without:

- task identity;
- task owner;
- task type;
- priority;
- workflow mapping;
- audit record;
- execution status.

---

# 5. Task Intake Model

Task Router accepts tasks from:

- business processes;
- agent workflows;
- platform services;
- application services;
- external systems through MCP Gateway;
- human requests;
- scheduled events;
- escalation events.

---

# 6. Task Identity Model

Every task must have:

```text
Task ID
Task Type
Source
Created At
Created By
Owner
Priority
Status
Workflow ID
Audit ID
```

---

# 7. Task Classification Model

Canonical task classes:

```text
Business Task
Decision Task
Execution Task
Approval Task
Review Task
Escalation Task
Audit Task
System Task
```

---

# 8. Task Priority Model

Priority levels:

```text
P0 Critical
P1 High
P2 Normal
P3 Low
P4 Background
```

Priority is calculated from:

- business impact;
- deadline;
- risk level;
- compliance sensitivity;
- customer impact;
- executive visibility.

---

# 9. Routing Logic

Routing uses:

- task type;
- business domain;
- required capability;
- workflow mapping;
- agent availability;
- authority level;
- escalation rules;
- compliance requirements.

---

# 10. Workflow Mapping

Task Router maps tasks to workflows:

```text
Sales Task → SALES_WORKFLOW.md
Procurement Task → PROCUREMENT_WORKFLOW.md
Hiring Task → HIRING_WORKFLOW.md
Finance Task → FINANCE_WORKFLOW.md
Compliance Task → COMPLIANCE_WORKFLOW.md
Logistics Task → LOGISTICS_WORKFLOW.md
```

---

# 11. Agent Assignment Model

Assignment considers:

- agent role;
- agent capability;
- agent authority;
- current workload;
- domain ownership;
- availability;
- conflict-of-interest controls.

---

# 12. Queue Model

Queues:

```text
New Task Queue
Domain Queue
Agent Queue
Approval Queue
Escalation Queue
Retry Queue
Completed Queue
```

---

# 13. Task State Model

```text
Created
↓
Classified
↓
Queued
↓
Assigned
↓
Executing
↓
Waiting
↓
Completed
```

Alternative states:

```text
Rejected
Escalated
Failed
Cancelled
Archived
```

---

# 14. Decision Routing

Decision tasks are routed through:

```text
Task Router
↓
Decision Runtime
↓
Decision Service
↓
Human Approval if Required
```

---

# 15. Human Approval Routing

Approval routing applies when:

- authority threshold exceeded;
- confidence threshold violated;
- financial limit exceeded;
- compliance requirement triggered;
- human-in-the-loop policy applies.

---

# 16. Escalation Routing

Escalation path:

```text
Assigned Agent
↓
Workflow Owner
↓
Domain Owner
↓
Executive Owner
↓
CEO
```

---

# 17. Task Validation

Before routing, Task Router validates:

- completeness;
- source authenticity;
- required context;
- required authority;
- duplicate task risk;
- policy constraints.

---

# 18. Audit Model

Audited events:

```text
Task Created
Task Classified
Task Routed
Task Assigned
Task Escalated
Task Completed
Task Failed
```

Every routing decision must be auditable.

---

# 19. Observability Model

Metrics:

- task intake volume;
- routing latency;
- assignment latency;
- queue depth;
- escalation rate;
- retry rate;
- completion rate.

---

# 20. Security Model

Task Router enforces:

- identity checks;
- authority checks;
- access controls;
- segregation of duties;
- audit requirements;
- policy constraints.

---

# 21. Failure Handling

Failure types:

- no matching workflow;
- no available agent;
- missing context;
- invalid task source;
- authority conflict;
- routing timeout.

Failure actions:

```text
Retry
Escalate
Reject
Hold
Reassign
```

---

# 22. KPIs

Task Router KPIs:

- Routing Accuracy
- Mean Routing Time
- Assignment Success Rate
- Escalation Rate
- Queue Health
- Duplicate Task Rate
- Audit Coverage

---

# 23. Governance

AG002_Chief_Orchestrator owns Task Router governance.

AG054_Enterprise_Architect owns architectural consistency.

AG003_AI_Auditor owns traceability and routing audit validation.

---

# 24. Architectural Role

Task Router is the work intake and routing brain of the runtime orchestration layer.

```text
Signal
↓
Task Router
↓
Workflow Engine
↓
Agent Runtime
↓
Execution
```

It ensures that every task is classified, owned, routed, executed, and audited.