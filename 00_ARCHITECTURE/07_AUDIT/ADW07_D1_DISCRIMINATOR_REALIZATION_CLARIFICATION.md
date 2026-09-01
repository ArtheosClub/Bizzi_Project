# ADW-07 — D1 Discriminator Realization Clarification

**Workshop:** ADW-07 — Events, Audit, and Provenance  
**Workshop Status:** OPEN  
**Decision:** Clarification of accepted D1 — realization of the durable subject-type discriminator  
**Decision Status:** ACCEPTED  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-08-30  
**Affected accepted authority:** `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`  
**Effect category (accepted-record lifecycle authority):** **Clarifies an ambiguity.** This artifact does not amend, supersede, or edit the accepted D1 record, and does not change its substantive requirement. The accepted D1 text remains the historical record of what was accepted on 2026-08-30 and is unchanged.

## 1. The ambiguity being clarified

Accepted D1 requires an explicit durable subject-type discriminator as part of the durable subject-reference contract, requires that it identify exactly one of the five accepted subject kinds, states that type qualification within a durable subject identity satisfies the rule, and expressly does not decide the discriminator's physical placement or persistence mechanism.

Two readings of that text are available and produce different outcomes:

- one reading takes "discriminator" and "the discriminator's committed value" to require a persisted kind token — a stored value naming the subject kind;
- the other takes D1's express non-decision on placement and mechanism to leave open any realization that makes the subject kind explicit and determinate, including one in which the kind is carried by the structure of the persisted reference rather than by a stored token.

The ambiguity is material because a conforming realization in which the subject kind is determined by which typed reference path is populated has no separately stored kind token, and therefore no "committed value" in the first reading's sense.

## 2. Clarification

**D1's requirement is a property requirement, not a mechanism requirement.**

A persisted AuditRecord subject reference satisfies accepted D1 where its realization guarantees all three of the following:

1. **Explicit.** The subject kind is determinable from the persisted AuditRecord subject reference alone, under a rule fixed by architecture, without consulting any source that accepted D4 excludes from establishing subject identity.
2. **Determinate.** The persisted state yields exactly one subject kind from the accepted set. No committed record can be read as identifying two kinds, or none.
3. **Durable and stable.** The subject kind so determined does not change for a committed record, consistent with D3 and D4.

A realization that stores a kind token satisfies this requirement where the token is authoritative for the record. A realization that carries the kind structurally — for example, by which typed reference path of a fixed, architecture-authorized set is populated — likewise satisfies it, **provided that the realization guarantees property 2**. Type qualification within a durable subject identity, as D1 already states, remains one instance of the same requirement rather than a separate allowance.

## 3. Consequence for realizations carrying the kind twice

Where a realization carries the subject kind in more than one place — for example a stored kind token alongside a structurally encoded kind — those representations are two statements of one fact. Property 2 is satisfied only where the realization guarantees their agreement for every committed record.

Where the representations disagree, the persisted state does not yield exactly one determinate subject kind under this clarification's conformance test. Such a record therefore fails property 2. Once committed, that contradiction cannot be repaired by reinterpreting or mutating the historical record consistently with D3, D4, and D10 §7.4.

This is a conformance consequence, not a preference among realizations. This clarification expresses no preference between token-carrying and structural realizations.

## 4. Relationship to Q2-EX

Property 2 requires the persisted state of each committed record to yield exactly one subject kind. It does not decide **how** that guarantee is obtained, at which layer it is enforced, or what constraint expresses it. That question is the separate open Q2-EX surface and is not decided here.

## 5. Rationale

D1's fourth sentence states that D1 does not decide the discriminator's physical placement or persistence mechanism. Reading D1's first two sentences to require one specific mechanism — a stored kind token — would give the decision a scope it expressly disclaimed, and would decide by implication a question D1 declined to decide.

Stating the requirement as a property test rather than enumerating permitted mechanisms keeps every candidate realization under one rule, so that a stored token, a typed identifier, and a structural encoding are each judged by whether they make the subject kind explicit, determinate, durable, and stable — which is what D1 required.

This clarification therefore resolves how D1's requirement is tested. It adds no new requirement, removes none, and changes no accepted subject kind.

## 6. Explicit non-decisions

This clarification does not:

- amend, supersede, or edit accepted D1, or any part of D1–D5, Q2-RI, or Q2-ST;
- change D1's five accepted subject kinds or authorize a sixth;
- decide Q2-EX, the exactly-one guarantee mechanism, or its enforcement layer;
- select N1–N5 or BR1–BR5, or decide the Q2 persisted representation;
- prefer a structural realization over a token realization, or the reverse;
- authorize any mapping exception under accepted Q2-ST;
- define columns, constraints, indexes, migrations, ORM mappings, or resolver contracts;
- decide actor attribution or ActorContext persistence semantics;
- authorize WP19 implementation.

## 7. Current state

- D1: **CLOSED — ACCEPTED**, unchanged; realization test clarified by this artifact;
- D2–D5: **CLOSED — ACCEPTED**, unaffected;
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**, unaffected;
- Q2-ST: **CLOSED — ACCEPTED — O2**, unaffected;
- Q2-EX: **OPEN** — BR3-conditional;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.
