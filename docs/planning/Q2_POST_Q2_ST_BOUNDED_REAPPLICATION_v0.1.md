# WP19 / Q2 Post-Q2-ST Bounded Re-application v0.1

**Status:** Active planning evaluation — post-Q2-ST  
**Date:** 2026-08-30  
**Subject:** BR1–BR5 re-check under accepted D1–D5, Q2-RI, and Q2-ST-O2  
**Authority:** None. This artifact evaluates; it does not select the persisted Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Controlling authority

This re-check applies:

- D1–D5 — CLOSED / ACCEPTED;
- Q2-RI — CLOSED / ACCEPTED — O2 PREFERENCE;
- Q2-ST — CLOSED / ACCEPTED — O2 persisted-entity identity default with explicit architecture-controlled mapping exceptions;
- current D1 subject-kind set: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`;
- no mapping exception currently authorized.

Canonical Q2-ST authority: `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.

## 2. Effect of accepted Q2-ST on the current bounded test set

For the five current D1 subject kinds, accepted Q2-ST introduces no mapping exception and no one-kind-to-many-persisted-form mapping. Each current bounded subject kind continues to resolve to one canonical persisted identity target in the BR realizations under evaluation.

Therefore the prior bounded comparison does not require structural redesign merely because Q2-ST is now closed. The earlier provisionality is removed for the current five-kind test set.

This finding does **not** authorize a future standalone specialization under `EnterpriseObject`. Under accepted Q2-ST, such a distinct persisted identity form requires separate subject-kind authority or an explicit mapping exception before AuditRecord use.

## 3. BR1 / N1 — typed polymorphic reference

**D1–D5:** CONFORMING in the bounded current-five realization.  
**Q2-RI credit:** NONE.

Accepted Q2-ST does not add an auxiliary registry or DB target abstraction. The explicit subject kind plus durable identifier and type-dispatch/write-validation contract remains sufficient for bounded conformity, subject to final Q2 representation authority defining the actual persisted contract.

## 4. BR2 / N2 — composite-FK family

**Current-five sufficiency:** NOT SUFFICIENT in its corpus-grounded bounded form.  
**Q2-RI credit:** LOCAL ONLY where a concrete composite relation actually applies.

Q2-ST does not cure the existing structural asymmetry: `Workspace` and `User` do not expose the same `(workspace_id, id)` target shape as the workspace-scoped entities. No synthetic identity or registry is introduced.

## 5. BR3 / N3 — per-type nullable relations

**D1–D5:** CONFORMING in the bounded current-five realization.  
**Q2-RI credit:** POSITIVE for the five current concrete target relations.

Accepted Q2-ST preserves the current bounded one-kind/one-canonical-target profile. Each current subject-specific relation can therefore retain ordinary FK enforcement to its concrete target without adding an auxiliary abstraction solely for RI.

The exactly-one/discriminator-match invariant remains a separate required integrity property; Q2-RI credit for target FKs does not solve it automatically.

A future authorized mapping exception that makes one logical kind span multiple persisted identity forms would require a bounded Q2-RI re-application and could reduce this credit for the affected kind.

## 6. BR4 / N4 — typed opaque identity

**D1–D5:** CONFORMING only with an explicit durable resolver contract.  
**Q2-RI credit:** NONE in the bounded realization.

Accepted Q2-ST simplifies the current resolver burden by keeping each present kind associated with one canonical persisted identity target, but it does not itself define the opaque-key resolver or authorize mapping infrastructure.

## 7. BR5 / N5 — dedicated subject identity in persisted content

**D1–D5:** CONFORMING only with a mandatory dedicated subject-identity content contract.  
**Q2-RI credit:** NONE in the bounded realization.

Accepted Q2-ST does not alter the current content contract requirement: subject kind and durable identifier must be explicit and stable; actor/context/diff data cannot establish subject identity by implication.

## 8. Post-Q2-ST comparative state

The current five-kind bounded comparison is now non-provisional with respect to Q2-ST:

1. BR1 remains conforming without ordinary DB-RI credit.
2. BR2 remains insufficient in its current corpus-grounded five-type form, with local RI credit only.
3. BR3 remains conforming and retains positive per-realization Q2-RI credit for the current five concrete target relations.
4. BR4 remains a qualified alternative with resolver-governance burden and no bounded RI credit.
5. BR5 remains a qualified alternative with content/query-validation burden and no bounded RI credit.

Accepted Q2-ST does not itself select BR3 or any other representation.

## 9. Future reopen effect

Per accepted Q2-ST, before implementation of an auditable mutation whose subject has a persisted identity form not already covered by an accepted AuditRecord subject kind and canonical subject-identity contract, subject-kind/mapping authority MUST reopen.

If a future explicit mapping exception is accepted, D-11 is reopened and affected BR/Q2-RI evaluation must be repeated before implementation where the mapping changes canonical target shape or RI availability.

## 10. Gate result

**POST-Q2-ST BOUNDED RE-APPLICATION COMPLETE FOR THE CURRENT FIVE SUBJECT KINDS — PRIOR Q2-ST PROVISIONALITY REMOVED — BR3 RETAINS POSITIVE Q2-RI CREDIT WITHOUT AUTOMATIC SELECTION — FINAL Q2 PERSISTED REPRESENTATION REMAINS OPEN.**

Next bounded step: prepare the separate persisted-representation decision for Project Owner review. No implementation is authorized by this artifact.
