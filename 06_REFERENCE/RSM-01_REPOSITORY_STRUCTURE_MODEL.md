# RSM-01 — Repository Structure Model

## 00. Document Control

| Field | Value |
|---|---|
| Document ID | RSM-01 |
| Title | Repository Structure Model |
| Version | 1.0 |
| Status | **DRAFT — Derived Design Document. Not yet approved for generation.** |
| Artifact Type | Generated (from RKM-01) — see RKM-01 §07.3 |
| Repository | ArtheosClub/Bizzi_Project |
| Owner | Project Owner |
| Derived from | `06_REFERENCE/RKM-01_REPOSITORY_KNOWLEDGE_MODEL.md` (also DRAFT — see §02) |
| Placement note | Placed beside RKM-01 because Repository Numbering (§07) is itself only proposed by this document, not yet generated; no canonical location exists for either file until numbering is approved. |

This document performs no repository change. Nothing is moved, renamed,
or restructured by its creation.

---

## 01. Purpose

RSM-01 transforms RKM-01's semantic model (Knowledge Domains, Layer
Model, Ownership Model) into a logical repository structure: root
domains, subdomains, canonical placement rules, and a numbering
proposal. It introduces no semantics RKM-01 did not already define. Every
structural element below cites the RKM-01 section it derives from.

---

## 02. Authority Chain

```text
Repository Knowledge Model (RKM-01)   — normative, DRAFT
        |
        v
Repository Structure Model (RSM-01)   — this document, generated, DRAFT
        |
        v
Repository Navigation                 — not yet generated
        |
        v
Repository Numbering                  — proposed in §07, not yet adopted
        |
        v
Migration Plan                        — not yet generated
        |
        v
Filesystem                            — unchanged
```

RSM-01 is itself only DRAFT, because RKM-01 is only DRAFT (RKM-01 §00,
§12 item 1). Nothing in this document may be treated as authoritative
over RKM-01, and RKM-01 remains unmodified by this document's existence.

---

## 03. Derivation Principles

1. No structural element exists without semantic origin (RKM-01 §05 or §06).
2. No semantic domain is merged, split, renamed, or created by this document.
3. Every structural decision is traceable to a specific RKM-01 section.
4. Numbering (§07) is proposed as a generation rule, not copied from the current filesystem (RKM-01 §01: "current repository layout is NOT authoritative").
5. Where RKM-01 does not decide a structural question, this document records the question as unresolved (see §11) rather than deciding it unilaterally.

---

## 04. Repository Structure

### 04.1 Root Domains

One root domain per RKM-01 §05 Knowledge Domain, with no merging or splitting:

| Root Domain | Originating Knowledge Domain (RKM-01 §05) | Originating Layer (RKM-01 §06) |
|---|---|---|
| Constitution | Constitutional | Constitutional Layer |
| Architecture | Architectural | Architectural Layer |
| Engineering | Engineering Process | (dual-typed with Constitutional, per RKM-01 §05) |
| Patterns | Implementation Pattern | Implementation-Pattern Layer |
| Planning | Planning & Sequencing | Planning Layer |
| Illustration | Illustrative | Illustrative Layer |
| Codebase | Codebase | Codebase Layer |
| Platform | Platform Vision | Platform-Vision Layer |
| Reference | Reference | Reference Layer |

### 04.2 Subdomains

Subdomains are derived only where RKM-01 §07.2's worked examples or §08
Ownership Model already imply an internal split. No subdomain is
invented beyond what RKM-01 supports:

| Root Domain | Subdomain | Origin |
|---|---|---|
| Constitution | Decisions (Decision 0001, DECISION_0002) | RKM-01 §07.2 worked examples |
| Constitution | Resolutions (ABR-01) | RKM-01 §07.2 |
| Constitution | Charters (EGC-01) | RKM-01 §07.2 |
| Constitution | Interpretations (AI-01) | RKM-01 §07.3 Artifact Types — Interpretive |
| Architecture | Foundation (domain-semantics groundwork) | RKM-01 §07.2 (`DOMAIN_FOUNDATION.md`-class artifacts) |
| Architecture | Domain Decisions (D01–D10, Decision Register) | RKM-01 §07.2 |
| Patterns | Accepted | RKM-01 §07.3 Artifact Types — Normative-for-implementation |
| Patterns | Superseded | RKM-01 §07.3 Artifact Types — Historical |
| Planning | Gates (sequencing packages) | RKM-01 §05 Planning & Sequencing |
| Reference | Models (RKM-01, RSM-01 themselves) | RKM-01 §07.3 Artifact Types — Reference |
| Reference | Generated (§10 artifacts, once produced) | RKM-01 §10 |

