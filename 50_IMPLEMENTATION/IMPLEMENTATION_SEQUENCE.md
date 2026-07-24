# Implementation Sequence — Gate C / Gate D

Version: 1.0
Scope: WP12a, WP13–WP32. See `IMPLEMENTATION_BACKLOG.md` for per-WP detail.

---

## 01. Mandatory Order (Critical Path)

```text
WP12a (Workspace)
  -> WP13 (EnterpriseObject)
  -> WP14 (AgentDefinition)          [BLOCKED: GC-001, ADW-05]
  -> WP15 (Task)
  -> WP16 (Identity/Auth)
  -> WP18 (Event)
  -> WP19 (AuditRecord)
  -> WP20 (ContextPackage)
  -> WP23 (Business Request Intake)
  -> WP24 (Agent Selection)           [blocked transitively via WP14]
  -> WP25 (Context Assembly)          [blocked transitively]
  -> WP26 (LLM Provider Adapter)      [BLOCKED: GC-001, ADW-05 — direct]
  -> WP27 (Agent Runtime Execution)   [blocked transitively]
  -> WP28 (Structured Recommendation) [blocked transitively]
  -> WP29 (Human Approval Flow)       [blocked transitively]
  -> WP30 (Decision Record + Events)  [blocked transitively]
  -> WP31 (Task/Session Completion)   [blocked transitively]
  -> WP32 (Internal End-to-End Demo)
```

This is unchanged from `MVP_WORK_PACKAGE_PLAN.md` §04's own critical path
for the WP13–WP32 span, with one addition: **WP12a inserted before WP13**,
correcting the Planning Gap identified by the Implementation Readiness
Review — every downstream WP's `workspace_id` foreign key needs WP12a's
table to exist first.

## 02. Why Each Dependency Exists

- **WP12a → WP13–WP22 (all)**: every Gate C entity carries `workspace_id`
  as a required, indexed field (ADR-0004). The column cannot be declared
  against a table that doesn't exist.
- **WP13 → WP14, WP15**: `AgentDefinition` and `Task` both reference an
  `EnterpriseObject` as their source/subject.
- **WP13, WP15 → WP20**: a `ContextPackage` is assembled from a task and
  its related object.
- **WP14 → WP17, WP21, WP24**: role checks need an agent role to check
  against; a `RuntimeSession` needs an `AgentDefinition` to execute; agent
  assignment needs an `AgentDefinition` to assign.
- **WP16 → WP17, WP19, WP23**: permission checks, audit actor
  attribution, and authenticated request intake all need `ActorContext`.
- **WP18 → WP21, WP30**: `RuntimeSession` and `Decision` both emit events.
- **WP13, WP16 → WP19**: an audit record needs both a subject (what was
  changed) and an actor (who changed it).
- **WP20, WP23, WP24 → WP25**: context assembly needs the task, the
  intake request, and the assigned agent all to exist first.
- **WP09, WP25 → WP26**: the provider adapter needs configuration
  (WP09) and something to execute against (WP25's assembled context).
- **WP17, WP21, WP25, WP26 → WP27**: agent execution needs
  authorization, a session container, context, and a provider — all four.
- **WP27 → WP28**: the recommendation is the shaped output of execution.
- **WP16, WP17, WP28 → WP29**: approval needs an authenticated,
  authorized human and something to approve.
- **WP18, WP19, WP29 → WP30**: a decision record is itself an audited
  event.
- **WP21, WP30 → WP31**: completion closes both the task and the session
  the decision was recorded against.
- **WP23–WP31 → WP32**: the demo is the whole chain running together;
  it has no dependency of its own beyond every prior step existing.

## 03. Parallel Work

Not everything sits on the critical path. These can proceed independently
once their own listed dependency is met, without waiting on the chain
above:

| Work Package | Depends only on | Can run in parallel with |
|---|---|---|
| WP17 (RBAC) | WP16 (human-role half); WP14 (agent-role half, blocked) | WP18, WP19, WP20, WP22 |
| WP22 (API standard) | WP06, WP10 | Everything in Gate C — has no Gate C entity dependency |
| WP18 (Event) | WP08, WP13 | WP19, WP20, WP21 (once WP13 lands) |
| WP20 (ContextPackage) | WP13, WP15 | WP18, WP19 |

**Practical effect**: a team does not need to wait for WP14/WP21 (the
Critical Path blockers) to make progress on WP13, WP15, WP16, WP18, WP19
(partially), WP20, and WP22 — five of the ten Gate C work packages are
fully unblocked today, and an sixth (WP17) is partially unblocked.

## 04. Critical Path (Restated, With Blockers)

The chain in §01, filtered to only the links that currently cannot
proceed, per the Implementation Readiness Review:

```text
WP14 (AgentDefinition)  <- BLOCKED: GC-001 (Approval Gap), ADW-05 (Modeling Gap)
   |
   +-> WP17 (partial), WP21, WP24 -> WP25 -> WP26 <- BLOCKED (same root cause, direct)
                                                |
                                                v
                                        WP27 -> WP28 -> WP29 -> WP30 -> WP31 -> WP32
```

Every work package from WP24 through WP32 — nine of Gate D's ten packages
— is downstream of the single WP14/WP26 root cause. Clearing GC-001 and
completing ADW-05 is therefore the highest-leverage action available:
it unblocks not one work package, but the entire back half of the
reference implementation in one step.

## 05. Dependency Tree (Full)

```text
WP12a
 └─ WP13
     ├─ WP14 [BLOCKED]
     │   ├─ WP17 (partial)
     │   ├─ WP21 [BLOCKED]
     │   └─ WP24 [blocked]
     │       └─ WP25 [blocked]
     │           └─ WP26 [BLOCKED, direct]
     │               └─ WP27 [blocked]
     │                   └─ WP28 [blocked]
     │                       └─ WP29 [blocked]
     │                           └─ WP30 [blocked]
     │                               └─ WP31 [blocked]
     │                                   └─ WP32 [blocked]
     ├─ WP15
     │   └─ WP20
     └─ WP18
         └─ WP19

WP16 ─┬─ WP17 (partial)
      ├─ WP19
      └─ WP23

WP22 (no Gate C entity dependency — parallel from the start)
```
