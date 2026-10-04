"""Reject destinations and libpq query overrides before any connection."""

import pytest

from app.core.preproduction_guard import ScopeViolationError, require_test_destination


def test_exact_test_destination_allowed():
    require_test_destination("postgresql+psycopg://localhost:5433/bizzi_test")


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://localhost:5432/bizzi_dev",
        "postgresql+psycopg://remote:5433/bizzi_test",
        "postgresql+psycopg://127.0.0.1:5433/bizzi_test",
        "postgresql+psycopg://localhost/bizzi_test",
        "postgresql+psycopg://localhost:5433/bizzi_test?host=remote",
        "not-a-url",
    ],
)
def test_other_destinations_rejected_without_values(url):
    with pytest.raises(ScopeViolationError) as caught:
        require_test_destination(url)
    assert str(caught.value) == "Database destination is outside record-5 scope"
