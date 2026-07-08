# CORE Decision Framework

Version: 1.0
Status: Core Architecture Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Enterprise_Event_Model.md
- GOVERNANCE_MODEL.md

Related Capability:
- C15 Governance
- C07 Operations
- C12 Finance
- C14 Knowledge Management

Primary Owner:
- AG002 Chief Orchestrator

Governance Owner:
- AG010 Governance Agent

Audit Owner:
- AG003 AI Auditor

Risk Owner:
- AG005 Risk Manager

---

## 00. Executive Summary

The CORE Decision Framework defines the universal decision logic for Bizzi.

It standardizes how decisions are requested, prepared, reviewed, approved, rejected, escalated, audited, and stored.

Core principle:

```text
No important action without a traceable decision.
No decision without owner, authority, rationale, and source evidence.
```

---

## 01. Purpose

This document defines:

- decision object structure;
- decision types;
- decision levels;
- decision lifecycle;
- decision routing;
- evidence requirements;
- escalation rules;
- audit and memory integration.

---

## 02. Decision Definition

A Decision is a governed choice that authorizes, rejects, changes, escalates, defers, or records an enterprise action.

Examples:

- approve process rollout;
- reject scenario;
- escalate risk;
- approve budget;
- change agent authority;
- publish pattern;
- trigger rollback;
- archive object.

---

## 03. Decision Object Model

```yaml
id: DEC-YYYY-####
decision_type:
decision_level:
decision_owner:
requesting_agent:
related_object:
related_playbook:
source_evidence:
risk_review:
economic_review:
audit_requirement:
human_override_required:
decision:
rationale:
conditions:
status:
created_at:
decided_at:
```

---

## 04. Decision Types

| Decision Type | Meaning |
|---|---|
| Approve | Authorize action |
| Approve with Conditions | Authorize only if conditions are met |
| Reject | Do not allow action |
| Request Rework | Return to earlier stage |
| Defer | Postpone decision |
| Escalate | Route to higher authority |
| Rollback | Return to previous state |
| Archive | Close or preserve without active use |
| Override | Human or higher authority overrides recommendation |

---

## 05. Decision Levels

| Level | Scope |
|---|---|
| L1 | Routine operational or knowledge update |
| L2 | Standard process or agent action |
| L3 | Material operational or cross-team decision |
| L4 | Financial, legal, compliance, or high-risk decision |
| L5 | Strategic, irreversible, or Human Board decision |

Decision level must align with Governance Model.

---

## 06. Decision Lifecycle

```text
Requested
  -> Prepared
  -> Reviewed
  -> Decided
  -> Communicated
  -> Executed
  -> Audited
  -> Archived
```

---

## 07. Evidence Requirements

Every non-routine decision should include:

- source object;
- problem or request statement;
- options considered;
- risk view;
- economic view where relevant;
- affected agents;
- affected capabilities;
- rollback or reversal logic;
- audit requirement.

---

## 08. Human Override

Human Override is required when:

- decision is L5;
- delegated authority is exceeded;
- legal, financial, or strategic exposure is material;
- AI recommendation conflicts with human judgment;
- irreversible or hard-to-reverse action is proposed.

Human Override status must be explicit.

---

## 09. Escalation Rules

A decision must escalate if:

- owner lacks authority;
- risk rating is High or Critical;
- cross-domain conflict exists;
- budget threshold is exceeded;
- legal or compliance exposure exists;
- Human Board control point is affected;
- audit detects governance violation.

---

## 10. Decision Quality Rules

A high-quality decision has:

- correct owner;
- correct decision level;
- source evidence;
- clear rationale;
- risk visibility;
- conditions if any;
- execution owner;
- audit path;
- memory path where relevant.

---

## 11. Integration

Decision Framework integrates with:

- Enterprise Object Model;
- Event Model;
- Workflow Framework;
- Audit Trail;
- Enterprise Memory;
- KPI Framework;
- PB032 Continuous Improvement Engine.

---

## 12. Success Criteria

This specification is successful if Bizzi can:

- make decisions traceable;
- route authority correctly;
- prevent unauthorized actions;
- preserve rationale;
- support audit and memory;
- distinguish recommendations from approvals.

---

## 13. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Core Decision Framework foundation specification |
