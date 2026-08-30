# WP19 / Q2-ST Impact on BR1–BR5 v0.1

**Status:** Draft — comparative evaluation only  
**Date:** 2026-08-30  
**Subject:** Effect of Q2-ST-O1/O2/O3 on bounded candidate realizations and accepted Q2-RI  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact does not decide Q2-ST or final Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Purpose

The prior bounded realization pass evaluated BR1–BR5 under the current five D1 kinds while Q2-ST remained open. Accepted Q2-RI states that RI credit is applied under the subject-type rule then in force. This artifact therefore tests how each live Q2-ST option would change the bounded realizations and their comparative RI profile.

This is a sensitivity analysis, not a candidate-selection pass.

## 2. Baseline carried forward

Before Q2-ST:

- BR1/N1 typed polymorphic: D1–D5 conforming; no DB-RI credit.
- BR2/N2 composite family: incomplete for the current five types; local RI credit only.
- BR3/N3 per-type relations: D1–D5 conforming; positive DB-RI credit for current direct per-type FKs; separate exclusivity burden.
- BR4/N4 typed opaque: conforming only with durable resolver contract; no RI credit.
- BR5/N5 dedicated content identity: conforming only with dedicated stable content contract; no RI credit.

No final representation was selected.

## 3. O1 impact — domain-concept-derived ranging

### Readiness limitation

O1 cannot be treated as a valid controlling rule yet because it does not reproduce four of the five accepted D1 values without additional authority. Therefore the following is conditional sensitivity analysis only.

### BR1 / N1

**Impact:** semantic burden increases.

A typed polymorphic reference could naturally carry a domain-level kind plus identifier, but `EnterpriseObject` would have to resolve both base-row and standalone specialization identities. That makes durable type-dispatch/mapping semantics more complex than the current five-table BR1 contract.

**Q2-RI:** remains no direct ordinary multi-target FK credit for domain kinds spanning multiple physical forms.

### BR2 / N2

**Impact:** worsens for domain kinds with heterogeneous physical forms.

Composite-FK semantics become harder to apply when one logical domain kind resolves to multiple table shapes. Current incompleteness is not cured.

**Q2-RI:** local only; likely reduced wherever the logical kind is not bound to one canonical target table.

### BR3 / N3

**Impact:** the original “one slot per current D1 kind → one target table” assumption no longer holds cleanly.

A slot such as `EnterpriseObject` could need to resolve both ordinary `enterprise_objects` rows and standalone D02 specialization rows. A single ordinary FK from that slot to one table would no longer enforce the full domain-kind mapping.

**Q2-RI:** positive credit for BR3 would be reduced for any kind mapped to more than one physical identity form unless additional justified structure is introduced. Q2-RI does not authorize such structure merely to recover credit.

### BR4 / N4

**Impact:** comparatively natural fit, but resolver governance burden increases.

Opaque typed keys can hide heterogeneous physical forms behind a durable resolver, but that resolver must remain historically stable/versioned.

**Q2-RI:** none unless a concrete DB-native target structure is separately justified.

### BR5 / N5

**Impact:** content contract can encode domain kind plus durable identity-form information, but stable interpretation/versioning burden increases.

**Q2-RI:** none in the bounded form.

### O1 net effect

O1 tends to move complexity from discriminator vocabulary into durable cross-form resolution and reduces ordinary per-kind FK availability for BR3-like designs. But O1 is not decision-ready until its D1 vocabulary conflict is separately resolved.

## 4. O2 impact — persisted-entity identity default

### BR1 / N1

**Impact:** remains straightforward for the current five kinds.

Each current auditable persisted identity kind has its own explicit subject kind. A future standalone auditable specialization would default to requiring its own separately authorized subject kind; Option A specialization sharing canonical base-row identity can remain under `EnterpriseObject` if that base identity is the accepted audited subject identity.

**Q2-RI:** BR1 still receives no ordinary multi-target FK credit. O2 does not force auxiliary registry structure.

### BR2 / N2

**Impact:** current structural asymmetry remains; O2 does not solve `Workspace`/`User` composite-shape mismatch.

**Q2-RI:** local credit remains where concrete composite relations apply.

### BR3 / N3

**Impact:** strongest preservation of the current bounded realization.

Under the default one subject kind → one canonical persisted identity target, each subject-specific slot can retain an ordinary FK to its target table. A newly authorized standalone specialization would normally require a new subject kind and therefore a new subject-specific relation/slot if BR3 remains the chosen representation. D5 permits that schema evolution and forbids extensibility convenience alone from ranking the representation.

