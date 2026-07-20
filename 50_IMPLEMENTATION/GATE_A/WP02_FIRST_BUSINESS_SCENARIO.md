# WP02 — First Business Scenario

Version: 1.0  
Status: Proposed for Retrospective Approval  
Gate: A — Product Definition  
Priority: P0  
Depends On: WP01  
Blocks: WP03

## 1. Scenario Name

Business Process Problem Analysis and Improvement Recommendation.

## 2. Scenario Goal

Prove that Bizzi can transform an unstructured operational concern into a governed, traceable recommendation and human decision without requiring the full future agent ecosystem.

## 3. Actor

Primary actor: business owner or operating leader defined in WP01.

Supporting actors:

- Chief Orchestrator configuration;
- Process Analysis Agent configuration;
- Reviewer/Auditor configuration;
- Human Approver.

## 4. Example Input

```text
Our customer quotations take too long. Sales sends requests to purchasing,
purchasing asks several suppliers, and the owner often has to intervene.
Customers wait three to five days and some stop responding. Analyze the
process, identify the main problem, and recommend an improvement.
```

Optional structured fields:

- business area: Sales / Purchasing;
- urgency: High;
- desired outcome: quotation within one business day;
- known constraints: supplier prices change frequently;
- approval required: Yes.

## 5. Canonical Flow

```text
Authenticated User
→ submits business problem in a workspace
→ Bizzi creates EnterpriseObject and Task
→ Chief Orchestrator selects Process Analysis Agent
→ ContextPackage is assembled
→ RuntimeSession executes
→ structured recommendation is produced
→ Reviewer/Auditor validates completeness and constraints
→ Human Approver approves, rejects, or requests rework
→ decision and final task state are persisted
→ event and audit records are written
→ result appears in Command Center
→ approved result becomes eligible for Enterprise Memory
```

## 6. Expected Structured Output

The recommendation must contain:

- normalized problem statement;
- observed symptoms;
- likely root cause or process constraint;
- proposed future-state process;
- recommended first action;
- expected benefit;
- assumptions;
- risks and dependencies;
- confidence level;
- approval requirement;
- traceable references to task, context, session, and decision.

## 7. Example Expected Recommendation

```yaml
problem_statement: Quotation preparation is delayed by sequential handoffs and owner-dependent exception handling.
likely_root_cause: No standardized supplier-response workflow, quotation SLA, or delegated approval threshold.
recommendation: Introduce a quotation workflow with approved supplier lists, one-hour supplier-response windows, reusable price validity rules, and owner escalation only above a defined margin or value threshold.
first_action: Map the current quotation steps and define approval thresholds for three common quotation types.
expected_benefit: Reduce routine quotation turnaround from 3–5 days to less than 1 business day.
confidence: medium
assumptions:
  - most quotations use recurring suppliers
  - pricing exceptions can be categorized
risks:
  - outdated supplier prices
  - poorly defined approval thresholds
approval_required: true
```

## 8. Human Decision Outcomes

The human approver must be able to:

- Approve — recommendation becomes the accepted outcome;
- Reject — recommendation is closed with a reason;
- Request Rework — task returns to an explicit rework state with comments.

No recommendation may be silently treated as approved.

## 9. Negative and Boundary Cases

The scenario must handle:

- unauthenticated request — denied;
- user without workspace membership — denied;
- missing or empty problem statement — validation error;
- provider/runtime failure — visible failure state, no false completion;
- reviewer rejection — result cannot advance to approval;
- cross-workspace object access — denied and security-signaled;
- missing audit record for a state-changing action — stop condition;
- duplicate submission — controlled by idempotency policy or explicitly recorded as a separate request.

## 10. Out of Scope for This Scenario

- automatic implementation of the recommendation;
- purchasing-system integration;
- supplier communication;
- autonomous financial commitment;
- multi-agent debate beyond the required configured roles;
- graph-based impact analysis as a dependency.

## 11. Completion Condition

WP02 is complete when the example input can be traced to the expected output contract and every step in the canonical flow has a named system record, actor, state transition, and approval boundary.
