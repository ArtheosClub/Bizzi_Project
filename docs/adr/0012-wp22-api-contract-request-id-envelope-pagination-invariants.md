# ADR-0012: WP22 API contract — request-ID propagation, error envelope shape, pagination invariants

- Status: Accepted
- Date: 2026-08-11
- Deciders: Andrew (Project Owner), direct decision
- Governance level: L3 (cross-module API contract — every WP23–WP39
  endpoint inherits this shape). This is an engineering/API-contract
  decision: it does not change D01–D10, does not collapse any D07
  orthogonal dimension, and does not resolve or constrain ADW-07/ADW-08
  Domain Event semantics — decided directly by the Project Owner,
  satisfying the sign-off this level requires.

## Context

WP22 (API Error and Response Standard) had no current-tier authority
settling several real alternatives it depends on: external request-ID
representation, error/response envelope scope, validation status
code/detail shape, generic error-code vocabulary, and pagination contract
timing. The one prior source that would have settled these,
`28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md` and
`11_PAGINATION_FILTERING_SORTING.md`, is Epoch II — `Status: Draft v0.1`,
pre-dates the Python/FastAPI stack decision (ADR-0007), and is
superseded. It is cited below only as historical lineage, never as
authority.

Amendment A-07 (2026-08-11) transferred per-HTTP-request identifier
generation and propagation from WP10 to WP22, with an explicit Tier-6
boundary against Domain Event correlation, causation, provenance,
distributed tracing, and cross-request workflow identity — ADW-07/ADW-08
territory, undecided. This ADR preserves that boundary; it does not
reopen it.

