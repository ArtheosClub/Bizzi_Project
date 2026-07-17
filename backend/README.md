# Bizzi Platform Backend

Python + FastAPI backend for the Bizzi Platform MVP ("Workspace Execution
Loop v0.1"). Stack decided in `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`
(supersedes the earlier TypeScript/NestJS scope in ADR-0002).

Being built per `docs/planning/PRE-CODING-BRIEF.md` Gate B (Engineering
Foundation) — this README grows one section per Gate B step; it is not a
finished runbook yet.

## Status

Gate B in progress. Currently: FastAPI skeleton with a health endpoint, a
Postgres dev/test Docker Compose setup, typed startup configuration,
Alembic migrations, and a CI workflow enforcing all of the above. No route
touches the database yet — nothing in Gate B needs that (Gate C's concern).

## Requirements (so far)

- Python 3.13 (pinned to 3.13.14 in `.python-version`; see
  `docs/planning/TECH_STACK.md` for why)
- [uv](https://docs.astral.sh/uv/) for dependency management, virtual
  environments, and the lockfile — no plain `pip`/`venv` workflow is
  maintained
- Docker + Docker Compose (for Postgres)
- SQLAlchemy + Alembic + `psycopg[binary]` (v3) for migrations (step 5)
- ruff + mypy + pytest + httpx as dev tooling (step 6)

Full rationale for every pinned version lives in
`docs/planning/TECH_STACK.md`.

## Run locally

```sh
cd backend
cp .env.example .env   # required from step 4 onward — see Configuration below
uv sync
uv run uvicorn app.main:app --reload
```

`uv sync` creates `.venv` and installs exactly what's locked in `uv.lock`;
`uv run` executes inside that environment without a separate activation
step. Then `curl http://127.0.0.1:8000/health` should return
`{"status":"ok"}`.

Logs are structured JSON on stdout (`app/core/logging.py`), including any
extra fields passed via `logger.info(..., extra={...})` — no external
logging dependency yet, per MVP-simplicity principle B15.

## Configuration (step 4)

`app/core/config.py` loads typed settings (`pydantic-settings`) from `.env`
or the real environment. `database_url` is **required** — startup fails
fast with a clear `pydantic` validation error if it's missing, even though
nothing queries the database yet (that's intentional: the fail-fast
behavior is proven now, before step 5 gives it something to actually do).
`env` and `port` have defaults and are optional.

Verified both directions locally: running with `DATABASE_URL` unset raises
`ValidationError: 1 validation error for Settings / database_url / Field
required` and the server exits; running with it set starts normally and the
startup log line includes `"env": "development"`.

## PostgreSQL (step 3 — dev + test instances)

```sh
cd backend
cp .env.example .env   # defaults are fine for local dev
docker compose up -d
```

This starts two Postgres 18 instances:

| Service | Host port | Database | Purpose |
|---|---|---|---|
| `postgres` | 5432 | `bizzi_dev` | local development |
| `postgres-test` | 5433 | `bizzi_test` | test runs (no persistent volume — safe to reset) |

Both have a `pg_isready` healthcheck.

## Migrations (step 5)

```sh
cd backend
uv run alembic upgrade head
```

- `app/db/base.py`: empty `Base` (`DeclarativeBase`) — no ORM models yet,
  Gate C's concern, not this pass's. It exists now so `alembic/env.py` has
  a stable `target_metadata` to import, instead of being retrofitted later.
- `app/db/session.py`: sync SQLAlchemy engine + `SessionLocal` +
  `get_db()` dependency generator. Not imported by `app/main.py` yet — no
  route touches the database in Gate B, this only proves the migration
  path works.
- `alembic/env.py` reads `DATABASE_URL` from `get_settings()` (single
  source of truth) rather than duplicating it in `alembic.ini`.
- `alembic/versions/e0aa881262f5_baseline.py`: an intentionally empty
  baseline migration — its only job is to prove `alembic upgrade head`
  succeeds against a clean database, per the stop condition in `CLAUDE.md`
  ("A migration fails against a clean database").

Verified: started the sandbox's native PostgreSQL 16 (same substitution
noted in step 3 and `docs/planning/TECH_STACK.md` — the actual
`postgres:18.4-alpine` container needs a Docker daemon this sandbox
doesn't have), created a fresh `bizzi_dev` database, ran
`alembic upgrade head`, confirmed the `alembic_version` table exists and
contains the baseline revision, then `alembic current` reported it as
`(head)`. Database and role dropped afterward, cluster stopped.

## Dev tooling & CI (step 6)

```sh
cd backend
uv sync --all-groups     # installs the dev dependency-group too
uv run ruff check .
uv run mypy app
uv run pytest -v
```

`.github/workflows/backend-ci.yml` runs all of this on every PR/push
touching `backend/**`, against a real `postgres:18.4-alpine` service
container: checkout, install uv + Python 3.13.14
(`astral-sh/setup-uv@v8.3.2`), `uv sync --locked --all-groups` (fails if
`uv.lock` is stale), ruff, mypy, `alembic upgrade head` against the service
container, then pytest. Action versions verified current via
`git ls-remote --tags` on 2026-07-17 (GitHub's REST API wasn't reachable
from this session to cross-check via a different method, but `git
ls-remote` talks to the same repositories directly over git's protocol, so
it's an equally direct source, not a fallback guess).

**This is the step where "it actually works" stops being a locally-verified
claim and becomes something CI proves independently**: GitHub Actions
runners have a working Docker daemon, unlike this sandbox, so the
Postgres-service-container + migration + test steps above will run for
real, against the exact pinned versions, the first time this workflow
executes — not against the native-Postgres-16 substitute used for local
verification in steps 3 and 5.

Added `backend/tests/test_health.py` (`fastapi.testclient.TestClient` +
`httpx`) as the first real test, and switched `app/main.py` from
`@app.on_event("startup")` (deprecated in current FastAPI) to the `lifespan`
context manager — found via the deprecation warning pytest surfaced when
this step ran the test locally for the first time, fixed immediately rather
than shipped as a known warning.