No subdomain is proposed for Platform, since RKM-01 §08 places its
ownership entirely outside the MVP Project Owner's structural authority
— Platform's internal subdomain structure belongs to that separate
system's own governance, not to RSM-01.

### 04.3 Canonical Placement Hierarchy

```text
Constitution/
    Decisions/
    Resolutions/
    Charters/
    Interpretations/
Architecture/
    Foundation/
    DomainDecisions/
Engineering/
Patterns/
    Accepted/
    Superseded/
Planning/
    Gates/
Illustration/
Codebase/
Platform/               (opaque to RSM-01; internal structure out of scope)
Reference/
    Models/
    Generated/
```

### 04.4 Indexes, Generated Directories, Reserved Namespaces

- **Indexes** — one index artifact per Root Domain (a Repository Index entry, RKM-01 §10), generated, not hand-authored.
- **Generated directories** — none exist yet. RKM-01 §10's twelve generated artifacts are the candidates; each would occupy `Reference/Generated/<artifact-name>` once produced.
- **Reserved namespaces** — `Reference/Generated/` is reserved in full for generated output; no hand-authored content may be placed there once generation exists, to preserve RKM-01 §06's rule that the Reference Layer carries no authority of its own.

### 04.5 Navigation Entry Points

One entry point per Root Domain (an index file at the domain's own
root), plus a single repository-level entry point that lists all nine
Root Domains. Both are Generated artifacts (RKM-01 §10: Repository
Navigation), not yet produced.

### 04.6 Structural Dependencies

- `Constitution/` has no structural dependency (RKM-01 §08: self-owning).
- `Architecture/` depends on `Constitution/` being resolvable first (authority derivation, RKM-01 §09 derives-from).
- `Engineering/` depends on `Constitution/` and `Architecture/`.
- `Patterns/`, `Planning/`, `Illustration/`, `Codebase/` each depend on `Architecture/` per RKM-01 §06's tier order.
- `Reference/` depends on all other Root Domains existing and being classified (it can only index what already has a canonical placement).
- `Platform/` has no dependency on, and no dependency from, any other Root Domain (RKM-01 §08: separate system).

---

## 05. Root Domain Model

Restates §04.1 as a single table with authority source, for direct
cross-reference against RKM-01 §06:

| Root Domain | Authority Source (RKM-01 §06 Layer → DECISION_0002 Tier) |
|---|---|
| Constitution | Constitutional Layer → Tier 0–1 |
| Architecture | Architectural Layer → Tier 2 |
| Engineering | Constitutional Layer (EGC-01 itself) + governs Tier-6-adjacent activity |
| Patterns | Implementation-Pattern Layer → Tier 3 |
| Planning | Planning Layer → Tier 4 |
| Illustration | Illustrative Layer → Tier 5 |
| Codebase | Codebase Layer → Tier 6 |
| Platform | Platform-Vision Layer → Unranked |
| Reference | Reference Layer → Unranked, non-authoritative |

---

## 06. Structural Hierarchy

Depth is capped at three levels (Root Domain / Subdomain / Artifact) for
every domain except Platform, whose internal depth is not RSM-01's to
define (§04.2). This is a structural convention proposed by RSM-01, not
a rule stated in RKM-01 — recorded as such rather than presented as
already-derived, per §03 rule 5.

---

## 07. Repository Numbering Model

RKM-01 does not specify a numbering scheme; RSM-01 proposes one, as a
generated artifact in its own right (RKM-01 §10 treats numbering as part
of Repository Structure).

- **Allocation policy** — each Root Domain receives one stable two-digit
  number, assigned once, at generation time, in the order the domains
  are first generated — not by any meaning encoded in the number itself
  (RKM-01 §02: "folders never define meaning").
