# D10 — Deletion and Supersession

**Subtitle:** The Bizzi Historical Integrity Constitution
**Document ID:** ARCH-DOMAIN-D10
**Version:** 1.0
**Status:** APPROVED — CLOSED
**Decision class:** Class A — Constitutional
**Workshop:** ADW-01 — Core Domain Semantics
**Owner:** Project Owner
**Decision authority:** Project Owner
**Approved by:** Project Owner
**Approval date:** 2026-07-23
**Closure date:** 2026-07-23
**Opened:** 2026-07-23
**Last updated:** 2026-07-23
**Builds on:** D01–D09 — all **APPROVED — CLOSED**, none modified by this document.

---

## 1. Purpose

D10 defines the constitutional semantics of cancellation, expiration, revocation, supersession, reversal, compensation, archival, deletion, retention, and historical-preservation for the six domain-owning concepts named in `DOMAIN_FOUNDATION.md` §7 — **Enterprise Object, Actor, Work Item, Decision, Business Operation, Runtime Session** — and for the relationships D09 established among them.

D10 is the tenth and final ADW-01 decision. It does not introduce a new domain concept, aggregate, or architectural layer — Decision 0001 (MVP First & Architecture Freeze) prohibits that, and nothing here requires it. D10 answers a question D06, D07, and D09 each explicitly deferred to it: **what happens when something ends?**

D10 is implementation-independent. It defines no SQL, storage model, API, ORM mapping, or event-sourcing mechanism.

---

## 2. Governing Question

> How does Bizzi end, replace, or remove a subject's active relevance without ever destroying the historical truth that other subjects' own authority, accountability, and reconstructability depend on?

---

## 3. Scope

D10 governs, for the six domain-owning concepts and the D09 relationship model:

1. the semantic meaning of Deletion, Archive, Replacement, Supersession, Cancellation, Invalidation, Expiration, Deprecation, and Historical Preservation;
2. per-concept lifecycle capability: deletable, archivable, supersedable, obsolescence-capable, immutability-capable;
3. the difference between Physical Deletion, Logical Deletion, Semantic Replacement, Historical Record, and Projection Cleanup;
4. mandatory invariants governing when a subject's disappearance is and is not permitted;
5. inheritance of historical responsibility across Supersession;
6. preservation rules for what D09 classified Historical;
7. semantic identity continuity across lifecycle transitions.

D10 does not define:

- retention *periods* (how long preserved history must be kept) — this is a business/compliance/legal decision outside architecture's authority, not an architectural gap (§9);
- physical archival storage, cold storage, or database partitioning strategy — ADW-08;
- the detailed audit/event record schema for lifecycle transitions — ADW-07;
- authorization policy for *who* may request a given lifecycle transition — ADW-03;
- Runtime Session's internal execution-attempt state machine — ADW-05.

---

## 4. Lifecycle Principles

1. **Historical truth outlives operational relevance.** A subject's lifecycle ending (cancelled, archived, superseded, expired) never erases what it authoritatively was while active. This is D07 Rule 4 / LAW-D07-13 and AP-16, applied to endings specifically.
2. **Disappearance is not a single concept.** "Deletion" as commonly used conflates at least five semantically distinct operations (§7). Bizzi never uses an undifferentiated `deleted = true` flag as an authoritative lifecycle state — this directly extends D07 Rule 5 / LAW-D07-15's prohibition on collapsing orthogonal dimensions into one field.
3. **The right to disappear is earned by never having mattered to anyone else.** A subject may be physically removed only if no other subject's own historical integrity depends on its continued resolvability (§8, Invariant 7). This is the single organizing rule beneath every concept-specific rule in §6.
4. **Supersession creates a new identity; it does not mutate an old one.** The successor and predecessor remain two distinct, separately identified subjects connected by a governed relationship (D09 §14, Semantic/Temporal category), never one subject retroactively rewritten to look like another.
5. **Deprecation judges the future, not the past.** Marking something deprecated changes guidance for new use. It never retroactively invalidates instances created while it was current.
6. **Projections carry no lifecycle obligation.** Derived state (D07 §4.3) may be freely discarded and rebuilt at any time; none of this document's rules apply to it (§7.5).
7. **Every disappearance is itself an attributed, governed act.** Even the narrow case where physical deletion is permitted (§8, Invariant 7) requires an Actor, an authority basis, and a durable record that the deletion happened — accountability does not end merely because the deleted subject's own content did (AP-14).

