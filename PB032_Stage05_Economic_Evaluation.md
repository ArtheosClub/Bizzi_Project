# PB032 Stage 5 — Economic Evaluation

Related Playbook: PB032_Process_Optimization_v2.0.md
Version: 1.0
Status: Draft Stage File

---

## Purpose

Stage 5 translates simulated process improvement scenarios into economic language.

The purpose is to ensure that Bizzi does not approve process changes only because they appear operationally elegant. Every serious optimization must be evaluated by its expected economic effect, cost, risk adjustment, payback, capacity impact, and cost of doing nothing.

Stage 5 creates an `ECON` Economic Evaluation object linked to the selected `SCN`, `SIM`, `TWIN`, `OPT`, and baseline `MET` records.

---

## Function

OPS-COS-001 Cost Optimization Review  
OPS-PER-001 Operational KPI Monitoring

---

## Primary Owner

AG016 Financial Planning & Analysis Agent

---

## Operational Owner

AG047 Process Controller

---

## Supporting Agents

| Agent | Role |
|---|---|
| AG012 CFO Agent | Reviews high-impact financial assumptions |
| AG066 BI Analyst | Provides baseline and comparison metrics |
| AG067 Analytics Agent | Provides simulation outputs |
| AG007 Operations Manager | Validates operational feasibility |
| AG005 Risk Manager | Supplies risk adjustment logic |
| AG003 AI Auditor | Reviews traceability between economic claim and evidence |
| AG004 Business Analyst | Reviews business impact reasoning |

---

## Decision Level

L2 for low-impact economic evaluation.  
L3 for material operational cost or capacity impact.  
L4 if the scenario affects major financial exposure, strategic allocation, pricing, headcount, or capital expenditure.

---

## Input Objects

Stage 5 consumes:

- `SCN` — Optimization Scenario;
- `SIM` — Simulation Run;
- `MET` — Baseline Metrics;
- `TWIN` — Digital Twin;
- `OPT` — Optimization Opportunity;
- scenario assumptions;
- simulation limitations;
- cost data where available.

---

## Economic Evaluation Object Structure

```yaml
id: ECON-YYYY-####
related_opportunity: OPT-YYYY-####
related_scenario: SCN-YYYY-####
related_simulation: SIM-YYYY-####
related_process: PROC-YYYY-####
baseline_cost:
implementation_cost:
expected_savings:
capacity_value:
risk_adjustment:
expected_roi:
risk_adjusted_roi:
payback_period:
npv:
cost_of_delay:
cost_of_doing_nothing:
confidence_level:
finance_review_required:
cfo_review_required:
recommendation:
status:
```

---

## Economic Metrics

Stage 5 may evaluate:

- implementation cost;
- operating cost reduction;
- cycle time value;
- capacity value;
- rework reduction value;
- error reduction value;
- cost avoidance;
- opportunity cost;
- cost of delay;
- cost of doing nothing;
- payback period;
- ROI;
- risk-adjusted ROI;
- NPV where relevant;
- sensitivity range.

---

## Evaluation Activities

1. Confirm baseline cost and baseline metric set.
2. Review simulation outputs from Stage 4.
3. Estimate implementation cost.
4. Estimate operating savings.
5. Estimate capacity or revenue-enabling value where relevant.
6. Estimate cost avoidance and risk reduction value.
7. Calculate payback period and expected ROI.
8. Apply risk adjustment where uncertainty is material.
9. Identify cost of delay and cost of doing nothing.
10. Assign confidence level.
11. Determine whether CFO review is required.
12. Produce recommendation for governance review.

---

## Confidence Model

| Confidence | Meaning |
|---|---|
| Low | Economic estimate is highly assumption-based |
| Medium | Baseline is reasonable but uncertainty remains |
| High | Strong cost, metric, and simulation evidence exists |
| Verified | Economic impact has been reviewed by finance and later validated by audit |

Expected ROI must never be treated as realized ROI.

---

## CFO Review Triggers

AG012 CFO Agent review is required if:

- expected cost or savings exceeds L3 financial threshold;
- implementation requires material budget;
- headcount, pricing, margin, or capital allocation is affected;
- economic assumptions are highly uncertain but material;
- risk-adjusted ROI differs significantly from expected ROI;
- scenario affects investor, lender, grant, or board reporting.

---

## Stage Gate 5

The scenario may proceed to Stage 6 only if Stage 5 produces:

- Economic Evaluation ID;
- baseline cost or cost-gap note;
- implementation cost estimate;
- expected benefit estimate;
- payback / ROI logic;
- risk adjustment or explanation why not needed;
- confidence level;
- finance review status;
- recommendation.

---

## Control Points

| Control Point | Owner | Purpose |
|---|---|---|
| Baseline Cost Confirmed | AG016 / AG066 | Prevent fake savings |
| Implementation Cost Estimated | AG016 / AG047 | Show true investment need |
| Simulation Linked | AG067 | Preserve evidence chain |
| ROI Calculated | AG016 | Compare scenarios economically |
| Risk Adjustment Applied | AG005 / AG016 | Avoid overconfident economics |
| CFO Review Flagged | AG012 / AG016 | Route high-impact decisions correctly |
| Audit Traceability Checked | AG003 | Preserve later validation path |

---

## Rejection or Rework Criteria

A scenario is rejected or returned for rework if:

- economic benefit is not material;
- implementation cost exceeds expected value;
- payback period is unacceptable;
- expected ROI depends on weak assumptions;
- risk-adjusted ROI is negative or too low;
- cost of doing nothing is low and urgency is weak;
- economic analysis contradicts operational assumptions;
- finance review identifies missing cost components.

---

## Output

Primary output:

- Economic Impact Report (`ECON`)

Secondary outputs:

- Cost Assumption Register
- ROI Calculation Note
- Risk-Adjusted ROI Note
- CFO Review Request
- Rework Recommendation

---

## Completion Criteria

Stage 5 is complete when Bizzi has a traceable economic evaluation that shows whether the candidate scenario is worth governance review, rework, parking, or rejection.

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Stage 5 Economic Evaluation stage file |
