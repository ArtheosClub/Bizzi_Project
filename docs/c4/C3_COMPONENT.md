# C3 — Component Diagram (Backend API container)

Scope: components inside the Backend API container. Solid = built (Gate B,
`backend/app/`, merged to `main`). Dashed = planned (Gate C,
`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` WP13–WP22).

This is a from-scratch rewrite for the actual Python/FastAPI package
structure — the previous version of this diagram was NestJS-module-based
(`ConfigModule` → `HealthModule`) and had no equivalent in this codebase;
ADR-0007 §9.4 flagged it as needing this rewrite when the stack changed.

```mermaid
flowchart TB
    subgraph API["Backend API (FastAPI) — backend/app/"]
        config["app.core.config<br/>Settings (pydantic-settings)<br/>fail-fast on missing DATABASE_URL"]
        logging_["app.core.logging<br/>JsonFormatter, structured stdout logs"]
        dbsession["app.db.session<br/>SQLAlchemy engine + SessionLocal + get_db()"]
        dbbase["app.db.base<br/>Declarative Base (empty — no models yet)"]
        health["app.api.health<br/>GET /health"]
        main["app.main<br/>FastAPI app, lifespan, router registration"]

        eo["EnterpriseObject router/service/model<br/>(WP13)"]
        agentDef["AgentDefinition router/service/model<br/>(WP14) — PRE-CODING-BRIEF.md §5.1"]
        task["Task router/service/model<br/>(WP15)"]
        identity["Identity/Auth<br/>(WP16)"]
        rbac["Role/Permission checks<br/>(WP17)"]
        event["Event model/service<br/>(WP18)"]
        audit["AuditRecord model + AuditService.record(...)<br/>+ append-only workspace-scoped repository<br/>(WP19 — implemented on feat/wp19-audit-record-core,<br/>pending merge)"]
        context["ContextPackage model/service<br/>(WP20) — PRE-CODING-BRIEF.md §5.2"]
        runtime["RuntimeSession model/service<br/>(WP21) — PRE-CODING-BRIEF.md §5.1"]
        apistd["API error/response standard<br/>(WP22)"]
    end
    db[("PostgreSQL 18.4")]

    main -->|"registers"| health
    main -->|"reads settings via"| config
    main -->|"configures"| logging_
    dbsession -->|"reads settings via"| config
    dbsession -->|"Prisma-free: psycopg v3"| db

    identity -.->|"supplies ActorContext to"| eo
    eo -.->|"checked via"| rbac
    task -.->|"checked via"| rbac
    task -.->|"assigned to"| agentDef
    task -.->|"assembles"| context
    agentDef -.->|"executes within"| runtime
    runtime -.->|"produces"| event
    eo -.->|"records via"| audit
    task -.->|"records via"| audit
    task -.->|"persists via (workspace-scoped repository, ADR-0004)"| dbsession
    eo -.->|"persists via"| dbsession
    apistd -.->|"wraps"| eo
    apistd -.->|"wraps"| task

    style main fill:#2b6cb0,color:#fff
    style config fill:#2b6cb0,color:#fff
    style logging_ fill:#2b6cb0,color:#fff
    style dbsession fill:#2b6cb0,color:#fff
    style dbbase fill:#2b6cb0,color:#fff
    style health fill:#2b6cb0,color:#fff
    style db fill:#2b6cb0,color:#fff
    style eo fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style agentDef fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style task fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style identity fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style rbac fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style event fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style audit fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style context fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style runtime fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style apistd fill:#4a5568,color:#fff,stroke-dasharray: 5 5
```

## Components — built (Gate B)

| Component | Responsibility | Governing doc |
|---|---|---|
| `app.main` | FastAPI app instance, `lifespan` context (not the deprecated `on_event`), router registration | `backend/README.md` |
| `app.core.config` | Typed `Settings` (pydantic-settings); `database_url` required, fails fast at startup if missing | `docs/planning/TECH_STACK.md` "Environment files" |
| `app.core.logging` | `JsonFormatter` — structured JSON to stdout, including `extra=` fields | `backend/README.md` "Run locally" |
| `app.db.session` | Sync SQLAlchemy engine, `SessionLocal`, `get_db()` dependency generator — not wired into any route yet | `backend/README.md` "Migrations" |
| `app.db.base` | Empty `DeclarativeBase` — exists so `alembic/env.py` has a stable `target_metadata`, no models defined yet | ADR-0003 |
| `app.api.health` | `GET /health` → `{"status": "ok"}` | `docs/c4/C1_CONTEXT.md` |
| Alembic (`backend/alembic/`) | Migration tooling, one intentionally-empty baseline revision proving `alembic upgrade head` works on a clean DB | ADR-0007 (supersedes Prisma) |

