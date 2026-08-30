# WP19 / Q2 D1–D5 Decision Pass v0.1

**Status:** Draft — Q2 decision analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — explicit D1–D5 decision pass after A1–A6, S1–S10, and C1–C5
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact structures D1–D5 for explicit decision authority; it does not itself decide D1–D5 or select, approve, reject, recommend, or default a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending explicit Q2 resolution.

## 1. Scope and boundary

The approved ADW-07 Block 4 / D6 procedure has completed the following analytical stages:

1. A1–A6 authoritative-constraint application;
2. S1–S10 semantic stress tests;
3. C1–C5 qualitative comparison.

This artifact performs the next bounded stage: **structure D1–D5 as explicit decision questions for Project Owner decision authority.**

It does not:

- select a Q2 persisted representation;
- turn qualitative comparison strength into a default candidate;
- treat stress-test support/failure as candidate approval/rejection;
- decide any D1–D5 question by implication;
- create implementation authorization;
- modify WP19 backlog or implementation sequence;
- restore a WP18 → WP19 dependency;
- resolve GC-006 or GC-007;
- close ADW-07.

### Governance guardrail — evaluation result versus architecture decision

A1–A6, S1–S10, and C1–C5 are evaluation inputs. They may expose contradiction, support, uncertainty, burden, advantage, or dependency. They do not by themselves approve or reject a candidate.

In particular:

- a stress-test `UNSUPPORTED` result is not architecture rejection;
- a stress-test `SUPPORTED` result is not architecture approval;
- a stronger qualitative result on one or more C1–C5 dimensions does not make a candidate the default;
- a candidate remains unapproved until appropriate decision authority explicitly acts.

Any later candidate rejection, preference, or selection must be recorded as a separate architecture decision after D1–D5 are explicitly addressed to the extent necessary.

## 2. Blocker provenance

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

This blocker is the direct ADR-0014 Q2 blocker: the persisted AuditRecord subject-reference representation remains unresolved. It is **not** a restored dependency on WP18. PR #31's removal of the `WP18 → WP19` sequencing dependency remains unaffected.

Therefore neither completion of this D1–D5 analysis artifact nor any individual D1–D5 decision makes WP19 buildable by itself. A separate explicit Q2 representation decision is still required before WP19 readiness can be reconsidered.

## 3. Inputs carried forward without reinterpretation

### A1–A6

- No N1–N5 candidate was eliminated by authoritative contradiction.
- A1 and A2 remain unresolved for all five candidates for candidate-specific reasons.
- A3–A6 are PASS for all five normalized candidates.

### S1–S10

- Stress findings are diagnostic only.
- N3 has several class-level current-scope `SUPPORTED` findings but no A1 PASS.
- N2 exposes current-scope adaptation pressure for Workspace/User.
- S6/S7 remain unresolved for all candidates.
- S8 is D5-dependent for all candidates.
- S9 does not block any candidate on R1.
- S10 remains D2-sensitive for all candidates.

### C1–C5

- N2/N3 expose more persisted relational structure at class level.
- N1/N4/N5 place more semantics in interpretation/resolution/content contracts.
- Those are tradeoff locations, not preference or default signals.
- C1–C5 produced no winner, recommendation, rejection, or ranking.

## 4. D1 — Type disambiguation

### Decision question

**What durable information is required for a committed AuditRecord subject reference to distinguish the subject's type sufficiently for stable resolution?**

The decision must determine whether subject type must be structurally encoded in the persisted reference, may be derived through another durable interpretation convention, or whether some other bounded rule is authoritative.

### Why D1 is required

A1 exposed D1 directly for N1, N4, and N5. C1/C2/C5 show that the answer changes query shape, integrity location, and historical interpretation burden. D1 may also affect concrete realizations of N2/N3, but no such realization is assumed.

### What D1 must not decide by accident

D1 must not silently choose:

- `subject_type + subject_id`;
- a registry or global namespace;
- payload placement;
- DB FK enforcement;
- a specific discriminator vocabulary;
- the winning candidate.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 5. D2 — Reference-level workspace semantics

### Decision question

**What workspace/scoping semantics must the persisted AuditRecord subject reference itself preserve or enforce across Workspace, EnterpriseObject, User, WorkspaceMembership, and Task?**

This includes whether the reference must independently carry or enforce workspace context, may rely on the referenced subject's durable identity/scoping semantics, or may use another durable rule.

### Why D2 is required

S10 is unresolved for all candidates. N2's documented `(workspace_id, id)` form expresses workspace-scoped identity strongly where the target has that shape, but Workspace and User are structurally asymmetric. N3/N1/N4/N5 likewise do not have an approved Q2-wide workspace rule.

