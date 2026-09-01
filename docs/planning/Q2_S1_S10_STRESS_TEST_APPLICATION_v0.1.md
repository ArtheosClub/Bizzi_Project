# WP19 / Q2 S1–S10 Semantic Stress-Test Application v0.1

**Status:** Draft — Q2 application analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — semantic stress-test application to normalized candidates N1–N5
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact applies the approved stress-test stage; it does not rank, recommend, approve, reject, or select a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED for implementation.

## 1. Scope and boundary

ADW-07 Block 4 / D6 approves the Q2 procedure in the order: A1–A6 constraint check → S1–S10 semantic stress tests → C1–C5 qualitative comparison → exposed D1–D5 decisions → separate Q2 representation decision.

`Q2_A1_A6_APPLICATION_v0.1.md` completed A1–A6 and established:

- no N1–N5 candidate is eliminated by authoritative contradiction;
- A1 and A2 remain `UNDETERMINED` for all five candidates for different explicit reasons;
- D1–D5 remain open.

This artifact performs **only S1–S10**. It does not:

- run C1–C5;
- convert stress results into points, weights, ranking, recommendation, or winner selection;
- use `UNSUPPORTED` as an automatic FAIL against A1–A6;
- decide D1–D5;
- invent a concrete candidate realization;
- authorize WP19 implementation.

Allowed stress-test results are exactly:

- `SUPPORTED`;
- `UNSUPPORTED`;
- `UNDETERMINED — DECISION REQUIRED`;
- `NOT APPLICABLE`.

A result records what the normalized candidate class exposes under that stress surface. It is diagnostic, not dispositive.

## 2. Result matrix

| Stress test | N1 Polymorphic reference | N2 Composite FK | N3 Per-type nullable columns | N4 Opaque identifier | N5 In-payload |
|---|---|---|---|---|---|
| S1 Workspace as subject | UNDETERMINED | UNDETERMINED | SUPPORTED | UNDETERMINED | UNDETERMINED |
| S2 User as subject | UNDETERMINED | UNDETERMINED | SUPPORTED | UNDETERMINED | UNDETERMINED |
| S3 WorkspaceMembership distinction | UNDETERMINED | UNDETERMINED | SUPPORTED | UNDETERMINED | UNDETERMINED |
| S4 EnterpriseObject subject | UNDETERMINED | SUPPORTED | SUPPORTED | UNDETERMINED | UNDETERMINED |
| S5 Task subject | UNDETERMINED | UNDETERMINED | SUPPORTED | UNDETERMINED | UNDETERMINED |
| S6 Subject deletion | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED |
| S7 Lifecycle change | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED |
| S8 New subject type | UNDETERMINED — D5 | UNDETERMINED — D5 | UNDETERMINED — D5 | UNDETERMINED — D5 | UNDETERMINED — D5 |
| S9 R1 unresolved | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S10 Cross-workspace ambiguity | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED |

No `UNSUPPORTED` result is established at the normalized-class level in this pass. That does not mean every candidate handles every stress surface well; it means normalization deliberately does not contain enough concrete representation detail to prove an inherent failure on those surfaces.

## 3. S1 — Workspace as subject

Framework question: can the representation identify the workspace without inventing a parent workspace?

### N1 Polymorphic reference — UNDETERMINED

N1 can conceptually reference more than one subject type, but normalization does not establish the durable interpretation used for `Workspace`. A favorable realization could identify a workspace directly, but supplying that realization would be new design work. No parent-workspace assumption is built into N1, so this is not `UNSUPPORTED`.

**Dependency:** D1 may matter depending on how the concrete workspace reference is interpreted.

### N2 Composite FK — UNDETERMINED

GC-002's documented `(workspace_id, id)` composite-FK formulation is naturally expressed for a workspace-scoped target, while `Workspace` is itself the workspace boundary and has no parent `workspace_id` in current implementation evidence. Normalization explicitly refuses to invent an adapted composite-FK shape for Workspace.

This stress therefore exposes a current-scope adaptation problem. It is not marked `UNSUPPORTED` because the candidate class has not been fully defined across all five types and no authority says such an adaptation is impossible.

### N3 Per-type nullable columns — SUPPORTED

