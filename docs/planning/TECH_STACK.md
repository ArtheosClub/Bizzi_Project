# Bizzi Platform Backend — Tech Stack

Source of truth for every pinned technology choice in Gate B
(`docs/planning/PRE-CODING-BRIEF.md` §8). This file is kept in sync with
what's actually pinned in `backend/pyproject.toml`, `backend/uv.lock`, and
`backend/docker-compose.yml` — if this file and those files disagree, the
files are correct and this file is stale and needs updating.

Stack decision itself is recorded in
`docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`. This document is
the version-pinning detail underneath that ADR, not a separate decision.

Versions below were verified live against PyPI's JSON API and Docker Hub's
tags API on **2026-07-17**, not recalled from training data. Re-verify
before trusting these numbers if it's been a while.

## Pinned versions

| Component | Choice | Pinned version | Why this version |
|---|---|---|---|
| Language runtime | Python | 3.13.14 (`.python-version`, `requires-python = ">=3.13,<3.14"`) | Latest 3.13.x patch (Docker Hub `python` image tags). **Not** 3.14: SQLAlchemy 2.0.51 and Alembic 1.18.5 — both load-bearing for Gate B step 5 — do not yet declare Python 3.14 in their PyPI classifiers, while FastAPI/Pydantic/psycopg/ruff/mypy/pytest all do. Upper-bounding at `<3.14` makes that constraint explicit instead of implicit. |
| Package manager | uv | 0.11.29 (latest stable per PyPI; this sandbox has 0.8.17 pre-installed and both are lockfile-compatible) | Replaces pip + venv per explicit instruction: single tool for dependency resolution, venv creation, and lockfile (`uv.lock`), faster and more reproducible than pip's resolver. |
| Backend framework | FastAPI | 0.139.2 | Current stable on PyPI; declares 3.13/3.14 support. |
| ASGI server | Uvicorn (`[standard]`) | 0.51.0 | Current stable; the `[standard]` extra pulls in `uvloop`/`httptools` for production-realistic performance in dev too. |
| Data validation | Pydantic | 2.13.4 | Current stable v2 line; FastAPI 0.139.2 is built against Pydantic v2. |
| Settings/config | pydantic-settings | 2.14.2 | Current stable; typed env-var loading for Gate B step 4. |
| ORM | SQLAlchemy | 2.0.51 | Current stable 2.x; does not yet declare 3.14 support (see Python row). |
| Migrations | Alembic | 1.18.5 | Current stable; the direct equivalent of Prisma Migrate from the superseded NestJS plan (ADR-0002/ADR-0007). Does not yet declare 3.14 support. |
| DB driver | psycopg (v3), `psycopg[binary]` | 3.3.4 | Current, actively-developed driver. Deliberately **not** `psycopg2-binary`: psycopg2 is in maintenance-only mode; psycopg3 is the SQLAlchemy-2.0-recommended current choice. Flagged as a change from an earlier draft plan that had tentatively named psycopg2. |
| Linter | ruff | 0.15.22 | Current stable; single fast tool covering what flake8+isort+black used to need separately. |
| Type checker | mypy | 2.3.0 | Current stable. Chosen over pyright per Gate B step 6 (either was acceptable; picking one to enforce consistently in CI). |
| Test runner | pytest | 9.1.1 | Current stable. |
| Test HTTP client | httpx | 0.28.1 | Current stable; used with FastAPI's `TestClient`. PyPI classifiers only list up to 3.12, which lags the package's actual compatibility — not a blocker. |
| Database | PostgreSQL | 18.4 (`postgres:18.4-alpine` image) | Current stable major (18), patch 18.4, image last updated 2026-07-08 — mature GA (multiple patches past 18.0), not beta/rc. Bumped up from an earlier draft's `postgres:16-alpine`. |
| Base Docker image (backend, Gate B step 7) | `python:3.13.14-slim-bookworm` | pinned patch + Debian codename | Matches the language pin exactly (3.13.14); `-slim-bookworm` over plain `-slim` for a named, stable Debian base rather than a floating "whatever's current" tag. |

## CI GitHub Actions (step 6)

| Action | Pinned version | How verified |
|---|---|---|
| `actions/checkout` | v7.0.0 | `git ls-remote --tags --refs https://github.com/actions/checkout` on 2026-07-17. `api.github.com` wasn't reachable from this session (scoped to `ArtheosClub/Bizzi_Project` only) so this used git's own protocol against the target repo directly instead — not a fallback guess, an equally direct source. |
| `astral-sh/setup-uv` | v8.3.2 | Same method, same date, `astral-sh/setup-uv` repo. |

Both pin uv itself to `0.11.29` and Python to `3.13.14` via
`astral-sh/setup-uv`'s `version`/`python-version` inputs — matching the
Language runtime and Package manager rows above exactly, with no separate
`actions/setup-python` step needed.

## Explicitly not included

- **Redis** — no Gate B step has a concrete, demonstrated need for it yet.
  Brief §6 says add it only when one exists; adding it speculatively would
  violate that.
- **Kubernetes** — deferred per ADR-0007 / Brief §1 ("Kubernetes-ready, but
  not Kubernetes-dependent"). MVP deployment is Docker Compose only.

## Known local-environment caveat (sandbox-specific, not a repo decision)

This development sandbox's outbound network goes through a policy-enforcing
proxy that allows direct access to `pypi.org`/`files.pythonhosted.org` (so
every version above was verified live) but denies `releases.astral.sh`
(confirmed via the proxy's own status endpoint: `403` to `CONNECT`, logged
as a policy denial, not a transient failure). That host is where `uv python
install` downloads standalone CPython builds from — so `uv` in this sandbox
cannot fetch the pinned 3.13.14 build.

**What this does and doesn't affect:**
- The repo's pin stays 3.13.14 — that's correct and unaffected.
- Local verification in this sandbox used the pre-installed system
  `python3.13` (3.13.12, two patches behind) via `uv sync --python 3.13.12`
  / `uv run --python 3.13.12 ...`. Same 3.13.x minor line, functionally
  equivalent for everything exercised in Gate B so far.
- **CI is where 3.13.14 itself actually gets proven**: GitHub Actions
  runners are not behind this sandbox's proxy, so `astral-sh/setup-uv`
  with `python-version: '3.13.14'` (Gate B step 6,
  `.github/workflows/backend-ci.yml`) genuinely installs and runs the exact
  pinned patch. Anyone running this locally outside this sandbox should hit
  no such restriction either.
- Same pattern as the Docker-daemon and Postgres-version caveats already
  noted in the Gate B step 3 commit: substitute the closest available
  real thing locally, verify against it honestly, rely on CI/a real machine
  for the final proof against the actual pin.

## Docker Compose service inventory (current, updated through step 3; step 7 adds `api`)

| Service | Image/build | Purpose | Port | Persistent volume |
|---|---|---|---|---|
| `postgres` | `postgres:18.4-alpine` | Dev database | 5432 | yes (`bizzi_postgres_dev`) |
| `postgres-test` | `postgres:18.4-alpine` | Test database | 5433 | no (ephemeral by design) |
| `api` *(step 7, not yet added)* | built from `backend/Dockerfile`, `python:3.13.14-slim-bookworm` base | the FastAPI app | 8000 | n/a |

`.env`/`.env.example` map straight into `docker-compose.yml` via Compose's
`${VAR:-default}` interpolation — `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_DB`, `POSTGRES_TEST_DB` today; `DATABASE_URL` is read by the app
itself (not by Compose) once step 4/5 wire up configuration and the DB
session.
