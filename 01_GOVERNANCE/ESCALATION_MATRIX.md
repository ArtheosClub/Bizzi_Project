# ESCALATION_MATRIX.md

# Art of Business

## Escalation Matrix

**Version:** 1.0
**Layer:** Governance
**Purpose:** Define when, how, and to whom issues, risks, decisions, authority conflicts, and execution problems must be escalated.

---

## 1. Escalation Principle

No critical issue may remain unresolved inside a single agent, domain, or workflow.

When authority, risk, uncertainty, conflict, or impact exceeds the current level, escalation is mandatory.

---

## 2. Escalation Levels

| Level | Name | Owner |
|---|---|---|
| E0 | No Escalation | Executing Agent |
| E1 | Agent-Level Escalation | Specialized Agent |
| E2 | Domain Escalation | Domain Manager |
| E3 | Orchestration Escalation | AG002 Chief Orchestrator |
| E4 | Executive Escalation | AG001 CEO |
| E5 | Human Governance Escalation | Human Governance Board |

---

## 3. Standard Escalation Path

```text
Execution Agent
↓
Domain Manager
↓
AG002 Chief Orchestrator
↓
AG001 CEO
↓
Human Governance Board
```

---

## 4. Escalation Triggers

Escalation is required when:

- authority is insufficient;
- task cannot be completed;
- data is missing or conflicting;
- risk exceeds approved tolerance;
- legal or compliance uncertainty exists;
- customer impact is material;
- financial exposure exceeds limits;
- cross-domain disagreement occurs;
- system or MCP tool fails;
- agent confidence is below threshold;
- human approval is required.

---

## 5. Risk-Based Escalation

| Risk Level | Escalation Level | Required Owner |
|---|---|---|
| Low | E0 | Executing Agent |
| Moderate | E1 | Specialized Manager |
| Medium | E2 | Domain Manager |
| High | E3 | Chief Orchestrator |
| Critical | E4 | CEO |
| Existential / Legal / Ethical | E5 | Human Governance Board |

---

## 6. Authority-Based Escalation

| Situation | Escalation |
|---|---|
| Agent lacks authority | E1 |
| Domain lacks authority | E3 |
| Decision affects multiple domains | E3 |
| Decision affects strategy | E4 |
| Decision requires human approval | E5 |

---

## 7. Financial Escalation

| Event | Escalation |
|---|---|
| Routine budget question | Finance Manager |
| Budget conflict | Chief Orchestrator |
| New budget required | CEO |
| Major financial commitment | CEO + Human |
| Bank access / irreversible transaction | Human Governance Board |

---

## 8. Legal and Compliance Escalation

| Event | Escalation |
|---|---|
| Contract ambiguity | Legal Manager |
| Compliance uncertainty | Compliance Manager |
| Regulatory exposure | CEO |
| Litigation risk | CEO + Human |
| Ethical or prohibited action | Human Governance Board |

---

## 9. Operational Escalation

| Event | Escalation |
|---|---|
| Task delay | Domain Manager |
| Process blockage | Chief Orchestrator |
| Vendor failure | Operations Manager |
| Delivery failure | Project Delivery Manager |
| Business continuity issue | CEO |

---

## 10. Technology Escalation

| Event | Escalation |
|---|---|
| Tool failure | Technology Manager |
| MCP failure | AI Automation Manager |
| Data inconsistency | Data Manager |
| Architecture conflict | Enterprise Architect |
| Production outage | CEO + Human if critical |

---

## 11. AI Behavior Escalation

| Event | Escalation |
|---|---|
| Low confidence | Domain Manager |
| Repeated error | AI Auditor |
| Authority breach | Chief Orchestrator |
| Unsafe recommendation | Risk Manager + AI Auditor |
| Autonomous behavior outside policy | CEO + Human |

---

## 12. Escalation Record Schema

Each escalation must create a record:

```yaml
escalation_id:
timestamp:
source_agent:
current_owner:
escalation_level:
reason:
risk_level:
affected_domain:
affected_customer:
affected_process:
required_decision:
recommended_action:
status:
resolution_owner:
resolution_deadline:
outcome:
```

---

## 13. SLA for Escalations

| Level | Response Time |
|---|---|
| E1 | Same working day |
| E2 | 4 business hours |
| E3 | 2 business hours |
| E4 | 1 business hour |
| E5 | Immediate / emergency protocol |

---

## 14. Escalation Resolution States

```text
Open
↓
Assigned
↓
Under Review
↓
Decision Required
↓
Resolved
↓
Closed
```

---

## 15. Anti-Patterns

Forbidden escalation behaviors:

- hiding uncertainty;
- retrying indefinitely without escalation;
- bypassing domain owners;
- escalating without context;
- escalating only after failure;
- executing while escalation is pending when action is high-risk.

---

## 16. Governance Rule

When in doubt, escalate.

The cost of unnecessary escalation is lower than the cost of uncontrolled execution.

---

## 17. Related Documents

- GOVERNANCE_MODEL.md
- AUTHORITY_MATRIX.md
- RACI_MATRIX.md
- DECISION_ROUTING_MODEL.md