At class level, subject-type-specific slots can include a Workspace-specific relation without requiring Workspace itself to carry a parent `workspace_id`. This conclusion does not assume a concrete column name, FK, CHECK, or exclusivity rule.

This is a stress-test support finding only; A1 remains UNDETERMINED because subject-cardinality/exclusivity semantics are unresolved.

### N4 Opaque identifier — UNDETERMINED

An opaque identifier could in principle identify a Workspace without a parent workspace key, but the durable resolution convention is unspecified. The stress cannot be passed from the opaque value alone.

### N5 In-payload — UNDETERMINED

Persisted content could carry a Workspace identity directly, but no approved content contract establishes how. The candidate does not require a parent workspace, but the actual resolution semantics remain unspecified.

## 4. S2 — User as subject

Framework question: does the representation incorrectly assume every subject row carries `workspace_id`?

### N1 Polymorphic reference — UNDETERMINED

N1 does not inherently require `workspace_id`, but its concrete durable interpretation is unspecified. It therefore does not fail the User stress, yet cannot receive `SUPPORTED` without supplying a concrete realization.

### N2 Composite FK — UNDETERMINED

Current implementation evidence says User has no `workspace_id`, while the documented GC-002 form uses `(workspace_id, id)`. Normalization intentionally does not invent a User-specific adaptation. This is a material stress surface for N2, but not an established impossibility.

### N3 Per-type nullable columns — SUPPORTED

A User-specific reference slot does not inherently require User to have `workspace_id`. No concrete FK or workspace enforcement rule is assumed.

### N4 Opaque identifier — UNDETERMINED

The opaque identifier class does not inherently require User.workspace_id, but durable User resolution remains unspecified.

### N5 In-payload — UNDETERMINED

Persisted AuditRecord content could identify a User without relying on User.workspace_id, but no concrete durable content contract is established.

## 5. S3 — WorkspaceMembership as subject

Framework question: does the representation preserve the distinction between mutation of a WorkspaceMembership and mutation of the User?

### N1 Polymorphic reference — UNDETERMINED

The candidate class is capable in principle of referencing multiple subject types, but D1/type interpretation remains open. Without the concrete durable distinction mechanism, the Membership-vs-User distinction cannot be proved.

### N2 Composite FK — UNDETERMINED

GC-002's documented `AuditRecord`→aggregate form does not define how the Q2 mechanism distinguishes WorkspaceMembership from User. No multi-target adaptation is invented here.

### N3 Per-type nullable columns — SUPPORTED

The class semantics are explicitly subject-type-specific reference slots. At that class level, a WorkspaceMembership relation is distinct from a User relation. This does not decide slot cardinality, FK enforcement, or column layout.

### N4 Opaque identifier — UNDETERMINED

Without an approved durable resolution convention, an opaque value cannot yet prove that WorkspaceMembership and User identities remain distinguishable.

### N5 In-payload — UNDETERMINED

Persisted content could encode enough information to distinguish membership from user, but no approved content/type contract establishes that distinction.

## 6. S4 — EnterpriseObject as subject

Framework question: does the representation work for the canonical EnterpriseObject case without implying all subjects must become EnterpriseObjects?

### N1 Polymorphic reference — UNDETERMINED

N1 does not imply that all subjects are EnterpriseObjects, but the concrete EnterpriseObject resolution contract is not established. It therefore avoids the forbidden implication but does not yet prove durable support.

### N2 Composite FK — SUPPORTED

GC-002's documented composite-FK candidate explicitly includes an `AuditRecord`→aggregate relation and the corpus treats EnterpriseObject as the canonical enterprise-object case. At the stress-test level, the documented candidate has a natural workspace-scoped target case here.

This `SUPPORTED` result does not extend GC-002 to the other four Q2 types, approve Alternative B, or resolve D4.

### N3 Per-type nullable columns — SUPPORTED

A type-specific EnterpriseObject reference slot supports this subject without requiring the other four subject types to become EnterpriseObjects.

### N4 Opaque identifier — UNDETERMINED

The class does not imply universal EnterpriseObject identity, but the durable resolver needed to establish EnterpriseObject resolution is unspecified.

### N5 In-payload — UNDETERMINED

Persisted content could identify an EnterpriseObject without converting all subjects into EnterpriseObjects, but the content contract is unspecified.

## 7. S5 — Task as subject

Framework question: does the representation work for a conventional workspace-scoped work item?

