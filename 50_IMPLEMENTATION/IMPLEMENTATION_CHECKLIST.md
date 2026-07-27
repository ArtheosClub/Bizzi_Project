# Implementation Checklist — Gate C / Gate D

Version: 1.0

Nine checks per work package, matching ADR-0003's Controller(Router)
→ Service → Repository layering and this repository's existing
coding-standards/testing conventions. A work package is not done until
every applicable box is true — this is the same bar `bizzi-pre-merge-check`
applies at merge time, expressed per-WP instead of per-PR.

Legend: ✅ applies and is required · — not applicable to this WP.

| WP | Database | Migration | ORM Model | Repository | Service | API | Validation | Tests | Documentation |
|---|---|---|---|---|---|---|---|---|---|
| WP12a Workspace | ✅ `workspaces` table | ✅ | ✅ | ✅ | ✅ | — | ✅ required fields | ✅ unit | ✅ update `C3_COMPONENT.md` |
| WP13 EnterpriseObject | ✅ | ✅ | ✅ | ✅ workspace-scoped | ✅ | ✅ CRUD endpoints | ✅ `workspace_id` required/indexed | ✅ unit + cross-workspace negative test | ✅ |
| WP14 AgentDefinition | 🔴 blocked | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | ✅ record GC-001/ADW-05 outcome once resolved |
| WP15 Task | ✅ | ✅ | ✅ | ✅ | ✅ D07 state machine | ✅ | ✅ transition rules enforced | ✅ every D07 transition + invalid-transition tests | ✅ |
| WP16 Identity/Auth | ✅ `users`, `workspace_memberships` | ✅ | ✅ | ✅ | ✅ `ActorContext` resolution | ✅ auth endpoints | ✅ | ✅ login + role-resolution tests | ✅ |
| WP17 RBAC | ✅ (role columns) | ✅ | ✅ | ✅ | ✅ permission checks | ✅ middleware | ✅ | ✅ allow/deny tests per role | ✅ record GC-003/004/008 outcome |
| WP18 Event | ✅ | ✅ | ✅ | ✅ invariant-scoped (GC-002 pending) | ✅ | — internal only | ✅ | ✅ workspace-isolation negative test | ✅ |
| WP19 AuditRecord | ✅ | ✅ | ✅ | ✅ workspace_id inherited, never set independently | ✅ atomic with audited write | — internal only | ✅ high-impact-mutation coverage | ✅ atomicity test (write fails ⇒ audit fails) | ✅ record GC-006/007 interim defaults used |
| WP20 ContextPackage | ✅ | ✅ | ✅ | ✅ | ✅ | — internal only | ✅ expiry handling | ✅ survives session-end test | ✅ |
| WP21 RuntimeSession | 🔴 blocked (depends on WP14) | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | ✅ record resolution once WP14 clears |
| WP22 API standard | — | — | — | — | ✅ shared envelope | ✅ applied to every endpoint | ✅ | ✅ error-shape contract test | ✅ record GC-005 outcome |
| WP23 Business Request Intake | — (composes WP13/15) | — | — | — | ✅ orchestrates WP13+WP15 | ✅ `POST /requests` | ✅ | ✅ end-to-end intake test | ✅ |
| WP24 Agent Selection | 🟡 blocked via WP14 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ |
| WP25 Context Assembly | 🟡 blocked via WP24 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ |
| WP26 LLM Provider Adapter | 🔴 blocked (GC-001 direct) | 🔴 | 🔴 | 🔴 | 🔴 | — internal only | 🔴 | 🔴 | ✅ record GC-001/ADW-05 outcome |
| WP27 Agent Runtime Execution | 🟡 blocked via WP26 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ |
| WP28 Structured Recommendation | 🟡 blocked via WP27 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ |
| WP29 Human Approval Flow | 🟡 blocked via WP28 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ `POST /decisions` (once unblocked) | 🟡 | 🟡 | ✅ |
| WP30 Decision Record + Events | 🟡 blocked via WP29 | 🟡 | 🟡 | 🟡 | 🟡 | — internal only | 🟡 | 🟡 | ✅ |
| WP31 Task/Session Completion | 🟡 blocked via WP21, WP30 | 🟡 | 🟡 | 🟡 | 🟡 | — internal only | 🟡 | 🟡 | ✅ |
| WP32 Internal E2E Demo | — (integration only) | — | — | — | — | — | — | ✅ full-scenario integration test | ✅ demo script |

**Reading the blocked rows**: 🔴 marks a check that cannot be started at
all (the design it would implement doesn't exist yet). 🟡 marks a check
that is technically startable in isolation but has no real dependency to
build against until its own upstream WP clears — per
`IMPLEMENTATION_SEQUENCE.md` §04, both classes trace back to the same
root cause (GC-001 approval, ADW-05 completion).

**Documentation** is marked ✅ for every row, including blocked ones,
because even a blocked WP has one documentation duty now: recording the
GC-item's outcome once it resolves, so the next engineer doesn't have to
re-discover why a table looks the way it does.
