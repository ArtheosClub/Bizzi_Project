#!/bin/sh
# Migrate then serve — this is what makes `docker compose up` deliver a
# running, migrated, health-checked backend in one command
# (docs/planning/PRE-CODING-BRIEF.md Section 6 exit criteria).
set -e

uv run alembic upgrade head
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
