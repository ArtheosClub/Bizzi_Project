# Bizzi Platform — Backend Development Plan

- Status: Active
- Scope: Bizzi Platform MVP backend ("Workspace Execution Loop v0.1")
- Owner: Engineering (project owner retains approval per Governance Model)

## 1. Purpose

This plan turns the existing specification corpus (`29_BACKEND_SERVICE_DESIGN` →
`33_BACKEND_SOURCE_CODE_IMPLEMENTATION`) into an executable, dependency-ordered
sequence of Work Packages (WPs). It exists because layers 31–33 already audit
themselves honestly: the *specifications* are complete, but **no source code
exists in the repository yet** — verified by filesystem search (no
`package.json`, `*.prisma`, `*.ts`, `*.js` anywhere outside `node_modules`) and
confirmed by `33_BACKEND_SOURCE_CODE_IMPLEMENTATION/16_BACKEND_SOURCE_CODE_MILESTONE.md`
("PENDING SOURCE VERIFICATION") and
`33_BACKEND_SOURCE_CODE_IMPLEMENTATION/17_BACKEND_SOURCE_CODE_AUDIT.md`
("Audit Result: PENDING"). This plan is the bridge from "fully specified" to
"actually built."

See also: `docs/adr/` (decision records to follow while building),
`docs/c4/` (architecture diagrams), `WORK_PACKAGES.md` (the WP register).

## 2. Governing scope decision — read this first

Two tech stacks appear in this repository at different altitudes:

- `10_IMPLEMENTATION/TARGET_TECH_STACK.md` / `TARGET_ARCHITECTURE.md` — the
  long-term, platform-wide **"Art of Business"** stack: Python, FastAPI,
  LangGraph, Neo4j, Qdrant, Kafka, Kong, Keycloak, Vault, Kubernetes/Terraform/AWS.
  This is vision-level; no execution detail exists for it.
- `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md` — the near-term
  **"Bizzi Platform"** MVP backend stack: TypeScript, NestJS, PostgreSQL,
  Prisma. Layers 31, 32, and 33 all build on this decision.

Nothing in the corpus reconciles the two. **This development plan builds only
the Bizzi Platform MVP backend, on the TypeScript/NestJS stack**, because it
is the only layer with execution-level detail (repo structure, module
sequence, coding standards, testing strategy) that later layers already
depend on. This is formally recorded in **ADR-0002** — read it before
starting Phase 0. If this scope choice is wrong, resolve it with the project
owner before any WP below is started; that decision is out of this plan's
authority (see §7).

## 3. Source of truth per concern

