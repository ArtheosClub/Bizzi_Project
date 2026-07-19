# Bizzi_Project — Pre-Coding Brief for Claude Code

**Purpose of this document:** Read this in full before writing any code or modifying WP-planning, ADRs, or C4 diagrams. It resolves open architectural questions and defines the actual MVP build order — which is *not* the same as the PB (playbook) numbering or the full 94-WP catalog.

---

## 1. Architecture Decision (supersedes prior ADR ambiguity)

**This is now a decided stack, not an open question.**

| Layer | Choice |
|---|---|
| Backend | Python + FastAPI |
| Frontend | React + TypeScript |
| MVP deployment | Docker Compose |
| Architecture style | Modular monolith |
| Kubernetes | **Not** part of MVP. Adopted only after the MVP works and scaling need is proven. |

**Guiding principle:** *Kubernetes-ready, but not Kubernetes-dependent.*
Design module boundaries and service interfaces so a future extraction to Kubernetes is possible, but do not build Kubernetes manifests, service mesh, or orchestration complexity now. If the existing ADR still states TypeScript/NestJS as the MVP backend, update it — this Python/FastAPI decision is the one to build against.

---

## 2. Critical distinction: PB numbering ≠ build order

The playbook numbering (PB001–PB054) and the 94 total work packages are a **capability catalog**, not a sequencing plan. Do not build in PB-number order or attempt all 94 WPs before shipping something real.

- **94 total work packages** ≠ 94 prerequisites for MVP.
- **20–25 WP** = mandatory MVP critical path.
- **15–20 WP** = MVP hardening.
- Everything else = post-MVP backlog.

---

## 3. Real dependency chain (what actually blocks what)

```
Product Scenario
  ↓
Repository + Local Environment
  ↓
Canonical Models + Database
  ↓
Minimal API + Authentication
  ↓
Event Log
  ↓
Task Engine
  ↓
Context Package
  ↓
One Agent Runtime
  ↓
Human Approval / Decision
  ↓
Result + Audit
  ↓
One Command Center Screen
  ↓
Memory
  ↓
Graph Projection
```

### Component dependency table

| Component | Depends on | What it blocks |
|---|---|---|
| Repository and environment | nothing | all development |
| Canonical models | Domain Model | DB, API, events |
| PostgreSQL and migrations | models | tasks, decisions, audit |
| Minimal Auth | identity model | user operations |
| API skeleton | models, DB | frontend and runtime |
| Event log | canonical Event | timeline, audit, monitoring |
| Task Engine | API, DB, events | Runtime |
| Context Engine | MVP task, object storage | Agent Runtime |
| Agent Runtime | task, context, permissions | real execution |
| Decision/Approval | MVP runtime result, identity | business cycle completion |
| Command Center | MVP task, events, decisions | user value |
| Memory | result and audit | learning loop |
| Knowledge Graph | stable objects/relations | impact analysis, semantic context |

---

## 4. MVP runtime roles (not the full 83+ agent library)

For the MVP, only **3–5 runtime roles** are needed:

1. **Chief Orchestrator** — routes the scenario.
2. **Execution Agent** — performs the core task.
3. **Reviewer / Auditor** — validates the result.
4. **Human Approver** — makes the critical decision.
5. *(Optional)* **Knowledge Curator** — persists the outcome to memory.

The full 83+ agent specification library remains a **catalog of future roles** — it is not a build list for v1. Do not implement or scaffold agents beyond these 3–5 roles in the MVP phase.

---

## 5. One universal Agent Runtime — not per-agent implementations

Build a single generic runtime with these core entities:

- `AgentDefinition`
- `AgentSession`
- `AgentCapability`
- `PermissionProfile`
- `PromptConfiguration`
- `ToolBinding`

Every one of the 3–5 MVP roles should be a *configuration* of this runtime, not a separately coded implementation.

---

## 6. Definition of "scaffolding is done" (exit criteria for infra phase)

Infrastructure and scaffolding work is complete — and business-logic work can begin — once the following exist and run:

- Runnable backend
- Frontend shell
- PostgreSQL with migrations
- Redis (only if there's a real, demonstrated need — do not add speculatively)
- Docker Compose setup
- Health endpoint
- Minimal authentication
- Base models: `Object`, `Task`, `Event`, `Agent`
- Structured logging
- One CI workflow
- One local-run command

Do not let scaffolding open-endedly expand beyond this list before moving to Gate D (first vertical slice).

---

## 7. First real business scenario (the actual "hello world" of Bizzi)

The first end-to-end flow to implement is:

```
User creates a request
  → Bizzi creates a Task
  → selects an Agent
  → assembles Context
  → Agent produces a Result
  → (if required) user approves
  → Result is stored
  → Event appears in Command Center
```

**Concrete first scenario to build:**
> "Analyze a described business process, identify a problem, propose an improvement, and pass the recommendation to the owner for approval."

This maps well to the already-mature **PB032** and exercises nearly the entire minimal contour:
`Object → Task → Agent → Context → Recommendation → Decision → Event → Audit → Memory → Command Center`

---

## 8. Recommended WP-plan structure (Gates)

Restructure/interpret the WP plan as five gates, not a flat 0–93 sequence:

**Gate A — Product Definition** (WP00–WP04)
- MVP scenario, user, problem, expected outcome, acceptance criteria

**Gate B — Engineering Foundation** (WP05–WP12)
- Repo structure, Python/FastAPI skeleton, PostgreSQL, migrations, Docker Compose, configuration, CI, health checks

**Gate C — Platform Backbone** (WP13–WP22)
- `EnterpriseObject`, `AgentDefinition`, `Task`, `Event`, `Auth`, `Audit`, `API`, `RuntimeSession`, `ContextPackage`

**Gate D — First Vertical Slice** (WP23–WP32)
- Create request → create task → assign one agent → build context → execute → return result → human approve/reject → store decision → emit event → display result

**Gate E — MVP Completion** (WP33–WP39)
- Memory entry, basic timeline, error handling, integration tests, demo data, deployment, user documentation

Everything beyond WP39 in the current 94-WP catalog is post-MVP backlog and should not block Gate A–E execution.

---

## 9. Stack decision supersedes PR #1 — explicit resolution required

PR #1 already merged (or is about to merge) a full governance scaffold built around **TypeScript/NestJS/PostgreSQL/Prisma**, formalized in `docs/adr/0002-bizzi-mvp-backend-stack-scope.md`. This brief **overrides that decision**: the MVP backend stack is now **Python + FastAPI**, per Section 1.

This must be handled as a proper ADR supersession, not a silent rewrite:

1. **Do not edit ADR-0002 in place.** Create a new ADR — e.g. `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md` — that:
   - States the new decision (Python + FastAPI + PostgreSQL, modular monolith, Docker Compose, Kubernetes-ready-not-dependent per Section 1)
   - Explicitly marks ADR-0002 as **Superseded by ADR-0007**
   - Explains the rationale for the change
2. **Update ADR-0002's status header** to `Superseded by ADR-0007` (status line only — do not delete or rewrite its original content; it stays as a historical record).
3. **Carry over what is stack-agnostic** — these ADRs and diagrams encode architectural principles, not NestJS-specific implementation, and remain valid as-is:
   - ADR-0003 (Controller-Service-Repository layering) — reinterpret as Router/Endpoint → Service → Repository for FastAPI
   - ADR-0004 (workspace-scoped multi-tenancy)
   - ADR-0005 (audit-first mutations)
   - ADR-0006 (authorization model for MVP)
   - `docs/c4/C1_CONTEXT.md` (system context)
   - `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — the canonical mutation flow (Controller → Service → Authorization → Validation → Transaction → Repository → Audit → Event) is a valid pattern for FastAPI; only relabel "Controller" as "Router/Endpoint" if needed.
4. **Must be rewritten for the new stack:**
   - `docs/c4/C2_CONTAINER.md` — if it names NestJS-specific containers
   - `docs/c4/C3_COMPONENT.md` — this is explicitly NestJS-module-based (ConfigModule → HealthModule) and has no FastAPI equivalent; rewrite for the actual Python module/router structure once it exists
   - Any source code already written against NestJS/Prisma (audit what exists before writing new code; do not leave orphaned NestJS files in the repo)
   - `WORK_PACKAGES.md` / `DEVELOPMENT_PLAN.md` where they reference NestJS/Prisma-specific deliverables (e.g. Prisma migrations → replace with SQLAlchemy/Alembic or equivalent)
5. **`CLAUDE.md` governance gates and stop conditions stay valid** (workspace isolation, authorization bypass, missing audit records, CI failures as hard blockers) — these are stack-agnostic and should not be touched.

## 10. Instructions to Claude Code

1. Treat the backend stack question as **resolved in favor of Python/FastAPI**, per Section 9. Do not re-litigate NestJS vs. FastAPI — implement the ADR supersession described above, then proceed.
2. Do not begin coding until Gate A (WP00–WP04) product-definition artifacts exist and are reviewed.
3. Do not implement more than the 3–5 MVP runtime roles listed in Section 4, even if playbooks reference other agents — reference them as future catalog entries only.
4. Follow the dependency chain in Section 3 strictly; do not start a component before its dependencies exist and pass their own checks.
5. Before making any change to `docs/adr/`, `docs/c4/`, or `docs/planning/`, list out exactly what will change and why, and flag anything ambiguous, rather than silently overwriting content.
6. Report back explicitly on what (if any) NestJS/Prisma source code already exists in the repo before writing new FastAPI code, so nothing orphaned is left behind.
