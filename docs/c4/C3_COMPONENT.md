# C3 — Component Diagram (Backend API container)

Scope: components (NestJS modules) inside the Backend API container, MVP
only. Ordering follows `30_BACKEND_IMPLEMENTATION_PLAN/06_MODULE_IMPLEMENTATION_SEQUENCE.md`
and WP IDs in `docs/planning/WORK_PACKAGES.md`.

```mermaid
flowchart TB
    subgraph API["Backend API (NestJS) — MVP components"]
        config["ConfigModule (WP-01)"]
        database["DatabaseModule (WP-02)<br/>Prisma provider, TransactionManager"]
        shared["SharedKernelModule (WP-03)<br/>errors, DTO base, mappers"]
        identity["IdentityModule (WP-04)<br/>dev auth stub, ActorContext"]
        workspace["WorkspaceModule (WP-05)"]
        authz["AuthorizationModule (WP-06)<br/>ADR-0006"]
        validation["ValidationModule (WP-07)"]
        audit["AuditModule (WP-08)<br/>ADR-0005"]
        event["EventModule (WP-09)<br/>ADR-0005"]
        task["TaskModule (WP-10)"]
        decision["DecisionModule (WP-11)"]
        memory["MemoryModule (WP-12, minimal)"]
        dashboard["DashboardModule (WP-13, minimal)"]
        health["HealthModule (WP-15)"]
    end
    db[("PostgreSQL")]

    identity -->|"supplies ActorContext"| workspace
    workspace -->|"checks via"| authz
    task -->|"checks via"| authz
    decision -->|"checks via"| authz
    task -->|"validates via"| validation
    decision -->|"validates via"| validation
    task -->|"records via"| audit
    decision -->|"records via"| audit
    workspace -->|"records via"| audit
    task -->|"emits via"| event
    decision -->|"emits via"| event
    task -->|"persists via (Repository, workspace-scoped)"| database
    decision -->|"persists via"| database
    workspace -->|"persists via"| database
    memory -->|"persists via"| database
    dashboard -->|"reads via"| database
    database -->|"Prisma Client"| db

    config -.->|"provides config to"| database
    shared -.->|"base classes used by"| workspace
    shared -.->|"base classes used by"| task
    shared -.->|"base classes used by"| decision

    style database fill:#2b6cb0,color:#fff
    style db fill:#2b6cb0,color:#fff
```

## Module responsibilities

| Module | Responsibility | Governing ADR/doc |
|---|---|---|
| ConfigModule | Typed, validated env config | `01_TECH_STACK_DECISION.md` |
| DatabaseModule | Prisma client, `TransactionManager` | ADR-0003 |
| SharedKernelModule | Base errors/DTOs/mappers, imports nothing from `modules/` | ADR-0003 |
| IdentityModule | Dev auth stub → `ActorContext` | `01_TECH_STACK_DECISION.md` §Auth |
| WorkspaceModule | `CompanyWorkspace`, `WorkspaceSettings` — root aggregate | ADR-0004 |
| AuthorizationModule | Central `AuthorizationService`, owner-only for MVP | ADR-0006 |
| ValidationModule | Business-rule validation, separate from DTO validation | `07_SERVICE_IMPLEMENTATION_GUIDE.md` |
| AuditModule | `AuditService` — sole path to audit writes | ADR-0005 |
| EventModule | `RuntimeEventService` — post-commit coordination signal | ADR-0005 |
| TaskModule | Task create/complete lifecycle | `02_MVP_VERTICAL_SLICE.md` |
| DecisionModule | Decision create/confirm lifecycle | `02_MVP_VERTICAL_SLICE.md` |
| MemoryModule | `MemoryEntry` create/activate (minimal, no semantic search) | `02_MVP_VERTICAL_SLICE.md` |
| DashboardModule | `DashboardMetric` read (minimal, no custom dashboards) | `02_MVP_VERTICAL_SLICE.md` |
| HealthModule | Liveness/readiness | `11_CI_CD_READINESS_PLAN.md` |

Every arrow in the diagram above is one-directional per ADR-0003
(Controller→Service→Repository). No module in this list imports "up" from a
module that depends on it.
