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
