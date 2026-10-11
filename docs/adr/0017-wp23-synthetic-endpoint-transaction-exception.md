# ADR-0017: Bounded synthetic WP23 endpoint transaction exception

- Status: Accepted
- Date: 2026-10-07
- Publication authority: separately recorded Owner adoption of this exact publication text.
- Deciders: Project Owner.
- Governance level: L3 cross-module / A7 human-reserved Owner decision; DECISION_0003 section 11.

## Context

ADR-0003 normally places transaction ownership in services. The adopted synthetic
WP23 contract creates an EnterpriseObject and Task atomically through two bounded
primitives. The Owner chose a narrow documented exception, not a general rewrite.

## Decision

Only POST /business-requests under the adopted synthetic contract may own one
caller Session transaction: begin, one commit after both creates and both audits,
rollback on any exception. The handler performs no entity query/add/flush,
repository import, audit or inline actor/business policy. Other endpoints and
service lifecycles remain governed by unchanged ADR-0003; it is not superseded.

Scope is separately admitted synthetic test execution profiles only. The
exception expires before the first real user or first authoritative use,
whichever first, or on leaving synthetic scope. Any deviation, transaction-policy
change or P4 ACR trigger reopens review before execution; no automatic renewal.
Block E AR-3 retains this exact one-route boundary, not a broader exception.

## Consequences

Pair creation is atomic within the endpoint-owned transaction and returns only
Task ID; no EO-Task relationship, RuntimeEvent delivery or production readiness
is implied. P4 governance is decided; code conformance/publication/runtime
verification are separate facts. This reference creates no implementation grant.

## Alternatives considered

Keep transaction ownership strictly in service; redesign the pair primitive;
choose a narrow synthetic exception. The Owner selected the last under section 11.

## References

- [ADR-0003](0003-controller-service-repository-layering.md), unchanged.
- [ADR-0016](0016-synthetic-execution-boundary.md).
- [DECISION_0003](../../00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md).
- backend/app/api/business_request_intake.py and
  backend/app/services/business_request_intake_service.py (code, not authority).
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_ARCHITECTURE_DECISIONS_F1_AND_P4_2026-10-07.md`, SHA-256 `9e20ac1b3e418dfb09a8e4685acfba6f4ea2748f9d8e013c2062349c0ad61011`.
- External adopted source `workflow_BIZZI/2026-10_adw02/CODEX_DRAFT_ACR_P4_WP23_ENDPOINT_TRANSACTION_EXCEPTION_2026-10-07_rev2.md`, SHA-256 `c67ff74b13ec99650e97537bc93f6630cf0fbc3b1d89314d41f70ebb02a93164`.
- External adopted source `workflow_BIZZI/2026-10_adw02/CODEX_DRAFT_WP23_CONTRACT_SELECTION_2026-10-05_rev2.md`, SHA-256 `30d5f61087d9f6aa54546fbf3dd78d870d7d82940273bf6c59999f1073441f83`.
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_DECISION_BACKEND_CI_APPROVAL_AND_DECISION_2026-10-07.md`, SHA-256 `99d9efcdbd6644035cec2c13d16cb782648a4a114077f851b448cafbc2cb44a2`.
