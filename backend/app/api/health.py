"""Liveness/readiness endpoint.

Deliberately dependency-free at this step: no DB check yet, because the
database doesn't exist as a dependency until Gate B step 3/5. Readiness
against the database is added once DB wiring lands, without changing this
route's contract.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
