# Matches docs/planning/TECH_STACK.md exactly: Python 3.13.14, uv 0.11.29.
FROM python:3.13.14-slim-bookworm

WORKDIR /app

# uv via pip (PyPI-hosted) rather than COPY --from=ghcr.io/astral-sh/uv —
# keeps the build to one verifiable source (PyPI) instead of adding an
# external registry image this sandbox has no way to check the tag of.
RUN pip install --no-cache-dir uv==0.11.29

COPY pyproject.toml uv.lock ./
# --no-dev: ruff/mypy/pytest/httpx are dev-only tooling, not runtime deps.
RUN uv sync --locked --no-dev

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Non-root user / production hardening deliberately deferred — Gate B scope
# is "runs", not "hardened for production" (that's Gate E territory).

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
