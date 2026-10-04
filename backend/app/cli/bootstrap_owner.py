"""Owner bootstrap transaction wrapper. CLI COMMAND execution not admitted.

Record-5 amendment 1 permits this path through pytest only on bizzi_test.
No argument parser/entry point or provider contact is installed.
"""

from sqlalchemy.orm import Session

from app.core.preproduction_guard import require_test_destination
from app.services.bootstrap_service import BootstrapResult, BootstrapService


def bootstrap_owner(
    db: Session, *, issuer: str, subject: str, workspace_name: str
) -> BootstrapResult:
    require_test_destination(str(db.get_bind().engine.url.render_as_string(hide_password=False)))
    with db.begin():
        return BootstrapService.create_owner(
            db, issuer=issuer, subject=subject, workspace_name=workspace_name
        )