### N1 Polymorphic reference — UNDETERMINED

No Task-specific durable realization is established, although N1 does not inherently conflict with a workspace-scoped Task.

### N2 Composite FK — UNDETERMINED

A workspace-scoped Task resembles the structural conditions under which composite `(workspace_id, id)` semantics can be meaningful, but the documented GC-002 `AuditRecord` target is `aggregate`, not a complete Q2 Task reference contract. Treating the resemblance as a PASS would silently extend the proposal.

### N3 Per-type nullable columns — SUPPORTED

A Task-specific persisted reference slot supports the class-level Task case without requiring a shared identity model across all subject types.

### N4 Opaque identifier — UNDETERMINED

Task resolution depends on the still-unspecified durable convention.

### N5 In-payload — UNDETERMINED

Persisted content could identify Task, but no concrete content contract proves durable resolution.

## 8. S6 — Subject deletion

Framework question: does historical subject identity remain meaningful if a subject may later be physically deleted, and does the candidate assume without authority that AuditRecord itself prevents deletion?

### N1 — UNDETERMINED — D3 / A2 DEPENDENCY

The durable reference convention is unspecified, so post-deletion historical meaning cannot be established. N1 does not itself assert that AuditRecord blocks deletion.

### N2 — UNDETERMINED — D3 / A2 DEPENDENCY

A DB FK may interact directly with physical deletion behavior, but D3 is explicitly open and D4 does not establish DB-enforced RI as mandatory. The normalized candidate does not specify delete action, tombstone behavior, retained target rows, or historical-key strategy. No behavior may be invented here.

### N3 — UNDETERMINED — D3 / A2 DEPENDENCY

Type-specific slots alone do not establish what remains resolvable after target deletion, nor whether an FK blocks deletion.

### N4 — UNDETERMINED — D3 / A2 DEPENDENCY

Historical resolution after deletion depends on the unspecified durable resolution convention.

### N5 — UNDETERMINED — D3 / A2 DEPENDENCY

Persisted content may potentially retain identifying facts after target deletion, but the normalized content contract is intentionally insufficient to claim that historical subject identity remains resolvable.

No candidate is rewarded merely because one favorable implementation could preserve a deleted subject's identity.

## 9. S7 — Lifecycle change

Framework question: does reference meaning survive archival, supersession, or other lifecycle changes without rewriting AuditRecord?

### N1 — UNDETERMINED — A2 DEPENDENCY

Stable interpretation across lifecycle change was already unresolved under A2. S7 exposes the same dependency without resolving it.

### N2 — UNDETERMINED — A2 DEPENDENCY

The normalized candidate does not establish how composite target identity behaves through supersession or other lifecycle changes. A FK alone does not prove historical semantic stability.

### N3 — UNDETERMINED — A2 DEPENDENCY

Immutable reference slots do not by themselves establish that the referenced identity's interpretation remains stable through lifecycle transitions.

### N4 — UNDETERMINED — A2 DEPENDENCY

The durable resolver's evolution semantics are unspecified.

### N5 — UNDETERMINED — A2 DEPENDENCY

Immutable payload/content bytes do not automatically guarantee stable interpretation if the content contract's semantics can later change.

## 10. S8 — New subject type

Framework question: what changes if a sixth auditable subject type is introduced?

For **all N1–N5**:

**UNDETERMINED — D5 DECISION REQUIRED.**

Normalization explicitly records D5 as open and forbids treating future extensibility as a mandatory architecture requirement before D5 is decided. Therefore S8 may expose the kinds of changes a concrete candidate would require, but this stage cannot classify future-extension burden as a defect or advantage.

No candidate receives `SUPPORTED` simply because it appears generically extensible, and no candidate receives `UNSUPPORTED` because it appears to require a schema change. Those are later C3 observations, subordinate to D5.

## 11. S9 — R1 unresolved

Framework question: does the candidate require one particular answer to Block 2 R1 concerning Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity?

### N1 — SUPPORTED
### N2 — SUPPORTED
### N3 — SUPPORTED
### N4 — SUPPORTED
### N5 — SUPPORTED

None of the normalized candidate contracts depends on Domain Event identity, AuditRecord/Event identity, outbox identity, or publication-intent identity. Therefore all five candidates can be evaluated while R1 remains unresolved.

