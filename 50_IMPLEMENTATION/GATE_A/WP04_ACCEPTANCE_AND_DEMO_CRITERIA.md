# WP04 — Acceptance and Demo Criteria

Version: 1.0  
Status: Proposed for Retrospective Approval  
Gate: A — Product Definition  
Priority: P0  
Depends On: WP03  
Blocks: WP05

## 1. Purpose

This document defines the product-level PASS/FAIL contract for the first Bizzi MVP scenario. It does not replace implementation-level acceptance criteria in Gates B–E.

## 2. Gate A Acceptance Checklist

Gate A is ready for approval when all items below are true:

- [x] MVP scope and non-goals are explicit in WP00.
- [x] One primary user and top pain are defined in WP01.
- [x] One first business scenario with example input/output is defined in WP02.
- [x] Measurable value and guardrails are defined in WP03.
- [x] Product acceptance criteria and demo sequence are defined here.
- [x] Human approval remains explicit and mandatory where required.
- [x] The full future agent catalog is excluded from the MVP critical path.
- [x] The stack and gate sequence align with the accepted Pre-Coding Brief and ADR-0007.

## 3. End-to-End MVP Acceptance Criteria

The release-quality scenario receives PASS only when all mandatory criteria are demonstrated.

### 3.1 Request and Identity

- An authenticated primary user can submit the WP02 example problem.
- The request is associated with exactly one resolved workspace.
- A user without active workspace membership cannot submit or read the request.
- Invalid input returns a consistent validation response with request/correlation identity.

### 3.2 Records and Traceability

The flow creates or links:

- EnterpriseObject;
- Task;
- AgentDefinition;
- ContextPackage;
- RuntimeSession;
- structured recommendation/result;
- human Decision Record;
- Event records;
- immutable AuditRecord entries;
- optional Memory Entry after approval.

Every workspace-scoped record must carry or enforce the same workspace identity.

### 3.3 Recommendation Quality Contract

The result contains:

- problem statement;
- symptoms;
- likely root cause;
- one primary recommendation;
- first action;
- expected benefit;
- assumptions;
- risks/dependencies;
- confidence;
- approval requirement.

Missing mandatory fields produce an incomplete/rework state, not a successful completion.

### 3.4 Human Decision

The approver can:

- approve;
- reject with reason;
- request rework with comments.

Each action changes state consistently and creates an audit record. The system never infers approval from inactivity or agent output.

### 3.5 Visibility

The Command Center or equivalent MVP view shows:

- request/task identity;
- current status;
- assigned agent configuration;
- recommendation;
- human decision;
- key timestamps;
- visible failure or rework state;
- event timeline.

### 3.6 Failure and Security

The demo must prove at least these negative cases:

1. unauthenticated request is denied;
2. cross-workspace lookup is denied;
3. malformed request is rejected;
4. simulated runtime/provider failure remains visible and recoverable;
5. rejected or rework result cannot be marked approved;
6. missing-audit behavior is covered by an automated failing test or hard stop.

### 3.7 Reproducibility

- A clean environment starts with the documented command.
- Database migrations apply successfully.
- Demo data can be created deterministically.
- The automated integration scenario passes in CI.
- No tests are skipped to obtain PASS.

## 4. Demo Script

### Step 1 — Start

Start the documented Docker Compose environment and verify the health endpoint and database migration state.

### Step 2 — Authenticate

Sign in as the approved demo business owner and select the demo workspace.

### Step 3 — Submit

Submit the WP02 quotation-delay problem, including urgency and desired outcome.

### Step 4 — Observe Execution

Show creation of the EnterpriseObject and Task, agent assignment, ContextPackage, and RuntimeSession status.

### Step 5 — Review Result

Open the structured recommendation and verify every mandatory field.

### Step 6 — Human Decision

First demonstrate Request Rework or Reject on one run. Then execute a second controlled run and Approve it.

### Step 7 — Verify Traceability

Show the decision, events, audit records, correlation identity, and consistent workspace identity across records.

### Step 8 — Verify Visibility

Show the final approved state and timeline in the Command Center view.

### Step 9 — Verify Memory

Where Gate E memory is enabled, show that only the approved result is eligible for validated memory storage.

### Step 10 — Negative Test

Attempt access from a user or context without membership in the workspace and demonstrate denial without data disclosure.

## 5. PASS / FAIL Rule

### PASS

PASS requires:

- all Gate A artifacts approved;
- all mandatory end-to-end criteria demonstrated or covered by approved automated evidence;
- no active critical stop condition;
- explicit project-owner approval.

### CONDITIONAL PASS

Not permitted for Gate A. Open product-definition ambiguity must be resolved before PASS.

### FAIL

FAIL applies when any mandatory product artifact is absent, the user/value/scenario is ambiguous, or the acceptance contract permits silent approval, missing audit, or cross-workspace access.

## 6. Evidence Register

Future Gate D/E review must record:

- commit and deployment reference;
- integration test run;
- demo date;
- reviewer;
- project-owner decision;
- open non-blocking observations;
- links to defects or follow-up WPs.
