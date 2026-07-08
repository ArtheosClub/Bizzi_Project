# PB037 Enterprise KPI Framework

Version: 1.0
Status: Foundation Specification

Related Playbooks:
- PB032_Process_Optimization_v2.0.md
- PB032_Stage05_Economic_Evaluation.md
- PB032_Stage09_Audit_and_Validation.md
- PB032_Stage12_Portfolio_Management.md
- PB036_Enterprise_Simulation_Framework.md

Related Architecture:
- PB032A_Enterprise_Continuous_Improvement_Engine_Architecture.md
- PB032B_Enterprise_Improvement_Data_Model.md

Related Capability:
- C07 Operations
- C12 Finance
- C13 Technology
- C14 Knowledge Management
- C15 Governance

Primary Owner:
- AG066 BI Analyst

Operational Owner:
- AG047 Process Controller

Financial Owner:
- AG016 Financial Planning & Analysis Agent

Governance Owner:
- AG002 Chief Orchestrator

Audit Owner:
- AG003 AI Auditor

Dashboard Owner:
- AG083 Dashboard Manager

---

## 00. Executive Summary

PB037 defines the Enterprise KPI Framework for Bizzi.

The framework standardizes how Bizzi defines, measures, compares, governs, and learns from key performance indicators across processes, agents, capabilities, playbooks, simulations, and improvement initiatives.

KPIs are the measurement layer of the enterprise operating system.

Core flow:

```text
Objective
  -> Metric Definition
  -> Baseline
  -> Target
  -> Measurement
  -> Dashboard
  -> Decision
  -> Audit
  -> Learning
```

PB037 ensures that Bizzi does not optimize based on vague impressions, isolated numbers, or inconsistent measurement logic.

---

## 01. Purpose

PB037 defines:

- what counts as a KPI in Bizzi;
- how KPIs are created;
- how baselines and targets are defined;
- how KPIs connect to PB032 and simulation;
- how KPI ownership works;
- how KPI quality is governed;
- how dashboards and audits use KPIs;
- how expected and realized performance are compared.

---

## 02. Definition

A KPI is a governed performance measure tied to an enterprise objective, capability, process, agent, or initiative.

A KPI must have:

- name;
- purpose;
- owner;
- formula or measurement method;
- source data;
- baseline;
- target;
- measurement period;
- confidence level;
- decision use;
- review cadence.

A number without ownership, source, and decision use is not a KPI.

---

## 03. KPI Categories

| Category | Purpose |
|---|---|
| Strategic KPI | Measures progress toward enterprise goals |
| Capability KPI | Measures performance of a capability area |
| Process KPI | Measures process speed, quality, cost, risk, or throughput |
| Agent KPI | Measures agent performance or workload |
| Financial KPI | Measures cost, ROI, savings, margin, or value |
| Risk KPI | Measures exposure, incidents, controls, or compliance |
| Knowledge KPI | Measures learning, reuse, memory quality, and SOP health |
| Simulation KPI | Measures predicted scenario outcomes |
| Portfolio KPI | Measures improvement portfolio health and value |
| Customer KPI | Measures external experience, satisfaction, or friction |

---

## 04. KPI Data Model

```yaml
id: KPI-YYYY-####
kpi_name:
kpi_category:
purpose:
related_capability:
related_process:
related_agent:
related_playbook:
owner_agent:
formula_or_method:
source_data:
baseline_value:
target_value:
current_value:
measurement_period:
unit:
confidence_level:
decision_use:
review_cadence:
status:
```

---

## 05. Baseline and Target Rules

Every KPI used in PB032 should define:

- baseline value;
- baseline period;
- target value;
- target period;
- source data;
- measurement confidence;
- owner agent.

If baseline data is missing, Bizzi must create a Metric Gap Note rather than inventing a number.

---

## 06. KPI Lifecycle

```text
Proposed
  -> Defined
  -> Approved
  -> Measured
  -> Reviewed
  -> Used in Decision
  -> Audited
  -> Updated / Deprecated / Archived
```

### Lifecycle Statuses

| Status | Meaning |
|---|---|
| Proposed | KPI candidate identified |
| Defined | Formula and owner assigned |
| Approved | KPI accepted for use |
| Active | KPI is measured and used |
| Under Review | KPI definition or quality is being reviewed |
| Deprecated | KPI should no longer guide decisions |
| Archived | Preserved for history |