---

## 5. Semantic Definitions

Nine terms, precisely distinguished. Each builds on D07's and D09's already-approved vocabulary without altering it.

### 5.1 Deletion
The removal of a subject such that it is no longer resolvable as an existing domain subject. Always qualified as Physical or Logical (§7) — "Deletion" alone is never a sufficient lifecycle state name.

### 5.2 Archive
A governed lifecycle state marking a subject as no longer operationally active while its identity, current state, and full history remain resolvable and preserved. Archive is reversible in principle (a subject may be unarchived) unless a concept-specific rule forbids it. Archive changes operational relevance; it does not change historical truth.

### 5.3 Replacement (Semantic Replacement)
A new subject is created to serve the role or purpose an existing subject previously served, without asserting the prior subject was ever wrong. Both remain historically valid for their respective periods of currency. Replacement is the general case; Supersession (§5.4) is its formal, governed subtype.

### 5.4 Supersession
A specific, governed form of Replacement in which a new subject explicitly and formally succeeds an existing one through a named D09 relationship, and the predecessor's ongoing authority or currency ends at a defined point — while its historical validity for the period it was authoritative remains fully intact. Supersession is the mechanism by which Decision, Enterprise Object, and Business Operation formally end their active role without disappearing (§6).

### 5.5 Cancellation
A governed termination of a subject's intended course before it reaches its planned or natural completion, without asserting the subject was ever invalid. The subject was valid; its continuation was intentionally stopped. Distinct from failure (unintended) and from Invalidation (§5.6, which asserts a defect).

### 5.6 Invalidation
A governed determination that a subject's state, decision, or result must no longer be treated as authoritative or trustworthy — typically because it is discovered to be defective, non-compliant, or based on invalid input. Distinct from Cancellation: Invalidation is retrospective and asserts something was wrong; Cancellation is prospective and asserts nothing more than "stop here."

### 5.7 Expiration
A time-bound transition, often automatic, in which a subject's validity ends because a previously defined validity window (an effective-time boundary set by a prior governed decision) has elapsed. Expiration requires no new decision at the moment it occurs — the decision was already made when the validity window was set.

### 5.8 Deprecation
A governed, forward-looking signal that a subject, type, or relationship type is discouraged for new use going forward. Existing instances remain fully valid and historically intact (Principle 5). Deprecation is not a judgment on the past; it is guidance for the future.

### 5.9 Historical Preservation
The constitutional guarantee — already established by D07 Rule 4 / LAW-D07-13 and AP-16, and by D09's Historical classification (D09 §5) — that once a subject or relationship has participated in committed, significant business truth, its record remains resolvable, attributable, and reconstructable regardless of what lifecycle transition (§5.1–5.8) it later undergoes. This is the umbrella principle every other definition in this section operates under.

---

## 6. Per-Concept Lifecycle Capability