- **Reserved ranges** — `00–09` reserved for Root Domains with
  Constitutional or Architectural authority sources (§05); `10–39`
  reserved for Engineering, Patterns, Planning, Illustration, and
  Codebase; `40–49` reserved for Reference; `50–99` reserved for
  Platform, kept numerically separate to make its non-authoritative,
  separate-system status visible at the filesystem level, not only in
  prose.
- **Expansion rules** — a new subdomain receives the next unused number
  within its Root Domain's reserved range; a Root Domain's range is
  never renumbered once assigned, even if it is later found to be
  under-provisioned — a new adjacent range is opened instead.
- **Future compatibility** — numbers are never reused after an artifact
  they identified is archived; an archived number's directory is
  retained as a redirect stub pointing to the artifact's new Canonical
  Representation (RKM-01 §07.1), not deleted.
- **Collision avoidance** — no two Root Domains may share a number; the
  Repository Catalog (RKM-01 §10) is the single authority checked before
  any number is allocated.
- **Number stability** — once generated and adopted, a number is
  immutable for the lifetime of the domain it identifies; renumbering
  is itself a change to this section of RSM-01, not a filesystem
  operation performed independently of it.

This model does not allocate any actual number to any actual domain in
this revision; it defines the policy by which future generation would
do so.

---

## 08. Namespace Analysis

Read-only observation of the current filesystem against RKM-01's
semantics. No resolution below is executed.

| Finding | Evidence | Semantic Domain Affected |
|---|---|---|
| **Duplicate root: `GOVERNANCE_MODEL.md`** | A 85-line root-level `GOVERNANCE_MODEL.md` and a 587-line `01_GOVERNANCE/GOVERNANCE_MODEL.md` exist under the identical filename with substantially different, non-superset content (different section structure, different agent lists, the root version partly in Russian). | Platform Vision |
| **Duplicate root: `CAPABILITY_MAP_v1.0.md`** | A 236-line root-level file and a 545-line `02_CAPABILITY_MAP/CAPABILITY_MAP.md` file, same pattern as above — shorter root copy, longer numbered-directory copy. | Platform Vision |
| **Namespace fragmentation: Playbooks** | 102 `PB0*.md` files exist loose at repository root; the canonical `06_PLAYBOOKS/` directory contains only `.gitkeep` — the directory that names itself as the playbook home holds none of them. | Platform Vision |
| **Namespace collision risk: `06_PLAYBOOKS` vs `06_REFERENCE`** | Two root directories currently share the `06_` number (`06_PLAYBOOKS`, and `06_REFERENCE`, created for RKM-01 and this document). Flagged previously at RKM-01's creation. | Reference / Platform Vision |
| **Temporary/historical artifacts at root (deleted)** | `TEST_WRITE.md` ("Repository Write Capability Test... Created for GitHub Capability Audit") and `CONNECTOR_TEST.md` ("GitHub Connector Test") were operational test artifacts, not specification content. Both were deleted under Repository Cleanup Operation RTC-01 after validation confirmed no operational dependency (README, index, workflow, script, or CI/CD) referenced either file — see the historical audit record below. | None — never classifiable into any RKM-01 domain; infrastructure test residue, now removed. |
| **Granularity difference, not a collision: `AGENT_REGISTRY.md` vs `04_AGENT_LIBRARY/`** | Root `AGENT_REGISTRY.md` is a single registry document; `04_AGENT_LIBRARY/` holds 23 individual per-agent files. Complementary, not duplicate — recorded here only because it was checked, not because it is a defect. | Platform Vision |
| **131 loose root-level `.md` files in total** | Includes `CORE_*.md` (14 files), milestone documents, `README.md`, `Vision.md`, `CLAUDE.md`, `PLAYBOOK_ROADMAP.md`, `PLAYBOOK_TEMPLATE.md`, `MASTER_INDEX_FULL.md`, in addition to the items above. Not all are collisions or legacy placements; several (`README.md`, `CLAUDE.md`) are conventionally root-level by nature and would remain so under most repository conventions. | Mixed — requires per-file classification (RKM-01 §07.1) before any recommendation, which RSM-01 does not perform in this revision. |

