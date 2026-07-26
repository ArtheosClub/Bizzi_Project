# Engineering Index

Document ID: ESF-INDEX
Title: Engineering Specification Index
Version: 1.0
Status: ACTIVE
Document Type: Governance Catalog
Part of: Engineering Specification Framework
Repository: ArtheosClub/Bizzi_Project

This document SHALL be the future registry of Engineering Specifications.
It does not itself define any module's implementation contract; each
Engineering Specification's own document is authoritative for its
content. This document records identity and status only.

---

## Registry

| Specification ID | Module ID | Module Name | Engineering Specification | Version | Status | Implementation Status | Verification Status | Gate D Status |
|---|---|---|---|---|---|---|---|---|
| _(none)_ | | | | | | | | |

No Engineering Specification currently exists. This registry SHALL be
extended with one row per Engineering Specification as each is created,
following `ENGINEERING_SPECIFICATION_TEMPLATE.md`.

---

## Column Definitions

- **Specification ID** — the Engineering Specification's own identifier,
  assigned when the specification is created.
- **Module ID** — the permanent engineering identifier of the module the
  specification implements, per `60_MODULE_SPECIFICATIONS/MODULE_INDEX.md`.
- **Module Name** — the name of the module the specification implements.
- **Engineering Specification** — the file path of the Engineering
  Specification document.
- **Version** — the Engineering Specification's own document version.
- **Status** — the Engineering Specification's own lifecycle status
  (e.g. `Draft`, `Under Review`, `Approved`).
- **Implementation Status** — the module's status against the
  Implementation stage of the engineering lifecycle defined in
  `README.md` §8.
- **Verification Status** — the module's status against the
  Verification stage of that lifecycle.
- **Gate D Status** — the module's status against the Gate D stage of
  that lifecycle.

---

## Usage Instructions

A new row SHALL be added to the Registry above only when a new
Engineering Specification is created, following
`ENGINEERING_SPECIFICATION_TEMPLATE.md` in full. Each row SHALL be kept
consistent with the Engineering Specification document it references;
where the two diverge, the Engineering Specification document itself is
authoritative and this registry SHALL be corrected to match it. No row
SHALL be added for a module lacking an approved Module Specification in
`60_MODULE_SPECIFICATIONS/`.