| Concept | Physically deletable | Archivable | Supersedable | Can become obsolete | Can become immutable |
|---|---|---|---|---|---|
| **Enterprise Object** | Only if never referenced by any committed Business Operation, Decision, or Work Item (§8 Invariant 5) | Yes | Yes — the standard mechanism for closing out a superseded version while preserving history | Yes, at the type or instance level | Yes — its committed historical state becomes immutable once no further authoritative mutation applies (e.g., archived or superseded) |
| **Actor** | Only if never attributed (R10) to any committed governed action — in practice, rare once an identity has acted at all | Yes, expressed as *deactivation* rather than archival, but semantically equivalent: identity persists, active participation ends | **No** — Actor identity is not superseded; a new Actor is simply a new, distinct identity. A role, delegation, or permission *held by* an Actor may be superseded, but that is a Decision/authorization concept, not a transition of Actor itself | **Not applicable in the formal sense** — "obsolete" implies a better replacement type exists for a role a subject played; identity does not have a replacement type. Actor supports only Deactivation, not Obsolescence | Yes — every attribution record (R10) is immutable the instant it is committed, independent of the Actor's own current active/inactive status |
| **Work Item** | Only if never coordinated by a Business Operation (R2) and never had a Runtime Session executed against it (R5) | Yes | Yes | Yes, at the type or instance level | Yes — once completed, cancelled, or archived, its committed history becomes immutable |
| **Decision** | Only if it has never governed anything (R1) — the rarest case, since a Decision's whole purpose is to govern | Rarely the applicable term (Revocation is more precise for an active-but-withdrawn Decision), but the closed record may still be archived | **Yes — the primary mechanism.** Decision content itself is treated as immutable once approved (mirroring D07's Significant Transition treatment); a changed determination is always a new, superseding Decision, never an edit | Yes — a Decision's basis can become obsolete relative to a later policy without being formally revoked | Yes, immediately upon approval — an approved Decision's determination does not change; only supersession, revocation, or expiration end its currency |
| **Business Operation** | Only if it has never been governed by a Decision (R1) and never coordinated a Work Item (R2) — rare once an Operation has begun real coordination | Yes | Yes | Yes | Yes — once completed, compensated, or archived, its committed history becomes immutable |
| **Runtime Session** | **Yes, freely**, once its execution attempt has concluded and any significant facts it produced are committed to the owning aggregate's own transition history and Domain Events (D07 §10) | Yes, or simply deleted — no historical dependency requires retaining it | **No** — a retry or re-execution is a new, distinct Runtime Session related to its predecessor only by a Temporal ("follows") relationship (D09 §13), never a formal Supersession, because Runtime Session is not authoritative for anything a successor would need to formally succeed | Not applicable in the formal sense, for the same reason as Actor: there is no "better replacement type" for one execution attempt relative to another — they are simply distinct historical attempts | Yes — once ended, its recorded execution trace becomes immutable, though the trace itself carries no ongoing authority |

Domain Event and Significant Transition records are not additional rows in this table — they are not domain-owning concepts (D07 §5 lists them as state domains, not aggregates) — but §7.4 and §8 apply to them directly: they are Historical Record by construction and are never subject to Physical Deletion once committed.

---

## 7. Differentiating Five Operations Commonly Confused as "Deletion"

### 7.1 Physical Deletion
Irreversible removal of a subject's representation such that it can no longer be resolved, reconstructed, or referenced at all. Constitutionally permitted **only** for a subject that has never participated in any committed, significant relationship, transition, or attribution (§8 Invariant 7). This is a narrow mistake-correction mechanism — never a general-purpose lifecycle tool, and never the default meaning of "delete" for any of the six concepts once they have done anything of consequence.

### 7.2 Logical Deletion
A governed state transition — Cancelled, Archived, Superseded, Invalidated, or Expired, whichever is semantically correct for the situation — that marks a subject as no longer active or current while its identity and full history remain resolvable and preserved. This is the default, constitutionally required mechanism for any of the six concepts once they have participated in committed business truth (which, per §6, is nearly immediately for Decision, Business Operation, and Actor). A generic, undifferentiated "soft delete" flag is prohibited (Principle 2) — the specific transition type must be named.

### 7.3 Semantic Replacement
Not a deletion at all. The prior subject is not required to change lifecycle state merely because a successor exists — Replacement (§5.3) and its formal subtype Supersession (§5.4) are additive: a new subject is introduced; the old subject's own state changes only if a separate, explicit rule says so (typically, the predecessor does transition to Superseded as part of the same governed act — but this is the Supersession relationship's own defined consequence, not an automatic side effect of "replacement" as a general concept).

