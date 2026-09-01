# WP19 / Q2-RI Referential-Integrity Weight Options v0.1

**Status:** Draft — options/evaluation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — architectural weight of DB-enforced referential integrity  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures Q2-RI; it does not decide it.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Bounded question

**For the persisted AuditRecord subject-reference representation, what architectural weight, if any, should DB-enforced referential integrity receive: mandatory requirement, comparative preference, or neither?**

Q2-RI is not a persistence-shape decision. It does not itself select N1–N5, a foreign-key layout, deletion behavior, or an enforcement implementation.

## 2. Why Q2-RI exists

The approved Q2 evaluation framework originally exposed this question under the identifier `D4`. The identifier `D4` was subsequently assigned to the accepted Subject Reference Semantics decision. The unresolved referential-integrity surface is therefore reconciled under the identifier **Q2-RI**.

The question remains substantively open. Existing authority establishes that DB-enforced RI is **not already mandatory**, but that statement does not answer whether DB-enforced RI should receive comparative preference when multiple conforming candidates are available.

This distinction matters especially to N1 versus N3:

- N1 can satisfy D1–D5 but conventional multi-table polymorphic references do not inherently provide ordinary DB foreign-key enforcement to one of several target tables;
- N3 can satisfy D1–D5 and can naturally expose type-specific relations that may support ordinary DB-native foreign keys;
- D4's requirement for one logical subject identity does not require one physical reference path and therefore cannot by itself rank N1 above N3.

Until Q2-RI is decided, **N1 vs N3 remains UNDETERMINED — Q2-RI DECISION REQUIRED**.

## 3. Inherited boundaries

Q2-RI must preserve accepted D1–D5 and may not redefine them.

In particular:

- subject identity remains mandatory, explicit, durable, stable, and independently resolvable;
- actor/context/payload cannot substitute for subject identity;
- historical identity survives later lifecycle change under D3;
- the current five-type Q2 scope remains as accepted by D5;
- future extensibility convenience is not itself a ranking criterion;
- retention/legal/compliance policy remains outside this question;
- FK delete actions, cascade behavior, and subject-deletion permission are not decided here.

## 4. Options

### Q2-RI-O1 — DB-enforced referential integrity is a REQUIREMENT

**Rule:** A Q2 representation is acceptable only if the database itself enforces referential integrity between the persisted AuditRecord subject reference and the referenced subject identity for the complete current Q2 scope.

**Consequences:**

- candidates without a complete DB-enforced reference story would fail or require material supporting structure;
- N3 gains a natural path to per-type FK enforcement;
- N1 would need additional DB structure beyond a naive multi-table `type + id` reference;
- N2's DB-native property becomes materially important, although its documented five-type incompleteness remains;
- N4/N5 would need a DB-enforced target/resolution structure rather than only application/content validation.

**Risk:** This is a strong new architectural constraint. No accepted authority currently requires it. It may force additional persistence abstraction solely to satisfy enforcement location.

### Q2-RI-O2 — DB-enforced referential integrity is a PREFERENCE

**Rule:** D1–D5 compliance is mandatory. Among otherwise conforming representations, stronger DB-native referential integrity is a legitimate comparative advantage, but lack of ordinary DB FK enforcement is not automatically disqualifying if durable correctness is established by another explicit mechanism.

**Consequences:**

- N1 and N3 can both remain admissible;
- N3 receives a genuine comparative strength from type-specific DB relations if the concrete realization uses them;
- N1 must justify the integrity and validation trade-off rather than being preferred merely for one logical reference shape;
- N2's relational enforcement is a positive property but still does not cure its incomplete documented five-type form;
- application/domain enforcement remains allowed where justified.

**Risk:** A preference needs disciplined application so it does not silently become a requirement or an automatic candidate winner.

### Q2-RI-O3 — DB-enforced referential integrity is NEITHER requirement nor preference

**Rule:** Enforcement location is representation-neutral. A candidate is evaluated only on whether it satisfies the required semantic/integrity outcome; DB constraints, application/domain validation, durable resolver rules, and other explicit mechanisms receive no architectural preference solely because of enforcement location.

**Consequences:**

- N1 vs N3 must be compared using other established criteria rather than DB-native enforcement;
- a DB FK remains an implementation/engineering advantage where useful but carries no architecture-level weight by itself;
- GC-002 Alternative B receives no preference merely for composite FK enforcement.

**Risk:** This deliberately gives up the database as an architecture-preferred correctness boundary even where it could cheaply prevent invalid references.

### Q2-RI-O4 — Context-dependent / per-subject-type weighting

**Rule:** DB-enforced RI is required or preferred only for some subject types or representation paths, while other subject types may rely on different enforcement mechanisms.

**Evaluation:** POSSIBLE BUT REQUIRES ADDITIONAL RULES.

This option could match the structural asymmetry of the five subjects, but it does not answer Q2-RI without defining which cases receive which weight and why. Selecting O4 therefore requires a further bounded rule rather than an implicit implementation-by-implementation choice.

## 5. What Q2-RI does not decide

Q2-RI does not decide:

- N1–N5 selection;
- `subject_type + subject_id` or any other concrete fields;
- FK column layouts or composite keys;
- CHECK constraints or exclusivity rules;
- FK delete action / cascade / restrict / set-null behavior;
- subject retention or legal erasure;
- runtime resolver design;
- migration design;
- actor attribution / ActorContext;
- Q2-ST subject-type ranging rule;
- GC-002 Alternative B approval;
- WP19 implementation.

## 6. Decision effect

Once Q2-RI is explicitly accepted by the Project Owner, it becomes a valid comparison input for the final N1–N5 re-application.

Until then:

**Q2-RI OPEN — N1 VS N3 UNDETERMINED — NO REPRESENTATION RECOMMENDATION AUTHORIZED.**
