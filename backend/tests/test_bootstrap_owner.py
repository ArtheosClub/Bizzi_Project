"""Bootstrap CLI-wrapper exercised only through rollback-bound pytest."""

from app.cli.bootstrap_owner import bootstrap_owner
from app.models import User


def test_cli_wrapper_creates_owner_inside_external_test_transaction(identity_db):
    result = bootstrap_owner(
        identity_db,
        issuer="synthetic-issuer",
        subject="synthetic-cli-owner",
        workspace_name="Synthetic CLI",
    )
    assert identity_db.get(User, result.user_id) is not None
