"""Reporter/validator evidence uses isolated synthetic subprocess probes only."""

import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tests.ci_verification import RunSummary, validate


@pytest.fixture
def probe_dir():
    root = Path(os.environ["BIZZI_EVIDENCE_DIR"])
    with TemporaryDirectory(prefix="reporter-probe-", dir=root) as directory:
        yield Path(directory)


def report_files(path):
    report = asdict(RunSummary(
        collected=["tests/test_probe.py::test_ok"],
        completed=["tests/test_probe.py::test_ok"],
        files=["tests/test_probe.py"], exit_code=0,
    ))
    summary = path / "summary.json"
    junit = path / "junit.xml"
    inventory = path / "inventory.json"
    summary.write_text(json.dumps(report))
    junit.write_text('<testsuites><testsuite><testcase name="test_ok"/></testsuite></testsuites>')
    inventory.write_text(json.dumps({"files": ["tests/test_probe.py"]}))
    return summary, junit, inventory, report


def test_valid_complete_report(probe_dir):
    summary, junit, inventory, _ = report_files(probe_dir)
    validate(summary, junit, inventory)


@pytest.mark.parametrize(
    "key", ["failed", "errors", "skipped", "xfailed", "xpassed", "deselected", "exit_code"]
)
def test_adverse_result_rejected(probe_dir, key):
    summary, junit, inventory, report = report_files(probe_dir)
    report[key] = 1
    summary.write_text(json.dumps(report))
    with pytest.raises(ValueError):
        validate(summary, junit, inventory)


@pytest.mark.parametrize(
    "case",
    ["missing", "malformed", "duplicate", "incomplete", "inventory", "junit", "head",
     "keyword", "marker"],
)
def test_incomplete_evidence_rejected(probe_dir, case):
    summary, junit, inventory, report = report_files(probe_dir)
    if case == "missing":
        summary.unlink()
    elif case == "malformed":
        summary.write_text("{")
    elif case == "duplicate":
        report["completed"] *= 2
    elif case == "incomplete":
        report["completed"] = []
    elif case == "inventory":
        inventory.write_text(json.dumps({"files": ["tests/test_other.py"]}))
    elif case == "junit":
        junit.write_text('<testsuites><testcase><skipped/></testcase></testsuites>')
    elif case == "keyword":
        report["keyword"] = "ok"
    elif case == "marker":
        report["marker"] = "unit"
    if case not in {"missing", "malformed"}:
        summary.write_text(json.dumps(report))
    with pytest.raises((ValueError, OSError)):
        validate(summary, junit, inventory, "a" * 40 if case == "head" else None)


def test_validator_module_has_no_database_or_conftest_import(probe_dir):
    summary, junit, inventory, _ = report_files(probe_dir)
    code = '''
import runpy,sys
from sqlalchemy.engine import Engine
Engine.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("connection forbidden"))
try:
 runpy.run_module("tests.ci_verification",run_name="__main__")
except SystemExit as error:
 assert not any(n == "app" or n.startswith("app.") or n.endswith("conftest") for n in sys.modules)
 raise error
'''
    env = dict(os.environ, DATABASE_URL="invalid", SYNTHETIC_EXECUTION_PROFILE="disabled")
    args = [sys.executable, "-c", code, "--summary", str(summary),
            "--junit", str(junit), "--inventory", str(inventory)]
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    assert result.returncode == 0
    args = [sys.executable, "-m", "tests.ci_verification", "--summary",
            str(probe_dir / "absent"), "--junit", str(junit), "--inventory", str(inventory)]
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    assert result.returncode == 1
    assert "invalid" not in result.stdout


