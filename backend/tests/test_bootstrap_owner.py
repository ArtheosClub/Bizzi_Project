"""No Stage-1 bootstrap mutation before reviewed WP19 audit integration."""

import pytest

from app.cli.bootstrap_owner import bootstrap_owner


def test_bootstrap_not_callable_before_wp19():
    with pytest.raises(RuntimeError, match="reviewed WP19 audit"):
        bootstrap_owner()