### Recommended resolutions (not executed)

- `GOVERNANCE_MODEL.md` and `CAPABILITY_MAP_v1.0.md`: resolve via the
  same two-commit pattern already established in this repository's
  constitutional history (verify divergence, do not choose a version
  unilaterally, get explicit direction, import-then-reconcile as
  separate commits) — this is a content decision, not a structural one,
  and is out of RSM-01's scope.
- Playbooks: either populate `06_PLAYBOOKS/` from the root `PB0*.md`
  files, or remove `06_PLAYBOOKS/` and record `Platform/` (RSM-01 §04)
  as the playbooks' actual home once Repository Numbering (§07) is
  adopted — a choice for the Migration Plan, not for this document.
- `06_PLAYBOOKS` vs `06_REFERENCE`: resolved automatically once
  Repository Numbering (§07) is adopted and both are renumbered into
  their correct ranges; no manual renumbering recommended before then.
- `TEST_WRITE.md` / `CONNECTOR_TEST.md`: deleted under Repository
  Cleanup Operation RTC-01 — see §08a for the historical audit record.

### §08a Historical Audit Record — Repository Cleanup Operation RTC-01

| Artifact | Disposition | Reason | Operation | Validation |
|---|---|---|---|---|
| `TEST_WRITE.md` | Deleted | Temporary repository write-capability verification artifact; no knowledge, operational, or historical value; no operational dependency found. | Repository Cleanup Operation RTC-01 | No Category A (operational) reference found; RSM-01 itself was the only Category B (documentary) reference, updated in this same commit. |
| `CONNECTOR_TEST.md` | Deleted | Temporary GitHub connector verification artifact; no knowledge, operational, or historical value; no operational dependency found. | Repository Cleanup Operation RTC-01 | Same as above. |

This record is retained per RTC-01's instruction to convert documentary
references into historical audit records rather than silently removing
them. The commit that performed this deletion and this update is
identifiable via `git log`/`git blame` on this file and on the two
removed paths; no SHA is embedded here to avoid a self-referential value
that would require amending this same commit to fill in.

---

## 09. Canonical Placement Rules

One canonical structural location per artifact class, per RKM-01 §03
principle 5 ("changing folders never requires changing repository
semantics") and principle 3 (every artifact has exactly one canonical
logical location):