### 7.4 Historical Record
The durable, immutable trace — significant transition records, audit records, attribution records, Domain Events — that exists independently of its subject's current lifecycle state. This survives Archive, Cancellation, Supersession, Expiration, and Invalidation without exception. It is removable only via Physical Deletion, and per §8 Invariant 7, Physical Deletion is unavailable to anything that produced a Historical Record in the first place. In practice, therefore, Historical Records are permanent under this constitution; any future time-bound retention policy is a business/compliance decision layered on top, not an architectural one (§9).

### 7.5 Projection Cleanup
Not a domain-level operation at all. Projections, read models, caches, indexes, and search representations (D07 §4.3, LAW-D07-09) may be purged, invalidated, or rebuilt at any time, for any reason, without authority basis, validation, or preservation obligation, because they were never authoritative. Conflating Projection Cleanup with any of §7.1–7.4 is the single most likely implementation-time error this chapter exists to prevent — clearing a search index or dashboard cache is not "deleting" anything in the domain sense.

---

## 8. Mandatory Invariants

1. **A Decision that has governed (R1) a Business Operation cannot be physically deleted** — only superseded, revoked, or allowed to expire. The Business Operation's authority basis must remain reconstructable indefinitely (D07 LAW-D07-13; D09 R1).
2. **A Business Operation that has been governed by a Decision, or has coordinated (R2) a Work Item, cannot be physically deleted** — only cancelled, compensated, completed, or superseded. The governing Decision's own record of what it authorized, and any coordinated Work Item's own record of what coordinated it, must remain resolvable.
3. **A Runtime Session may be physically deleted** once its execution attempt concludes and its significant facts are committed elsewhere, because Runtime Session never owns authoritative state of any other concept (D04; D09 Prohibition 2) — its disappearance compromises no other concept's historical integrity.
4. **An Actor that has been attributed (R10) to any committed governed action cannot be physically deleted** — only deactivated. Accountability (AP-14) requires the attributed identity to remain resolvable for as long as the action it is attributed to remains part of the historical record, which by Invariants 1–2 is generally indefinite for significant actions.
5. **An Enterprise Object referenced (R7/R8/R9) by any committed Business Operation, Decision, or Work Item cannot be physically deleted** — only archived, deprecated, or superseded — for the same reconstruction reason.
6. **A Work Item coordinated by a Business Operation, or the target of a committed Runtime Session execution, cannot be physically deleted** — only cancelled, completed, or superseded.
7. **A subject with zero committed relationships, transitions, or attributions referencing it may be physically deleted.** This is the only condition under which Physical Deletion is constitutionally available to any of the six concepts — the narrow exception, not the rule (Lifecycle Principle 3).
8. **No lifecycle transition — Cancellation, Invalidation, Expiration, Supersession, or Archival — ever deletes or rewrites a subject's own already-committed significant transition history** (extends D07 LAW-D07-13 / Rule 4 to this chapter's vocabulary explicitly).
9. **Supersession never physically deletes the superseded subject.** It creates a new subject and a governed Supersession relationship between them (D09 Semantic/Temporal category); the superseded subject's own lifecycle state transitions to reflect that it has been superseded — it is never overwritten to look like the successor.
10. **Projection and read-model cleanup is exempt from every invariant above.** It carries no domain consequence and requires no authority basis (D07 LAW-D07-09; §7.5).
11. **Deprecation never invalidates or retroactively judges existing instances.** A deprecated relationship type, capability, or object type remains fully valid and historically preserved for every instance created before or during its deprecated status.
12. **No lifecycle transition governed by this chapter may cross a Workspace boundary**, mirroring D09's LAW-D09-10 applied to endings: a subject's Archive, Cancellation, Supersession, or deletion decision is itself a workspace-scoped governed action.
13. **Every Physical Deletion permitted under Invariant 7 must itself be attributed and auditable** — an Actor, an authority basis, and a durable record that the deletion occurred are required even though the deleted subject's own content is gone (Lifecycle Principle 7; AP-14).

