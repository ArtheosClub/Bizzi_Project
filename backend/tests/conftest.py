"""Test environment setup.

Loads backend/.env.test so the test suite runs against the same
non-sensitive, fixed values docker-compose.yml's postgres-test service
uses, instead of a value hardcoded in Python. Settings.database_url is
required (fail-fast, see app/core/config.py), so tests need a value even
though nothing in Gate B's test suite actually queries a database yet.

load_dotenv never overrides an already-set environment variable by
default, so a real DATABASE_URL set explicitly (e.g. by CI's job-level
`env:` block, which points at a different port than .env.test) still wins.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env.test")
