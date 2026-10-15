"""Metadata-only pytest reporting and validation; no application or DB imports."""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import cast

import pytest


@dataclass
class RunSummary:
    collected: list[str] = field(default_factory=list)
    completed: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    xfailed: int = 0
    xpassed: int = 0
    deselected: int = 0
    warnings: int = 0
    exit_code: int = -1
    arguments: list[str] = field(default_factory=list)
    addopts: list[str] = field(default_factory=list)
    keyword: str = ""
    marker: str = ""
    checkout_sha: str = ""
    event_head_sha: str = ""
    event: str = ""
    push_before: str | None = None
    push_after: str | None = None
    push_forced: bool | None = None
    push_deleted: bool | None = None


def event_metadata(env: dict[str, str]) -> dict[str, object]:
    if any(key in env for key in ("BIZZI_PR_HEAD_SHA", "BIZZI_PR_HEAD_REPOSITORY")):
        raise ValueError("Legacy event input refused")
    event = env.get("GITHUB_EVENT_NAME", "")
    if event not in {"", "pull_request", "push"}:
        raise ValueError("Unknown event")
    values: dict[str, object] = {"event": event, "push_before": None,
        "push_after": None, "push_forced": None, "push_deleted": None}
    names = ("BIZZI_PUSH_BEFORE", "BIZZI_PUSH_AFTER", "BIZZI_PUSH_FORCED", "BIZZI_PUSH_DELETED")
    if event == "push":
        head = env.get("BIZZI_EVENT_HEAD_SHA", "")
        if (env.get("GITHUB_REF") != "refs/heads/main"
            or re.fullmatch(r"[0-9a-f]{40}", head) is None
            or env.get("GITHUB_SHA") != head or env.get("BIZZI_PUSH_AFTER") != head
            or re.fullmatch(r"[0-9a-f]{40}", env.get("BIZZI_PUSH_BEFORE", "")) is None
            or env.get("BIZZI_PUSH_FORCED") not in {"true", "false"}
            or env.get("BIZZI_PUSH_DELETED") != "false"):
            raise ValueError("Invalid push metadata")
        values.update(push_before=env["BIZZI_PUSH_BEFORE"], push_after=head,
                      push_forced=env["BIZZI_PUSH_FORCED"] == "true", push_deleted=False)
    elif any(env.get(name) for name in names):
        raise ValueError("Mixed event metadata")
    return values


_summary: RunSummary | None = None


def pytest_configure(config: pytest.Config) -> None:
    global _summary
    metadata = event_metadata(dict(os.environ))
    _summary = RunSummary(
        arguments=list(config.invocation_params.args),
        addopts=list(config.getini("addopts")),
        keyword=str(config.option.keyword),
        marker=str(config.option.markexpr),
        checkout_sha=os.environ.get("BIZZI_CHECKOUT_SHA", ""),
        event_head_sha=os.environ.get("BIZZI_EVENT_HEAD_SHA", ""),
        event=str(metadata["event"]),
        push_before=cast(str | None, metadata["push_before"]),
        push_after=cast(str | None, metadata["push_after"]),
        push_forced=cast(bool | None, metadata["push_forced"]),
        push_deleted=cast(bool | None, metadata["push_deleted"]),
    )


def pytest_collection_finish(session: pytest.Session) -> None:
    if _summary is not None:
        _summary.collected = [item.nodeid for item in session.items]
        _summary.files = sorted({item.nodeid.split("::", 1)[0] for item in session.items})


def pytest_collectreport(report: pytest.CollectReport) -> None:
    if _summary is not None:
        if report.failed:
            _summary.errors += 1
        elif report.skipped:
            _summary.skipped += 1


