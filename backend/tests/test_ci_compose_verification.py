"""Pure synthetic probes; never invoke Docker, HTTP or a database in these tests."""

import json
from copy import deepcopy
from unittest.mock import MagicMock, Mock
from urllib.error import HTTPError

import pytest

from tests.ci_compose_verification import (
    EXPECTED_SCHEMA,
    QUERIES,
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
        "push_before": None, "push_after": None, "push_forced": None, "push_deleted": None,
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


@pytest.fixture
def mocked_collection(tmp_path, monkeypatch):
    collector = Collector(tmp_path / "fresh", context())
    state = {"migrated": False, "address": [["127.0.0.1", 5432]],
             "identity": [["bizzi_test", "bizzi"]], "system": "123",
             "schema": deepcopy(EXPECTED_SCHEMA), "rows": 0,
             "health": 200, "intake": 404}

    def command(argv, **kwargs):
        if argv == ["git", "--no-optional-locks", "rev-parse", "HEAD"]:
            return "a" * 40
        if argv == ["git", "--no-optional-locks", "rev-parse", "HEAD^{tree}"]:
            return "b" * 40
        if argv == ["git", "--no-optional-locks", "diff", "--exit-code", "HEAD", "--"]:
            return ""
        assert argv[:len(collector.prefix)] == collector.prefix
        if "api" in argv:
            state["migrated"] = True
        return ""

    def rows(statement):
        if statement == QUERIES["tables"]:
            return [[v] for v in state["schema"]["tables"]] if state["migrated"] else []
        if statement == QUERIES["identity"]:
            return state["identity"]
        if statement == QUERIES["psql_address"]:
            return state["address"]
        if statement == QUERIES["system_identifier"]:
            return [[state["system"]]]
        for key in ("columns", "indexes", "foreign_keys"):
            if statement == QUERIES[key]:
                return state["schema"][key]
        if statement == QUERIES["revisions"]:
            return [[v] for v in state["schema"]["revisions"]]
        assert statement in {"SELECT count(*) FROM " + name for name in TABLES}
        return [[state["rows"]]]

    def http(request, **kwargs):
        if isinstance(request, str):
            assert request == "http://127.0.0.1:8000/health"
            response = MagicMock()
            response.__enter__.return_value = response
            response.status = state["health"]
            response.read.return_value = b'{"status":"ok"}'
            return response
        assert request.full_url == "http://127.0.0.1:8000/business-requests"
        raise HTTPError(request.full_url, state["intake"], "synthetic", None, None)

    monkeypatch.setattr(collector, "command", Mock(side_effect=command))
    monkeypatch.setattr(collector, "rows", Mock(side_effect=rows))
    monkeypatch.setattr(collector, "inspect", Mock(return_value={"Id": "c" * 64}))
    monkeypatch.setattr("tests.ci_compose_verification.urlopen", Mock(side_effect=http))
    return collector, state


def test_psql_address_query_uses_host_without_netmask():
    # This pins the SQL interface that the former mocked scalar test missed.
    assert QUERIES["psql_address"] == "SELECT host(inet_server_addr()), inet_server_port()"


def test_complete_mocked_collection_checks_schema_health_and_intake(mocked_collection):
    collector, _ = mocked_collection
    result = collector.collect()
    validate_summary(result)
    assert json.loads((collector.root / "PUBLIC_SUMMARY.json").read_text()) == result
    assert result["host"] == "postgres-test" and result["port"] == 5432
    assert result["schema_match"] and result["table_counts"] == dict.fromkeys(TABLES, 0)


@pytest.mark.parametrize("case,reason", [
    ("identity", "destination"), ("address", "destination"),
    ("schema", "schema"), ("rows", "rows"), ("health", "health"), ("intake", "intake"),
])
def test_collection_preserves_adverse_findings(mocked_collection, case, reason):
    collector, state = mocked_collection
    if case == "identity":
        state["identity"] = [["other", "bizzi"]]
    elif case == "address":
        state["address"] = [["10.0.0.1", 5432]]
    elif case == "schema":
        state["schema"]["indexes"].pop()
    elif case == "rows":
        state["rows"] = 1
    elif case == "health":
        state["health"] = 503
    else:
        state["intake"] = 200
    with pytest.raises(EvidenceRefused, match="^" + reason + "$"):
        collector.collect()
    assert not (collector.root / "PUBLIC_SUMMARY.json").exists()


@pytest.mark.parametrize("address", [
    [["127.0.0.1/32", 5432]], [["10.0.0.1", 5432]], [["127.0.0.1", 5433]],
])
def test_psql_destination_acceptance_is_not_widened(mocked_collection, address):
    collector, state = mocked_collection
    state["address"] = address
    with pytest.raises(EvidenceRefused, match="^destination$"):
        collector.collect()
    assert not state["migrated"]


@pytest.mark.parametrize("empty", [False, True])
def test_push_context_and_public_report_have_no_pr_number(empty):
    from tests.test_preproduction_guard import push_context

    env = push_context("compose-e2e", empty=empty)
    env.update(GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="1")
    validate_context(env)
    value = summary()
    value.update(event="push", pr=None, push_before="b" * 40,
                 push_after="a" * 40, push_forced=True, push_deleted=False)
    validate_summary(value)
    assert value["push_forced"] is True


@pytest.mark.parametrize("key,value", [
    ("BIZZI_PR_HEAD_SHA", ""), ("BIZZI_PR_HEAD_REPOSITORY", ""),
    ("GITHUB_BASE_REF", "main"), ("GITHUB_SHA", "d" * 40),
    ("BIZZI_PUSH_DELETED", "true"), ("BIZZI_PUSH_FORCED", "False"),
    ("GITHUB_REF", "refs/tags/main"), ("GITHUB_JOB", "backend"),
])
def test_push_collector_refuses_mixed_or_legacy_context(key, value):
    from tests.test_preproduction_guard import push_context

    env = push_context("compose-e2e")
    env.update(GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="1")
    env[key] = value
    with pytest.raises(EvidenceRefused):
        validate_context(env)


@pytest.mark.parametrize("key,value", [
    ("pr", 0), ("push_before", "bad"), ("push_after", "c" * 40),
    ("push_forced", "false"), ("push_deleted", True), ("event", "workflow_dispatch"),
])
def test_push_report_refuses_wrong_types_or_invented_pr(key, value):
    data = summary()
    data.update(event="push", pr=None, push_before="b" * 40,
                push_after="a" * 40, push_forced=False, push_deleted=False)
    data[key] = value
    with pytest.raises(EvidenceRefused):
        validate_summary(data)


def test_full_mocked_push_collection_reports_native_flags(mocked_collection):
    from tests.test_preproduction_guard import push_context

    collector, _ = mocked_collection
    env = push_context("compose-e2e")
    env.update(GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="1")
    collector.context = validate_context(env)
    collector.env = env
    result = collector.collect()
    assert result["event"] == "push" and result["pr"] is None
    assert result["push_before"] == "b" * 40 and result["push_after"] == "a" * 40
    assert result["push_forced"] is False and result["push_deleted"] is False
