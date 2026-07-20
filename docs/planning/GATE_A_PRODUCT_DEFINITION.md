# Gate A — Product Definition

**Superseded by `50_IMPLEMENTATION/GATE_A/`.** This file originally
contained a short, single-document Gate A backfill (WP00–WP04: charter,
primary user, first business scenario, value hypothesis, acceptance/demo
criteria), written to close the sequencing gap flagged in
`docs/planning/DEVELOPMENT_PLAN.md` §4 (Gate B shipped before Gate A's
product-definition artifacts existed).

A separate, deliberately-commissioned Gate A audit produced a more
thorough and rigorous package covering the same WP00–WP04 scope — one
file per work package plus a formal review/approval record with an
explicit PASS/FAIL exit-criteria contract, negative/failure cases, and a
demo script. That package is canonical for Gate A going forward:

- `50_IMPLEMENTATION/GATE_A/WP00_MVP_CHARTER.md`
- `50_IMPLEMENTATION/GATE_A/WP01_PRIMARY_USER_DEFINITION.md`
- `50_IMPLEMENTATION/GATE_A/WP02_FIRST_BUSINESS_SCENARIO.md`
- `50_IMPLEMENTATION/GATE_A/WP03_MVP_VALUE_HYPOTHESIS.md`
- `50_IMPLEMENTATION/GATE_A/WP04_ACCEPTANCE_AND_DEMO_CRITERIA.md`
- `50_IMPLEMENTATION/GATE_A/GATE_A_REVIEW_AND_APPROVAL.md`

Its first-business-scenario content was checked against the scenario in
`docs/planning/PRE-CODING-BRIEF.md` §7 (the PB032-based "analyze a
business process, identify a problem, propose an improvement, pass to the
owner for approval" scenario) and confirmed compatible — same
`EnterpriseObject → Task → Agent → ContextPackage → RuntimeSession →
Recommendation → Decision → Event/Audit → Command Center → Memory`
contour, same MVP role set (Chief Orchestrator, Process Analysis Agent,
Reviewer/Auditor, Human Approver), same primary-user persona. It is a
concrete instantiation of §7's scenario, not a divergent one.

This file is kept only as a stable redirect — do not use it to plan new
work, and do not resurrect its original content; use
`50_IMPLEMENTATION/GATE_A/` instead.