@pytest.mark.parametrize("case", ["pass", "fail", "skip", "xfail", "xpass", "deselect"])
def test_real_reporting_hooks_on_isolated_probes(probe_dir, case):
    bodies = {
        "pass": "def test_probe(): assert True\n",
        "fail": "def test_probe(): assert False\n",
        "skip": "import pytest\ndef test_probe(): pytest.skip('synthetic probe')\n",
        "xfail": "import pytest\n@pytest.mark.xfail\ndef test_probe(): assert False\n",
        "xpass": "import pytest\n@pytest.mark.xfail\ndef test_probe(): assert True\n",
        "deselect": "def test_probe(): assert True\n",
    }
    test_file = probe_dir / "test_probe.py"
    test_file.write_text(bodies[case])
    summary, junit = probe_dir / "report.json", probe_dir / "junit.xml"
    inventory = probe_dir / "inventory.json"
    inventory.write_text(json.dumps({"files": ["test_probe.py"]}))
    env = dict(os.environ, BIZZI_REPORT_PATH=str(summary), DATABASE_URL="invalid")
    args = [sys.executable, "-m", "pytest", "-p", "tests.ci_verification", "-p", "no:cacheprovider",
            "--confcutdir", str(probe_dir), "--rootdir", str(probe_dir),
            "--junitxml", str(junit), str(test_file)]
    if case == "deselect":
        args += ["--deselect", "test_probe.py::test_probe"]
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    assert summary.exists()
    metadata = json.loads(summary.read_text())
    evidence = {
        "probe": case, "exit_code": result.returncode,
        "counts": {key: metadata[key] for key in
                   ("failed", "errors", "skipped", "xfailed", "xpassed", "deselected")},
        "type": "isolated synthetic probe, not backend acceptance",
    }
    with (Path(os.environ["BIZZI_EVIDENCE_DIR"]) / "REPORTER_PROBES.jsonl").open("a") as log:
        log.write(json.dumps(evidence) + "\n")
    if case == "pass":
        validate(summary, junit, inventory)
    else:
        with pytest.raises(ValueError):
            validate(summary, junit, inventory)


LOCAL_FILE = "tests/test_enterprise_object_repository_lock_local.py"
DECISION_SHA = "0123ced0601f832838cc0d0ccc4ab0c9a13c1bccdea30091d8b1e18b76d149b3"


def _partition(root, inventory, manifest):
    files = inventory["files"]
    local = manifest["files"]
    assert local == [LOCAL_FILE], "local-filename"
    assert manifest["owner_decision_id"] == "Owner record L", "decision-metadata"
    assert manifest["owner_decision_source_sha256"] == DECISION_SHA, "decision-metadata"
    assert len(files) == len(set(files)) and not set(files) & set(local)
    for name in files + local:
        assert ".." not in Path(name).parts and not Path(name).is_absolute(), "path-traversal"
    corpus = set()
    for path in (root / "tests").rglob("test_*.py"):
        assert (
            path.is_file() and (root / "tests").resolve() in path.resolve().parents
        ), "symlink-escape"
        corpus.add(path.relative_to(root).as_posix())
    assert set(files) | set(local) == corpus
    for name in files + local:
        assert ".." not in Path(name).parts and not Path(name).is_absolute()
    return {"CI_files": sorted(files), "local_only": local, "decision": "Owner record L"}


def test_repository_partition_matches_declared_venues():
    root = Path(__file__).resolve().parent.parent
    result = _partition(root, json.loads((root / "tests/ci_test_inventory.json").read_text()),
                        json.loads((root / "tests/local_only_manifest.json").read_text()))
    assert len(result["local_only"]) == 1
    destination = Path(os.environ["BIZZI_EVIDENCE_DIR"]) / "PARTITION_RESULT.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")


@pytest.mark.parametrize("case", [
    "good", "missing", "extra", "overlap", "duplicate", "wrong-metadata",
    "wrong-local-filename", "path-traversal", "symlink-escape",
])
def test_partition_negative_cases(probe_dir, case):
    root = probe_dir / "partition"
    tests = root / "tests"
    tests.mkdir(parents=True)
    (tests / "test_ci_verification.py").write_text("")
    (root / LOCAL_FILE).write_text("")
    inventory = {"files": ["tests/test_ci_verification.py"]}
    manifest = {"files": [LOCAL_FILE], "owner_decision_id": "Owner record L",
                "owner_decision_source_sha256": DECISION_SHA}
    if case == "missing":
        (tests / "test_ci_verification.py").unlink()
    if case == "extra":
        (tests / "test_extra.py").write_text("")
    if case == "overlap":
        inventory["files"].append(LOCAL_FILE)
    if case == "duplicate":
        inventory["files"] *= 2
    expected_reason = None
    if case == "wrong-metadata":
        manifest["owner_decision_source_sha256"] = "0" * 64
        expected_reason = "decision-metadata"
    if case == "wrong-local-filename":
        manifest["files"] = ["tests/test_other_local.py"]
        expected_reason = "local-filename"
    if case == "path-traversal":
        inventory["files"] = ["tests/../tests/test_ci_verification.py"]
        expected_reason = "path-traversal"
    if case == "symlink-escape":
        outside = probe_dir / "outside.py"
        outside.write_text("")
        (tests / "test_escape.py").symlink_to(outside)
        expected_reason = "symlink-escape"
    if case == "good":
        _partition(root, inventory, manifest)
    else:
        with pytest.raises(AssertionError, match=expected_reason):
            _partition(root, inventory, manifest)


