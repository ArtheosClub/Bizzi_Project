# Gate A — Product Definition (backfilled)

- Status: Active (backfill)
- Scope: Gate A, WP00–WP04 (`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`)
- Owner: Engineering (project owner retains approval per Governance Model)

## Why this document exists, and why it's dated after Gate B

`PRE-CODING-BRIEF.md` §10.2 (via the Gate table in §8) says Gate A —
Product Definition — should complete before Gate B — Engineering
Foundation — starts. In practice, Gate B was built and merged to `main`
first, and Gate A's artifacts (WP00–WP04: charter, user, scenario, value
hypothesis, acceptance/demo criteria) never existed as a written
deliverable. `docs/planning/DEVELOPMENT_PLAN.md` §4 flags this sequencing
gap explicitly rather than silently ignoring it.

This document is the backfill that closes that gap before Gate C starts,
per the project owner's direction. It does not roll anything back — Gate
B's engineering foundation is proven and stays as-is. It records, after
the fact, the product definition that should have preceded it. Treat the
gap itself as documented history, not erased.

This is a short backfill, not a full product spec — it exists to satisfy
Gate A's exit criteria (WP00–WP04) with the minimum content needed to
unblock Gate C, using material already present in
`docs/planning/PRE-CODING-BRIEF.md` §7 and
`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` §01.

## WP00 — MVP Charter

**Scope**: Bizzi Platform MVP backend — a system that takes a described
business process, runs it through one configured AI agent to produce an
improvement recommendation, and routes that recommendation to a human
owner for approval, with full traceability (task, agent, context,
decision, event, audit).

**Non-goals** (see `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` §09 for the
full list): the 83+ agent library, semantic memory search, custom
dashboards, file export, a production identity provider, Kubernetes
deployment.

**Owner**: project owner (Engineering delivers, project owner approves
gate exits per `01_GOVERNANCE/GOVERNANCE_MODEL.md`).

**Release definition**: MVP is released when the Gate E exit criteria in
`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` §08 are all met.

## WP01 — Primary User Definition

**Persona**: a **Workspace Owner** — a business owner or manager
responsible for a specific business process, operating inside one
`CompanyWorkspace` (ADR-0004). Not a named individual — a role: whoever in
an organization has the authority to describe a process and act on a
recommendation about it.

**Top pain**: improving a business process today requires either
in-house process-analysis expertise (scarce, slow) or external
consulting (expensive, slow, low traceability). The owner has no fast,
structured way to get an AI-assisted first pass at "what's wrong with this
process and how do I fix it" that they can trust enough to act on.

## WP02 — First Business Scenario

Verbatim from `PRE-CODING-BRIEF.md` §7 / `MVP_WORK_PACKAGE_PLAN.md` §01
(these two already agree — no reconciliation needed here):

> "Analyze a described business process, identify a problem, propose an
> improvement, and pass the recommendation to the owner for approval."

Maps to PB032. Flow:

```
User creates a request
  → Bizzi creates an EnterpriseObject and Task
  → assigns one configured Process Analysis Agent
  → assembles Context
  → Agent executes a RuntimeSession, produces a structured Recommendation
  → Human Approver approves / rejects / requests rework
  → Decision is recorded
  → Events and audit records are emitted
  → Result appears in the Command Center
  → an approved result is stored in Enterprise Memory
```

**Example input**: "Our invoice approval process takes 9 days on average
because every invoice over $500 needs three sequential manual sign-offs,
even for repeat vendors we've paid dozens of times before."

**Example output** (structured recommendation, shape per WP28): a summary
of the bottleneck, a concrete proposed change (e.g., "auto-approve
repeat-vendor invoices under $500 that match a prior approved pattern;
keep sequential sign-off only for new vendors or amounts over $500"), a
confidence level, and the assumptions the recommendation relies on —
pending the owner's approve/reject/rework decision.

## WP03 — MVP Value Hypothesis

**Hypothesis**: a Workspace Owner who describes a business process to
Bizzi receives a concrete, actionable improvement recommendation faster
than their current path (in-house analysis or external consulting), with
enough traceability (task → agent → context → decision → audit) that they
trust it enough to act on without re-deriving the reasoning themselves.

**Success signal for the MVP**: the scenario above runs end to end at
least once with a human approver who accepts the recommendation as
plausible and actionable — not a benchmark against a specific cycle-time
number, since the MVP has no baseline data yet. Cycle-time and
adoption-rate measurement are post-MVP (Gate F+) concerns.

## WP04 — Acceptance and Demo Criteria

These are the same criteria already defined as the Gate D exit condition
and the MVP exit criteria — restated here to close Gate A's WP04, not
duplicated as a separate list that could drift out of sync:

- **Demo script** = the WP32 "Internal End-to-End Demo" deliverable
  (`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` Gate D table): "Full
  scenario runs from request to visible approved result."
- **Acceptance checklist** = `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
  §08 MVP Exit Criteria — reproduced here for Gate A traceability, not
  redefined:
  - the WP02 scenario above works end to end;
  - one user can authenticate;
  - one business request creates an object and task;
  - one configured agent executes through the generic runtime;
  - one context package is assembled and source-linked;
  - one structured recommendation is produced;
  - a human can approve, reject, or request rework;
  - task, session, decision, event, and audit records remain traceable;
  - the Command Center displays the full request history;
  - an approved result can be stored in Enterprise Memory;
  - integration tests pass;
  - Docker Compose deployment and runbook work from a clean environment.

This ties Gate A directly to Gate D's exit criteria, as intended — Gate D
(WP23–WP32) is where this scenario actually gets built; Gate A only had to
define it well enough to build toward.

## References

- `docs/planning/PRE-CODING-BRIEF.md` §7 (scenario source), §8 (gate
  structure)
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` §01 (scenario), Gate A and
  Gate D tables, §08 (exit criteria)
- `docs/planning/DEVELOPMENT_PLAN.md` §4 (sequencing-gap callout this
  document backfills)