---

## 9. Inheritance of Historical Responsibility

When a subject is superseded, its successor does **not** inherit the predecessor's historical transition records as its own history. The predecessor's history remains attributed to the predecessor, permanently. The successor's own history begins at its own creation, connected to the predecessor only through the explicit Supersession relationship (D09 §14) — never by absorption or relabeling. This prevents what this chapter names **history laundering**: a successor claiming credit or blame for facts that occurred under the predecessor's own authority, before the successor existed.

The *responsibility* to keep the predecessor resolvable does not transfer to the successor subject either. It is inherited by the platform's own constitutional preservation guarantee (§5.9, §8 Invariant 8) — the same guarantee that already applies to every other Historical Record — not by any single successor instance. A successor going out of existence in the future (through its own later supersession) does not, and could not, discharge the platform's obligation to keep the original predecessor's history resolvable.

**Retention duration is explicitly not decided here.** How long a preserved Historical Record must remain queryable, whether older records may move to a different storage tier, and what (if any) legal retention or erasure obligation applies are business, compliance, and legal questions this project's own planning corpus has already flagged as outside architecture's authority to originate (mirrored by `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` GC-009's identical scoping for audit-record retention). D10 establishes only that preservation is indefinite **by default**, absent such a decision — not that no such decision will ever be made.

---

## 10. Preservation Rules

1. Anything D09 §5 classifies **Historical** — every significant transition record, every Actor attribution (R10), every Runtime Session's execution trace once concluded — remains resolvable indefinitely by default, subject only to a future, explicitly separate retention decision (§9).
2. Preservation applies to the **record**, not to operational or active status. An Archived, Superseded, Cancelled, Invalidated, or Expired subject is preserved but is not thereby active or current — the two are independent (§5.2's Archive definition already establishes this; this rule generalizes it to all logical-deletion outcomes).
3. Preservation is never waived by any lifecycle transition in §5 — only Physical Deletion removes a record, and Physical Deletion is available only precisely where §8 Invariant 7 confirms nothing needs preserving in the first place. Preservation is not "turned off"; it is simply inapplicable to a subject that never produced anything to preserve.
4. A rebuilt or reconciled projection (§7.5) never counts as, or substitutes for, preservation of the authoritative record it was derived from (D07 §11's reconstruction order already establishes this; restated here because deletion-adjacent contexts are exactly where the two are most likely to be confused).

---

## 11. Semantic Identity Continuity

A subject's identity — what it fundamentally *is*, distinct from its current lifecycle state — persists across every lifecycle transition in §5 **except** Physical Deletion. A Cancelled, Archived, Invalidated, Expired, or Deprecated instance remains the *same* identified subject throughout, addressable by the same identity before, during, and after the transition.

**Supersession is the sole exception, by design.** Supersession does not evolve one identity into another — it creates a genuinely new, distinct identity, connected to its predecessor only through a governed relationship (D09 §14; consistent with D09's own LAW-D09-15/29, "one assertion, one identity," applied here to the relationship instance rather than conflating the two endpoint subjects into one). A Decision that supersedes an earlier Decision is a new Decision with its own identity, its own approval record, and its own governance history — not the old Decision "updated." This resolves what would otherwise be a natural point of confusion: Supersession is *replacement of one identity by another*, never *evolution of a single identity*.

---

## 12. Final Decision

### D10 — Deletion and Supersession

**Status:** APPROVED — CLOSED
**Approved by:** Project Owner
**Approval date:** 2026-07-23
**Closure date:** 2026-07-23

> Bizzi distinguishes nine lifecycle-ending concepts — Deletion, Archive, Replacement, Supersession, Cancellation, Invalidation, Expiration, Deprecation, and Historical Preservation (§5) — and five operations commonly conflated with deletion — Physical Deletion, Logical Deletion, Semantic Replacement, Historical Record, and Projection Cleanup (§7).
>
> Physical Deletion is constitutionally available only to a subject with zero committed relationships, transitions, or attributions referencing it (§8 Invariant 7) — the narrow exception, never the default. Decision, Business Operation, Enterprise Object, Work Item, and Actor each become effectively non-physically-deletable the moment they participate in committed business truth; Runtime Session remains freely deletable throughout, because it never owns authoritative state belonging to any other concept.
>
> No lifecycle transition ever deletes, rewrites, or retroactively judges a subject's own already-committed history. Supersession creates a new identity rather than mutating an old one, and its successor never inherits the predecessor's history as its own — preventing history laundering. Deprecation affects only future use, never past validity. Projection cleanup carries no domain consequence whatsoever.
>
> Retention duration — how long a preserved record must remain queryable — is explicitly not decided by this chapter and remains a business/compliance decision outside architecture's authority to originate.

### Sub-decisions

| Sub-decision | Subject | Status |
|---|---|---|
| D10.1 | Semantic Definitions (Deletion, Archive, Replacement, Supersession, Cancellation, Invalidation, Expiration, Deprecation, Historical Preservation) | APPROVED (§5) |
| D10.2 | Per-Concept Lifecycle Capability | APPROVED (§6) |
| D10.3 | Physical vs. Logical Deletion, Semantic Replacement, Historical Record, Projection Cleanup | APPROVED (§7) |
| D10.4 | Mandatory Invariants | APPROVED (§8) |
| D10.5 | Inheritance of Historical Responsibility | APPROVED (§9) |
| D10.6 | Preservation Rules | APPROVED (§10) |
| D10.7 | Semantic Identity Continuity and Constitutional Review | APPROVED — CLOSED (§11, this section) |

### Binding consequences (upon approval)

1. No Gate C repository or service method may implement a bare `delete()` for Decision, Business Operation, Enterprise Object, or Work Item without first checking Invariants 1, 2, 5, and 6 — such a method is a constitutional violation, not an implementation shortcut.
2. Runtime Session's schema and repository may implement genuine physical deletion/purge directly, consistent with §6 and Invariant 3, once its significant facts are confirmed committed elsewhere.
3. Any "soft delete" mechanism in Gate C's implementation must use the specific transition name (Cancelled, Archived, Superseded, Invalidated, Expired) applicable to the concept and situation — a generic `is_deleted` boolean is a Gate C implementation defect under Lifecycle Principle 2.
4. Supersession implementations must create a new aggregate instance with its own identity and record a D09-typed Supersession relationship — never mutate the predecessor's own identity or content in place.
5. ADW-01 is complete upon this decision's closure: D01–D10 constitute the full Core Domain Semantics baseline referenced by `ARCHITECTURE_SPECIFICATION.md` §7.

### Deferred responsibilities

- Retention duration and any legal/compliance erasure obligation — a future business/compliance decision, not an ADW chapter (§9).
- ADW-03: authorization policy for who may request Cancellation, Invalidation, Supersession, or the narrow Physical Deletion case.
- ADW-05: Runtime Session's internal execution-attempt state machine and what "concluded" precisely means for it operationally.
- ADW-07: the durable audit/event record schema for lifecycle transitions themselves.
- ADW-08: physical archival storage, cold-tier persistence, and projection rebuild mechanics.
- ADW-10: Governance and Architecture Freeze — closes Gate C v1.1 once all ten ADW chapters, including this one, are approved.

### Closure record

D10 is closed. The Project Owner reviewed §2–§12 and explicitly approved this document on 2026-07-23, after re-confirming: D10 is complete and internally consistent; introduces no unresolved architectural questions within its own scope (the four items in §14 are explicitly-scoped deferrals to ADW-02/ADW-05 or an out-of-architecture business decision, matching the pattern D07 and D09 also closed against); requires no further semantic changes; is compatible with Decision 0001 (no new entities, no architecture expansion beyond what §5–§11 already scoped); and satisfies the same closure criteria D07 and D09 met (sub-decisions D10.1–D10.7 all complete, binding consequences stated, deferred responsibilities named, supersession rule stated). **ADW-01 is complete: D01–D10 constitute the full Core Domain Semantics baseline**, per Binding Consequence 5 above.

### Supersession rule

D10 may be changed only by an explicit Class A architecture decision that preserves: the Historical Preservation guarantee (§5.9, §10); the narrow-exception-only availability of Physical Deletion (§8 Invariant 7); the prohibition on history laundering through Supersession (§9); and Runtime Session's status as the one concept exempt from historical deletion restriction (§6, Invariant 3).

---

## 13. Synchronization Requirements

D10 is now approved and closed (§12). The following remain to be executed as separate, later steps of the Architecture Baseline governance execution sequence — not performed by this document, and not yet done as of this closure:

1. `ADW_01_DECISION_REGISTER.md` — add the D10 register entry mirroring D07's and D09's closure format; update §2 status table (D10: `OPEN — NEXT` → `APPROVED — CLOSED`); update the Current Workshop State block; note ADW-01 itself as complete (D01–D10 all approved). *(Executed alongside this closure — see the Decision Register directly.)*
2. `ARCHITECTURE_SPECIFICATION.md` §8 (ADW-01 Decision State table) — D10 row: `OPEN — NEXT` → `APPROVED — CLOSED`. §14 (Current Architecture Status) — update `D10` and note ADW-01 complete; `Next constitutional step` becomes ADW-02 (Identity and Workspace Boundary) per the workshop structure in §7, not another ADW-01 decision. *(Not yet done — scheduled as a later step, contingent on the Authority Hierarchy approval per the Architecture Baseline Resolution Package.)*
3. `DOMAIN_FOUNDATION.md` §13 (Stabilization Record) — add a D10 closure entry, consistent with the existing D06/D09 entries. *(Not yet done — scheduled as a later step.)*

---

## 14. Open Questions Carried Forward

1. What retention duration, if any, applies once a business/compliance decision is made — explicitly out of this chapter's scope (§9), tracked here so it is not forgotten.
2. Whether a formal "Deactivated" status for Actor requires its own typed representation distinct from a generic Archive, given §6 treats it as semantically equivalent but names it separately — a candidate refinement for ADW-02 (Identity and Workspace Boundary), which owns Actor's identity model in more detail.
3. Whether Runtime Session's "concluded" state (the precondition for Invariant 3's physical deletion permission) needs a more precise operational definition than D07's existing state dimensions provide — deferred to ADW-05 (Agent Runtime).
4. Whether the Gate C entity/index/repository work already proposed in `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` (GC-001–GC-010, drafted independently of ADW-01) is consistent with D10's invariants — not evaluated here, since reconciling the two Gate C planning tracks is a separate, already-flagged open item outside this chapter's scope.

---

## 15. Current Workshop Status

```text
D10.1 Semantic Definitions: APPROVED
D10.2 Per-Concept Lifecycle Capability: APPROVED
D10.3 Deletion/Replacement/Record/Cleanup Differentiation: APPROVED
D10.4 Mandatory Invariants: APPROVED
D10.5 Inheritance of Historical Responsibility: APPROVED
D10.6 Preservation Rules: APPROVED
D10.7 Semantic Identity Continuity and Constitutional Review: APPROVED — CLOSED

D10 overall status: APPROVED — CLOSED
ADW-01 overall status: D01-D10 APPROVED — CLOSED. Decision-level closure of ADW-01 is complete.
Governance-level baseline activation (Authority Hierarchy approval, repository
synchronization, Architecture Baseline Resolution signature) remains pending
per the Architecture Baseline Resolution Package, Execution Order steps 2-9.
```
