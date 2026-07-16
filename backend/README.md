# Bizzi Platform Backend

Python + FastAPI backend for the Bizzi Platform MVP ("Workspace Execution
Loop v0.1"). Stack decided in `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`
(supersedes the earlier TypeScript/NestJS scope in ADR-0002).

Being built per `docs/planning/PRE-CODING-BRIEF.md` Gate B (Engineering
Foundation) — this README grows one section per Gate B step; it is not a
finished runbook yet.

## Status

Gate B in progress. Currently: FastAPI skeleton with a health endpoint, plus
a Postgres dev/test Docker Compose setup. The app doesn't talk to the
database yet — that's step 4/5 (config module, then Alembic).

## Requirements (so far)

- Python 3.11+
- Docker + Docker Compose (for Postgres)

Further requirements (Alembic, dev tooling) are added as later Gate B steps
land, each noted here when it does.

## Run locally (step 2 — no database required)

```sh
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then `curl http://127.0.0.1:8000/health` should return `{"status":"ok"}`.

Logs are structured JSON on stdout (`app/core/logging.py`) — no external
logging dependency yet, per MVP-simplicity principle B15.

## PostgreSQL (step 3 — dev + test instances)

```sh
cd backend
cp .env.example .env   # defaults are fine for local dev
docker compose up -d
```

This starts two Postgres 16 instances:

| Service | Host port | Database | Purpose |
|---|---|---|---|
| `postgres` | 5432 | `bizzi_dev` | local development |
| `postgres-test` | 5433 | `bizzi_test` | test runs (no persistent volume — safe to reset) |

Both have a `pg_isready` healthcheck. Nothing in the app connects to these
yet (that's step 4/5) — this step only proves the database layer boots and
is reachable, per `docs/planning/PRE-CODING-BRIEF.md` Section 3's dependency
chain (Postgres blocks tasks/decisions/audit, but nothing blocks Postgres
existing on its own first).
