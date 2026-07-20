# WP01 — Primary User Definition

Version: 1.0  
Status: Proposed for Retrospective Approval  
Gate: A — Product Definition  
Priority: P0  
Depends On: WP00  
Blocks: WP02

## 1. Primary User

The primary MVP user is an owner, managing director, or operating leader of a small or medium-sized business who is responsible for solving operational problems but does not have a permanent internal business-analysis team.

## 2. User Context

The primary user:

- understands the business problem but may describe it informally;
- needs a decision-ready recommendation rather than a long analytical report;
- works under time pressure;
- must remain accountable for the final decision;
- needs visibility into how the recommendation was produced;
- expects the system to preserve context, decisions, and lessons for future use.

## 3. Top Pain

The primary pain is the gap between noticing an operational problem and receiving a structured, traceable recommendation that can be approved and acted upon.

Typical symptoms:

- decisions depend on scattered messages and individual memory;
- root causes are not separated from symptoms;
- recommendations are difficult to compare or audit;
- responsibility for the next step is unclear;
- previous decisions and outcomes are not reused;
- the business owner becomes the bottleneck for analysis and coordination.

## 4. Jobs to Be Done

When I notice a recurring or material business-process problem, I need to:

1. describe the problem in ordinary language;
2. have Bizzi structure it as a governed task;
3. receive a concise analysis and improvement recommendation;
4. inspect assumptions, confidence, and relevant context;
5. approve, reject, or request rework;
6. preserve the decision and outcome for later review.

## 5. User Outcome

The primary user should leave the flow with:

- a clear problem statement;
- an identified likely cause or constraint;
- one primary recommendation;
- supporting rationale and assumptions;
- a visible confidence level;
- a recorded decision;
- an accountable next action;
- a reconstructable event and audit trail.

## 6. Secondary Participants

Secondary participants are not independent MVP personas. They support the primary user:

- Reviewer/Auditor — checks quality, policy, and completeness;
- Process Analysis Agent — produces the structured recommendation;
- Chief Orchestrator — routes the execution;
- Knowledge Curator — optional post-approval memory action;
- Workspace Administrator — configures access but is not the product-value persona.

## 7. Excluded Primary Personas for MVP

The following are not primary MVP users:

- software developer;
- enterprise platform administrator;
- external consultant operating across many customers;
- marketplace provider;
- autonomous AI agent acting without a human owner;
- large-enterprise specialist requiring complex departmental workflows.

## 8. Design Implications

The MVP must:

- accept plain-language business input;
- avoid requiring technical configuration during the main flow;
- present concise, decision-oriented output;
- make human approval explicit;
- show status, ownership, and history;
- preserve traceability without exposing implementation complexity;
- support one workspace and one active business context per request.

## 9. Validation Statement

WP01 is satisfied when product, UX, API, and demo decisions consistently optimize for the business owner/operator described above rather than for the engineering team or the full future agent ecosystem.