C2 shows that workspace integrity location materially affects comparison, but existing authority does not choose that location.

### What D2 must not decide by accident

D2 must not silently require:

- `workspace_id` on every subject type;
- a universal composite key;
- conversion of User or Workspace into EnterpriseObject;
- DB enforcement rather than application/domain enforcement;
- a particular candidate.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 6. D3 — Subject deletion / historical resolution

### Decision question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later physically deleted, and may the AuditRecord subject reference itself constrain that deletion?**

The decision must separate two issues:

1. historical identity/resolution after subject deletion; and
2. whether the reference is permitted or required to prevent physical deletion.

### Why D3 is required

A2, S6, S7, and C5 expose a shared historical-stability requirement. None of N1–N5 currently establishes post-deletion behavior. A DB FK does not answer D3 by itself because delete actions and historical policy remain undecided.

D10 governs Historical Record immutability/permanence for AuditRecord itself; it does not by itself establish a universal deletion rule for every possible audited subject.

### What D3 must not decide by accident

D3 must not silently create:

- universal `RESTRICT`/`CASCADE`/`SET NULL` behavior;
- tombstones;
- permanent retention of every subject row;
- a historical identity registry;
- a preference for payload or FK representation.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 7. D4 — DB-enforced referential integrity

### Decision question

**Is database-enforced referential integrity required, preferred, optional, or inappropriate for the AuditRecord subject-reference contract, and must that answer be uniform across all five current subject types?**

### Why D4 is required

C2 exposes materially different enforcement locations across candidates. N2 has the clearest DB-native enforcement semantics in its documented applicable case; N3 can potentially support per-relation enforcement; N1/N4/N5 may rely more heavily on domain/application/content contracts depending on realization.

Existing authority does not say DB-native enforcement is inherently superior or mandatory. GC-002 Alternative B remains Proposed only.

### What D4 must not decide by accident

D4 must not silently:

- approve GC-002 Alternative B;
- require one uniform FK shape across structurally asymmetric subject types;
- reject application/domain validation categorically;
- select N2 merely because it has stronger DB-native integrity in one documented case.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 8. D5 — Subject-type set / extensibility requirement

### Decision question

**For Q2, is the architecture requirement limited to the current five subject types, or must the persisted representation also satisfy an explicit extensibility requirement for future auditable subject types?**

If extensibility is required, the decision must state the required property at architecture level without choosing an implementation mechanism by implication.

### Why D5 is required

Normalization explicitly removed open-ended extensibility as a hidden premise. S8 therefore remained unresolved for every candidate. C3 could describe where future change would occur but was prohibited from treating that location as an automatic advantage or defect.

Without D5, C3 cannot legitimately influence an eventual preference beyond descriptive tradeoff analysis.

### What D5 must not decide by accident

D5 must not silently:

- require zero-schema-change extension;
- require a polymorphic/opaque/payload solution;
- penalize N2/N3 merely because future types may require relational schema change;
- declare the current five permanently exhaustive unless that is the explicit architecture decision.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 9. Decision interaction map

The five decisions are related but must not be collapsed into a single hidden representation choice.

| Decision | Primary exposed surfaces | Candidate classes most visibly affected | Does answering it select a candidate by itself? |
|---|---|---|---|
| D1 Type disambiguation | A1, C1, C2, C5 | N1, N4, N5; potentially all concrete realizations | No |
| D2 Workspace semantics | S10, C2 | All; N2 asymmetry especially visible | No |
| D3 Subject deletion | A2, S6, S7, C5 | All | No |
| D4 DB referential integrity | C2, C4, N2 documented form | All; N2/N3 especially visible | No |
| D5 Subject-type set | S8, C3, C4c, C5 | All | No |

A combination of D1–D5 answers may make some candidate realizations incompatible, more burdensome, or more coherent. That later consequence is not recorded as rejection or selection in this artifact.

## 10. Decision-pass gate result

**D1–D5 DECISION QUESTIONS STRUCTURED — NO D1–D5 ANSWER ASSUMED — NO CANDIDATE DEFAULT, RECOMMENDATION, REJECTION, OR SELECTION CREATED.**

Current state remains:

- Q2 persisted representation: **OPEN**;
- D1–D5: **OPEN — PROJECT OWNER DECISIONS REQUIRED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**.

The next step is not implementation. Project Owner decision authority must address D1–D5 to the extent required for a rational Q2 representation decision. Only after those explicit decisions may a separate persisted-representation decision compare the surviving/coherent candidate realizations and approve or reject them. WP19 readiness must then be reconsidered separately.