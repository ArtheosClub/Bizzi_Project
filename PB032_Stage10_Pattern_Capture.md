# PB032 Stage 10 — Pattern Capture

Related Playbook: PB032_Process_Optimization_v2.0.md
Version: 1.0
Status: Draft Stage File

---

## Purpose

Stage 10 converts an audited process improvement into a reusable Optimization Pattern.

The purpose is to make Bizzi smarter over time. A successful local improvement should not remain local. If audit confirms that the improvement worked, the core logic must be captured as a reusable pattern that can be applied to other processes.

Stage 10 creates a `PAT` Optimization Pattern object linked to the source `AUD`, `ROLLOUT`, `SCN`, `SIM`, `ECON`, and `PROC` records.

---

## Function

KNW-LES-001 Lessons Learned Capture  
KNW-SOP-001 SOP Drafting / Update

---

## Primary Owner

AG053 Knowledge Curator

---

## Supporting Agents

| Agent | Role |
|---|---|
| AG047 Process Controller | Explains process logic and applicability |
| AG003 AI Auditor | Confirms pattern is based on validated result |
| AG067 Analytics Agent | Supplies measured effect and variance data |
| AG005 Risk Manager | Defines known risks and control requirements |
| AG007 Operations Manager | Confirms operational usefulness |
| AG002 Chief Orchestrator | Identifies cross-domain reuse potential |

---

## Decision Level

L1 for draft capture.  
L2 for publication into the Pattern Library.  
L3 if pattern affects cross-domain governance or standard operating model.

---

## Input Objects

Stage 10 consumes:

- `AUD` — Audit Report;
- `ROLLOUT` — Rollout Record;
- `SCN` — Optimization Scenario;
- `SIM` — Simulation Run;
- `ECON` — Economic Evaluation;
- `RISKREV` — Risk Review;
- `PROC` / `PROCV` — Process and Version;
- lessons learned;
- SOP changes;
- measured outcomes.

---

## Pattern Eligibility

A pattern may be captured only if:

- audit outcome is Effective or Partially Effective;
- source evidence is traceable;
- the improvement logic can be generalized;
- risks and constraints are known;
- applicable context can be defined;
- pattern does not depend on one unique local exception.

A pattern must not be published if:

- audit outcome is Harmful or Ineffective;
- improvement effect is unverified;
- source assumptions are unclear;
- risks are not understood;
- pattern would encourage governance bypass.

---

## Pattern Object Structure

```yaml
id: PAT-YYYY-####
pattern_name:
problem_type:
source_audit_report: AUD-YYYY-####
source_process: PROC-YYYY-####
source_scenario: SCN-YYYY-####
context:
before_state:
after_state:
core_mechanism:
applicable_processes:
required_controls:
expected_benefits:
known_risks:
contraindications:
reuse_conditions:
owner_agent: AG053
status:
```

---

## Pattern Categories

Patterns may be classified as:

- Approval Compression;
- Parallel Review;
- Queue Elimination;
- AI-First Validation;
- Exception-Only Human Review;
- Handoff Clarification;
- Batch-to-Flow Conversion;
- Auto-Triage;
- Decision Node Merge;
- Control Relocation;
- Rework Loop Removal;
- SLA Guardrail Addition;
- Capacity Rebalancing;
- Cost Leakage Closure;
- Governance Gate Reinforcement.

---

## Pattern Capture Activities

1. Review audit outcome.
2. Confirm eligibility for pattern capture.
3. Extract problem type.
4. Describe before-state and after-state.
5. Identify core mechanism of improvement.
6. Define applicability conditions.
7. Define required controls.
8. Define known risks and contraindications.
9. Link measured benefits.
10. Create Pattern Card.
11. Submit pattern for publication review.
12. Add pattern to Optimization Pattern Library if approved.

---

## Reuse Rules

Before applying an existing pattern elsewhere, Bizzi must check:

- similar problem type;
- compatible process context;
- compatible governance level;
- compatible risk profile;
- required controls available;
- no known contraindication;
- expected benefit still relevant.

Pattern reuse should create a link back to the original `PAT` object.

---

## Stage Gate 10

Stage 10 is complete only if:

- pattern eligibility is decided;
- Pattern Card is created or rejection rationale is recorded;
- source audit report is linked;
- applicability and risks are documented;
- publication status is assigned;
- Enterprise Memory handoff is prepared.

---

## Control Points

| Control Point | Owner | Purpose |
|---|---|---|
| Audit Eligibility Checked | AG003 | Prevent learning from unverified changes |
| Pattern Generalized | AG053 / AG047 | Convert local change into reusable logic |
| Risks Captured | AG005 | Prevent unsafe reuse |
| Applicability Defined | AG047 / AG002 | Avoid overgeneralization |
| Pattern Published | AG053 | Add to Pattern Library |
| Reuse Conditions Defined | AG053 | Support future matching |

---

## Output

Primary output:

- Optimization Pattern (`PAT`)

Secondary outputs:

- Pattern Rejection Note
- Reuse Conditions
- Contraindication Note
- Pattern Library Entry
- Enterprise Memory Handoff

---

## Completion Criteria

Stage 10 is complete when the audited improvement has either been converted into a validated Optimization Pattern or explicitly rejected as non-reusable.

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Stage 10 Pattern Capture stage file |
