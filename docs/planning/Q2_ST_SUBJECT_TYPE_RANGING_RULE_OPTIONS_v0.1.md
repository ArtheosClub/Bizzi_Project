# WP19 / Q2-ST Subject-Type Ranging Rule Options v0.1

**Status:** Draft — options/evaluation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — rule determining the admissible AuditRecord subject-type discriminator vocabulary  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures Q2-ST; it does not decide it.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Bounded question

**What architecture-level rule determines the admissible durable AuditRecord subject-type discriminator vocabulary and its mapping to persisted subject identities?**

Q2-ST must be decision-sufficient under the approved framework: if multiple options can satisfy inherited authority, the artifact must expose enough common comparison dimensions to explain a rational Project Owner choice.

Q2-ST does not itself authorize `AgentDefinition` as a sixth current subject type and does not silently expand the current D1/D5 scope.

## 2. Existing authority and the mismatch Q2-ST must explain

Accepted D1 fixes the current discriminator vocabulary to:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

Accepted D5 makes those five the current Q2 acceptance scope and requires separate explicit architecture authority for any future auditable subject type.

The current five are **not** a direct projection of the six domain-owning concepts used in ADW-01/D09/D10:

- `Workspace` is the D01 primary boundary, not one of the six;
- `EnterpriseObject` directly matches one domain-owning concept;
- `User` is persisted identity, while the domain concept is `Actor`;
- `WorkspaceMembership` is a concrete persisted association entity, not one of the six;
- `Task` is a persisted Work Item specialization, not the generic `Work Item` concept.

Therefore any option claiming to derive the vocabulary from domain concepts must explicitly reconcile this already-accepted D1 vocabulary rather than treating the mismatch as incidental.

## 3. ADR-0015 test surface: two persistence forms, not one

ADR-0015 establishes standalone persistence as the MVP default for D02 EnterpriseObject specializations, but it expressly permits a separately approved deviation to:

- **Option A:** an `enterprise_objects` base row plus a specialization row whose PK is also an FK to the base row; or
- **Option B:** standalone specialization persistence with no corresponding `enterprise_objects` row.

`AgentDefinition` currently uses the standalone default. ADR-0015 also describes reversibility from standalone to Option A as a real data migration that creates corresponding `enterprise_objects` rows for existing specialization identities.

A valid Q2-ST rule must therefore define how audited-subject identity behaves for both A and B and across an explicitly authorized A ↔ B evolution. It may not reason only from the current standalone case.

## 4. Inherited constraints

Any Q2-ST answer must preserve:

- D1: subject type is explicit and durable;
- D2: context does not substitute for subject identity;
- D3: committed historical identity survives later lifecycle/persistence changes;
- D4: subject identity is stable and independently resolvable;
- D5: current five remain the present scope; future auditable subject expansion requires separate explicit architecture authority;
- accepted Q2-RI: DB-RI comparative credit is evaluated under the subject-type rule then in force and attaches to concrete realizations, not candidate classes;
- accepted-record / ADR lifecycle rules: accepted authority is not silently rewritten in place.

## 5. Common comparison dimensions

All options are compared on the same six dimensions.

### ST-C1 — Compatibility with accepted D1 vocabulary
Can the rule explain the existing five D1 values without silently amending D1 or inventing an undefined source set?

### ST-C2 — Self-execution
Does the rule determine the treatment of a newly auditable specialization/entity from already-known facts, or does it require a new mapping decision case by case?

### ST-C3 — Preservation of the D5 authority gate
Can the rule expand the real audited-subject universe without adding a discriminator value? If so, does it require equivalent explicit authority for that expansion?

### ST-C4 — Historical stability under D3/D4
If a committed AuditRecord depends on a mapping from logical kind to persisted identity form, can later mapping or persistence evolution change interpretation of the committed record? What immutable/versioned contract is required?

### ST-C5 — Reopen-trigger complexity
What concrete future events must force architecture review before AuditRecord use with a new or changed subject identity form?

### ST-C6 — Effect on accepted Q2-RI application
How does the ranging/mapping rule affect availability of ordinary per-kind DB FK enforcement in concrete BR1–BR5-style realizations? Q2-ST does not choose based on RI alone, but it must expose the effect.

## 6. Options

### Q2-ST-O1 — Domain-concept-derived ranging

**Rule:** AuditRecord discriminator kinds are derived from an approved domain-subject concept set; persisted entities/specializations map to the applicable domain kind and do not create discriminator kinds merely because they have separate tables.

**Current readiness: NOT READY.**

The present formulation cannot be accepted without an additional authority step because the accepted D1 vocabulary is not derivable from the six domain-owning concepts as currently defined. A strict projection would not reproduce `Workspace`, `User`, `WorkspaceMembership`, or `Task` as accepted D1 values.

