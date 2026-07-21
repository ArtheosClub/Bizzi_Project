# D07 — Iteration 0.3: Validation and Authority

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.3-draft  
**Status:** IN WORKSHOP  
**Decision:** D07.3 — Validation and Authority  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration defines who may request, validate, authorize, and commit a change of authoritative state in Bizzi.

## 2. Constitutional Decision

> A state transition is valid only when the owning domain authority confirms the subject, authority basis, actor attribution, expected state, invariants, evidence, and applicable policy or Decision requirements.
>
> Authority to request change is not authority to approve change, and authority to approve change is not authority to commit foreign aggregate state.

**Status:** PROPOSED

## 3. Authority Basis

Every governed transition must identify an authority basis. Valid forms include:

- explicit Decision;
- standing policy;
- delegated authority;
- contractual obligation;
- legal or regulatory duty;
- ownership right;
- emergency authority;
- system invariant;
- approved automated rule.

A missing authority basis is grounds for rejection when the transition is governed or significant.

## 4. Policy-Authorized and Decision-Authorized Transitions

A transition may rely on standing policy when:

- the policy is active and applicable;
- the subject and actor are within scope;
- all conditions are objectively satisfied;
- no higher-order Decision is required;
- the transition remains auditable.

A transition requires an explicit Decision when:

- discretion materially affects rights, money, risk, compliance, access, or strategic direction;
- policy requires human or designated authority approval;
- competing interests must be resolved;
- an exception is requested;
- the transition supersedes or revokes a prior determination.

## 5. Actor Attribution

Every significant transition must distinguish:

- `requested_by_actor` — who initiated the request;
- `effective_actor` — whose authority the action represents;
- `validated_by` — who or what performed validation;
- `authorized_by` — the authority basis or approving actor;
- `committed_by` — the owning aggregate or authorized domain process.

A service, agent, or workflow may act operationally, but it must not conceal the human, policy, Decision, or delegated authority under which it acts.

## 6. Delegation

Delegation must be explicit, scoped, time-bounded where appropriate, revocable, and auditable.

Delegation does not transfer ownership of authoritative state. It grants a defined ability to request or authorize specific transitions.

## 7. Validation Layers

The minimum semantic validation sequence is:

```text
Identity Validation
  -> Workspace and Subject Resolution
  -> Ownership Resolution
  -> Authority-Basis Validation
  -> Delegation Validation
  -> Current-State and Expected-Version Validation
  -> Invariant Validation
  -> Evidence and Result Validation
  -> Policy / Decision Validation
  -> Transition Acceptance or Rejection
```

Validation may be implemented synchronously or asynchronously, but the final commit must preserve the validated basis.

## 8. Evidence and Result Validation

A Result is evidence of execution output, not proof of accepted business truth.

Validation must determine:

- provenance;
- completeness;
- authenticity where required;
- relevance to the proposed transition;
- freshness and effective time;
- confidence or uncertainty;
- policy compliance;
- whether contradictory evidence exists.

AI-generated evidence must be identified as such and may not be treated as independently authoritative.

## 9. Rejection Semantics

A rejected transition request must not advance authoritative state.

A rejection should preserve:

- request identity;
- subject;
- requested target;
- actor attribution;
- authority basis presented;
- validation failures;
- rejection reason;
- decision time;
- retry or appeal eligibility.

## 10. Architectural Laws Added

### LAW-D07-20 — Authority Must Be Explicit

Every governed transition must have an identifiable and auditable authority basis.

### LAW-D07-21 — Request, Approval, and Commit Are Distinct

The ability to request, approve, or commit a transition are separate powers and must not be silently conflated.

### LAW-D07-22 — Delegation Does Not Transfer Ownership

Delegation grants scoped authority but does not transfer aggregate ownership of authoritative state.

### LAW-D07-23 — Validation Must Be Attributable

Validation and authorization of significant transitions must identify the actors, rules, policies, or Decisions responsible.

### LAW-D07-24 — Evidence Is Evaluated, Not Assumed

Results and evidence must be validated before they may support authoritative state change.

## 11. Decision Record

```text
D07.3 Validation and Authority: PROPOSED
Iteration 0.3: COMPLETE AS DRAFT
D07 overall status: IN WORKSHOP
```
