# C1 — System Context

Scope: Bizzi Platform Backend (MVP). See `docs/c4/README.md` for the
solid = in-scope / dashed = future convention, and ADR-0007 for why the
platform-wide "Art of Business" system is drawn as external/future.

Stack: Python + FastAPI + PostgreSQL, per ADR-0007 (supersedes the
original NestJS/TypeScript scope this diagram used to describe — see
`docs/planning/TECH_STACK.md` for exact pinned versions).

```mermaid
flowchart TB
    owner(["Business Owner / User"])
    agent(["AI Agent — future<br/>not wired to real agents in MVP"])

    subgraph SYS["Bizzi Platform Backend (this system)"]
        bizzi["Bizzi Platform Backend<br/>Python / FastAPI API<br/>Workspace Execution Loop v0.1"]
    end

    aob[["Art of Business Platform — future<br/>LangGraph multi-agent enterprise OS<br/>separate system (ADR-0007)"]]
    mcp[["MCP Gateway / Tool Ecosystem — future"]]
    exportc[["Export / Reporting consumers — future"]]

    owner -->|"HTTPS/JSON, /api/v1"| bizzi
    agent -.->|"planned: authority-scoped API calls (A0-A7)"| bizzi
    bizzi -.->|"possible future integration — not implemented, see ADR-0007"| aob
    bizzi -.->|"future: via Execution Service, never bypassed"| mcp
    bizzi -.->|"future: export jobs"| exportc

    style bizzi fill:#2b6cb0,color:#fff,stroke:#1a4971
    style owner fill:#276749,color:#fff
    style agent fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style aob fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style mcp fill:#4a5568,color:#fff,stroke-dasharray: 5 5
    style exportc fill:#4a5568,color:#fff,stroke-dasharray: 5 5
```

## Actors

- **Business Owner / User** — the only actor with real authorization in the
  MVP (ADR-0006, owner-only). Uses the API directly over HTTPS/JSON.
- **AI Agent (future)** — the enterprise spec (`04_AGENT_LIBRARY`,
  `01_GOVERNANCE/AUTHORITY_MATRIX.md`) defines 84 agents with authority
  levels A0–A7. None are wired to this backend in the MVP; this is Phase 3,
  WP-19 (Agent module), and is explicitly flagged as governance-sensitive in
  `docs/planning/WORK_PACKAGES.md`.

## External systems (all future)

- **Art of Business Platform** — the platform-wide LangGraph multi-agent OS
  described in `10_IMPLEMENTATION/TARGET_TECH_STACK.md`. Per ADR-0007, this
  backend is scoped independently; any integration is a future decision
  requiring its own ADR. (The MVP backend now shares that stack's Python/
  FastAPI foundation, but remains a separate system with its own scope.)
- **MCP Gateway / Tool Ecosystem** — governed external-tool access
  (`09_MCP_INFRASTRUCTURE`). Per `12_APPLICATION_SERVICES/APPLICATION_SERVICE_ARCHITECTURE.md`,
  application-level services must never call MCP directly — only through an
  Execution Service. Not built in the MVP.
- **Export / Reporting consumers** — anything consuming exported data;
  `ExportFileStorage` is only a skeleton interface in the MVP (WP-14).
