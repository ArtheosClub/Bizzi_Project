# ADW-07 Accepted Decision Record Lifecycle Options v0.1

**Status:** Draft — governance options/evaluation only  
**Date:** 2026-08-30  
**Subject:** Lifecycle and correction mechanism for ACCEPTED ADW-07 decision records  
**Decision owner:** Project Owner  
**Authority:** None. This artifact structures a governance gap; it does not decide it.  
**Implementation effect:** None.

## 1. Bounded question

**After an ADW-07 decision record has status `ACCEPTED`, may that canonical record be edited in place, and if correction or reconciliation is later required, what governance mechanism preserves provenance without silently changing accepted meaning?**

This question is about decision-record lifecycle only. It does not reopen the substance of Blocks 1–4, D1–D5, Q2-RI, Q2-ST, or the final Q2 representation.

## 2. Why a lifecycle rule is required now

ADR records already have an accepted-record lifecycle convention: accepted ADRs are treated as immutable and substantive change is recorded through later authority rather than silently rewriting the accepted decision.

ADW-07 now contains two recording forms:

1. Blocks 1–3 embedded in `EVENTS_AUDIT_AND_PROVENANCE.md`;
2. later accepted decisions in separate canonical authority files, discoverable through `ADW07_DECISION_INDEX.md`.

No approved governance rule currently states whether an accepted ADW-07 decision record may be edited in place.

The gap is no longer theoretical. Earlier accepted D1 and D2 records refer, in their explicit non-decision lists, to the historical framework label `D4 — DB-enforced referential integrity`. The active framework later reconciled that unresolved surface under the identifier `Q2-RI`, while `D4` became the accepted Subject Reference Semantics decision. The old text remains historically understandable but is now address-ambiguous.

Editing accepted D1/D2 in place would create a precedent unless an explicit lifecycle rule authorizes it. Leaving the text untouched while a later authority provides a reconciliation clause preserves provenance but also requires a defined mechanism.

## 3. Requirements for any option

Any lifecycle rule should preserve:

- canonical decision provenance;
- visibility of what the Project Owner actually accepted at the time;
- no silent change to normative meaning, scope, outcome, or decision identity;
- discoverability of later corrections, reconciliations, amendments, or supersession;
- no duplication of canonical normative wording into the pointer-only decision index;
- a clear distinction between historical typo/address correction and substantive architectural change.

## 4. Options

### L1 — Immutable after acceptance; all corrections via separate authority

**Rule:** Once an ADW-07 decision record is `ACCEPTED`, its canonical text is not edited in place. Any later correction, clarification, identifier reconciliation, amendment, or supersession is recorded in a separate authority artifact that explicitly identifies the affected accepted record and the exact effect of the later authority.

The original accepted record remains historical evidence of what was accepted at that time.

**Consequences:**

- strongest provenance and simplest audit trail;
- avoids arguments over whether an in-place edit was “only editorial”;
- O-1 is handled by the future Q2-RI authority through an explicit reconciliation clause, not by rewriting D1/D2;
- later readers may need to follow a correction/amendment pointer to get current interpretation;
- decision index may point to the original canonical record and, where governance later defines it, a separate amendment/reconciliation record, but must not restate normative text.

**Evaluation:** **PREFERRED.** It matches the repository's existing anti-silent-decision discipline and avoids creating a mutable-authority precedent.

### L2 — Immutable normative text; narrowly permitted in-place metadata/traceability corrections

**Rule:** Normative decision meaning is immutable after acceptance, but clearly non-normative metadata or traceability fields may be corrected in place if the edit cannot change meaning, scope, outcome, or decision identity and is explicitly logged as a non-normative correction.

Examples might include a broken path, typo in a citation, or identifier alias where the original meaning is unambiguous.

**Consequences:**

- cheaper for obvious clerical defects;
- requires a reliable test separating metadata from normative meaning;
- creates borderline cases, including O-1: changing `D4` to `Q2-RI` appears address-only, but the collision arose from a later substantive reuse of `D4`, so the historical text itself carries provenance value;
- needs a correction-log convention not currently established.

**Evaluation:** VIABLE BUT HIGHER GOVERNANCE AMBIGUITY.

### L3 — Accepted records may be edited with changelog

**Rule:** Accepted ADW-07 records may be updated in place if every change is documented in a changelog and no explicit superseding decision is required by the editor's judgment.

**Consequences:**

- operationally cheap;
- weakens the distinction between “what was accepted then” and “what the file says now”;
- makes semantic-vs-editorial classification depend on later editors;
- creates the same class of silent-authority risk the architecture process has repeatedly tried to avoid.

**Evaluation:** NOT RECOMMENDED.

## 5. Recommended governance rule

Recommended option: **L1 — immutable after acceptance; later change via separate authority.**

Proposed rule for Project Owner acceptance:

> **Once an ADW-07 decision record is ACCEPTED, its canonical accepted text MUST NOT be edited in place. Any later correction, clarification, identifier reconciliation, amendment, or supersession MUST be recorded through a separate explicit authority artifact that identifies the affected accepted record and states the effect of the later authority. The original accepted record remains the historical record of what was accepted at that time. Pointer/index artifacts MAY improve discoverability but MUST NOT alter, restate, or silently correct canonical normative meaning.**

## 6. Effect on current findings if L1 is accepted

### O-1 historical `D4 = DB RI` references

Do not edit D1 or D2 in place. The future accepted Q2-RI authority should include a reconciliation clause stating that references in earlier Q2 records to `D4 — DB-enforced referential integrity` refer to the unresolved surface now identified as `Q2-RI`, not to the later accepted `D4 — Subject Reference Semantics` decision.

The same reconciliation can enumerate the known historical planning references without converting those planning files into authority.

### O-4 ADW-07 recording/discoverability wording

The current navigation preamble in `EVENTS_AUDIT_AND_PROVENANCE.md` should not be treated as authority establishing a general future recording convention. Under L1, any general convention for where future accepted ADW-07 decisions must live should itself be decided explicitly if needed.

A later non-normative navigation repair may describe the repository factually (for example, that Blocks 1–3 are embedded and later accepted records currently exist as separate canonical files), but it must not create new permission or lifecycle rules by wording alone.

### Future amendments

This option does not require every later authority to use the word `ADR`. A separate ADW-07 amendment/reconciliation/supersession artifact can be sufficient if its status, decision owner, affected authority, and effect are explicit and discoverable.

## 7. Explicit non-decisions

This artifact does not:

- itself establish L1, L2, or L3;
- edit accepted Blocks 1–4 or D1–D5;
- decide Q2-RI or Q2-ST;
- decide the final Q2 representation;
- define a general lifecycle for all repository document classes;
- change ADR lifecycle rules;
- authorize implementation.

## 8. Gate

**PROJECT OWNER GOVERNANCE DECISION REQUIRED.**

Until a lifecycle rule is accepted, accepted ADW-07 decision records should be treated conservatively as non-editable in place, and O-1 should remain unresolved by direct edits.