# C4 Architecture Documentation

Four views of the Bizzi Platform backend, following the
[C4 model](https://c4model.com) (Context → Container → Component → Code).
Diagrams are Mermaid flowcharts/sequence diagrams (not the experimental
Mermaid `C4Context`/`C4Container` syntax) so they render reliably in GitHub,
VS Code, and any standard Markdown+Mermaid viewer.

Scope boundary: **solid nodes and solid edges are MVP scope** (what
`docs/planning/WORK_PACKAGES.md` Phase 0/1 actually builds). **Dashed nodes
and dashed edges are future/planned** — named in the spec corpus but not part
of this build. See ADR-0002 for why the platform-wide "Art of Business"
services are drawn as external/future rather than in-scope containers.

## Views

| Level | File | Shows |
|---|---|---|
| C1 — Context | [`C1_CONTEXT.md`](C1_CONTEXT.md) | Bizzi backend, its users, and its (mostly future) external systems |
| C2 — Container | [`C2_CONTAINER.md`](C2_CONTAINER.md) | The API, the database, and planned containers around them |
| C3 — Component | [`C3_COMPONENT.md`](C3_COMPONENT.md) | NestJS modules inside the API container and how they call each other |
| C4 — Dynamic | [`C4_DYNAMIC_CANONICAL_FLOW.md`](C4_DYNAMIC_CANONICAL_FLOW.md) | The canonical request flow (Controller→Service→Repository) for a state-changing call |

## Keeping this current

Update the relevant view in the same PR that:
- adds/removes a container (new deployable service, new datastore) → C2
- adds/removes a NestJS module or changes which services a module calls → C3
- changes the canonical CSR flow (auth/validation/transaction/audit/event
  order) → C4 dynamic view, and check ADR-0003/0005 still hold

If a change here contradicts an existing ADR, write a new ADR that
supersedes it (see `docs/adr/README.md`) rather than silently redrawing the
diagram.