| Artifact Class | Canonical Placement |
|---|---|
| Constitution (Decision 0001, DECISION_0002) | `Constitution/Decisions/` |
| Constitution (ABR-01) | `Constitution/Resolutions/` |
| Constitution (EGC-01) | `Constitution/Charters/` |
| Constitution (AI-01) | `Constitution/Interpretations/` |
| Governance | Architecture (ARCHITECTURE_SPECIFICATION.md, DOMAIN_FOUNDATION.md, D01–D10) | `Architecture/Foundation/` and `Architecture/DomainDecisions/` |
| Engineering | `Engineering/` |
| Patterns (accepted ADRs) | `Patterns/Accepted/` |
| Patterns (superseded ADRs) | `Patterns/Superseded/` |
| Playbooks | `Platform/` (internal structure not defined by RSM-01, §04.2) |
| Platform (Governance Model, Authority Matrix, Capability Map, Agent Library, etc.) | `Platform/` |
| Implementation (planning, work packages, gates) | `Planning/Gates/` |
| Reference (diagrams) | `Illustration/` |
| Historical (superseded ADR-0002, `WORK_PACKAGES.md`) | Retained inside the same Root Domain as the artifact they supersede, marked Historical (RKM-01 §07.3), never moved to a separate "Archive" root — archival is a Lifecycle state (RKM-01 §07.1), not a location. |
| Generated | `Reference/Generated/`, reserved namespace (§04.4) |
| Templates | `Reference/` (a Templates subdomain is not yet warranted by current volume; one loose `PLAYBOOK_TEMPLATE.md`-class file does not justify a dedicated subdomain per §03 rule 5's minimalism) |
| Indexes | `Reference/`, one per Root Domain (§04.5) |

---

## 10. Repository Mapping

Current root → generated structure. `Required Action` uses the allowed
action set only; none is executed.

| Current Root | Semantic Domain (RKM-01 §05) | Target Structural Domain (§04) | Required Action | Reason | Migration Dependency | Risk |
|---|---|---|---|---|---|---|
| `00_ARCHITECTURE/` | Architectural | `Architecture/` | MOVE | Domain name differs from target; content already correctly scoped | Repository Numbering (§07) adopted | Low — internal structure already matches RKM-01 |
| `00_CONSTITUTION/` | Constitutional | `Constitution/` | MOVE | Directory already semantically correct; only the number/name form differs | Repository Numbering (§07) adopted | Low |
| `01_GOVERNANCE/` (EGC-01 only) | Constitutional + Engineering Process | `Constitution/Charters/` | SPLIT | `01_GOVERNANCE/` mixes a Constitutional artifact (EGC-01) with Platform Vision artifacts (GOVERNANCE_MODEL.md, AUTHORITY_MATRIX.md, RACI_MATRIX.md, ESCALATION_MATRIX.md, DECISION_ROUTING_MODEL.md) under one root | None yet — depends on §08's namespace findings being resolved first | Medium — this is the clearest domain-mixing case found |
| `01_GOVERNANCE/` (all other files) | Platform Vision | `Platform/` | MOVE | Same as above | Same as above | Medium |
| `06_REFERENCE/` | Reference | `Reference/` | MOVE | Name/number differ from target; content already correct | Repository Numbering (§07) adopted | Low |
| `06_PLAYBOOKS/` | Platform Vision (intended) | `Platform/` | REVIEW | Directory is empty; its intended content (root `PB0*.md`) was never placed inside it — needs an explicit decision, not a mechanical move | §08 recommended resolution | Low — nothing to lose, decision only |
| `02_CAPABILITY_MAP/` … `33_BACKEND_SOURCE_CODE_IMPLEMENTATION/` | Platform Vision | `Platform/` | MOVE | Consistent, single-domain block | Repository Numbering (§07) adopted | Low — internally consistent already |
| `00_RELEASE/`, `00_VISION/` | Platform Vision | `Platform/` | MOVE | Same reasoning | Same | Low |
| `50_IMPLEMENTATION/` | Planning & Sequencing | `Planning/Gates/` | MOVE | Matches target domain directly | Repository Numbering (§07) adopted | Low |
| `docs/adr/` | Implementation Pattern | `Patterns/Accepted/` + `Patterns/Superseded/` | SPLIT | ADR directory currently mixes accepted and superseded ADRs undifferentiated by location | Per-ADR status classification (RKM-01 §07.1 Lifecycle field) | Low |
| `docs/planning/` | Planning & Sequencing | `Planning/` | MOVE | Direct match | Repository Numbering (§07) adopted | Low |
| `docs/c4/` | Illustrative | `Illustration/` | MOVE | Direct match | Repository Numbering (§07) adopted | Low |
| `backend/` | Codebase | `Codebase/` | REVIEW | Code repositories conventionally resist semantic renumbering (build tooling, CI paths, import roots depend on the literal path) — moving it has a different risk profile than documentation | Requires an engineering-track decision under EGC-01 §06, not just RKM-01/RSM-01 | High — the only Root Domain whose current path is likely load-bearing outside the documentation system itself |
| `CLAUDE.md`, `README.md` | Reference (process-layer, self-describing) | Root-level exception — remains outside all Root Domains | KEEP | Both are conventionally expected at repository root by tooling and human readers regardless of internal semantic model | None | Low |
| `GOVERNANCE_MODEL.md` (root copy), `CAPABILITY_MAP_v1.0.md` (root copy) | Platform Vision | `Platform/` | UNRESOLVED | Cannot assign a single target until the content divergence identified in §08 is resolved — moving either copy now would silently pick a winner | §08 content-divergence resolution (out of RSM-01 scope) | Medium — risk is in the content decision, not the move itself |
| `TEST_WRITE.md`, `CONNECTOR_TEST.md` | None (not classifiable) | N/A | DELETED (RTC-01) | Operational test residue, not specification content; deleted per Repository Cleanup Operation RTC-01 after validation found no operational dependency — see §08a historical audit record | None — action completed | None — historical |
| `.github/`, `.claude/` | Codebase-adjacent (tooling) | N/A — outside RKM-01's nine domains | REVIEW | RKM-01 does not currently classify CI/agent-tooling configuration; a tenth domain or an explicit "tooling is Codebase-adjacent" ruling is needed before these can be mapped | RKM-01 amendment (out of RSM-01 scope — RSM-01 may not create new domains, §03 rule 2) | Low |

---

## 11. Structural Validation

| Check | Result |
|---|---|
| Every Knowledge Domain has structural representation | PASS — all nine RKM-01 §05 domains map to a Root Domain in §04.1 |
| Every Layer has structural representation | PASS — all eight RKM-01 §06 layers map via §05 |
| Every artifact type has canonical placement | PASS — all six RKM-01 §07.3 types placed in §09 |
| Every generated artifact has a destination | PASS — all twelve RKM-01 §10 artifacts resolve to `Reference/Generated/` (§04.4) |
| No duplicate namespaces exist | FAIL — §08 identifies two content-divergent filename duplicates (`GOVERNANCE_MODEL.md`, `CAPABILITY_MAP_v1.0.md`) and one number collision (`06_`) |
| No structural ambiguity exists | FAIL — `01_GOVERNANCE/` mixes two Semantic Domains under one root (§10); `.github/`, `.claude/` are unclassifiable under the current nine-domain model |
| No orphan structural nodes exist | FAIL — `06_PLAYBOOKS/` is an intended-but-unpopulated node (§08). (`TEST_WRITE.md`/`CONNECTOR_TEST.md` were the other orphans identified here; both were deleted under Repository Cleanup Operation RTC-01 and no longer contribute to this finding — see §08a.) |

Structural Validation as a whole: **NOT CLEAN**. This is an expected
outcome of a first structural pass against an organically-grown
filesystem, not a defect in RSM-01 or RKM-01 — it is the reason §12
gates any migration behind explicit resolution of exactly these
findings.

---

## 12. Future Generated Artifacts

Unchanged from RKM-01 §10; RSM-01 adds no new generated artifact and
removes none. Repository Numbering (§07 of this document) is the one
addition RSM-01 contributes to that list, since RKM-01 named numbering
as part of "Repository Structure" without detailing it.

---

## 13. Migration Preconditions

All of RKM-01 §12's seven criteria apply unchanged and are not repeated
here. RSM-01 adds no new precondition, but records that, given §11's
findings, criterion 2 ("complete classification coverage") and
criterion 4 ("no traceability loss") cannot currently be satisfied
without first resolving:

1. The `GOVERNANCE_MODEL.md` and `CAPABILITY_MAP_v1.0.md` content
   divergences (§08) — classification cannot proceed while two
   artifacts claim the same canonical name with different content.
2. The `01_GOVERNANCE/` domain-mixing (§10) — a SPLIT action requires a
   decision RSM-01 is not authorized to make (§03 rule 2: no domain
   merging or splitting).
3. Whether `.github/` and `.claude/` require a tenth Knowledge Domain,
   which would be an RKM-01 amendment, not an RSM-01 decision.
4. Whether `backend/`'s physical path may move at all, which RSM-01
   defers entirely to EGC-01 §06's engineering change-classification
   process (§10, REVIEW).

---

## 14. Conclusions

RSM-01 successfully derives a complete logical structure — nine Root
Domains, their subdomains, a placement rule per artifact class, and a
numbering policy — entirely from RKM-01, without introducing, merging,
or renaming any semantic domain. Applying that structure to the current
filesystem (§10) surfaces four categories of pre-existing disorder that
predate both RKM-01 and RSM-01: two content-divergent filename
duplicates, one populated-elsewhere-instead-of-in-place directory
(`06_PLAYBOOKS/`), one domain-mixed directory (`01_GOVERNANCE/`), and two
classes of artifact RKM-01's domain model does not yet cover (tooling
configuration, and non-specification test residue).

None of these findings block RKM-01 or RSM-01 from standing as valid
models. They block only the next step — a Migration Plan — per §13.
No filesystem change has occurred as part of producing this document.
