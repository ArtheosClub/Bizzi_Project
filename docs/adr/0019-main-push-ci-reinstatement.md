# ADR-0019: Event-discriminated PR and main-push synthetic CI

Purpose: Restore main-push CI with explicit event contracts and a bounded rollout exception.
Why this exists: AR-2 became immediately due when the first tested candidate reached main.
What it changes: Adds push-main context to ci_test/ci_compose and defines rollout/closure.
Affected modules: policy guard, CI reporter, compose collector, workflow.
Affected Work Packages: CI/governance for bounded WP16/WP19/WP15/WP23.

- Status: Accepted
- Date: 2026-10-15
- Deciders: Project Owner, recorded MAINCI-A.
- Governance level: L3 / A7.
- Supersedes: ADR-0018, retaining its constraints except the explicitly extended event boundary.

## Context

Backend CI/compose currently accept only same-repository initial feature pull requests. Block E and AR2-55 require main-push reinstatement and freeze further main writes/second PR. Merely adding a YAML trigger leaves policy/collector/report metadata inconsistent. The reviewer recommends one event-discriminated policy per existing profile, not new profiles per event.

## Decision

Retain local_test, ci_test and ci_compose destinations, no active PG overrides and disabled defaults. ci_compose remains migration/health-only and refuses business app/Session paths. Actor/audit/domain/DTO/transaction obligations, P4 and arbitrary Session/raw SQL exclusions remain unchanged.

Admit two explicit event contracts. PR: same repository ArtheosClub/Bizzi_Project, base main, head feat/wp15-bounded-task-service, true PR number/refs/head repository, exact workflow ref, proper backend or compose-e2e job, hosted runner and exact event-head checkout. Main push: same repo/owner, event push, ref refs/heads/main, workflow backend-ci.yml@refs/heads/main, proper job and hosted runner, native event SHA/after equal recorded head and checkout. No invented PR number (absent/null); no PR-specific metadata injected on push. Reject deleted refs, tags, other branches/repositories/events, malformed or mixed context and any legacy PR-head variable presence. Migrate workflow and synthetic fixtures to event-neutral head inputs together; no dual-input fallback.

Main push has no path filter. PR filters/head gate stay narrow; arbitrary future PR branches are not admitted. Every push report includes native before/after SHA, forced and deleted flags with strict types. Deleted events refuse synthetic execution. Forced events may run and must report forced=true faithfully: evidence is not authorization for rewriting main. For this admitted rollout require before=ebf7dec5, after=the final reviewed candidate H, forced=false, deleted=false. No failed/unknown metadata becomes PASS.

Grant only one restoration delivery PR, explicitly the second PR to main, by appending to the existing feature branch without reset. It and one expected-old-main lease protected fast-forward of final reviewed H are the sole freeze exception. Candidate revisions can occur only within separate action budgets on the same restoration PR; any H change after evidence requires new exact-head verification, not a new restoration PR. No second restoration PR without a new Owner decision.

Before main write require reviewed exact-H full local partition, successful hosted PR backend/compose, fresh prospective Record L local lock evidence and Owner disposition, current state/protection/tree checks and exact-tip lease plus ancestry. Actual successful push-event main backend/compose reports on exact H and bounded log review are required after write. Do not assume trigger behaviour: no observed run means UNKNOWN; failure keeps freeze, no dispatch/rerun/repair implicit.

After reviewed actual push success and a separate Owner closure disposition, AR2-55's special documentary freeze ends and Block E item 4 is satisfied. This grants no subsequent main write, PR or new branch admission; Record L exact-head gates and explicit action permissions remain. Accept unprotected main as the bounded post-closure steady state for this decision, retaining Block E item 6's residual; branch protection is neither implemented nor falsely claimed. A separate protection decision can change that state later.

Publish D-12 history and conditional closure; do not mark complete until actual evidence and Owner closure exist. This record grants no implementation/runtime/Git/database/CI/publication action.

## Consequences

Push evidence reflects real events without fake PR context. One rollout exception avoids a deadlock in the documentary freeze. Head/type/summary changes require synchronized tests and report consumers. Main remains unprotected; other writers can violate policy. Mutable action/image references, installed tool identity, local venue and platform-disposal limits remain. Initial rollout may fail after main advances; recovery requires a separate decision, no revert or retry is automatic.

A02, entrypoint uv sync, hide_parameters, historical UNKNOWNs and six expiry-bound deferrals remain; A-13 unapproved, A-12 unchanged, A-14 unexpanded. No real-user/authoritative admission. No full ORM sandbox or provenance certificate.

## Alternatives considered

YAML trigger only fails guard/report contract. Generic CI environment trust is too broad. Separate event profiles add surface without new destination semantics. Broad future PR-head admission is outside this minimum. Branch protection before rollout may block the selected delivery method and needs its own decision; accept disclosed existing residual here.

## References

- [ADR-0018](0018-compose-synthetic-execution-boundary.md), preserved body.
- [ADR-0017](0017-wp23-synthetic-endpoint-transaction-exception.md), unchanged.
- [DECISION_0003](../../00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md), sections 10 and 11.
- [Deferred initiatives D-12](../planning/DEFERRED_ARCHITECTURE_INITIATIVES.md).
- External Owner MAINCI-A source: workflow_BIZZI/2026-10_adw02/main_push_ci_owner_decision_scope_sync_draft_2026-10-15/CODEX_DRAFT_OWNER_MAINCI_ARCHITECTURE_DECISION_2026-10-15.md, SHA-256 35abda606c016c60db4a4130835f99a9ef3120ed5aabb7ab338c3edf2e2695a4; adopted insert-only in mvp_decision_package_2026-10-04_revision_2/OWNER_SIGNATURE_SHEET.md, RC verification f1515d0120447b1276b7dc2343499e23fbeac65c07dd11a966fdd09e1f3ff119.
