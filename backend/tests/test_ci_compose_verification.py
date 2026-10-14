"""Pure synthetic probes; never invoke Docker, HTTP or a database in these tests."""

import json
from copy import deepcopy
from unittest.mock import Mock

import pytest

from tests.ci_compose_verification import (
    EXPECTED_SCHEMA,
    SCHEMA_SHA256,
    TABLES,
    Collector,
    EvidenceRefused,
    canonical_schema,
    validate_context,
    validate_summary,
)
from tests.test_preproduction_guard import CI_NAMES, CI_VALUES


def context():
    values = dict(zip(CI_NAMES, CI_VALUES, strict=True))
    values["GITHUB_JOB"] = "compose-e2e"
    values.update(GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="1")
    return values


def summary():
    return {
        "status": "PASS", "reason": "verified", "repository": "ArtheosClub/Bizzi_Project",
        "event": "pull_request", "pr": 1, "head_sha": "a" * 40, "checkout_sha": "a" * 40,
        "checkout_tree": "b" * 40, "run_id": 1, "attempt": 1, "job": "compose-e2e",
        "runner_environment": "github-hosted", "image": "postgres:18.4-alpine",
        "container_id": "c" * 64, "project": "bizzi-ci-1-1", "network": "bizzi-ci-1-1_default",
        "storage_kind": "tmpfs", "system_identifier": "123", "host": "postgres-test",
        "port": 5432, "database": "bizzi_test", "role": "bizzi", "migration_revision": "adw02_02",
        "schema_sha256": SCHEMA_SHA256, "schema_match": True,
        "table_counts": dict.fromkeys(TABLES, 0), "health_status": 200,
        "intake_unavailable": True, "observed_utc": "2026-10-13T00:00:00+00:00",
        "disposal_basis": "github-hosted-vm-platform-disposal",
    }


def test_good_context_schema_and_allowlisted_summary():
    validate_context(context())
    assert canonical_schema(EXPECTED_SCHEMA) == SCHEMA_SHA256
    validate_summary(summary())


@pytest.mark.parametrize("key", list(context()))
def test_missing_or_changed_context_fails(key):
    env = context()
    env.pop(key)
    with pytest.raises(EvidenceRefused):
        validate_context(env)
    env[key] = "unadmitted"
    with pytest.raises(EvidenceRefused):
        validate_context(env)


@pytest.mark.parametrize("key", list(summary()))
def test_any_missing_or_unknown_field_fails(key):
    value = summary()
    value.pop(key)
    with pytest.raises(EvidenceRefused):
        validate_summary(value)
    value = summary()
    value["raw_log"] = "synthetic-secret"
    with pytest.raises(EvidenceRefused):
        validate_summary(value)


@pytest.mark.parametrize("change", ["rows", "schema", "health", "intake", "checkout", "storage"])
def test_adverse_metadata_never_passes(change):
    value = summary()
    if change == "rows":
        value["table_counts"]["audit_records"] = 1
    elif change == "schema":
        value["schema_match"] = False
    elif change == "health":
        value["health_status"] = 500
    elif change == "intake":
        value["intake_unavailable"] = False
    elif change == "checkout":
        value["checkout_sha"] = "d" * 40
    else:
        value["storage_kind"] = "volume"
    with pytest.raises(EvidenceRefused):
        validate_summary(value)


def test_schema_change_changes_digest():
    changed = deepcopy(EXPECTED_SCHEMA)
    changed["indexes"].pop()
    assert canonical_schema(changed) != SCHEMA_SHA256


def test_existing_evidence_root_refuses_before_subprocess(tmp_path, monkeypatch):
    trap = Mock(side_effect=AssertionError("no subprocess"))
    monkeypatch.setattr("tests.ci_compose_verification.subprocess.run", trap)
    with pytest.raises(EvidenceRefused):
        Collector(tmp_path, context())
    trap.assert_not_called()


def test_metadata_client_is_fixed_read_only_tcp(tmp_path, monkeypatch):
    collector = Collector(tmp_path / "fresh", context())
    command = Mock(return_value='[{"system_identifier":"123"}]')
    monkeypatch.setattr(collector, "command", command)
    assert collector.rows("SELECT system_identifier::text FROM pg_control_system()") == [["123"]]
    argv = command.call_args.args[0]
    assert "PGOPTIONS=-c default_transaction_read_only=on" in argv
    assert argv[argv.index("-h") + 1] == "127.0.0.1"
    assert argv[-1].startswith("BEGIN READ ONLY;") and argv[-1].endswith("ROLLBACK;")


def test_shared_volume_is_rejected(tmp_path, monkeypatch):
    collector = Collector(tmp_path / "fresh", context())
    obj = {"Id": "a" * 64, "State": {"Running": True}, "Config": {
        "Image": "postgres:18.4-alpine", "Labels": {
            "com.docker.compose.project": collector.project,
            "com.docker.compose.service": "postgres-test"}},
        "NetworkSettings": {"Networks": {collector.project + "_default": {}}},
        "Mounts": [{"Type": "volume", "Destination": "/var/lib/postgresql"}]}
    monkeypatch.setattr(collector, "command", Mock(side_effect=["a" * 64, json.dumps([obj])]))
    with pytest.raises(EvidenceRefused, match="storage"):
        collector.inspect("postgres-test")


@pytest.mark.parametrize("reason", [
    "context", "checkout", "summary-fields", "summary-value", "rows",
    "fresh-evidence", "command", "metadata", "container", "storage", "destination",
    "fresh-project", "fresh-schema", "schema", "health", "intake",
])
def test_main_emits_only_known_failure_code(reason, tmp_path, monkeypatch, capsys):
    from tests import ci_compose_verification as module

    monkeypatch.setattr(module.sys, "argv", ["collector", "--evidence", str(tmp_path / "fresh")])
    monkeypatch.setattr(module, "Collector", Mock(side_effect=EvidenceRefused(reason)))
    assert module.main() == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {"status": "FAIL", "reason": reason}
    assert captured.err == ""


@pytest.mark.parametrize("exception_type", [EvidenceRefused, RuntimeError])
def test_main_withholds_unknown_exception_url_and_environment(
    exception_type, tmp_path, monkeypatch, capsys,
):
    from tests import ci_compose_verification as module

    secret = "synthetic-private-marker"
    url = "https://synthetic.invalid/private"
    monkeypatch.setenv("SYNTHETIC_PRIVATE_TEST_VALUE", secret)
    monkeypatch.setattr(module.sys, "argv", ["collector", "--evidence", str(tmp_path / "fresh")])
    error = exception_type(f"{url} {secret} arbitrary exception text")
    monkeypatch.setattr(module, "Collector", Mock(side_effect=error))
    assert module.main() == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {"status": "FAIL", "reason": "unexpected"}
    assert captured.err == ""
    assert secret not in captured.out and url not in captured.out
    assert "arbitrary exception text" not in captured.out


def test_public_failure_vocabulary_is_exact():
    from tests.ci_compose_verification import FAILURE_REASONS

    assert FAILURE_REASONS == {
        "context", "checkout", "summary-fields", "summary-value", "rows",
        "fresh-evidence", "command", "metadata", "container", "storage", "destination",
        "fresh-project", "fresh-schema", "schema", "health", "intake",
    }
