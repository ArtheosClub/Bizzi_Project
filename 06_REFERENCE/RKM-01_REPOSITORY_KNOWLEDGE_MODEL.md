# RKM-01 — Repository Knowledge Model

## 00. Document Control

| Field | Value |
|---|---|
| Document ID | RKM-01 |
| Title | Repository Knowledge Model |
| Version | 1.0 |
| Status | **DRAFT — Design Document. Not yet approved for generation.** |
| Artifact Type | Normative — Repository Organization (not a constitutional document; see §07) |
| Repository | ArtheosClub/Bizzi_Project |
| Owner | Project Owner |
| Related Documents | `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0001_MVP_FIRST.md`; `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`; `01_GOVERNANCE/EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md`; `00_CONSTITUTION/AI-01_AUTHORITATIVE_INTERPRETATION.md` |

This document performs no repository change. Nothing is moved, renamed,
or restructured by its creation. It designs the semantic model from
which repository organization may later be generated, per §11 and the
readiness gate in §12.

---

## 01. Purpose

RKM-01 defines the single semantic source of truth for how the Bizzi
Platform repository is organized. It exists because filesystem placement
has, until now, been an artifact of when and where something was
written, not a designed representation of what it means. RKM-01 gives
the repository a knowledge model independent of current folder layout,
so that folder layout can later be treated as a derived, regenerable
output rather than the thing itself.

RKM-01 does not govern architecture, engineering, or constitutional
authority. Those remain governed exclusively by Decision 0001,
DECISION_0002, ABR-01, EGC-01, and AI-01. RKM-01 governs only how
repository *artifacts* — including those constitutional documents — are
classified, related, and (later) physically represented.

---

## 02. Design Philosophy

Knowledge precedes information. Information precedes documents.
Documents precede folders. Folders never define meaning; meaning defines
folders.

Concretely: an artifact's meaning is determined by what it *is*
(its knowledge domain, layer, owner, and authority source), not by where
it currently sits in the filesystem. Where two disagree, the filesystem
is wrong, not the model — subject to the readiness gate in §12 before
that disagreement is ever corrected by moving anything.

---

## 03. Core Principles

1. Knowledge is primary. Filesystem is secondary.
2. Every repository artifact belongs to exactly one semantic domain.
3. Every artifact has a semantic owner, a constitutional owner (if any), a lifecycle, an authority source, a canonical (logical) location, and a physical (derived) location.
4. Repository organization is always generated from semantic organization, never the reverse.
5. Changing folders never requires changing repository semantics.
6. Any future repository technology (Git, wiki, knowledge graph, database, AI memory) must be capable of representing the same Repository Knowledge Model without altering it.

---

## 04. Repository Knowledge Model — Derivation Chain

```text
Repository Knowledge Model   (this document — normative)
        |
        v
Repository Semantic Domains  (§05 — derived, normative within RKM-01)
        |
        v
Repository Structure         (generated — not yet generated, see §10)
        |
        v
Repository Navigation        (generated)
        |
        v
Migration Plan                (generated, gated by §12)
        |
        v
Filesystem                    (derived, last, and only after §12 is satisfied)
```

Only this document is normative. Every layer below it is derivative and
regenerable. A disagreement between a lower layer and this document is,
by definition, a defect in the lower layer.

---

## 05. Semantic Domains

Domains answer "what is this artifact about," independent of authority
level. Nine domains are sufficient to classify every artifact currently
in the repository:

| Domain | Answers | Current examples |
|---|---|---|
| **Constitutional** | What governs the governance itself | Decision 0001, DECISION_0002, ABR-01, EGC-01, AI-01 |
| **Architectural** | What the MVP backend *is*, at the domain-semantics level | `ARCHITECTURE_SPECIFICATION.md`, `DOMAIN_FOUNDATION.md`, D01–D10, the Decision Register |
| **Engineering Process** | How engineering activity is constitutionally governed | EGC-01 (also Constitutional; see §07 on dual-typed artifacts) |
| **Implementation Pattern** | How approved architecture is technically realized | `docs/adr/*` |
| **Planning & Sequencing** | What gets built, in what order, at what scope | `docs/planning/*`, `50_IMPLEMENTATION/*` |
| **Illustrative** | How the above is diagrammed for comprehension | `docs/c4/*` |
| **Codebase** | The running system itself | `backend/*` |
| **Platform Vision** | The separate, broader "Art of Business" system | `00_VISION`, `00_RELEASE`, `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `01_GOVERNANCE/AUTHORITY_MATRIX.md`, `02_CAPABILITY_MAP` … `33_BACKEND_SOURCE_CODE_IMPLEMENTATION` |
| **Reference** | Material that describes the repository to itself | This document; future glossaries, indices, catalogs |

Domain assignment is orthogonal to authority. `EGC-01` is both
Constitutional (it is a constitutional document) and Engineering Process
(its subject matter is engineering). Domain describes subject matter;
Layer (§06) describes authority altitude.

---

## 06. Layer Model

Layers answer "how much authority does this artifact carry, and over
what." This reuses, and does not redefine, the tier structure already
established by DECISION_0002 §1 — RKM-01 adds only a Reference layer,
which DECISION_0002 did not need because it predates this document's
existence.

| Layer | Corresponds to (DECISION_0002 Tier) | Authoritative for |
|---|---|---|
| Constitutional Layer | Tier 0–1 | What may be decided at all, and by whom |
| Architectural Layer | Tier 2 | Domain semantics |
| Implementation-Pattern Layer | Tier 3 | Technology and implementation-pattern decisions |
| Planning Layer | Tier 4 | Sequencing and MVP scope |
| Illustrative Layer | Tier 5 | Diagrammatic explanation only |
| Codebase Layer | Tier 6 | Nothing architectural; conforms to all above |
| Platform-Vision Layer | Unranked (per DECISION_0002 §1) | The separate Art of Business system; source vocabulary only |
| Reference Layer | Unranked (new — introduced by RKM-01) | Describes the repository; authoritative for nothing outside itself |

The Reference Layer is deliberately non-authoritative: a catalog, index,
or navigation aid that is wrong is a defect to be regenerated, never a
justification for treating the catalog as a competing source of truth.

---

## 07. Artifact Classification

### 07.1 Classification schema

Every artifact is classified against ten fields:

| Field | Meaning |
|---|---|
| Knowledge Domain | One of §05's nine domains |
| Layer | One of §06's eight layers |
| Owner | The person/role accountable for the artifact's content |
| Authority Source | The document (if any) from which the artifact derives legitimacy |
| Lifecycle | Draft / Active / Superseded / Historical |
| Canonical Representation | The artifact's logical identity (Document ID, e.g., `ABR-01`), independent of path |
| Relationships | Other artifacts it derives from, is derived by, or cross-references |
| Dependencies | Artifacts whose state it presupposes |
| Visibility | Constitutional / Engineering / Reference-only |
| Generation Status | Hand-authored / Generated / Not-yet-generated |

### 07.2 Worked examples (classification only — nothing moved)

| Artifact | Domain | Layer | Owner | Authority Source | Lifecycle |
|---|---|---|---|---|---|
| Decision 0001 | Constitutional | Constitutional Layer | Project Owner (per AI-01 Interpretation 3) | None (foundational) | Active |
| ABR-01 | Constitutional | Constitutional Layer | Project Owner | Decision 0001, DECISION_0002 | Active |
| EGC-01 | Constitutional + Engineering Process | Constitutional Layer | Project Owner | Decision 0001, DECISION_0002, ABR-01 | Active |
| An approved ADR (e.g., ADR-0004) | Implementation Pattern | Implementation-Pattern Layer | Engineering | Architectural Layer (coordinates with, not subordinate to) | Active |
| A `docs/c4/*` diagram | Illustrative | Illustrative Layer | Engineering | Architectural + Planning Layers | Active |
| `backend/app/*` | Codebase | Codebase Layer | Engineering | All layers above it | Active |
| `01_GOVERNANCE/GOVERNANCE_MODEL.md` | Platform Vision | Platform-Vision Layer | Art of Business governance (AG-numbered roles) | None relative to the MVP build | Active, separate system |
| This document (RKM-01) | Reference | Reference Layer | Project Owner | None (self-describing) | Draft |

### 07.3 Artifact Types

Distinguish six types, cutting across domains and layers:

- **Normative** — binding on what it governs (Constitutional documents; RKM-01 itself is normative for repository organization only, never for architecture, engineering, or constitutional matters).
- **Interpretive** — clarifies normative text without amending it (AI-01).
- **Generated** — produced from a normative source, never hand-authored once generation exists (future Repository Structure, Navigation, Index, Catalog).
- **Operational** — runs or supports the system (`backend/*`, CI configuration).
- **Historical** — retained as evidentiary record only (superseded ADR-0002, `docs/planning/WORK_PACKAGES.md`).
- **Reference** — describes the repository to readers or tooling without governing anything (`docs/c4/*`, future glossaries, this document).

---

## 08. Ownership Model

| Domain | Semantic Owner | Constitutional Owner (if any) |
|---|---|---|
| Constitutional | Project Owner | Project Owner (self-owning) |
| Architectural | Project Owner, exercised through Architecture Governance | Decision 0001, DECISION_0002, ABR-01 |
| Engineering Process | Project Owner, exercised through EGC-01 | EGC-01 |
| Implementation Pattern | Engineering | Coordinates with Architectural domain, per DECISION_0002 Tier 3 |
| Planning & Sequencing | Engineering / Project planning | Derives vocabulary from Architectural domain |
| Illustrative | Engineering | None — illustration only |
| Codebase | Engineering | None — conforms to all above |
| Platform Vision | Art of Business governance (AG-numbered roles, per `GOVERNANCE_MODEL.md`) | Not the MVP Project Owner, except through vocabulary adaptation |
| Reference | Project Owner | None — non-authoritative by design (§06) |

An artifact's semantic owner is accountable for its content. Its
constitutional owner, where one exists, is the document that must
approve a change to its meaning.

---

## 09. Knowledge Relationships

Three relationship types connect artifacts, independent of physical
location:

- **Derives-from** — an artifact's legitimacy traces to another (e.g., EGC-01 derives from ABR-01, Decision 0001, and DECISION_0002).
- **Illustrates** — a Reference or Illustrative-layer artifact represents a higher-layer artifact without adding authority (e.g., a C4 diagram illustrates `ARCHITECTURE_SPECIFICATION.md`).
- **Cross-references** — artifacts at the same or different layers point to each other for context without either deriving from the other (e.g., an ADR cross-referencing the risk register).

Relationships are recorded per-artifact (§07.1 "Relationships" field);
their aggregate forms the Cross-reference Map and Knowledge Graph
described in §10 — both generated, neither hand-maintained once
generation exists.

---

## 10. Generated Artifacts

The following are declared as artifacts to be generated from this model.
None currently exist in generated form; all are Generation Status:
**Not yet generated**, pending the tooling and readiness gate in §12.

| Generated artifact | Derived from |
|---|---|
| Repository Structure | §05 Semantic Domains + §06 Layer Model |
| Repository Navigation | Repository Structure |
| Repository Index | Full artifact classification (§07) |
| Migration Plan | Repository Structure vs. current filesystem, diffed |
| Filesystem Layout | Migration Plan, executed only after §12 is satisfied |
| Document Placement | Repository Structure |
| Cross-reference Map | §09 Knowledge Relationships, aggregated |
| Ownership Matrix | §08 Ownership Model, expanded per-artifact |
| Repository Catalog | Full artifact classification (§07), one row per artifact |
| Knowledge Graph | §09 Knowledge Relationships, as a graph structure |
| AI Context Model | Repository Catalog + Cross-reference Map |
| Future Search Model | Repository Catalog + Knowledge Graph |

---

## 11. Evolution Model

Repository evolution occurs by editing this model, not by editing the
filesystem directly. The intended sequence for any future repository
change is:

1. Propose the change as an edit to §05–§09 of this document (domain, layer, classification, ownership, or relationship).
2. Regenerate the artifacts in §10 from the updated model.
3. Diff the regenerated Repository Structure against the current filesystem to produce a Migration Plan.
4. Apply the Migration Plan only after it satisfies every criterion in §12.

Today, no generation tooling exists. Until it does, this model is
descriptive and normative-in-intent, but the filesystem remains
manually maintained. This document does not create, and does not
presuppose, generation tooling — it only specifies what that tooling
must produce, and from what.

---

## 12. Migration Readiness Criteria

No repository migration derived from this model may occur until all of
the following are objectively satisfied:

1. **RKM-01 is approved**, not merely drafted — this document's own
   Status (§00) must move from DRAFT to an approved state through
   whatever review the Project Owner designates for repository-design
   documents, before it authorizes generation of anything in §10.
2. **Complete classification coverage** — every existing repository
   artifact has been classified against §07.1's schema, with zero
   unclassified or ambiguously-classified artifacts remaining.
3. **A generated Migration Plan exists**, produced mechanically from the
   model (§11 step 3), not hand-authored ad hoc.
4. **No traceability loss** — the Migration Plan is verified to preserve
   every artifact's Canonical Representation (Document ID) and every
   existing cross-reference, either unchanged or via an explicit,
   verified redirect.
5. **No unauthorized constitutional path change** — any proposed path
   change to a Constitutional-domain artifact is checked against
   Decision 0001's Architecture Freeze and EGC-01's Engineering Change
   Policy (§06) before inclusion in the Migration Plan; a path change
   affecting a Constitutional-layer document requires the same
   Architecture Governance authorization EGC-01 §06 requires for any
   other change of that class.
6. **Explicit Project Owner authorization** for the specific Migration
   Plan being applied — approval of RKM-01 as a model does not itself
   authorize any one migration.
7. **A verification mechanism exists** (automated or manual) capable of
   confirming, after migration, that the resulting filesystem matches
   the generated Repository Structure exactly, with no orphaned or
   duplicated artifacts.

Until all seven are satisfied, this model remains design-only: it
classifies and relates artifacts logically without changing where any
of them physically live.
