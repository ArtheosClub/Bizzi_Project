# ADR-0016: One explicit execution policy for synthetic mutation paths

- Status: Superseded by ADR-0018
- Date: 2026-10-07
- Publication authority: separately recorded Owner adoption of this exact publication text.
- Deciders: Project Owner.
- Governance level: L3 cross-module / A7 human-reserved Owner decision; DECISION_0003 section 11.

## Context

Ordinary settings and authority for synthetic writes were coupled. Removing the
get_settings destination check would otherwise widen Alembic and startup paths.
A profile label, UUID or test name proves neither authority nor non-authority.
The approved F1 rev4 is the original design snapshot; its not-yet-admitted CI
wording describes that date. Block E later approves a specifically bounded CI
design; neither decision is evidence of actual CI/compose execution.

## Decision

Separate typed settings from explicit immutable ExecutionPolicy admission.
Default policy is disabled. Named SQL/query/add/flush paths require policy,
actual Engine/Session bind destination/role and absence of active libpq overrides.
Local test destination is localhost:5433/bizzi_test, role bizzi. Arbitrary ORM/raw
SQL is outside certification. Session bound to an existing Connection can refuse
before query/add/flush, but cannot undo an already opened connection.
Use explicit calls, not ORM listeners. Apply the same policy before Alembic
connection/offline SQL generation; entrypoint failure prevents server startup.
The default app has no business intake route. Explicit admitted test composition
may include it; verifier defaults to rejection. Disabled-route 404 is separately
adopted contract text, not derived from this policy decision.

The subsequent Block E ci_test design is limited to the exact self-repository
PR/feature branch job and disposable GitHub service database localhost:5432/
bizzi_test, role bizzi, with matched job context and destination checks. No
profile variable alone suffices. Required reporter inventory/JUnit proof and
Option L local-only partition apply; runtime execution requires a separate record.
Compose uses a different proposed destination and remains separately unadmitted.
No provider, dev database, real-user or authoritative exposure is implied.

This ADR records A and E decisions, not their now-spent implementation grants.
The original approved F1 design retains all responsibility-zone/refusal distinctions
and alternatives. Later E/G/L controls are supplements, not retroactive rewriting.
P4's one-route transaction exception is recorded separately in ADR-0017.

## Consequences

Named synthetic mutation paths fail closed while settings remain usable.
URL/role checks before connection establish declared destination, not physical
provenance; actual metadata is collector-measured only after allowed connection.
No generic sandbox or historical non-authority certification. Global/system Git
configuration and inherited GIT_* need separately authorized read-only preflight
before the real local gate; installed .venv identity is not proved by lock hashes.
F1 publication closure still requires separate CI/compose/runtime evidence and
successful applicable exact-head jobs; local tests alone do not close it.
RuntimeEvent, version/concurrency, idempotency, transaction and history deferrals
remain governed by their own records and hard expiry, never waived by this ADR.

## Alternatives considered

Retain global settings gate; add an ORM event mechanism; trust a profile label;
exempt migrations. The approved F1 design selects explicit named-path guards and
one policy model, with migration coverage and later scoped CI activation.

## References

- [ADR-0003](0003-controller-service-repository-layering.md) remains unchanged.
- [ADR-0005](0005-audit-first-mutations.md) obligations retained.
- [ADR-0017](0017-wp23-synthetic-endpoint-transaction-exception.md).
- [Implementation baseline](../../00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md).
- app/core/preproduction_guard.py, Alembic/env.py and app/main.py are source
  references under backend; source presence is not authority.
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_ARCHITECTURE_DECISIONS_F1_AND_P4_2026-10-07.md`, SHA-256 `9e20ac1b3e418dfb09a8e4685acfba6f4ea2748f9d8e013c2062349c0ad61011`.
- External adopted source `workflow_BIZZI/2026-10_adw02/CODEX_PROPOSED_ADR_F1_SYNTHETIC_EXECUTION_BOUNDARY_2026-10-06_rev4.md`, SHA-256 `1be32dc33c38d2ee030389cce7583d9b2fe79290269b9ece2461505c8ee1fa00`.
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_DECISION_BACKEND_CI_APPROVAL_AND_DECISION_2026-10-07.md`, SHA-256 `99d9efcdbd6644035cec2c13d16cb782648a4a114077f851b448cafbc2cb44a2`.
- External adopted source `workflow_BIZZI/2026-10_adw02/CODEX_DRAFT_WP23_DISABLED_ROUTE_AMENDMENT_2026-10-06_rev2.md`, SHA-256 `14af366e5059b8c4ecc60852bf5930dc325c50924d763cc02ecde21c4520fce0`.
