# ADR-0018: Synthetic execution boundary including compose migration and health

Purpose: Record the adopted compose extension to the explicit execution policy.
Why this exists: The legacy compose job targets dev storage and conflicts with F1.
What it changes: Adds ci_compose for migration/health while retaining prior policies.
Affected modules: policy guard, app factory, Session provider, CI compose collector.
Affected Work Packages: bounded WP16/WP19/WP15/WP23; Gate B compose proof.
Affected code: backend/app/core/preproduction_guard.py, main.py, db/session.py,
backend/docker-compose.ci.yml, backend/tests/ci_compose_verification.py and workflow.

- Status: Accepted
- Date: 2026-10-13
- Deciders: Project Owner (recorded COMP-C01 and COMP-A-D).
- Governance level: L3 / A7; DECISION_0003 section 11.
- Supersedes: ADR-0016; its original body remains unchanged.

## Context

Settings are not authority to mutate. F1 separated ordinary typed configuration
from explicit immutable execution policy, including migration preflight.
Block E admitted backend ci_test but not the legacy compose job. The Owner now
adopts a distinct migration/health-only composition and bounded section 9 branch
exception. Prior Q/R publication is retained prospectively; no backdated compliance.

## Decision

Retain disabled defaults, local_test at localhost:5433/bizzi_test and ci_test at
localhost:5432/bizzi_test, role bizzi, PostgreSQL+psycopg, no URL query/active libpq
overrides. ci_test requires the admitted same-repository feature PR/backend job
context and exact event-head checkout. A label alone proves neither authority nor
provenance. Named Engine/Session paths use explicit guards, not ORM listeners.
Externally connected Session binds can refuse before query/add/flush, not undo
an existing connection. Arbitrary Session/raw SQL remains outside certification.

Add ci_compose only for same-repository admitted feature PR/compose-e2e, exact
head checkout, standalone API/postgres-test project and fresh tmpfs storage.
Migration destination is postgres-test:5432/bizzi_test, role bizzi. Alembic retains
its policy/URL/Engine checks; entrypoint migrates before health-only server startup.
require_business_policy refuses ci_compose at explicit app composition, before
provider Engine creation, and before named Session business operations. Default
app exposes health only; no provider, dev storage, seed or business mutation admitted.

The Option D inventory certifies current guarded application delegation, not every
repository entry. Direct caller-supplied Session entry and test-only list functions
are explicitly outside certification; new callers/changed paths require review.
Exactly one local-only lock venue and full CI inventory/zero-skip proof retained.
P4 transaction exception remains solely ADR-0017; no actor/domain/DTO/schema change.

Only a fixed positive summary may be public; raw logs, credentials, SQL/errors and
payloads are not exported. Metadata psql reads are separate READ ONLY transactions
on the synthetic superuser, not role-enforced confinement or proof of API bind.
Workflow-supplied container context is weaker than runner-native corroboration.
Evidence precedes hosted VM platform disposal; physical row preservation is not
proved. Unexpected audit/business rows invalidate the premise and stay adverse;
disposal is not an Invariant 13 ledger or D10 exception. No cleanup controller.

## Consequences

Backend/local acceptance remains bounded. Compose can demonstrate real migration
and startup once separately permitted and verified; source code is not runtime proof.
F1 publication gate requires separate exact-head CI/compose evidence and log review.
Current write permission authorizes no checks, DB, Docker, CI, commit, push or PR.
Artifact versus console-only and any uploader remain later Owner choices.
Mutable image/action references, workflow-supplied context, installed environment
identity and platform disposal remain honest residuals, not cryptographic provenance.
A-13 unapproved, A-12 unchanged, A-14 not expanded, historical exposure UNKNOWN.
RuntimeEvent and D07 deferrals retain their hard expiry before first real user or
first authoritative use; no additional waiver. D-12 main-push trigger unchanged.

## Alternatives considered

Dedicated architecture branch versus narrow same-branch exception: Owner selected
the latter only for this initial publication; no general section 9 cancellation.
Generic ORM event sandbox versus named explicit gates: retain explicit mechanism.
Legacy overlay/dev compose versus standalone two-service tmpfs: select standalone.
Repository-entry guard expansion versus delegation inventory: Owner chose D for
this phase; stronger entry guards require their own scope. Raw log redaction and
cleanup framework rejected in favour of positive summaries and platform disposal.

## References

- [ADR-0016](0016-synthetic-execution-boundary.md): preserved original rationale,
  F1 responsibility zones and alternatives; superseded only by this adopted extension.
- [ADR-0017](0017-wp23-synthetic-endpoint-transaction-exception.md): unchanged.
- [ADR-0003](0003-controller-service-repository-layering.md) and
  [ADR-0005](0005-audit-first-mutations.md): retained obligations.
- External COMP-C01/COMP-A-D source:
  workflow_BIZZI/2026-10_adw02/compose_owner_decisions_c01_c10_draft_2026-10-13_revision_3/CODEX_DRAFT_OWNER_COMPOSE_ARCHITECTURE_DECISIONS_C01_C10_2026-10-13_rev3.md,
  SHA-256 f46902913868f0598917777d1983d4f5eba8392f1a208b68e00602969482c757.
- External COMP-IMPL-A-D source:
  workflow_BIZZI/2026-10_adw02/compose_phase_a_option_d_amendment_draft_2026-10-13/CODEX_DRAFT_OWNER_AMENDMENT_COMP_IMPL_A_D_2026-10-13.md,
  SHA-256 93f59b408e3d1ba7c343b2e84c5bbab7836730531d1ab1b58604c70f3de16508.
- [Implementation baseline](../../00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md).
