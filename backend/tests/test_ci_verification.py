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
    results.extend(_merge_gate_probes(case_root, case, repo, profile, targets))
    (case_root / "PROBE_RESULT.json").write_text(json.dumps(results, indent=2) + "\n")


def _assert_no_observation_override(source):
    import ast

    tree = ast.parse(source)
    expected_env = {"BIZZI_LOCAL_LOCK_BINDING_PATH", "BIZZI_LOCAL_LOCK_BINDING_SHA256",
                    "BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_PATH",
                    "BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256"}
    reads = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if ast.unparse(node.func) == "os.environ.get":
                assert isinstance(node.args[0], ast.Constant)
                reads.add(node.args[0].value)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"eval", "exec", "getattr", "globals", "locals"}
        if isinstance(node, ast.Assign):
            for target in node.targets:
                assert not isinstance(target, ast.Attribute), "runtime observation override"
    assert reads == expected_env, "runtime observation override"
    calls = [ast.unparse(n.func) for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and ast.unparse(n.func).startswith("subprocess.")]
    assert sorted(calls) == ["subprocess.check_output", "subprocess.run"]
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert "subprocess.check_output" in ast.unparse(functions["_git"])
    remote = ast.unparse(functions["_remote_main"])
    assert "https://github.com/ArtheosClub/Bizzi_Project.git" in remote
    assert "credential.helper=" in remote and "timeout=20" in remote
    assert "--no-optional-locks" in remote
    assert "GIT_TERMINAL_PROMPT='0'" in remote


def test_no_runtime_observation_override():
    import hashlib

    root = Path(__file__).resolve().parent.parent
    source_path = root.parent / "backend/tests/test_enterprise_object_repository_lock_local.py"
    source = source_path.read_text()
    _assert_no_observation_override(source)
    with pytest.raises(AssertionError):
        _assert_no_observation_override(source + '\n_override = os.environ.get("FAKE_HEAD")\n')
    (Path(os.environ["BIZZI_EVIDENCE_DIR"]) / "NO_OVERRIDE_RESULT.json").write_text(json.dumps({
        "node": "tests.test_ci_verification::test_no_runtime_observation_override",
        "status": "PASS", "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "limit": "bounded AST check, not a Python sandbox",
    }) + "\n")


MERGE_CASES = {
    "missing-optin": ["mg-missing-optin"],
    "malformed-binding": ["mg-binding-hash", "mg-permission-hash", "mg-binding-occurrence",
        "mg-permission-field", "mg-binding-field", "mg-preparing-id-as-run", "mg-mixed-prefix",
        "mg-mode", "mg-collector", "mg-window", "mg-preparation-id", "mg-preparation-hash",
        "mg-preparation-path", "mg-preparation-field-missing", "mg-preparation-field-duplicate",
        "mg-run-fields", "mg-source-pins", "mg-source-byte", "mg-committed-source",
        "mg-dependency-missing", "mg-dependency-byte", "mg-dependency-committed",
        "mg-tracked", "mg-staged", "mg-untracked", "mg-root-env", "mg-backend-env",
        "mg-remote-timeout", "mg-remote-nonzero", "mg-remote-malformed", "mg-remote-mismatch",
        "mg-index"],
    "expired-binding": ["mg-expired"],
    "other-head": ["mg-head", "mg-tree", "mg-backend-tree", "mg-github-tree",
                   "mg-main", "mg-merge-base"],
    "wrong-profile": ["mg-profile"],
    "wrong-bind": ["mg-bind", "mg-pg-override"],
    "missing-directory": ["mg-directory"],
    "unwritable-directory": ["mg-writable"],
}