This result does not resolve R1 and does not say anything about the separate open Event↔AuditRecord relationship.

## 12. S10 — Cross-workspace ambiguity

Framework question: can subjects from different architectural scopes become indistinguishable under the persisted reference contract?

### N1 — UNDETERMINED — D1/D2 DEPENDENCY

The polymorphic durable convention is unspecified. Cross-workspace/scoped disambiguation cannot be proven or disproven without supplying D1/D2 semantics.

### N2 — UNDETERMINED — D2 / CURRENT-SCOPE ADAPTATION DEPENDENCY

Composite `(workspace_id, id)` semantics can strongly express workspace-scoped identity for targets that actually have that structural shape. But Workspace and User are structurally asymmetric, and the Q2-wide adaptation is unspecified. The stress therefore remains unresolved rather than automatically supported by DB composite keys.

### N3 — UNDETERMINED — D2 / INTEGRITY-SEMANTICS DEPENDENCY

Type-specific slots distinguish subject types, but normalization does not establish reference-level workspace semantics or enforcement. Cross-workspace correctness therefore remains unresolved.

### N4 — UNDETERMINED — D1/D2 DEPENDENCY

The opaque value's namespace/scope semantics are deliberately not invented. Cross-workspace ambiguity cannot be assessed until durable resolution semantics are defined.

### N5 — UNDETERMINED — D1/D2 / CONTENT-CONTRACT DEPENDENCY

Persisted content may carry workspace/scoping information, but normalization does not require or define it. No favorable payload schema may be supplied by assumption.

## 13. Cross-candidate findings from S1–S10 only

### Finding S-A — structural asymmetry is a real stress surface, not an automatic candidate rejection

S1 and S2 make the current structural asymmetry visible. N2's documented `(workspace_id, id)` form faces an explicit adaptation question for Workspace and User. N3's type-specific-slot class handles those two class-level shapes more directly. For N1/N4/N5 the concrete interpretation remains too underspecified to claim support.

These observations are not a ranking. C1–C5 have not yet been applied.

### Finding S-B — N3 receives several class-level SUPPORTED results without receiving A1 PASS

N3 supports S1–S5 at the class-description level because type-specific slots can represent distinct current subject relations without requiring a shared identity shape. However A1 remains UNDETERMINED because normalization does not establish the subject-cardinality/exclusivity semantics needed to prove that a committed AuditRecord resolves to one concrete subject.

Stress support therefore must not be mistaken for authoritative sufficiency.

### Finding S-C — deletion and lifecycle stability remain shared unresolved surfaces

S6 and S7 remain UNDETERMINED for every candidate and carry forward A2/D3 dependencies. No universal tombstone, deletion-blocking, resolver, retained-row, or historical-key rule is introduced.

### Finding S-D — D5 prevents premature extensibility bias

S8 is UNDETERMINED for all candidates because D5 remains open. The later C3 pass may describe extensibility consequences, but it may not silently assume that extensibility is mandatory or irrelevant.

### Finding S-E — R1 does not block Q2 representation analysis

All five normalized candidates are SUPPORTED on S9 because none requires a particular R1 answer. R1 therefore remains open but is not, at the normalized-class level, a blocking dependency for the Q2 representation comparison.

### Finding S-F — cross-workspace semantics remain D2-sensitive

S10 is UNDETERMINED for all five candidates. This prevents the later comparison from silently equating DB composite keys, type-specific slots, opaque identifiers, polymorphic references, or payload content with an already-decided workspace-integrity policy.

## 14. Stress-test gate result

**S1–S10 STRESS-TEST PASS COMPLETE — DIAGNOSTIC DIFFERENCES EXPOSED — NO RANKING OR RECOMMENDATION CREATED.**

The stress-test results do not alter the A1–A6 gate:

- no candidate is newly eliminated;
- no candidate is promoted to Q2 winner or preferred representation;
- A1/A2 dependencies remain unresolved where previously recorded;
- D1–D5 remain OPEN;
- Q2 remains OPEN;
- WP19 remains BLOCKED / UNAUTHORIZED.

**Next bounded step under the approved procedure:** conduct C1–C5 qualitative comparison using the A1–A6 and S1–S10 findings as inputs, without numeric scoring, without resolving D1–D5 by implication, and without selecting a representation until the comparison and explicit decision-gap stage are complete.