| Concern | Governing doc |
|---|---|
| Tech stack | `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md`, ADR-0002 |
| MVP scope | `30_BACKEND_IMPLEMENTATION_PLAN/02_MVP_VERTICAL_SLICE.md` |
| Repo layout | `30_BACKEND_IMPLEMENTATION_PLAN/03_REPOSITORY_STRUCTURE.md` |
| Build order | `30_BACKEND_IMPLEMENTATION_PLAN/06_MODULE_IMPLEMENTATION_SEQUENCE.md` |
| Service/repo pattern | `07_SERVICE_IMPLEMENTATION_GUIDE.md`, `08_REPOSITORY_IMPLEMENTATION_GUIDE.md`, ADR-0003 |
| Testing | `30_BACKEND_IMPLEMENTATION_PLAN/09_TESTING_STRATEGY.md` |
| Local dev / CI | `10_LOCAL_DEVELOPMENT_WORKFLOW.md`, `11_CI_CD_READINESS_PLAN.md` |
| Coding standards | `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` |
| Readiness gates | `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` |
| Risks | `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` |
| Governance / escalation | `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `01_GOVERNANCE/AUTHORITY_MATRIX.md` |
| Domain entities | `26_DOMAIN_MODEL/01_ENTITY_CATALOG.md` |
| API conventions | `28_API_CONTRACTS/01_API_DESIGN_PRINCIPLES.md` |
| Agent identity / runtime model (Gate C) | `docs/planning/PRE-CODING-BRIEF.md` §5.1–5.3 |

## 4. Phasing

1. **Phase 0 — Foundations**: scaffold, config, database, shared kernel, identity stub.
2. **Phase 1 — MVP Vertical Slice**: the "Workspace Execution Loop" — Workspace → Task → Decision → Memory → Audit → Event → Dashboard.
3. **Phase 2 — Quality Gates**: test suite, CI pipeline, local dev runbook, go/no-go audit.
4. **Phase 3 — Post-MVP Expansion** (backlog, gated behind Phase 2 passing): Operating Map, Function/Responsibility, Process, Agent, Integration, Security, advanced Export/Dashboard.

Phase gates map to `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md`
Levels 0–8. Do not start Phase 3 until Phase 2's WP-93 (go/no-go audit) passes.

## 5. Work Packages

Full register with dependencies, deliverables, and acceptance criteria: see
`WORK_PACKAGES.md`. WP IDs for Phase 0/1/3 mirror the step numbers in
`06_MODULE_IMPLEMENTATION_SEQUENCE.md` 1:1 for traceability.

## 6. Definition of Ready (every WP)

- Governing spec doc(s) for this WP identified and read.
- All WPs this one depends on are merged to the trunk.
- Governance level checked against §7 — if it trips an L3+/A3+ trigger,
  human consult obtained **before** any code is written.

## 7. Governance gate — when to consult before coding

Per `01_GOVERNANCE/GOVERNANCE_MODEL.md` (decision levels L1–L5) and
`01_GOVERNANCE/AUTHORITY_MATRIX.md` (authority levels A0–A7):

- **Proceed directly**: routine implementation of a module already named and
  sequenced in `06_MODULE_IMPLEMENTATION_SEQUENCE.md`, within an approved WP,
  following the CSR pattern and coding standards. This is L1/L2, A0–A2 work.
- **Stop and consult the project owner before writing code** when any of
  these are true — each is an L3+/A3+ trigger:
  - Adding a module, table, or endpoint not named in `02_MVP_VERTICAL_SLICE.md`
    or `06_MODULE_IMPLEMENTATION_SEQUENCE.md`.
  - Changing the authorization model, tech stack, or a cross-module contract.
  - Touching secrets, PII, or anything the Risk Register lists as **Critical**
    (`12_IMPLEMENTATION_RISK_REGISTER.md`): R-DATA-001, R-SEC-001,
    R-TEST-001, R-AI-001, R-SCOPE-001.
  - Anything that would trigger a Stop Condition (§9 below).
- Escalation order per Governance Model §14: **Escalate > Review > Approve > Execute.**
- Use the `bizzi-consult-before-coding` skill to run this gate before starting
  any WP.

## 8. Definition of Done (every WP)

- All acceptance criteria in `WORK_PACKAGES.md` for this WP are checked.
- Coding-standards review checklist passed
  (`30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` §27).
- Tests at the levels required by `09_TESTING_STRATEGY.md` pass.
- No Stop Condition (§9 below) is active.
- An ADR is written or updated if the WP made an architectural decision
  (`bizzi-write-adr` skill).
- The `bizzi-pre-merge-check` skill has been run before merging to a shared
  branch.

## 9. Stop conditions (from `14_IMPLEMENTATION_CHECKLIST.md` §20)

Any of these halts work immediately — do not push through for delivery
speed:

- Workspace isolation is broken (a query/response crosses `workspace_id`).
- An authorization bypass is found.
- A state-changing action is missing its audit event.
- Raw secrets, tokens, or passwords appear in logs, events, or responses.
- Migrations fail on a clean database.
- CI is repeatedly failing.
- Tests are being skipped to force progress.
- AI-generated code repeatedly violates the CSR/module boundaries.

"Stop conditions override delivery speed."

## 10. Critical risks to actively track

From `12_IMPLEMENTATION_RISK_REGISTER.md` (Critical tier):

| ID | Risk |
|---|---|
| R-DATA-001 | Workspace isolation failure |
| R-SEC-001 | Authorization bypass |
| R-TEST-001 | Happy-path-only testing |
| R-AI-001 | AI-generated code bypasses architecture |
| R-SCOPE-001 | MVP scope creep |

## 11. Non-goals of this plan

This plan does not replace docs 29–33; it sequences and gates them. It does
not cover the frontend, deployment automation beyond CI quality gates
(Phase 2–5 in `11_CI_CD_READINESS_PLAN.md` are explicitly staged, only
Phase 1 CI is in scope here), or the platform-wide "Art of Business"
Python/Kubernetes stack (see §2).

## 12. Gate C addendum — agent identity, session, and context model

This document still reflects the pre-Gate-A–E Phase 0-3 structure (§4) and
has **not** been reconciled with `docs/planning/PRE-CODING-BRIEF.md`'s
five-gate restructuring — that reconciliation is a separate, not-yet-done
task, not something this addendum silently resolves.

What this addendum does record: the agent identity/session/context model
refined in `PRE-CODING-BRIEF.md` §5.1–5.3 (itself adapted from
`50_IMPLEMENTATION/GATE_C_AGENT_CONTEXT_AND_HUMAN_INTERACTION_PLAN.md`
§02.6/§04/§06) governs Gate C's Platform Backbone work — `AgentDefinition`/
`AgentInstance`/`Provider`/`Model`/`RuntimeSession` identity, context
surviving session termination, and provider-neutral context/result
envelopes. As with §5.1–5.3 in the brief, this does **not** pull in that
source document's broader agent roster (Enterprise Architect, Memory
Manager, Legal and Regulatory Agent Group) or its legal-source-governance
subsystem — both remain out of scope pending a role beyond the five in
`PRE-CODING-BRIEF.md` §4 being approved.
