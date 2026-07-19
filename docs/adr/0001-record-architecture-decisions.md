# ADR-0001: Record architecture decisions

- Status: Accepted
- Date: 2026-07-11
- Deciders: Engineering
- Governance level: L2 (process decision, no cross-domain or budget impact)

## Context

The repository holds an extremely large specification corpus (00_RELEASE
through 50_IMPLEMENTATION, 100+ documents) but no lightweight,
chronologically-ordered record of *decisions actually made while coding*,
tied to git history. Two risks in `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md`
stem partly from this: R-ARCH-001 (architecture drift) and R-ARCH-002
(CSR boundary violation) — both are easier to prevent when the reasoning
behind a boundary is written down next to the code, not buried in a
15,000-word design document.

## Decision

Adopt Architecture Decision Records (ADRs) in `docs/adr/`, one Markdown file
per decision, Nygard format (`docs/adr/0000-adr-template.md`), sequentially
numbered, never edited after acceptance (superseded instead). An ADR is
required before merging any change that meets the criteria in
`docs/adr/README.md` ("When an ADR is required").

## Consequences

- Decisions affecting the codebase are traceable to a specific, small,
  reviewable document and a specific commit.
- Small overhead per architectural decision (a few minutes to write one).
- The existing numbered spec directories remain the source of *intended*
  architecture; ADRs record what was *actually decided and why*, and take
  precedence over spec prose when the two disagree (the spec should then be
  updated to match, or a new ADR written to change course).

## Alternatives considered

- Keep relying on the numbered spec docs only — rejected: they are
  vision/plan documents, not decision records; they are slow to update, not
  decision-shaped (no explicit alternatives/consequences), and don't map to
  git history the way a "why did we do this" question needs.
- A single running `DECISIONS.md` log — rejected: doesn't scale, hard to
  reference from PRs, no clean superseding mechanism.

## References

- `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` (R-ARCH-001, R-ARCH-002)
- `docs/adr/README.md`
