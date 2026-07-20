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
`docs/c4/` (architecture diagrams), `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
(the current WP register — see §5 below for why `WORK_PACKAGES.md` is no
longer it).

## 2. Governing scope decision — read this first

**Resolved, not open.** Two tech stacks appeared in this repository at
different altitudes — the long-term platform-wide "Art of Business" stack
(`10_IMPLEMENTATION/TARGET_TECH_STACK.md`: Python, FastAPI, LangGraph,
Neo4j, Qdrant, Kafka, Kong, Keycloak, Vault, Kubernetes) and the near-term
"Bizzi Platform" MVP backend stack, originally scoped to TypeScript/NestJS
in `docs/adr/0002-bizzi-mvp-backend-stack-scope.md`.

**ADR-0002 is superseded by ADR-0007.** The project owner resolved this
directly via `docs/planning/PRE-CODING-BRIEF.md`: the Bizzi Platform MVP
backend is **Python + FastAPI + PostgreSQL**, modular monolith, Docker
Compose for MVP deployment, Kubernetes deferred. Read `docs/adr/0007-*.md`
and `PRE-CODING-BRIEF.md` §1 before touching backend code — not ADR-0002,
which is kept only as a historical record of the original (now reversed)
scoping decision.

**`PRE-CODING-BRIEF.md` also restructured phasing** from this plan's
original Phase 0-3 (below, §4) into five-plus gates (A-G) with WP-level
detail in `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`. §4 and §5 below
reflect that restructuring; §6-§10 (Definition of Ready, governance gate,
Definition of Done, stop conditions, critical risks) are stack- and
phase-structure-agnostic and remain in force unchanged.

## 3. Source of truth per concern

| Concern | Governing doc |
|---|---|
| Tech stack (current) | `docs/adr/0007-*.md`, `docs/planning/TECH_STACK.md` |
| Tech stack (historical, superseded) | `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md`, `docs/adr/0002-*.md` |
| Gate structure / MVP scope | `docs/planning/PRE-CODING-BRIEF.md` |
| WP-level detail, dependencies, critical path | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` |
| Repo layout (as actually built) | `backend/` (see `backend/README.md`) |
| Service/repo pattern | ADR-0003 (Controller/Router→Service→Repository) |
| Testing | `backend/README.md` "Dev tooling & CI"; `30_BACKEND_IMPLEMENTATION_PLAN/09_TESTING_STRATEGY.md` for stack-agnostic principles |
| Local dev / CI | `backend/README.md`, `.github/workflows/backend-ci.yml` |
| Coding standards | `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` (principles apply per ADR-0003; literal NestJS syntax in that doc does not) |
| Readiness gates | `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` |
| Risks | `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` |
| Governance / escalation | `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `01_GOVERNANCE/AUTHORITY_MATRIX.md` |
| Domain entities (Gate C) | `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` WP13–WP22; `26_DOMAIN_MODEL/01_ENTITY_CATALOG.md` for the older, unreconciled entity set |
| API conventions | `28_API_CONTRACTS/01_API_DESIGN_PRINCIPLES.md` |
| Agent identity / runtime model (Gate C) | `docs/planning/PRE-CODING-BRIEF.md` §5.1–5.3 |

## 4. Phasing

Per `PRE-CODING-BRIEF.md` §8 and `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
§03, the build is seven gates, not the three-phase structure this plan
originally used (kept below only as a superseded historical note):

| Gate | Scope | Status |
|---|---|---|
| A — Product Definition | WP00–WP04: scenario, user, value, acceptance criteria | Not started |
| B — Engineering Foundation | WP05–WP12: repo, FastAPI skeleton, Postgres, migrations, config, logging, tests, CI | **Done, merged to `main`** |
| C — Platform Backbone | WP13–WP22: EnterpriseObject, AgentDefinition, Task, Auth, RBAC, Event, AuditRecord, ContextPackage, RuntimeSession, API standard | **Next** |
| D — First Vertical Slice | WP23–WP32: request → task → agent → context → result → approval → decision → event → demo | Not started |
| E — MVP Completion | WP33–WP39: Command Center, timeline, memory, error handling, integration tests, seed data, deployment | Not started |
| F — Post-MVP Platform Expansion | WP40–WP69 | Backlog |
| G — Productization | WP70–WP93 | Backlog |

Note that Gate B was completed and merged before Gate A's product-definition
artifacts (WP00–WP04) formally existed — `PRE-CODING-BRIEF.md` §10.2 says
not to begin coding before Gate A, and that sequencing was not followed in
practice. This is flagged here rather than silently glossed over; it does
not block Gate C, but Gate A should not be skipped indefinitely.

*(Historical: the original three-phase structure this section described —
Phase 0 Foundations / Phase 1 MVP Vertical Slice / Phase 2 Quality Gates /
Phase 3 Post-MVP Expansion, mapped to `14_IMPLEMENTATION_CHECKLIST.md`
Levels 0-8 — was written for the superseded NestJS/Prisma scope. It is
superseded by the gate table above, not merged with it.)

## 5. Work Packages

Full register with dependencies, priorities, and acceptance criteria: see
`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` (WP00–WP93, gate table
matches §4 above). `docs/planning/WORK_PACKAGES.md` is **superseded** by
that document — kept only as a historical record of the original
NestJS/Prisma-era WP register; do not use it to plan new work.

## 6. Definition of Ready (every WP)

- Governing spec doc(s) for this WP identified and read.
- All WPs this one depends on are merged to the trunk.
- Governance level checked against §7 — if it trips an L3+/A3+ trigger,
  human consult obtained **before** any code is written.

## 7. Governance gate — when to consult before coding

Per `01_GOVERNANCE/GOVERNANCE_MODEL.md` (decision levels L1–L5) and
`01_GOVERNANCE/AUTHORITY_MATRIX.md` (authority levels A0–A7):

- **Proceed directly**: routine implementation of a WP already named and
  sequenced in `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`, within an
  approved gate, following the CSR pattern (ADR-0003) and coding standards.
  This is L1/L2, A0–A2 work.
- **Stop and consult the project owner before writing code** when any of
  these are true — each is an L3+/A3+ trigger:
  - Adding a component, table, or endpoint not named in
    `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`'s current gate.
  - Changing the authorization model, tech stack, or a cross-module contract.
  - Touching secrets, PII, or anything the Risk Register lists as **Critical**
    (`12_IMPLEMENTATION_RISK_REGISTER.md`): R-DATA-001, R-SEC-001,
    R-TEST-001, R-AI-001, R-SCOPE-001.
  - Anything that would trigger a Stop Condition (§9 below).
- Escalation order per Governance Model §14: **Escalate > Review > Approve > Execute.**
- Use the `bizzi-consult-before-coding` skill to run this gate before starting
  any WP.

## 8. Definition of Done (every WP)

- All acceptance criteria in `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
  for this WP are checked.
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

*(Note: §4 was reconciled with the Gate A-G structure after this section
was originally written — see §4 above. This section's own content, below,
was correct at the time and remains correct; only the "not yet reconciled"
framing that used to introduce it has been removed.)*

What this addendum records: the agent identity/session/context model
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