ADMISSION_CASES = {
    "missing-optin": ["missing-optin"],
    "malformed-binding": ["binding-hash", "permission-hash", "malformed-binding",
        "binding-absent", "binding-duplicate", "permission-field", "binding-field",
        "permission-id", "mode", "collector", "window", "preparation", "run-fields",
        "source-pins", "source-byte", "preparation-id", "preparation-path"],
    "expired-binding": ["expired"],
    "other-head": ["head"],
    "wrong-profile": ["profile"],
    "wrong-bind": ["bind"],
    "missing-directory": ["directory"],
    "unwritable-directory": ["writable"],
}


@pytest.mark.parametrize("case", ADMISSION_CASES)
def test_local_admission_negative_subprocesses(case):
    import hashlib
    from datetime import UTC, datetime, timedelta

    root = Path(__file__).resolve().parent.parent
    profile = os.environ.get("SYNTHETIC_EXECUTION_PROFILE")
    preparation_path = os.environ.get("BIZZI_LOCAL_LOCK_PREPARATION_PROBE_SOURCE_PATH")
    if profile != "ci_test":
        assert preparation_path, "local preparation probe input is required"
    scratch = Path(os.environ["BIZZI_EVIDENCE_DIR"])
    case_root = scratch / "admission-probes" / case
    case_root.mkdir(parents=True, exist_ok=False)
    evidence, ledger = case_root / "evidence", case_root / "ledger"
    evidence.mkdir()
    ledger.mkdir()
    bind_path, grant_path = case_root / "binding.json", case_root / "owner-grant.md"
    head = subprocess.check_output(
        ["git", "--no-optional-locks", "rev-parse", "HEAD"], text=True
    ).strip()
    targets = ["backend/tests/test_enterprise_object_service_persistence.py",
               "backend/tests/test_enterprise_object_repository_lock_local.py",
               "backend/tests/local_only_manifest.json", "backend/tests/test_ci_verification.py",
               ".github/workflows/backend-ci.yml"]
    repo = root.parent
    results = []
    for subcase in ADMISSION_CASES[case]:
        start = datetime.now(UTC) - timedelta(minutes=1)
        end = datetime.now(UTC) + timedelta(minutes=10)
        binding = {
            "preparation_permission_id": "MVP-OPTION-L-IMPLEMENTATION-2026-10-08",
            "preparation_source_path": preparation_path or str(case_root / "absent-preparation"),
            "preparation_source_sha256":
                "c758a1a01725262dc89e1c03d09df250d73dc0c741565e8bb1f2ff2b905f7fb9",
            "collector": "synthetic-probe", "mode": "WORKTREE_VALIDATION",
            "valid_from_utc": start.isoformat(), "valid_until_utc": end.isoformat(),
            "base_head": head, "candidate_head": head,
            "source_sha256_by_path": {
                name: hashlib.sha256((repo / name).read_bytes()).hexdigest() for name in targets
            },
            "evidence_dir": str(evidence), "ledger_dir": str(ledger),
            "scratch_dir": str(case_root),
            "allowed_initial_contents": {"evidence_dir": [], "ledger_dir": []},
        }
        if subcase == "expired":
            binding["valid_until_utc"] = (start + timedelta(seconds=1)).isoformat()
        if subcase == "head":
            binding["candidate_head"] = "0" * 40
        if subcase == "preparation":
            binding["preparation_source_sha256"] = "0" * 64
        if subcase == "run-fields":
            binding["execution_permission_id"] = "forbidden"
        if subcase == "source-pins":
            binding["source_sha256_by_path"] = {}
        if subcase == "source-byte":
            binding["source_sha256_by_path"][targets[0]] = "0" * 64
        if subcase == "preparation-id":
            binding["preparation_permission_id"] = "invalid"
        if subcase == "preparation-path":
            binding["preparation_source_path"] = str(grant_path)
        if subcase == "directory":
            binding["evidence_dir"] = str(case_root / "absent")
        bind_path.write_text(json.dumps(binding))
        if subcase == "malformed-binding":
            bind_path.write_text("{")
        digest = hashlib.sha256(bind_path.read_bytes()).hexdigest()
        grant = ("Permission ID: MVP-OPTION-L-WORKTREE-VALIDATION-synthetic\n"
                 + "Binding SHA-256: " + digest + "\n"
                 + "Mode: WORKTREE_VALIDATION\nCollector: synthetic-probe\n"
                 + "Valid from UTC: " + binding["valid_from_utc"] + "\n"
                 + "Valid until UTC: " + binding["valid_until_utc"] + "\n")
        if subcase == "binding-absent":
            grant = grant.replace(digest, "0" * 64)
        if subcase == "binding-duplicate":
            grant += digest
        if subcase == "permission-field":
            grant += "Collector: duplicated\n"
        if subcase == "binding-field":
            grant = grant.replace(digest, "0" * 64) + "Note: " + digest + "\n"
        if subcase == "permission-id":
            grant = grant.replace("MVP-OPTION-L-WORKTREE-VALIDATION-synthetic",
                                  "MVP-OPTION-L-IMPLEMENTATION-2026-10-08")
        if subcase == "mode":
            grant = grant.replace("Mode: WORKTREE_VALIDATION", "Mode: invalid")
        if subcase == "collector":
            grant = grant.replace("Collector: synthetic-probe", "Collector: mismatch")
        if subcase == "window":
            grant = grant.replace("Valid from UTC: " + binding["valid_from_utc"],
                                  "Valid from UTC: mismatched")
        grant_path.write_text(grant)
        env = dict(os.environ,
                   BIZZI_LOCAL_LOCK_BINDING_PATH=str(bind_path),
                   BIZZI_LOCAL_LOCK_BINDING_SHA256=digest,
                   BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_PATH=str(grant_path),
                   BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256=
                       hashlib.sha256(grant_path.read_bytes()).hexdigest(),
                   DATABASE_URL="postgresql+psycopg://bizzi@localhost:5433/bizzi_test")
        if subcase == "missing-optin":
            env.pop("BIZZI_LOCAL_LOCK_BINDING_PATH")
        if subcase == "binding-hash":
            env["BIZZI_LOCAL_LOCK_BINDING_SHA256"] = "0" * 64
        if subcase == "permission-hash":
            env["BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256"] = "0" * 64
        if subcase == "profile":
            env["SYNTHETIC_EXECUTION_PROFILE"] = "ci_test"
        if subcase == "bind":
            env["DATABASE_URL"] = "postgresql+psycopg://bizzi@remote:5433/bizzi_test"
        code = r"""
import json,os,runpy,sys
import sqlalchemy
from sqlalchemy.engine import Engine
counts={"create_engine":0,"connect":0}
def trap(name):
 def refused(*a,**k):
  counts[name]+=1
  raise AssertionError("connection trap")
 return refused
sqlalchemy.create_engine=trap("create_engine")
Engine.connect=trap("connect")
if sys.argv[2]=="writable":
 os.access=lambda *a,**k: False
try:
 runpy.run_path(sys.argv[1])
except Exception as exc:
 message=str(exc)
 reason=message.split(":",1)[1] if message.startswith("LOCAL_ADMISSION_REFUSED:") else "refusal"
 print(json.dumps({"status":"refused","reason":reason,**counts}))
else:
 print(json.dumps({"status":"unexpected-success",**counts}))
"""
        child = subprocess.run([sys.executable, "-c", code, str(repo / LOCAL_FILE.replace(
            "tests/", "backend/tests/", 1)), subcase], env=env, capture_output=True, text=True)
        value = json.loads(child.stdout)
        reasons = {
            "binding-absent": "binding-occurrence", "binding-duplicate": "binding-occurrence",
            "run-fields": "binding-run-fields", "source-byte": "source-pins",
            "preparation-id": "preparation", "preparation-path": "preparation",
        }
        expected_reason = reasons.get(subcase, subcase)
        short_circuit = profile == "ci_test" and subcase in (
            "preparation-path", "directory", "writable"
        )
        if short_circuit:
            expected_reason = "profile"
        assert value["status"] == "refused"
        assert value["reason"] == expected_reason
        assert value["create_engine"] == value["connect"] == 0
        assert not list(evidence.glob("LOCAL_ADMISSION.json"))
        assert not list(ledger.glob("LOCAL_ADMISSION.json"))
        results.append({"check": subcase, "case": case, "expected_reason": expected_reason,
                        "short_circuit": short_circuit,
                        "local_counterpart": subcase if short_circuit else None, **value})
    (case_root / "PROBE_RESULT.json").write_text(json.dumps(results, indent=2) + "\n")
