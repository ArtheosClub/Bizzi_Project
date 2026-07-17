"""Test environment setup.

Settings.database_url is required (fail-fast, see app/core/config.py), so
tests need a value even though nothing in Gate B's test suite actually
queries a database yet. Set before any test imports app.main, so
get_settings() never sees a missing value.
"""

import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://bizzi:bizzi@localhost:5433/bizzi_test",
)
