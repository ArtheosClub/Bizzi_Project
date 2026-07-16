# Bizzi Platform Backend

Python + FastAPI backend for the Bizzi Platform MVP ("Workspace Execution
Loop v0.1"). Stack decided in `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`
(supersedes the earlier TypeScript/NestJS scope in ADR-0002).

Being built per `docs/planning/PRE-CODING-BRIEF.md` Gate B (Engineering
Foundation) — this README grows one section per Gate B step; it is not a
finished runbook yet.

## Status

Gate B in progress. Currently: FastAPI skeleton with a health endpoint.
No database dependency yet — that's step 3+.

## Requirements (so far)

- Python 3.11+

Further requirements (PostgreSQL/Docker, Alembic, dev tooling) are added as
later Gate B steps land, each noted here when it does.

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