For O1 to become viable, architecture would first have to do one of two things explicitly:

1. amend/reconcile D1 through separate authority so that its vocabulary follows the chosen domain set; or
2. define a different approved “domain subject concept” set that actually generates the current five values.

Until then, O1 is not a complete rule.

**ADR-0015 implication:** a D02 specialization would normally range under `EnterpriseObject`, but standalone persistence would still require a durable specialization-resolution contract. Option A can resolve through the base `enterprise_objects` identity; Option B cannot assume such a row exists.

**ST-C2:** comparatively self-executing once the source domain set is defined.

**ST-C3:** D5 gate generally holds because a new persisted table does not itself create a new kind; however any newly auditable concept outside the approved source set still needs explicit authority.

**ST-C4:** the durable resolution contract for a domain kind spanning heterogeneous persisted forms must be historically stable/versioned across A ↔ B changes.

**ST-C5:** trigger complexity centers on persistence-form changes that make an existing domain kind no longer durably resolvable under its accepted contract.

**ST-C6:** one logical kind mapping to multiple physical forms can reduce availability of a simple ordinary FK from one subject slot to one table.

### Q2-ST-O2 — Persisted-entity identity as the default ranging rule

**Rule:** An auditable persisted entity kind is, by default, represented by its own explicit AuditRecord subject kind. Reusing an existing subject kind for a different persisted identity form is **not part of O2 by default** and requires a separate explicit mapping exception under architecture authority.

This makes O2 and O3 distinct: O2 is **one persisted auditable identity kind → one subject kind by default**, with explicit exceptions; O3 is **no derivation default; every permitted mapping is architecture-defined**.

**ADR-0015 Option A rule:** where a specialization has an `enterprise_objects` base row and the specialization PK is the same identity, the audited persisted identity may be represented by the existing `EnterpriseObject` subject kind **only if the accepted AuditRecord contract treats the base row identity as the canonical audited subject identity**. The existence of a specialization row does not automatically create a second subject kind for the same canonical identity.

**ADR-0015 Option B rule:** a standalone auditable specialization has a distinct persisted identity form. Under O2 default it therefore requires separate explicit architecture authority for its own subject kind before AuditRecord use, unless a separately approved mapping exception explicitly maps that standalone identity into an existing kind.

**D5 guard:** both adding a new subject kind **and approving an exception that maps a previously unauditable/new persisted identity form into an existing subject kind** require separate explicit architecture authority. Exception mapping cannot be used to bypass D5's control over expansion of the audited-subject universe.

**Historical stability:** if an identity moves between standalone and base-row forms, committed AuditRecords must continue to resolve according to the canonical identity contract in force when they were committed. A migration may not silently reinterpret old records.

**ST-C1:** reproduces the current D1 vocabulary most naturally because the current list is largely persistence-identity-oriented rather than a pure domain taxonomy.

**ST-C2:** self-executing at the default level: a new auditable persisted entity kind defaults to requiring its own separately authorized subject kind. Mapping exceptions remain explicit decisions.

**ST-C3:** D5 gate is preserved by the explicit rule above for both new kinds and mapping exceptions.

**ST-C4:** comparatively simpler where one subject kind maps to one canonical persisted identity; A ↔ B evolution still requires explicit preservation of canonical historical identity.

**ST-C5:** primary trigger: a new auditable persisted entity identity kind, or a proposed change that would cause an existing subject kind to map to a materially different persisted identity form.

**ST-C6:** one-kind/one-canonical-target mappings preserve the best opportunity for ordinary per-kind FK enforcement in realizations such as BR3; approved exceptions may reduce that opportunity and must be re-evaluated under Q2-RI.

### Q2-ST-O3 — Explicit architecture-controlled mapping

**Rule:** The discriminator vocabulary is an explicit architecture-controlled logical subject-kind set. Every permitted mapping from a subject kind to one or more persisted identity forms is established by explicit architecture authority; neither domain taxonomy nor persisted-table identity supplies a default.

**Mandatory D5-equivalent guard:** adding a new permitted persisted identity form to an existing subject kind expands the audited-subject universe and therefore requires separate explicit architecture authority just as adding a new subject kind does. Mapping expansion cannot bypass D5.

**Mandatory D3/D4 stability rule:** a committed AuditRecord must not depend on a mutable unversioned mapping whose later change could alter historical resolution. An accepted O3 design must therefore ensure either:

1. the mapping applicable to a committed reference is immutable for the lifetime of that historical record; or
2. the committed AuditRecord durably binds enough mapping/version/identity-form information to preserve the exact historical interpretation under which it was written.

The choice between those two mechanisms is itself a required part of an eventual O3 authority; it is not deferred to implementation.

