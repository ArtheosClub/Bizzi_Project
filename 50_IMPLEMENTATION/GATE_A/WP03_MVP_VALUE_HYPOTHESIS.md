# WP03 — MVP Value Hypothesis

Version: 1.0  
Status: Proposed for Retrospective Approval  
Gate: A — Product Definition  
Priority: P0  
Depends On: WP02  
Blocks: WP04

## 1. Core Hypothesis

If a business owner can describe an operational problem in ordinary language and receive a structured, traceable recommendation with an explicit human approval step, then Bizzi will reduce the time and coordination required to move from problem recognition to a decision-ready action.

## 2. User Value

Bizzi should create value by:

- shortening the time from problem submission to decision-ready recommendation;
- reducing dependence on ad hoc meetings and scattered messages;
- making assumptions, risks, ownership, and confidence visible;
- preserving the full decision trail;
- turning approved outcomes into reusable organizational memory.

## 3. Primary Success Measures

For the reference demo scenario:

| Measure | MVP Target |
|---|---:|
| Time from accepted request to recommendation ready for human review | ≤ 5 minutes, excluding deliberate test delays |
| Required recommendation fields populated | 100% |
| Human decision actions available in the same governed flow | Approve, Reject, Request Rework |
| State-changing actions with audit records | 100% |
| Records carrying correct workspace identity | 100% |
| End-to-end scenario reproducible from documented clean setup | 100% |
| Critical stop conditions active at release decision | 0 |

## 4. Quality Signals

The recommendation is considered decision-ready when:

- it distinguishes symptoms from the likely root cause;
- it proposes one primary action rather than an unranked idea list;
- assumptions and risks are explicit;
- confidence is visible;
- the human approver can understand the recommendation without inspecting internal prompts or code;
- the full record chain can be reconstructed.

## 5. Product Learning Questions

The MVP must enable the project owner to answer:

1. Can the primary user submit a useful request without technical assistance?
2. Is the recommendation sufficiently concise and concrete to support a decision?
3. Does the user understand why human approval is required?
4. Is the execution and decision history trustworthy and easy to inspect?
5. Does the flow reveal which additional capabilities are genuinely needed next?

## 6. Invalidated Hypothesis Conditions

The hypothesis is not supported if any of the following occurs during the approved demo:

- the user must manually coordinate several disconnected tools;
- the recommendation lacks a concrete next action;
- the result cannot be linked to its input, context, execution, and decision;
- a recommendation is treated as approved without explicit human action;
- workspace isolation or authorization cannot be demonstrated;
- the flow requires implementation of the full agent catalog;
- failures disappear or produce a false successful state.

## 7. Guardrail Metrics

Speed alone does not establish value. The following guardrails must remain true:

- no cross-workspace data access;
- no authorization bypass;
- no missing audit record for a state-changing action;
- no raw secrets in logs, events, or responses;
- no skipped tests used to force a PASS;
- no autonomous execution beyond the approved authority level.

## 8. Evidence to Collect

Gate D and Gate E should collect:

- timestamps for request, recommendation, review, and decision;
- completeness validation results;
- actor and workspace linkage;
- user decision and reason;
- error/rework history;
- integration test result;
- qualitative owner assessment: useful, partially useful, or not useful.

## 9. Decision Rule

The MVP value hypothesis receives an initial PASS when the approved scenario meets every mandatory acceptance criterion in WP04 and the project owner judges the resulting recommendation useful enough to make or reject a real business decision.
