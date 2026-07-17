# Bizzi Platform Backend

Python + FastAPI backend for the Bizzi Platform MVP ("Workspace Execution
Loop v0.1"). Stack decided in `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`
(supersedes the earlier TypeScript/NestJS scope in ADR-0002).

Being built per `docs/planning/PRE-CODING-BRIEF.md` Gate B (Engineering
Foundation) — this README grows one section per Gate B step; it is not a
finished runbook yet.

## Status

Gate B (Engineering Foundation) is code-complete: FastAPI skeleton with a
health endpoint, Postgres dev/test via Docker Compose, typed startup
configuration, Alembic migrations, a CI workflow (confirmed green against
real Postgres/Python — see step 6 below), and a Dockerfile +
`docker compose up` path for the `api` service. No route touches the
database yet — nothing in Gate B needs that (Gate C's concern).

**One open item before Gate B can be called fully proven**: the `docker
compose up --build` command itself (step 7) has not been run anywhere yet —
this development sandbox has no Docker daemon. See "One command, fresh
clone to running backend" below for exactly what is and isn't verified.

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

**Confirmed, not just expected**: workflow run
[29603566268](https://github.com/ArtheosClub/Bizzi_Project/actions/runs/29603566268)
(commit `eb760fa`) completed with `conclusion: success`. GitHub Actions
runners have a working Docker daemon, unlike this sandbox, so the
Postgres-service-container + migration + test steps ran for real, against
the exact pinned versions (real `postgres:18.4-alpine`, real Python
3.13.14) — not the native-Postgres-16/Python-3.13.12 substitutes used for
local verification in steps 3-6.

Added `backend/tests/test_health.py` (`fastapi.testclient.TestClient` +
`httpx`) as the first real test, and switched `app/main.py` from
`@app.on_event("startup")` (deprecated in current FastAPI) to the `lifespan`
context manager — found via the deprecation warning pytest surfaced when
this step ran the test locally for the first time, fixed immediately rather
than shipped as a known warning.

## One command, fresh clone to running backend (step 7)

```sh
cd backend
cp .env.example .env
docker compose up --build
```

This is the exit criterion from `docs/planning/PRE-CODING-BRIEF.md` Section
6: a runnable backend, Postgres with migrations, Docker Compose, a health
endpoint, and structured logging, brought up by one command. `api`'s
`entrypoint.sh` runs `alembic upgrade head` before starting `uvicorn`, so a
fresh clone ends up migrated, not just running. Then
`curl http://127.0.0.1:8000/health` should return `{"status":"ok"}`.

- `backend/Dockerfile`: `python:3.13.14-slim-bookworm` base (matches the
  pinned language version exactly), `uv==0.11.29` installed via `pip`
  (PyPI-hosted — deliberately not `COPY --from=ghcr.io/astral-sh/uv`, to
  keep the build to one verifiable source instead of an external registry
  image this sandbox has no way to check the tag of), `uv sync --locked
  --no-dev` (runtime deps only — ruff/mypy/pytest/httpx stay dev-only).
- `backend/entrypoint.sh`: `alembic upgrade head` then
  `exec uv run uvicorn ...` — migrate-then-serve, one process.
- `docker-compose.yml`'s `api` service: builds from the Dockerfile,
  `depends_on: postgres: condition: service_healthy` (won't start against
  an unready database), its own `DATABASE_URL` pointing at the `postgres`
  service name rather than `localhost` (the Compose-network address, not
  the host-machine address `.env`'s `DATABASE_URL` uses for the plain
  `uv run uvicorn` workflow above), and a `urllib`-based healthcheck (no
  `curl` in the slim base image).

**What's verified versus what isn't, precisely:**
- `docker compose config` resolves the full merged config cleanly,
  including the `api` service's build block, env-var interpolation
  (confirmed `DATABASE_URL` resolves to the `postgres`-hostname form, not
  `.env`'s `localhost` form), healthcheck, and `depends_on` condition.
- `entrypoint.sh` passed a shell syntax check (`sh -n`), and every file it
  and the Dockerfile reference (`pyproject.toml`, `uv.lock`, `app/`,
  `alembic/`, `alembic.ini`) was confirmed to exist.
- The individual pieces this depends on — `alembic upgrade head`,
  `uvicorn` serving `/health`, ruff/mypy/pytest — are proven, either
  locally (steps 2-5) or in real CI against real Postgres/Python (step 6,
  run [29603566268](https://github.com/ArtheosClub/Bizzi_Project/actions/runs/29603566268)).
- **Not verified**: the actual `docker build` and `docker compose up
  --build` commands themselves have not been run anywhere in this change —
  this sandbox has no Docker daemon (`dockerd` fails on a `ulimit`
  permission restriction), and CI's Postgres-service-container approach
  doesn't build this Dockerfile or exercise `docker-compose.yml` at all.
  **This needs a real run — in CI (a follow-up workflow step, or manually)
  or on your machine — before Gate B step 7 can be called fully proven.**