A decision-analysis pass (2026-08-11) evaluated each alternative directly
against the current Gate B skeleton (`backend/app/` — bare `FastAPI()`,
`/health` the only route, no middleware, no exception handlers, no
pagination helper, no response envelope) and against existing authority
(`13_BACKEND_CODING_STANDARDS.md` §13/§15/§21,
`GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md` R-02/R-07,
`CLAUDE.md`'s Abstraction Justification Rule). The Project Owner selected
among the alternatives presented, plus one additional selection (uniform
`not_found`, §6 below). This ADR records those selections.

## Decision

**1. Request-ID external representation.** A response header
(`X-Request-Id`) on every HTTP response, success and error alike. No
error-envelope body field at this time. `request_id` is an opaque,
request-scoped string — clients must not infer semantics from its
format. An implementation may generate it as a UUIDv4 internally; that is
an implementation detail, not a wire-contract guarantee. Generation only:
no inbound client- or proxy-supplied request ID is accepted at this
time. `request_id` does not define, implement, alias, or constrain Domain
Event correlation, causation, provenance, distributed tracing, or
cross-request workflow identity — it is not named `correlation_id`.
Domain Event correlation, causation, provenance, distributed tracing, and
cross-request workflow identity remain outside this ADR's scope; the
relevant ADW-07/ADW-08 questions remain unresolved by this ADR.

**2. Envelope scope.** A standardized envelope for **errors only**.
Successful resource responses remain resource-shaped, decided per
endpoint by the WP that introduces it — not wrapped by this ADR. There is
no universal success wrapper. Operational/infrastructure endpoints
(`/health` today; any future liveness/readiness route) are outside this
standardized application error-envelope scope: they have no current error
path to govern, and are consumed by orchestration tooling, not
application clients.

Error envelope shape:

```json
{
  "error": {
    "code": "validation_error",
    "message": "human-readable, safe message",
    "details": [
      { "field": "title", "issue": "required", "message": "title is required" }
    ]
  }
}
```

The field names and their applicability are the selected contract, not
illustrative example text: `code`, `message`, and an optional `details`
array are the full error object. `details` is present **only** for
`validation_error`; it is omitted for `not_found`, `method_not_allowed`,
and `internal_error`.

**3. Validation status and detail shape.** FastAPI's native `422` for
request validation failures — no override to `400`. Validation detail
shape is the minimum stable per-field representation:

```json
{ "field": "title", "issue": "required", "message": "title is required" }
```

translated from Pydantic/FastAPI's raw validation errors by WP22's
handler — the raw structure is never passed through to clients.

**4. Generic error-code vocabulary.** WP22-owned, as of this ADR:
`validation_error` (422), `not_found` (404), `method_not_allowed` (405),
`internal_error` (500). `forbidden`, `unauthenticated`, `conflict`, and
any domain-specific code are deliberately **not** pre-registered here —
no caller for any of them exists anywhere in `backend/app/` today, and
each has a future owner, though the exact WP is not yet fixed by any
approved source: `forbidden`/`unauthenticated` are deferred until the
authorization/authentication work that first requires them (WP16's
deferred remainder and WP17 both name the relevant middleware/checks
without naming these specific codes); `conflict` is deferred until the
first lifecycle-transition endpoint that needs it.

Future WPs may extend the error-code vocabulary without changing the
envelope contract defined in §2. The concrete exception-type hierarchy
and mapping mechanism are WP22 implementation details, not fixed by this
ADR.

**5. No-leak invariant.** Unexpected server exceptions are logged
internally (full detail, with `request_id` attached) and never returned
to the client; public `500` responses use a fixed, generic
`internal_error` body with no exception text, traceback, or internal
attribute. This restates existing authority
(`13_BACKEND_CODING_STANDARDS.md` §15 — never expose raw
framework/ORM errors or provider stack traces to API clients; §21 —
`request_id`/`workspace_id`/operational context belongs in logs, not
responses) — it is not a new policy.

**6. Uniform `not_found` for cross-workspace and nonexistent-entity
access.** `GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md`
R-07 ("Deterministic Failure") requires that access to a cross-workspace
entity "behave as not found or denied... without revealing its
existence" — it permits either a `not_found` response or a denial
response; it does not itself mandate one. **This ADR selects `not_found`**
for WP22's generic HTTP error mapping as an engineering-contract choice
within the space R-07 permits, not as a consequence R-07 forces. GC-005
("Cross-Workspace Access API Behavior") remains `Proposed` in
`GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`'s own register; this
selection neither approves nor forecloses GC-005, and does not reach
membership-level or authentication-level denial semantics — those remain
undecided by this ADR.

**7. Pagination — invariants only.** This ADR fixes: list endpoints must
not return unbounded results; `page_size` must be bounded and validated
(a specific default and maximum are implementation choices, not fixed by
this ADR); any continuation mechanism, once needed, must not expose
persistence internals (e.g. a raw database offset) as a client-facing
guarantee. It does **not** fix concrete response field names (`items`,
`next_page_token`, offset, cursor, or any response-metadata wrapper) —
the first WP23+ list endpoint that actually needs continuation establishes
the concrete contract under these invariants, against a real query
pattern, not anticipated here.

**8. One request-ID lifecycle.** One request identifier exists per HTTP
request lifecycle; the same logical value is available to response
handling (§1) and to structured logging — never a second, independently
generated logging identifier. Middleware class, `ContextVar` usage, exact
source files, and the exception-type hierarchy are implementation choices
for the coding pass, not fixed by this ADR.

## Consequences

- Every WP23–WP39 endpoint inherits this contract; none may invent its
  own error shape, status-code mapping, or a second identifier.
- `/health` and future operational endpoints stay outside the
  application error envelope unless a separate, later decision brings
  them in.
- `forbidden`, `unauthenticated`, and `conflict` are unavailable until the
  WP that needs them adds them via the extensibility principle in §4.
  This is not a current gap — no caller for any of them exists yet.
- No concrete pagination wire contract exists yet. The first WP23+ list
  endpoint must both satisfy this ADR's invariants and establish the
  concrete continuation shape itself.
- Adding a request-ID error-body field, or inbound-ID acceptance, later
  is additive and backward-compatible if a concrete need emerges —
  neither is foreclosed by this ADR, only deferred. **Adopting a
  universal success wrapper later would be a separate, breaking contract
  change, not an additive extension — it is not implied or
  pre-authorized by this ADR** and would require its own decision record.
- `GC-005` remains open in its own register, unaffected by §6's
  selection; a future GC-005 approval or amendment could still choose
  differently for the membership-level question that selection doesn't
  reach.
- `IMPLEMENTATION_BACKLOG.md`'s WP22 "Definition of Done" ("every
  endpoint returns the standard envelope shape") is broader than what
  this ADR delivers. Corrected by Amendment A-08, recorded in the same
  change as this ADR.

## Alternatives considered

- **Request-ID: header + error-body field.** Real client benefit
  (clients often quote bodies, not headers), but nothing currently
  requires body duplication, and header-only is strictly reversible into
  this later at zero cost — the reverse direction is a breaking change.
  Rejected for now, not foreclosed.
- **Envelope: universal success + error wrapper.** No current source
  requires it; existing `13_BACKEND_CODING_STANDARDS.md` §13 already
  describes response DTOs as directly exposing "stable API output
  shape," unwrapped — even Epoch II's own (inadmissible) lineage never
  proposed wrapping success responses. Concretely breaks the shipped,
  CI-tested `/health` contract (`backend/tests/test_health.py`) for no
  offsetting requirement. Rejected.
- **Validation status: 400.** Matches only Epoch II's superseded
  precedent; requires actively overriding FastAPI's native `422` handler
  for no functional benefit beyond matching that non-authoritative
  lineage. Rejected.
- **Pre-registering all 7 candidate error codes now** (`forbidden`,
  `unauthenticated`, `conflict` included). Costs nothing at runtime, but
  no current code path in `backend/app/` can raise any of the three, and
  each has a future owner not yet fixed. Rejected in favor of the
  extensibility principle in §4, which makes deferring them free.
- **Pagination: concrete opaque-token wire contract now** (`items`,
  `page_size`, `next_page_token`). No real consumer exists — no list
  endpoint exists anywhere in the codebase, and WP23+ isn't yet
  unblocked. Fails `CLAUDE.md`'s Abstraction Justification Rule directly
  ("anticipated future need is not sufficient justification"; not "a
  necessary precondition for implementing the next Work Packages," since
  those Work Packages aren't unblocked). Rejected.

## References

- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` — Amendment A-07 (the
  ownership transfer this ADR's §1 and §1's boundary build on), Amendment
  A-08 (the resulting Definition of Done correction)
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP22, WP16, WP17
  entries
- `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` §13
  (DTO shape), §15 (error/no-leak principle), §21 (logging fields) —
  stack-agnostic principles carried over per `CLAUDE.md`
- `50_IMPLEMENTATION/GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md`
  R-02 (Scoped Lookup), R-07 (Deterministic Failure)
- `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` GC-005
  (remains Proposed; this ADR independently selects uniform `not_found`
  within the response space permitted by R-07)
- `CLAUDE.md` — Abstraction Justification Rule
- `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — the error-mapping step this
  ADR now gives a real (non-superseded) target
- `backend/app/main.py`, `backend/app/core/logging.py`,
  `backend/tests/test_health.py` — Gate B baseline verified against
  directly
- `28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md`,
  `28_API_CONTRACTS/11_PAGINATION_FILTERING_SORTING.md` — historical
  lineage only, superseded (Epoch II), not authority
- `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md` — stack this
  ADR implements against
