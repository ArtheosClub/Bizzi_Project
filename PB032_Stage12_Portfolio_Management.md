# PB032 Stage 12 — Portfolio Management

Related Playbook: PB032_Process_Optimization_v2.0.md
Version: 1.0
Status: Draft Stage File

---

## Purpose

Stage 12 manages process optimization initiatives as an enterprise portfolio.

The purpose is to ensure that Bizzi does not treat improvements as isolated local events. Every opportunity, scenario, rollout, audit, pattern, and knowledge entry should be visible as part of the Enterprise Improvement Portfolio.

Stage 12 updates the `PORT` Portfolio Item and connects the completed optimization cycle to future prioritization, reporting, pattern reuse, and enterprise learning.

---

## Function

OPS-IMP-001 Improvement Initiative Tracking  
OPS-PER-001 Operational KPI Monitoring

---

## Primary Owner

AG007 Operations Manager

---

## Portfolio Visibility Owner

AG083 Dashboard Manager

---

## Supporting Agents

| Agent | Role |
|---|---|
| AG047 Process Controller | Provides lifecycle status and operational result |
| AG002 Chief Orchestrator | Reviews cross-domain portfolio implications |
| AG016 FP&A Agent | Tracks expected vs realized economic value |
| AG003 AI Auditor | Confirms audit status |
| AG053 Knowledge Curator | Confirms pattern and memory status |
| AG067 Analytics Agent | Supports portfolio analytics |
| AG001 CEO Agent | Reviews strategic portfolio insights when needed |

---

## Decision Level

L2 for standard portfolio updates.  
L3 for reprioritization across Operations.  
L4/L5 if portfolio insights affect strategic allocation, budget, operating model, or Human Board decisions.

---

## Input Objects

Stage 12 consumes:

- `PORT` — Portfolio Item;
- `OPT` — Optimization Opportunity;
- `DEC` — Governance Decision;
- `ROLLOUT` — Rollout Record;
- `AUD` — Audit Report;
- `PAT` — Optimization Pattern;
- `KNOW` — Knowledge Entry;
- expected and realized economic data;
- current lifecycle status.

---

## Portfolio Item Structure

```yaml
id: PORT-YYYY-####
related_opportunity: OPT-YYYY-####
related_process: PROC-YYYY-####
current_stage:
portfolio_status:
priority:
expected_roi:
realized_roi:
risk_rating:
audit_outcome:
pattern_status:
memory_status:
owner_agent: AG007
next_action:
closed_at:
status:
```

---

## Portfolio Lifecycle

```text
Detected
  -> Intake
  -> Mining
  -> Twin Built
  -> Simulated
  -> Evaluated
  -> Approved
  -> Pilot
  -> Rollout
  -> Audited
  -> Patternized
  -> Memory Updated
  -> Closed / Monitoring / Rework / Rollback
```

---

## Portfolio Statuses

| Status | Meaning |
|---|---|
| Active | Initiative is moving through PB032 |
| Parked | Waiting for data, timing, or capacity |
| Blocked | Cannot continue without intervention |
| Rework | Returned to earlier stage |
| Rolled Back | Change reverted |
| Monitoring | Implemented but still under observation |
| Closed Effective | Completed with effective result |
| Closed Partial | Completed with partial result |
| Closed Rejected | Rejected or archived |
| Patternized | Result converted into reusable pattern |

---

## Portfolio Metrics

Stage 12 tracks:

- total opportunities detected;
- active initiatives;
- initiatives by stage;
- initiatives by capability;
- expected ROI;
- realized ROI;
- expected vs realized variance;
- average time from detection to decision;
- average time from approval to rollout;
- audit outcome distribution;
- rollback rate;
- pattern conversion rate;
- reusable pattern count;
- blocked initiatives;
- portfolio risk exposure;
- capacity consumed by optimization work.

---

## Portfolio Activities

1. Update Portfolio Item lifecycle status.
2. Attach latest source objects.
3. Record expected vs realized value.
4. Record audit outcome.
5. Record pattern and memory status.
6. Identify blocked or delayed initiatives.
7. Identify duplicate or overlapping initiatives.
8. Reprioritize backlog if needed.
9. Escalate portfolio-level risks.
10. Update dashboard.
11. Recommend next optimization candidates.
12. Close, monitor, rework, or escalate the initiative.

---

## Portfolio Review Rules

AG007 and AG002 should review the portfolio periodically to identify:

- too many initiatives in one capability;
- too many high-risk rollouts at once;
- repeated failures in same process family;
- patterns that should become enterprise standards;
- economic assumptions that repeatedly fail;
- agents overloaded by improvement work;
- opportunities stuck in analysis;
- improvements that conflict with each other.

---

## Stage Gate 12

Stage 12 is complete when:

- Portfolio Item is updated;
- final or current lifecycle status is assigned;
- expected vs realized value is recorded where available;
- audit outcome is linked;
- pattern status is linked;
- memory status is linked;
- next action is defined;
- dashboard is updated.

---

## Control Points

| Control Point | Owner | Purpose |
|---|---|---|
| Portfolio Status Updated | AG083 | Maintain visibility |
| Lifecycle Objects Linked | AG047 | Preserve traceability |
| Economic Result Updated | AG016 | Track value realization |
| Audit Outcome Linked | AG003 | Separate verified from unverified value |
| Pattern Status Linked | AG053 | Track reusable learning |
| Portfolio Risk Reviewed | AG007 / AG002 | Prevent overload or conflicting changes |
| Next Action Defined | AG007 | Avoid dead initiatives |

---

## Closure Rules

An initiative may be closed only if:

- audit outcome is recorded or explicit exception is approved;
- rollout status is known;
- expected vs realized effect is recorded where possible;
- pattern capture decision is recorded;
- memory update decision is recorded;
- no unresolved rollback or rework action remains;
- portfolio next action is clear.

---

## Output

Primary output:

- Updated Portfolio Item (`PORT`)

Secondary outputs:

- Portfolio Dashboard Update
- Portfolio Risk Note
- Reprioritization Recommendation
- Next Optimization Candidate List
- Closure Record

---

## Completion Criteria

Stage 12 is complete when the improvement initiative is fully visible in the Enterprise Improvement Portfolio and its final or current state is traceable across opportunity, decision, rollout, audit, pattern, and memory.

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Stage 12 Portfolio Management stage file |