def _merge_gate_probes(case_root, case, repo, profile, targets):
    import hashlib
    from datetime import UTC, datetime, timedelta

    prep_id = "MVP-OPTION-L-MERGE-GATE-IMPLEMENTATION-2026-10-10"
    run_id = "MVP-OPTION-L-MERGE-GATE-RUN-synthetic"
    preparation = case_root / "preparation-source.md"
    binding_path, grant_path = case_root / "binding.json", case_root / "owner-grant.md"
    observation_command = [
        "git", "--no-optional-locks", "rev-parse", "HEAD", "HEAD^{tree}",
        "HEAD:backend", "HEAD:.github",
    ]
    if profile != "ci_test":
        observation_command.append("origin/main")
    observations = subprocess.check_output(observation_command, text=True).splitlines()
    if profile == "ci_test":
        # Mock probe input only: shallow CI checkout has no local origin/main.
        # Runtime admission still observes the real ref and remote independently.
        observations.append("f" * 40)
    results = []
    for subcase in MERGE_CASES[case]:
        start = datetime.now(UTC) - timedelta(minutes=1)
        end = datetime.now(UTC) + timedelta(minutes=10)
        preparation.write_text("Preparation permission ID: " + prep_id + "\n")
        if subcase == "mg-preparation-field-missing":
            preparation.write_text("synthetic input without field\n")
        if subcase == "mg-preparation-field-duplicate":
            preparation.write_text(preparation.read_text() * 2)
        binding = {
            "mode": "MERGE_GATE", "collector": "synthetic-probe",
            "preparation_permission_id": prep_id, "preparation_source_path": str(preparation),
            "preparation_source_sha256": hashlib.sha256(preparation.read_bytes()).hexdigest(),
            "base_head": observations[0], "candidate_head": observations[0],
            "candidate_tree": observations[1], "backend_tree": observations[2],
            "github_tree": observations[3], "origin_main": observations[4],
            "merge_base": observations[4],
            "valid_from_utc": start.isoformat(), "valid_until_utc": end.isoformat(),
            "source_sha256_by_path": {
                n: hashlib.sha256((repo / n).read_bytes()).hexdigest() for n in targets},
            "dependency_sha256_by_path": {
                n: hashlib.sha256((repo / n).read_bytes()).hexdigest()
                for n in ("backend/pyproject.toml", "backend/uv.lock")},
            "evidence_dir": str(case_root / "evidence"),
            "ledger_dir": str(case_root / "ledger"), "scratch_dir": str(case_root),
            "allowed_initial_contents": {"evidence_dir": [], "ledger_dir": []},
        }
        if subcase == "mg-preparation-id":
            binding["preparation_permission_id"] = "invalid"
        if subcase == "mg-preparation-hash":
            binding["preparation_source_sha256"] = "0" * 64
        if subcase == "mg-preparation-path":
            binding["preparation_source_path"] = str(case_root / "absent")
        if subcase == "mg-run-fields":
            binding["execution_permission_id"] = "forbidden"
        if subcase == "mg-source-pins":
            binding["source_sha256_by_path"] = {}
        if subcase == "mg-source-byte":
            binding["source_sha256_by_path"][targets[0]] = "0" * 64
        if subcase == "mg-dependency-missing":
            binding.pop("dependency_sha256_by_path")
        if subcase == "mg-dependency-byte":
            binding["dependency_sha256_by_path"]["backend/uv.lock"] = "0" * 64
        for fault, field in [("head", "candidate_head"), ("tree", "candidate_tree"),
                             ("backend-tree", "backend_tree"), ("github-tree", "github_tree"),
                             ("main", "origin_main"), ("merge-base", "merge_base")]:
            if subcase == "mg-" + fault:
                binding[field] = "0" * 40
        if subcase == "mg-expired":
            binding["valid_until_utc"] = start.isoformat()
        if subcase == "mg-directory":
            binding["evidence_dir"] = str(case_root / "absent")
        binding_path.write_text(json.dumps(binding))
        digest = hashlib.sha256(binding_path.read_bytes()).hexdigest()
        grant = (f"Permission ID: {run_id}\nBinding SHA-256: {digest}\nMode: MERGE_GATE\n"
                 f"Collector: synthetic-probe\nValid from UTC: {binding['valid_from_utc']}\n"
                 f"Valid until UTC: {binding['valid_until_utc']}\n")
        for fault, old, new in [
            ("mg-preparing-id-as-run", run_id, prep_id),
            ("mg-mixed-prefix", run_id, "MVP-OPTION-L-WORKTREE-VALIDATION-synthetic"),
            ("mg-mode", "Mode: MERGE_GATE", "Mode: WORKTREE_VALIDATION"),
            ("mg-collector", "Collector: synthetic-probe", "Collector: mismatch"),
            ("mg-window", "Valid from UTC: " + binding["valid_from_utc"],
             "Valid from UTC: invalid"),
        ]:
            if subcase == fault:
                grant = grant.replace(old, new)
        if subcase == "mg-binding-occurrence":
            grant += digest
        if subcase == "mg-permission-field":
            grant += "Collector: duplicate\n"
        if subcase == "mg-binding-field":
            grant = grant.replace(digest, "0" * 64) + "Note: " + digest + "\n"
        grant_path.write_text(grant)
        env = dict(os.environ, BIZZI_LOCAL_LOCK_BINDING_PATH=str(binding_path),
                   BIZZI_LOCAL_LOCK_BINDING_SHA256=digest,
                   BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_PATH=str(grant_path),
                   BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256=
                       hashlib.sha256(grant_path.read_bytes()).hexdigest(),
                   DATABASE_URL="postgresql+psycopg://bizzi@localhost:5433/bizzi_test")
        if subcase == "mg-missing-optin":
            env.pop("BIZZI_LOCAL_LOCK_BINDING_PATH")
        if subcase == "mg-binding-hash":
            env["BIZZI_LOCAL_LOCK_BINDING_SHA256"] = "0" * 64
        if subcase == "mg-permission-hash":
            env["BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256"] = "0" * 64
        if subcase == "mg-profile":
            env["SYNTHETIC_EXECUTION_PROFILE"] = "ci_test"
        if subcase == "mg-bind":
            env["DATABASE_URL"] = "postgresql+psycopg://bizzi@remote:5433/bizzi_test"
        if subcase == "mg-pg-override":
            env["PGHOST"] = "synthetic-invalid"
        code = r"""
import json,os,runpy,sys,subprocess
from pathlib import Path
import sqlalchemy
from sqlalchemy.engine import Engine
fault=sys.argv[2]
values=json.loads(sys.argv[3])
repo=Path(sys.argv[1]).parents[2]
counts={"create_engine":0,"connect":0,"remote_calls":0}
def trap(name):
 def refuse(*a,**k):
  counts[name]+=1
  raise AssertionError("connection trap")
 return refuse
sqlalchemy.create_engine=trap("create_engine")
Engine.connect=trap("connect")
# These replacements exist only in this probe child, never in runtime source.
def git_observation(args,**kwargs):
 assert args[:2]==["git","--no-optional-locks"]
 command=args[2:]
 if command==["rev-parse","HEAD"]: return (values[0]+"\n").encode()
 if command and command[0] in ("diff","ls-files"):
  active=(fault=="mg-tracked" and "--cached" not in command and command[0]=="diff"
          or fault=="mg-staged" and "--cached" in command
          or fault=="mg-untracked" and command[0]=="ls-files")
  return b"backend/synthetic.py\n" if active else b""
 if command[0]=="show":
  name=command[1].split(":",1)[1]
  if fault=="mg-committed-source" and name.startswith("backend/tests/"):return b"changed"
  if fault=="mg-dependency-committed" and name=="backend/uv.lock":return b"changed"
  return (repo/name).read_bytes()
 if command[0]=="merge-base":return (values[4]+"\n").encode()
 if command[0]=="rev-parse":return ("\n".join(values[1:])+"\n").encode()
 raise AssertionError("unexpected observation command")
def remote_observation(args,**kwargs):
 counts["remote_calls"]+=1
 assert args==["git","--no-optional-locks","-c","credential.helper=","ls-remote",
               "--exit-code","https://github.com/ArtheosClub/Bizzi_Project.git","refs/heads/main"]
 assert kwargs["timeout"]==20 and kwargs["env"]["GIT_TERMINAL_PROMPT"]=="0"
 if fault=="mg-remote-timeout":raise subprocess.TimeoutExpired(args,20)
 main="0"*40 if fault=="mg-remote-mismatch" else values[4]
 out="malformed" if fault=="mg-remote-malformed" else main+"\trefs/heads/main\n"
 return subprocess.CompletedProcess(args,1 if fault=="mg-remote-nonzero" else 0,out,"")
subprocess.check_output=git_observation
subprocess.run=remote_observation
if fault in ("mg-root-env","mg-backend-env"):
 original=Path.exists
 target=repo/(".env" if fault=="mg-root-env" else "backend/.env")
 Path.exists=lambda p: True if p==target else original(p)
if fault=="mg-writable":os.access=lambda *a,**k: False
if fault=="mg-index":
 original=Path.stat
 index=repo/".git/index"
 calls=0
 def changed(p,*a,**k):
  global calls
  result=original(p,*a,**k)
  if p==index:
   calls+=1
   if calls>1:
    class Stat:
     st_size=result.st_size+1
     st_mtime_ns=result.st_mtime_ns
    return Stat()
  return result
 Path.stat=changed
try:runpy.run_path(sys.argv[1])
except Exception as exc:
 message=str(exc)
 reason=message.split(":",1)[1] if message.startswith("LOCAL_ADMISSION_REFUSED:") else "refusal"
 print(json.dumps({"status":"refused","reason":reason,**counts}))
else:print(json.dumps({"status":"unexpected-success",**counts}))
"""
        child = subprocess.run([sys.executable, "-c", code,
                               str(repo / LOCAL_FILE.replace("tests/", "backend/tests/", 1)),
                               subcase, json.dumps(observations)],
                              env=env, capture_output=True, text=True)
        value = json.loads(child.stdout)
        mapped = {
            "preparing-id-as-run": "permission-id", "mixed-prefix": "permission-id",
            "preparation-id": "preparation", "preparation-hash": "preparation",
            "preparation-path": "preparation", "preparation-field-missing": "preparation-field",
            "preparation-field-duplicate": "preparation-field", "run-fields": "binding-run-fields",
            "source-byte": "source-pins", "dependency-missing": "dependency",
            "dependency-byte": "dependency", "dependency-committed": "dependency",
            "tracked": "clean-tree", "staged": "clean-tree", "untracked": "clean-tree",
            "root-env": "env-file", "backend-env": "env-file", "backend-tree": "tree",
            "github-tree": "tree", "main": "main-base", "merge-base": "main-base",
            "remote-timeout": "remote-main", "remote-nonzero": "remote-main",
            "remote-malformed": "remote-main", "remote-mismatch": "remote-main",
            "pg-override": "bind",
        }
        expected = mapped.get(subcase[3:], subcase[3:])
        later = subcase not in {"mg-missing-optin", "mg-binding-hash", "mg-permission-hash",
            "mg-binding-occurrence", "mg-permission-field", "mg-binding-field",
            "mg-preparing-id-as-run", "mg-mixed-prefix", "mg-mode", "mg-collector", "mg-window",
            "mg-preparation-id", "mg-run-fields", "mg-source-pins", "mg-source-byte",
            "mg-expired", "mg-head", "mg-bind", "mg-pg-override"}
        short_circuit = profile == "ci_test" and later
        if short_circuit:
            expected = "profile"
        assert value["status"] == "refused" and value["reason"] == expected
        assert value["create_engine"] == value["connect"] == 0
        assert not (case_root / "evidence/LOCAL_ADMISSION.json").exists()
        assert not (case_root / "ledger/LOCAL_ADMISSION.json").exists()
        results.append({"check": subcase, "case": case, "expected_reason": expected,
                        "short_circuit": short_circuit,
                        "local_counterpart": subcase if short_circuit else None, **value})
    return results


def test_compose_verifier_is_in_full_partition():
    root = Path(__file__).resolve().parent.parent
    inventory = json.loads((root / "tests/ci_test_inventory.json").read_text())
    assert inventory["files"].count("tests/test_ci_compose_verification.py") == 1
    assert "tests/test_enterprise_object_service_persistence.py" in inventory["files"]
    assert LOCAL_FILE not in inventory["files"]


@pytest.mark.parametrize("case", ADMISSION_CASES)
def test_ci_admission_probes_need_no_remote_tracking_ref(probe_dir, monkeypatch, case):
    check_output = subprocess.check_output

    def shallow_checkout(command, **kwargs):
        assert "origin/main" not in command
        return check_output(command, **kwargs)

    monkeypatch.setattr(subprocess, "check_output", shallow_checkout)
    monkeypatch.setenv("SYNTHETIC_EXECUTION_PROFILE", "ci_test")
    monkeypatch.setenv("BIZZI_EVIDENCE_DIR", str(probe_dir))
    # Run every existing adverse case; child connection/remote calls stay trapped.
    test_local_admission_negative_subprocesses(case)
