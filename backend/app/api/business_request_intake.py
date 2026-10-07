"""Synthetic in-process WP23; endpoint is the sole transaction boundary.

Authorization before body validation. Default verifier denies; no provider.
No live exposure permission or production readiness is implied by this router.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.authentication import RejectingTokenVerifier, TokenVerifier
from app.core.preproduction_guard import require_session
from app.core.request_context import get_request_id
from app.db.session import get_db
from app.schemas.business_request_intake import BusinessRequestInput, BusinessRequestOutput
from app.services.business_request_intake_service import BusinessRequestIntakeService
from app.services.identity_service import IdentityService

router = APIRouter()


def get_token_verifier() -> TokenVerifier:
    return RejectingTokenVerifier()


@router.post("/business-requests", status_code=201, response_model=BusinessRequestOutput)
async def create_business_request(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    verifier: Annotated[TokenVerifier, Depends(get_token_verifier)],
) -> BusinessRequestOutput:
    header = request.headers.get("authorization", "")
    scheme, separator, value = header.partition(" ")
    token = value if separator and scheme.lower() == "bearer" else None
    # On exceptions, context manager rolls back before the shared HTTP handler.
    require_session(db)
    with db.begin():
        context = IdentityService(db, verifier).resolve_actor_context(token, get_request_id() or "")
        try:
            BusinessRequestInput.model_validate_json(await request.body())
        except ValidationError as exc:
            errors = [{**e, "loc": ("body", *e["loc"])} for e in exc.errors()]
            raise RequestValidationError(errors) from None
        task_id = BusinessRequestIntakeService.create(db, actor_context=context)
        response = BusinessRequestOutput(task_id=task_id)
    # Transaction commit must succeed before a 201 result leaves this handler.
    return response