## Components — planned (Gate C, WP13–WP22)

| Component | Responsibility | Governing doc |
|---|---|---|
| `EnterpriseObject` | Canonical object model: ID, type, status, owner, timestamps (WP13) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` |
| `AgentDefinition` | Enterprise role definition — one of `AgentDefinition`/`AgentInstance`/`Provider`/`Model`/`RuntimeSession` (WP14) | `PRE-CODING-BRIEF.md` §5.1 |
| `Task` | Task states, owner, priority, source object (WP15) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` |
| Identity/Auth | One authenticated human user + service/agent identities; workspace relationship via `WorkspaceMembership`, not a flat field on `User` (WP16) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`, "Multi-tenancy" section below |
| RBAC | Basic role/permission checks for user, agent, reviewer, approver (WP17) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` |
| `Event` | Trace ID, correlation ID, type, source, timestamp (WP18) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` |
| `AuditRecord` | Audit records for high-impact actions; the supported repository API is append-only — insert and workspace-scoped read only; `workspace_id` derived by `AuditService.record(...)` from the audited subject, never supplied by a calling service; `audit_record_repository` receives the formed record, adds and flushes it (WP19) — implemented on `feat/wp19-audit-record-core`, pending merge | ADR-0005, "Multi-tenancy" section below |
| `ContextPackage` | Sources, constraints, confidence, expiry; survives session termination | `PRE-CODING-BRIEF.md` §5.2 |
| `RuntimeSession` | One temporary agent execution, linked to task/agent/context (WP21) | `PRE-CODING-BRIEF.md` §5.1 |
| API error/response standard | Consistent errors, validation responses, request IDs, pagination (WP22) | `28_API_CONTRACTS/01_API_DESIGN_PRINCIPLES.md` |

## Layering rule (still applies once Gate C components exist)

Every solid arrow above is one-directional per ADR-0003 (reinterpreted for
FastAPI: Router/Endpoint → Service → Repository). The canonical mutation
flow for any Gate C write path is documented in
`docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` and does not change with the stack —
only "Controller" relabels to "Router/Endpoint".

WP19's realized write path, implemented on `feat/wp19-audit-record-core`
and pending merge, is the Service → Repository half of that flow with no
router yet: `AuditService.record(...)` validates the call and derives both
the canonical subject identity and `workspace_id` from a persistent subject
attached to the caller's own session; `audit_record_repository` receives the
already-formed record, adds and flushes it; neither layer commits or rolls
back. When the caller performs the business mutation and the audit write
through one session and one transaction, the two participate in that
caller-owned transaction; these modules do not enforce that the caller does
so. The repository is not drawn as a separate component because this
diagram's granularity represents persistence through `app.db.session`,
rather than drawing per-component repository functions.

## Multi-tenancy: workspace_id on every Gate C entity (resolved)

Confirmed by the project owner before any Gate C model is written — this
replaces the earlier "flagged, not yet resolved" note. Per ADR-0004, **no
exceptions**:

- `EnterpriseObject`, `Task`, `Event`, `AgentDefinition`, `ContextPackage`,
  `RuntimeSession` — each carries `workspace_id` as a required, indexed
  field, following ADR-0004's flat-field pattern directly.
- **Identity/Auth is the one exception to the flat-field shape, not to the
  isolation rule.** A `User` is not itself workspace-scoped (one user can
  belong to multiple workspaces). The workspace relationship lives on a
  `WorkspaceMembership` join entity instead:
  `id, workspace_id, user_id, role, created_at`. `ActorContext` for a
  request resolves to a role by looking up `(user_id, workspace_id)` in
  `WorkspaceMembership`, not by reading a field off `User` directly. Every
  repository method for workspace-scoped entities still takes
  `workspace_id` from this resolved context, same as ADR-0004 requires
  everywhere else — only how identity arrives at that `workspace_id`
  differs.
- `AuditRecord` carries `workspace_id`, but the value is never supplied
  independently by a calling service — `AuditService.record(...)` derives it
  from the audited subject and constructs the record; `audit_record_repository`
  receives an already-formed record and does not compute the scope. There is
  exactly one place that can get this wrong, not one place per calling
  service. No calling service constructs an `AuditRecord.workspace_id`
  itself.

This shape (in particular `WorkspaceMembership`) has been reported back to
the project owner and is confirmed — implement against it directly rather
than re-deriving it at WP16.
