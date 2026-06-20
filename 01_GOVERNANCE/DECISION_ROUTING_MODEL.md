# DECISION_ROUTING_MODEL.md

# Art of Business

## Decision Routing Model

**Version:** 1.0
**Layer:** Governance
**Purpose:** Define how decisions are classified, routed, escalated, approved, executed, audited, and learned from across the enterprise.

---

## 1. Purpose

The Decision Routing Model ensures that every enterprise decision:

- reaches the correct authority;
- follows governance rules;
- respects risk limits;
- is auditable;
- is explainable;
- produces organizational learning.

No important decision should depend on a single agent acting in isolation.

---

## 2. Decision Lifecycle

```text
Trigger
↓
Context Collection
↓
Analysis
↓
Decision Classification
↓
Routing
↓
Approval (if required)
↓
Execution
↓
Audit
↓
Knowledge Capture
```

---

## 3. Decision Types

### D1 — Operational

Routine decisions executed inside approved playbooks.

Examples:

- task assignment;
- workflow execution;
- routine procurement;
- customer support actions.

Owner:

Domain Manager or Specialized Agent.

---

### D2 — Tactical

Decisions affecting performance, priorities, or resources.

Examples:

- budget allocation;
- staffing changes;
- campaign adjustments;
- vendor selection.

Owner:

Domain Manager.

---

### D3 — Cross-Domain

Decisions impacting multiple domains.

Examples:

- product launch;
- transformation project;
- ERP implementation.

Owner:

AG002 Chief Orchestrator.

---

### D4 — Strategic

Decisions affecting enterprise direction.

Examples:

- market expansion;
- business model changes;
- major investments.

Owner:

AG001 CEO.

---

### D5 — Human Reserved

Decisions reserved for human governance.

Examples:

- ownership structure;
- mergers and acquisitions;
- litigation strategy;
- ethical exceptions.

Owner:

Human Governance Board.

---

## 4. Routing Inputs

Every decision request must include:

```yaml
decision_id:
requestor:
domain:
objective:
context:
constraints:
risk_level:
financial_impact:
legal_impact:
customer_impact:
urgency:
recommended_action:
```

---

## 5. Routing Logic

### Step 1 — Authority Check

```text
Can current actor decide?
        │
        ├─ YES → Continue
        │
        └─ NO → Escalate
```

---

### Step 2 — Risk Check

```text
Risk within tolerance?
        │
        ├─ YES → Continue
        │
        └─ Escalate
```

---

### Step 3 — Compliance Check

```text
Legal or compliance concern?
        │
        ├─ NO → Continue
        │
        └─ Route to AG015 / AG016
```

---

### Step 4 — Strategic Impact Check

```text
Impacts strategy?
        │
        ├─ NO → Execute
        │
        └─ Route to CEO
```

---

## 6. Decision Routing Table

| Decision Type | Routed To |
|---|---|
| Operational | Specialized Agent / Domain Manager |
| Tactical | Domain Manager |
| Cross-Domain | Chief Orchestrator |
| Strategic | CEO |
| Human Reserved | Human Governance Board |

---

## 7. Risk-Based Routing

| Risk | Destination |
|---|---|
| Low | Operational Layer |
| Moderate | Domain Manager |
| High | Chief Orchestrator |
| Critical | CEO |
| Legal / Ethical / Existential | Human Governance Board |

---

## 8. Financial Routing

| Event | Route |
|---|---|
| Routine Spend | Finance Manager |
| Budget Change | Finance Manager |
| New Budget | CEO |
| Capital Allocation | CEO |
| Major Commitment | Human Approval |

---

## 9. Legal Routing

| Event | Route |
|---|---|
| Contract Review | AG015 Legal Manager |
| Regulatory Review | AG016 Compliance Manager |
| Legal Exposure | CEO |
| Litigation | Human Governance Board |

---

## 10. Technology Routing

| Event | Route |
|---|---|
| Infrastructure Change | AG051 |
| Automation Change | AG052 |
| Data Change | AG053 |
| Architecture Change | AG054 |
| Enterprise-Wide Technology Shift | CEO |

---

## 11. Human Approval Triggers

Human approval is mandatory when:

- legal commitments are created;
- ownership changes occur;
- major financial obligations are accepted;
- ethical concerns exist;
- customer harm is possible;
- regulatory exposure is material;
- governance rules are modified.

---

## 12. Decision Record Schema

```yaml
decision_id:
decision_type:
owner:
risk_level:
authority_level:
requestor:
context_reference:
recommended_action:
alternatives:
selected_option:
approval_path:
execution_owner:
status:
outcome:
```

---

## 13. Decision Status Flow

```text
Draft
↓
Under Analysis
↓
Pending Approval
↓
Approved
↓
Executing
↓
Completed
↓
Audited
↓
Learned
```

---

## 14. AI Decision Rules

Agents may:

- analyze;
- recommend;
- simulate outcomes;
- rank alternatives.

Agents may not exceed their authority level.

Every recommendation must include:

- rationale;
- assumptions;
- risk assessment;
- confidence estimate.

---

## 15. Audit Integration

Every decision must generate:

- decision record;
- approval record;
- execution record;
- audit record.

Audit owner:

AG003 AI Auditor.

---

## 16. Knowledge Integration

Every significant decision becomes a reusable knowledge asset.

Captured items:

- context;
- alternatives;
- outcome;
- lessons learned;
- future recommendations.

Knowledge owner:

AG026 Knowledge Manager.

---

## 17. Architecture Governance Routing

Changes affecting:

- capabilities;
- functions;
- agents;
- data model;
- MCP infrastructure;
- execution engine;
- digital twin;

must be reviewed by AG054 Enterprise Architect before approval.

---

## 18. Governance Rule

Decision routing must always follow:

```text
Authority
↓
Risk
↓
Compliance
↓
Strategy
↓
Execution
```

Never the reverse.

---

## 19. Success Criteria

Decision routing is successful when:

- every decision reaches the correct owner;
- approval paths are clear;
- escalation occurs automatically;
- authority violations do not occur;
- audit trails exist;
- lessons are captured.

---

## 20. Related Documents

- GOVERNANCE_MODEL.md
- AUTHORITY_MATRIX.md
- RACI_MATRIX.md
- ESCALATION_MATRIX.md
- AI_OPERATING_SYSTEM.md