**Q2-RI:** current positive RI credit remains valid for the five present kinds. A separately approved mapping exception that makes one kind span multiple physical forms would require bounded re-evaluation and could reduce credit for that kind.

### BR4 / N4

**Impact:** still requires explicit durable resolver semantics, but one-kind/one-target default simplifies the resolver relative to O1/O3 multi-form mappings.

**Q2-RI:** none in bounded form.

### BR5 / N5

**Impact:** dedicated content identity remains straightforward: explicit kind + id; future new persisted kinds require separate authorized discriminator values unless an explicit exception is approved.

**Q2-RI:** none in bounded form.

### O2 net effect

O2 preserves the current BR comparison most closely. It does not choose BR3, but it preserves BR3's existing per-realization RI credit without manufacturing a class-level preference. Its recurring cost is explicit architecture authority whenever a new auditable persisted entity kind is added, plus explicit exception authority where reuse of an existing kind is desired.

## 5. O3 impact — explicit architecture-controlled mapping

### BR1 / N1

**Impact:** viable, but mapping/version contract becomes part of correctness.

The same logical type+id reference may resolve through different permitted identity forms. BR1 therefore needs enough durable mapping/version semantics to preserve historical interpretation.

**Q2-RI:** generally none unless a particular mapping exposes a single ordinary FK-compatible canonical target.

### BR2 / N2

**Impact:** depends strongly on each mapping; one-to-many mappings make a universal composite target harder.

**Q2-RI:** only mapping-local credit.

### BR3 / N3

**Impact:** material.

The current BR3 assumes each subject-specific slot maps to one target table. Under O3, a subject kind may have multiple permitted persisted identity forms. If `EnterpriseObject` maps both base rows and standalone specializations, one `EnterpriseObject` slot can no longer enforce all permitted targets with one ordinary FK.

Possible responses would include multiple physical slots within one logical kind, a registry/base target, generated indirection, or application-level dispatch. None is authorized merely by O3 and each would require bounded evaluation/abstraction justification.

**Q2-RI:** current positive credit can decrease for multi-form kinds. The accepted preference therefore changes in effect after mapping changes, exactly as Q2-RI allows.

### BR4 / N4

**Impact:** natural representational fit but highest resolver/mapping-governance burden.

Opaque keys can accommodate multiple physical identity forms, but O3 requires immutable/version-bound historical mapping semantics.

**Q2-RI:** none in bounded form.

### BR5 / N5

**Impact:** can durably record logical kind plus identity-form/version information inside the dedicated subject object, but content-contract complexity increases.

**Q2-RI:** none in bounded form.

### O3 net effect

O3 is the most flexible mapping rule but also the most expensive governance/evolution rule. It can materially erode BR3's current RI advantage for logical kinds spanning multiple persisted forms, and it requires two trigger classes: new identity forms and changes to existing mappings.

## 6. Cross-option matrix

| Effect | O1 | O2 | O3 |
|---|---|---|---|
| BR1 resolver complexity | High for multi-form domain kinds | Lowest/default one-kind-one-target | High + mapping/version governance |
| BR2 completeness | Not improved | Not improved | Mapping-dependent; not inherently improved |
| BR3 current FK profile | Reduced where domain kind spans forms | Preserved by default | Preserved only for one-target mappings; reduced for one-to-many |
| BR4 resolver fit | Good, high governance | Good, simpler default | Good, highest governance |
| BR5 content-contract burden | Higher identity-form semantics | Lowest of three | Higher mapping/version semantics |
| Re-evaluation frequency | Persistence-form changes | New auditable kinds / mapping exceptions | New identities + every mapping/form change |

## 7. Decision-sufficiency result

The sensitivity pass supports these readiness conclusions:

- **O1 remains not ready** because its incompatibility with accepted D1 is prior to candidate comparison.
- **O2 is the narrowest rule that preserves current D1 vocabulary, D5 gate, and the already-evaluated BR1–BR5 comparison with the fewest additional mapping semantics.** This is a comparative finding, not acceptance.
- **O3 is viable only with the mandatory D5-equivalent mapping-expansion guard and historical mapping/version rule; it has a demonstrably higher recurring governance and re-evaluation burden.**

No option is accepted by this artifact.

## 8. Next gate

The analysis is now sufficient to prepare a **Q2-ST recommendation** for Project Owner review. That recommendation must still distinguish recommendation from authority and must include the AuditRecord-specific reopen-trigger consequence of the recommended option.

Until explicit Project Owner acceptance:

- Q2-ST remains OPEN;
- BR1–BR5 conclusions remain provisional under the current five-kind rule;
- final Q2 representation decision remains unauthorized;
- WP19 remains BLOCKED / UNAUTHORIZED.