**ADR-0015 implication:** architecture may map a standalone D02 specialization into `EnterpriseObject`, or authorize a specialization-specific kind, but each such mapping is an explicit authority act. A later A ↔ B migration is also a mapping-change event and must preserve committed historical interpretation.

**ST-C1:** compatible with the current D1 vocabulary by construction because the set is declared rather than derived.

**ST-C2:** not self-executing for new persisted specializations; each new mapping/form normally requires a case-specific architecture decision.

**ST-C3:** preserved only because of the mandatory mapping-expansion guard above.

**ST-C4:** highest explicit governance burden because mapping identity/version must remain historically stable across future evolution.

**ST-C5:** two trigger classes are required: (a) a new auditable persisted identity; and (b) any change to permitted forms or mapping semantics for an existing kind, including authorized A ↔ B migration.

**ST-C6:** one-to-many mappings can reduce ordinary per-kind FK availability; therefore each accepted mapping change may require bounded Q2-RI re-application to affected concrete realization(s).

### Q2-ST-O4 — Implementation-defined ranging

**Rule:** implementation may add/reuse subject kinds as convenient so long as the persisted representation can encode them.

**Evaluation:** conflicts with D5 §2.2 and existing architecture-authority boundaries; **recommended for rejection**, not rejected by this non-authoritative planning artifact.

## 7. Common comparison matrix

| Dimension | O1 Domain-derived | O2 Persisted-entity default | O3 Explicit mapping |
|---|---|---|---|
| ST-C1 D1 vocabulary compatibility | **Not currently sufficient**; 4/5 accepted names are not direct domain-owning concepts | **Strongest fit** to current accepted values | Compatible by declaration |
| ST-C2 Self-execution | High once source domain set is fixed | High default; exceptions explicit | Low; per-case mapping authority |
| ST-C3 D5 gate | Generally preserved | Preserved with new-kind + exception-mapping guard | Preserved only with explicit mapping-expansion guard |
| ST-C4 Historical stability | Mapping/resolver stability needed across physical forms | Simpler one-kind/one-canonical-identity default; evolution still governed | Highest mapping/version stability burden |
| ST-C5 Reopen trigger | Persistence-form / resolver-contract break | New auditable identity or material canonical-target change | New identity **and** any permitted-form/mapping change |
| ST-C6 Q2-RI effect | Multi-form domain kinds can reduce direct per-kind FK availability | Best preserves ordinary per-kind FK opportunity by default | One-to-many mappings can reduce RI credit availability |

This matrix is comparative analysis only. It does not itself select O1/O2/O3.

## 8. Reopen-trigger recording location

ADR-0015 is Accepted and immutable under `docs/adr/README.md`; its existing R7/R8/R9/R11 reopen trigger must not be edited in place merely to add AuditRecord semantics.

The AuditRecord-specific reopen trigger derived from accepted Q2-ST should therefore be recorded in the eventual **ADW-07 Q2-ST authority (or a separate ADW-07 authority explicitly referenced by it)**, citing ADR-0015 without modifying ADR-0015.

A new superseding ADR is not required merely to add an AuditRecord governance trigger unless the new authority actually changes ADR-0015's standalone-persistence decision.

## 9. Required post-Q2-ST re-check

Accepted Q2-RI intentionally applies under the subject-type rule then in force. Therefore Q2-ST can change the RI profile of BR1–BR5 even though Q2-RI does not favor a Q2-ST option.

After Q2-ST acceptance and before final Q2 representation authority:

1. re-check each surviving bounded realization against the accepted ranging/mapping rule;
2. re-apply Q2-RI where target mapping changes DB-FK availability;
3. record any changed C1/C2/C4/C5 burden;
4. do not select a representation merely because one realization gains or loses RI credit.

## 10. Current readiness assessment

- **O1:** NOT READY without prior/companion resolution of its conflict with the accepted D1 vocabulary.
- **O2:** BEST-CURRENTLY-SPECIFIED BASELINE, but still a proposal; no Project Owner acceptance yet.
- **O3:** structurally viable only with the D5-equivalent mapping-expansion guard and mandatory historical mapping-stability mechanism stated above; carries higher recurring governance cost.
- **O4:** conflicts with D5; recommended for rejection.

This readiness assessment is analysis, not authority and not a final recommendation record.

## 11. Decision gate

Q2-ST remains **OPEN**.

Current five D1 values remain authoritative. `AgentDefinition` is neither declared a sixth subject kind nor automatically mapped into `EnterpriseObject`. No AuditRecord-specific ADR-0015 reopen trigger has yet been approved. Final Q2 persisted representation remains OPEN, and WP19 remains BLOCKED / UNAUTHORIZED.