def pytest_deselected(items: list[pytest.Item]) -> None:
    if _summary is not None:
        _summary.deselected += len(items)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if _summary is None:
        return
    xfail = hasattr(report, "wasxfail")
    if xfail and report.skipped:
        _summary.xfailed += 1
    elif xfail and report.passed:
        _summary.xpassed += 1
    elif report.skipped:
        _summary.skipped += 1
    elif report.failed:
        if report.when == "call":
            _summary.failed += 1
        else:
            _summary.errors += 1
    if report.when == "teardown":
        _summary.completed.append(report.nodeid)


def pytest_warning_recorded() -> None:
    if _summary is not None:
        _summary.warnings += 1


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if _summary is not None:
        _summary.exit_code = int(exitstatus)
        destination = os.environ.get("BIZZI_REPORT_PATH")
        if destination:
            Path(destination).write_text(json.dumps(asdict(_summary), indent=2) + "\n")


def inventory_files(path: Path) -> list[str]:
    value = json.loads(path.read_text())
    files = value.get("files") if isinstance(value, dict) else None
    if (
        not isinstance(files, list)
        or not files
        or any(
            not isinstance(n, str)
            or not re.fullmatch(r"(?:tests/)?test_[a-z0-9_]+\.py", n)
            for n in files
        )
        or len(set(files)) != len(files)
    ):
        raise ValueError("Invalid approved inventory")
    return cast(list[str], files)


def validate(summary: Path, junit: Path, inventory: Path, head: str | None = None) -> None:
    expected = inventory_files(inventory)
    report = json.loads(summary.read_text())
    if not isinstance(report, dict):
        raise ValueError("Invalid summary")
    for key in ("failed", "errors", "skipped", "xfailed", "xpassed", "deselected", "exit_code"):
        if type(report.get(key)) is not int or report[key] != 0:
            raise ValueError("Adverse or missing outcome")
    for key in ("collected", "completed", "files", "arguments", "addopts"):
        values = report.get(key)
        if not isinstance(values, list) or any(not isinstance(n, str) for n in values):
            raise ValueError("Invalid collection metadata")
    collected, completed, files = report["collected"], report["completed"], report["files"]
    if (
        not collected
        or len(set(collected)) != len(collected)
        or len(set(completed)) != len(completed)
        or set(collected) != set(completed)
        or sorted(files) != sorted(expected)
        or sorted({n.split("::", 1)[0] for n in collected}) != sorted(expected)
        or report.get("keyword") != ""
        or report.get("marker") != ""
    ):
        raise ValueError("Incomplete or filtered collection")
    tree = ET.parse(junit)
    cases = tree.findall(".//testcase")
    if (
        len(cases) != len(completed)
        or tree.findall(".//failure")
        or tree.findall(".//error")
        or tree.findall(".//skipped")
    ):
        raise ValueError("JUnit disagrees with successful completion")
    if report.get("event", "") == "push":
        if (re.fullmatch(r"[0-9a-f]{40}", str(report.get("push_before", ""))) is None
            or report.get("push_after") != report.get("event_head_sha")
            or report.get("checkout_sha") != report.get("event_head_sha")
            or type(report.get("push_forced")) is not bool
            or report.get("push_deleted") is not False):
            raise ValueError("Invalid push report")
    elif (report.get("event", "") not in {"", "pull_request"}
          or any(report.get(k) is not None for k in
                 ("push_before", "push_after", "push_forced", "push_deleted"))):
        raise ValueError("Mixed event report")
    if head is not None and (
        re.fullmatch(r"[0-9a-f]{40}", head) is None
        or report.get("checkout_sha") != head
        or report.get("event_head_sha") != head
    ):
        raise ValueError("Checkout and event head disagree")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-files", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--head")
    args = parser.parse_args()
    try:
        if args.list_files:
            print(" ".join(inventory_files(args.list_files)))
        else:
            if args.summary is None or args.junit is None or args.inventory is None:
                parser.error("summary, junit and inventory are required")
            validate(args.summary, args.junit, args.inventory, args.head)
            print("Verification gate passed")
    except (ValueError, OSError, ET.ParseError, TypeError, KeyError):
        print("Verification gate failed: invalid or incomplete metadata", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