---

## 07. KPI Quality Rules

A KPI is high quality if:

- it is tied to a real decision;
- it has an owner;
- it has reliable source data;
- it has a clear formula or method;
- it has baseline and target;
- it can be audited;
- it does not create harmful incentives;
- it is not duplicative;
- it is reviewed periodically.

A KPI should be rejected if:

- it is vague;
- it has no owner;
- source data is unknown;
- it cannot be measured consistently;
- it encourages metric gaming;
- it conflicts with a higher-priority KPI;
- it is not used for any decision.

---

## 08. KPI Confidence Levels

| Level | Meaning |
|---|---|
| Low | Weak source data or unclear measurement |
| Medium | Usable but with known limitations |
| High | Reliable data and stable method |
| Verified | Audited and trusted for governance decisions |

Critical decisions should not rely on Low-confidence KPIs unless explicitly approved.

---

## 09. PB032 KPI Set

PB032 improvement initiatives commonly use:

| KPI | Purpose |
|---|---|
| Cycle Time | Measures process duration |
| Waiting Time | Measures idle time between steps |
| Rework Rate | Measures repeated correction |
| Error Rate | Measures process defects |
| Throughput | Measures output volume |
| SLA Compliance | Measures deadline performance |
| Cost per Case | Measures process unit cost |
| Capacity Utilization | Measures workload balance |
| Automation Rate | Measures share of automated work |
| Control Integrity | Measures whether controls remain effective |
| Expected ROI | Measures projected financial return |
| Realized ROI | Measures actual post-rollout return |
| Pattern Reuse Rate | Measures learning reuse |
| Audit Confirmation Rate | Measures validated improvement success |

---

## 10. Expected vs Realized KPI Logic

Bizzi must distinguish:

- expected KPI impact from simulation;
- target KPI impact from decision record;
- actual KPI impact from rollout;
- audited KPI impact from post-implementation validation.

This prevents simulated or expected value from being treated as achieved value.

---

## 11. Dashboard Integration

PB037 supports dashboards for:

- process performance;
- improvement portfolio;
- agent workload;
- economic impact;
- risk exposure;
- pattern reuse;
- Enterprise Memory quality;
- governance health;
- simulation accuracy.

Dashboards must show data confidence and status, not only metric values.

---

## 12. Governance

KPI governance requirements:

- every KPI has an owner;
- formula or method is documented;
- source data is documented;
- confidence level is visible;
- KPI changes are versioned;
- deprecated KPIs are not used for active decisions;
- high-impact KPI changes require governance review;
- audit can trace KPI source and calculation.

---

## 13. Agent Responsibilities

| Agent | Responsibility |
|---|---|
| AG066 BI Analyst | Owns KPI definitions, baselines, and measurement quality |
| AG083 Dashboard Manager | Maintains KPI dashboards |
| AG047 Process Controller | Defines process KPI needs |
| AG016 FP&A Agent | Owns financial KPI logic |
| AG003 AI Auditor | Audits KPI traceability and reliability |
| AG005 Risk Manager | Defines risk KPIs |
| AG053 Knowledge Curator | Defines knowledge and reuse KPIs |
| AG002 Chief Orchestrator | Ensures cross-domain KPI alignment |

---

## 14. Anti-Patterns

PB037 must prevent:

- vanity metrics;
- ownerless KPIs;
- inconsistent formulas;
- hidden source data;
- expected ROI treated as realized ROI;
- local KPI optimization harming enterprise outcomes;
- too many dashboards with no decision use;
- metric gaming;
- stale KPIs still used in governance.

---

## 15. Success Criteria

PB037 is successful if Bizzi can:

- define measurable objectives;
- compare baseline, target, expected, actual, and audited results;
- support PB032 with reliable metrics;
- prevent metric misuse;
- power dashboards;
- guide governance decisions;
- learn from KPI variance over time.

---

## 16. Open Items

Future design decisions:

- Should KPI metadata use YAML frontmatter?
- Should KPI definitions become separate registry files?
- Should dashboards be generated automatically from KPI objects?
- Should KPI confidence be calculated automatically?
- Should every playbook define a standard KPI set?

---

## 17. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Enterprise KPI Framework foundation specification |
