# D07 — Iteration 0.2: State Dimensions

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.2-draft  
**Status:** IN WORKSHOP  
**Decision:** D07.2 — State Dimensions  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration defines the independent semantic dimensions used to describe state in Bizzi. It prevents the common failure mode in which lifecycle phase, current activity, final result, completion percentage, and operational condition are collapsed into one universal `status` field.

## 2. Constitutional Decision

> Phase, Status, Outcome, Progress, and Health are separate semantic dimensions.
>
> No aggregate, workflow, projection, interface, or integration may collapse them into a single authoritative attribute.
>
> Each dimension answers a different question, has its own transition rules, and may change independently unless an explicit domain invariant defines a dependency.

**Status:** PROPOSED

## 3. Phase

**Question:** Where is the subject in its governed lifecycle?

Phase identifies a stable lifecycle region. It changes less frequently than operational status and must not describe temporary execution conditions.

Possible normalized phases include:

```text
Draft
Evaluation
Authorized
Planning
Execution
Validation
Closure
Closed
```

These values are a shared semantic vocabulary, not a mandatory universal state machine. Specialized aggregates may use narrower or richer phase models.

## 4. Status

**Question:** What is currently happening to or with the subject?

Status describes the present operational condition within a phase.

Possible normalized statuses include:

```text
Pending
Ready
Active
Running
Waiting
Blocked
Suspended
Completed
Inactive
Unknown
```

`Completed` status means that the relevant activity stopped or reached its local completion condition. It does not automatically establish a successful business outcome.

## 5. Outcome

**Question:** What governed result was determined?

Outcome is the accepted business or domain result of an activity, decision, operation, validation, or lifecycle segment.

Possible normalized outcomes include:

```text
Succeeded
Partially Succeeded
Failed
Rejected
Cancelled
Expired
Revoked
Superseded
Compensated
Unknown
```

Outcome must be based on explicit completion criteria and domain validation. Technical execution success is evidence, not an outcome by itself.

## 6. Progress

**Question:** How much of the defined scope has been completed?

Progress is a quantitative or milestone-based observation relative to an explicit scope and measurement model.

Progress must declare:

- the measured scope;
- the calculation method;
- the observation time;
- whether it is authoritative or derived;
- the source version.

A percentage is not required. Valid progress representations may include milestones, completed units, weighted work, or an explicitly unknown value.

`100%` progress does not automatically mean successful outcome, closed phase, or healthy execution.

## 7. Health

**Question:** How safely and normally is the subject proceeding?

Health is an operational assessment such as:

```text
Healthy
Warning
Critical
Unknown
Not Applicable
```

Health is derived by default. It becomes authoritative only when a specialized domain explicitly owns health as governed business state.

Health may be based on risk, delay, errors, policy violations, resource constraints, or service-level indicators. It must never silently mutate phase, status, or outcome.

## 8. Terminal Semantics

A dimension is terminal only within its own semantic scope.

- a terminal phase means no normal forward lifecycle phase remains;
- a terminal status means the current activity has ended;
- a terminal outcome means the relevant result has been determined;
- progress is not terminal merely because it equals 100%;
- health has no terminal meaning by default.

A subject may have a terminal outcome while remaining administratively open for closure, audit, compensation, appeal, or supersession.

## 9. Special Conditions

### Unknown

`Unknown` means the value cannot currently be determined with sufficient authority. It is not equivalent to missing data, null, pending, or failed.

### Pending

`Pending` means a known condition is awaiting a defined prerequisite, authority, time, resource, or action.

### Waiting

`Waiting` means progression is paused by an expected external or internal dependency.

### Blocked

`Blocked` means progression cannot continue because a known impediment must be resolved.

### Suspended

`Suspended` means progression was intentionally paused by an authorized actor, rule, or domain process.

### Expired

`Expired` is an outcome or lifecycle condition caused by passage of an effective deadline without required completion or renewal.

### Cancelled

`Cancelled` means an authorized termination before the intended result was achieved. It does not erase prior history.

### Failed

`Failed` means defined success criteria were not achieved after the relevant process or evaluation concluded.

### Rejected

`Rejected` means an authoritative evaluator declined a proposal, request, result, or transition.

### Compensated

`Compensated` means a later governed operation addressed effects of an earlier committed operation. Compensation does not rewrite the original history.

## 10. Cross-Dimension Rules

1. Status must not automatically determine outcome.
2. Progress must not automatically determine phase or outcome.
3. Health must not automatically determine authoritative business state.
4. A phase transition may require status and outcome preconditions, but only through explicit invariants.
5. A failed Runtime Session outcome does not automatically fail a Work Item or Business Operation.
6. A successful Work Item outcome does not automatically complete a Business Operation.
7. An unknown value must be represented explicitly where uncertainty is material.
8. Null, absent, not applicable, and unknown are distinct semantics.
9. Derived dimensions must expose source version and observation time.
10. User-interface labels may simplify presentation but must preserve the underlying distinctions.

## 11. Architectural Laws Added

### LAW-D07-15 — Orthogonal Dimensions

Phase, Status, Outcome, Progress, and Health represent different semantic questions and must not be collapsed into one field.

### LAW-D07-16 — Explicit Dependency

A change in one state dimension may affect another only through an explicit domain invariant or governed transition rule.

### LAW-D07-17 — Completion Is Not Success

Completion status and 100% progress do not by themselves establish a successful outcome.

### LAW-D07-18 — Explicit Uncertainty

Unknown, absent, pending, and not applicable are distinct and must not be silently interchanged.

### LAW-D07-19 — Health Is Derived by Default

Health is a derived operational assessment unless a specialized domain explicitly owns it as authoritative state.

## 12. Decision Record

```text
D07.2 State Dimensions: PROPOSED
Iteration 0.2: COMPLETE AS DRAFT
D07 overall status: IN WORKSHOP
```
