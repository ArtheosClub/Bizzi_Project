---
name: bizzi-write-adr
description: Create a new Architecture Decision Record (ADR) for the Bizzi Platform backend, following the project's Nygard-format template and numbering rules in docs/adr/. Use when a coding task involves an architectural or cross-module decision, a real choice among alternatives, or anything the risk register flags as architecture drift (R-ARCH-001/002) — per docs/adr/README.md's "When an ADR is required" section. Also use to supersede an existing ADR when a prior decision needs to change.
---

# Write an ADR — Bizzi Platform backend

## When to actually use this skill

Per `docs/adr/README.md`, write an ADR when the change is:
- L3+ per `01_GOVERNANCE/GOVERNANCE_MODEL.md` (architectural/cross-module).
- A real choice among alternatives, not a mechanical application of an
  already-accepted ADR.
- Flagged by `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md`
  under R-ARCH-001 (architecture drift) or R-ARCH-002 (CSR boundary
  violation).

Routine module work that follows `06_MODULE_IMPLEMENTATION_SEQUENCE.md` and
an already-accepted ADR does **not** need a new one.

If you're unsure whether a decision rises to this bar, err toward writing a
short ADR — it's cheaper than a buried decision someone has to reverse-
engineer from a diff later.

## Steps

1. **Check the index** in `docs/adr/README.md` — the decision may already be
   recorded. If it conflicts with an existing Accepted ADR, you're
   superseding it (step 5), not writing a fresh one.
2. **Find the next number**: look at the highest-numbered file in
   `docs/adr/` (e.g. if `0006-*.md` is the latest, you're writing `0007-`).
   Zero-padded 4 digits.
3. **Copy the template**: start from `docs/adr/0000-adr-template.md`. Fill in
   every section — Context, Decision, Consequences (including honest
   downsides, not just benefits), Alternatives considered, References
   (cite real file paths in this repo, not paraphrases).
4. **Set the governance level** in the header using
   `01_GOVERNANCE/GOVERNANCE_MODEL.md` (L1-L5) and
   `01_GOVERNANCE/AUTHORITY_MATRIX.md` (A0-A7). If it's L4/L5 or A4+, this
   decision needs project-owner sign-off before status can be `Accepted` —
   use `AskUserQuestion` rather than marking it Accepted unilaterally.
5. **To change a prior decision**: write a new ADR referencing the old one,
   set the new ADR's Status to `Accepted`, and edit only the old ADR's
   Status line to `Superseded by ADR-XXXX` — never rewrite its Context/
   Decision/Consequences after the fact. History stays honest that way.
6. **Update the index** in `docs/adr/README.md` with the new row.
7. **Link it** from wherever it matters: the WP in
   `docs/planning/WORK_PACKAGES.md`, the C4 diagram it affects, or the PR
   description.

## Format reminder

Nygard format: Status / Date / Deciders / Governance level header, then
Context, Decision, Consequences, Alternatives considered, References. One
decision per file. See any of `docs/adr/0001-*.md` through `0006-*.md` for
worked examples.
