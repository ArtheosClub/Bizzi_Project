# Implementation Milestones — Gate C / Gate D

Version: 1.0

Each milestone below produces demonstrable working software — something
that can be run and shown, not a document, a decision, or an approval.
Clearing GC-001/ADW-05 (the Critical Path blockers) is a precondition for
M3 and M6, not a milestone in its own right — it has no demonstrable
software output.

---

## M0 — Workspace Foundation

**Work packages**: WP12a.
**Demonstrable outcome**: a Workspace can be created via the service layer
and persists across a restart.
**Status**: 🟢 Unblocked — recommended starting point.

## M1 — Core Objects

**Work packages**: WP13, WP15.
**Demonstrable outcome**: an `EnterpriseObject` and a `Task` can be
created, both correctly scoped to a Workspace, with the task's state
machine enforcing valid transitions.
**Status**: 🟢 Unblocked (after M0).

## M2 — Identity and Access

**Work packages**: WP16, WP17 (partial — human-role checks only).
**Demonstrable outcome**: a human user logs in, and role-based access
control correctly permits or denies an action within a Workspace.
**Status**: 🟢 Unblocked (after M0). Full WP17 (agent-role checks) waits
on M3.

## M3 — Agent and Observability Backbone

**Work packages**: WP14, WP18, WP19, WP20, WP21, WP22.
**Demonstrable outcome**: an agent can be defined; every action taken so
far produces an event and, where high-impact, an immutable audit record;
a context package can be assembled and survives session end. This
milestone completes Gate C's Infrastructure Boundary — after it, Bizzi
has a runnable backend with every canonical object model in place.
**Status**: 🔴 **Gated.** WP14 and WP21 are Critical Path — this milestone
cannot complete until GC-001 is approved and ADW-05 is written. WP18,
WP19, WP20, WP22 can and should be built in parallel while that
resolves (§03 of `IMPLEMENTATION_SEQUENCE.md`).

## M4 — Business Request Intake

**Work packages**: WP23.
**Demonstrable outcome**: an authenticated user submits a business
request through a real API call and receives a task ID back. This is the
first milestone with genuine business-facing functionality, not
infrastructure.
**Status**: 🟢 Unblocked (after M1, M2 — does not require M3).

## M5 — Agent Assignment and Context

**Work packages**: WP24, WP25.
**Demonstrable outcome**: a submitted task is assigned to an agent by
rule, and a valid context package is assembled for it.
**Status**: 🔴 Gated — depends on M3 (WP14).

## M6 — AI Execution

**Work packages**: WP26, WP27, WP28.
**Demonstrable outcome**: an agent actually runs against a real (or
test) LLM provider inside a controlled session and produces a structured
recommendation with a confidence score. This is the milestone that makes
Bizzi more than a CRUD application with an approval step.
**Status**: 🔴 Gated — depends on M3 and M5; WP26 additionally has a
direct, non-transitive dependency on GC-001/ADW-05.

## M7 — Human Approval and Decision

**Work packages**: WP29, WP30.
**Demonstrable outcome**: a human approver reviews the AI's
recommendation and approves, rejects, or requests rework; the decision
and its associated events/audit records are persisted.
**Status**: 🔴 Gated — depends on M6.

## M8 — Completion and Demo

**Work packages**: WP31, WP32.
**Demonstrable outcome**: the task and session close consistently, and
the complete scenario — Workspace → Enterprise Object → Task → AI
Analysis → Decision → Completion — runs end to end and is demonstrable
to the Project Owner. This is the Gate D exit milestone.
**Status**: 🔴 Gated — depends on M7.

---

## Milestone Summary

| Milestone | Demonstrable Outcome | Status | Gated By |
|---|---|---|---|
| M0 | Workspace persists | 🟢 | — |
| M1 | Object + Task with valid states | 🟢 | M0 |
| M2 | Login + human RBAC | 🟢 | M0 |
| M3 | Agent defined; events/audit/context wired | 🔴 | GC-001, ADW-05 |
| M4 | Business request submitted via API | 🟢 | M1, M2 |
| M5 | Task assigned; context assembled | 🔴 | M3 |
| M6 | Agent executes; recommendation produced | 🔴 | M3, M5 |
| M7 | Human approves/rejects; decision recorded | 🔴 | M6 |
| M8 | Full scenario demoable | 🔴 | M7 |

Five of nine milestones (M0, M1, M2, M4, and the parallelizable half of
M3) are buildable today. The remaining four are sequentially gated behind
one root cause: GC-001 approval and ADW-05 completion.
