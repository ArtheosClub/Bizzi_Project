# C2 — Container Diagram

Scope: containers inside and immediately around the Bizzi Platform Backend
system boundary. Solid = MVP (Phase 0/1). Dashed = planned (Phase 2+ or
external, per ADR-0002).

```mermaid
flowchart TB
    owner(["Business Owner / User"])

    subgraph BIZZI["Bizzi Platform (system boundary)"]
        api["Backend API<br/>NestJS / TypeScript<br/>REST JSON /api/v1"]
        db[("PostgreSQL 15+<br/>Prisma-managed migrations<br/>workspace-scoped tables")]
        jobs[["Job Queue — planned<br/>BullMQ / Redis<br/>deferred until async jobs needed"]]
        spa[["Frontend — planned<br/>not built yet, out of this plan's scope"]]
    end

    subgraph PLATFORM["Art of Business Platform Services — future, external (ADR-0002)"]
        agentRegistry[["Agent Registry Service"]]
        knowledgeGraph[["Knowledge Graph Service"]]
        memorySvc[["Memory Service (platform)"]]
        decisionSvc[["Decision Service (platform)"]]
        executionSvc[["Execution Service"]]
        mcpGw[["MCP Gateway Service"]]
        observability[["Observability Service"]]
        identitySvc[["Identity Access Service"]]
    end

    owner -->|"HTTPS/JSON"| api
    api -->|"Prisma Client,<br/>workspace-scoped queries"| db
    api -.->|"future: enqueue jobs"| jobs
    spa -.->|"future"| api
    api -.->|"future: may federate auth"| identitySvc

    style api fill:#2b6cb0,color:#fff,stroke:#1a4971
    style db fill:#2b6cb0,color:#fff,stroke:#1a4971
    style owner fill:#276749,color:#fff
    style jobs fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style spa fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style agentRegistry fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style knowledgeGraph fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style memorySvc fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style decisionSvc fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style executionSvc fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style mcpGw fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style observability fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style identitySvc fill:#4a5568,color:#fff,stroke-dasharray: 5 5
```

## Containers in MVP scope

| Container | Technology | Responsibility |
|---|---|---|
| Backend API | NestJS / TypeScript | All MVP modules (Workspace, Authorization, Validation, Audit, Event, Task, Decision, Memory, Dashboard, Health) — see C3 |
| PostgreSQL | PostgreSQL 15+, Prisma | Workspace-scoped relational store; schema changes only via committed Prisma migrations |

## Containers explicitly deferred (named, not built)

| Container | Status | Trigger to build |
|---|---|---|
| Job Queue (BullMQ/Redis) | Deferred | First real need for async/background work — `01_TECH_STACK_DECISION.md` |
| Frontend SPA | Not started | Separate plan, out of this document's scope |
| Identity Access Service (federated) | Dev stub only (WP-04) | Real provider selection (Auth0/Clerk/Supabase) |

## Containers that belong to the platform-wide vision, not this system

The eight "Art of Business Platform Services" boxes (Agent Registry,
Knowledge Graph, Memory, Decision, Execution, MCP Gateway, Observability,
Identity Access — full list and one-liners in
`11_PLATFORM_SERVICES/PLATFORM_SERVICE_ARCHITECTURE.md`) are part of the
platform-wide "Art of Business" architecture, not containers this backend
build produces. They're shown here only to make the system boundary honest
about what's outside it. Per ADR-0002, integrating with them is a future,
separately-ADR'd decision.
