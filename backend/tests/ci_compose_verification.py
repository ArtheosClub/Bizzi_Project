"""Compose migration/health collector; captured raw output never leaves the runner.

No application import, uploader, cleanup controller or generic reporter framework.
Physical hosted VM disposal is platform behavior, not a certified deletion ledger.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

REPOSITORY = "ArtheosClub/Bizzi_Project"
TABLES = ("users", "workspaces", "workspace_memberships", "agent_definitions",
          "enterprise_objects", "tasks", "audit_records")
SCHEMA_SHA256 = "7cb3f7528256b430cbb1ce57af9ef6ff391e0cb83ee8ff2b7721326ab919f4e2"
EXPECTED_SCHEMA = {'columns': [['agent_definitions', 'id', 'uuid'],
             ['agent_definitions', 'workspace_id', 'uuid'],
             ['agent_definitions', 'phase', 'character varying'],
             ['agent_definitions', 'owner_id', 'uuid'],
             ['agent_definitions', 'created_at', 'timestamp with time zone'],
             ['agent_definitions', 'updated_at', 'timestamp with time zone'],
             ['alembic_version', 'version_num', 'character varying'],
             ['audit_records', 'id', 'uuid'],
             ['audit_records', 'workspace_id', 'uuid'],
             ['audit_records', 'action', 'character varying'],
             ['audit_records', 'content', 'jsonb'],
             ['audit_records', 'subject_workspace_id', 'uuid'],
             ['audit_records', 'subject_enterprise_object_id', 'uuid'],
             ['audit_records', 'subject_user_id', 'uuid'],
             ['audit_records', 'subject_workspace_membership_id', 'uuid'],
             ['audit_records', 'subject_task_id', 'uuid'],
             ['audit_records', 'created_at', 'timestamp with time zone'],
             ['audit_records', 'actor_id', 'uuid'],
             ['audit_records', 'membership_id', 'uuid'],
             ['enterprise_objects', 'id', 'uuid'],
             ['enterprise_objects', 'workspace_id', 'uuid'],
             ['enterprise_objects', 'type', 'character varying'],
             ['enterprise_objects', 'phase', 'character varying'],
             ['enterprise_objects', 'owner_id', 'uuid'],
             ['enterprise_objects', 'created_at', 'timestamp with time zone'],
             ['enterprise_objects', 'updated_at', 'timestamp with time zone'],
             ['tasks', 'id', 'uuid'],
             ['tasks', 'workspace_id', 'uuid'],
             ['tasks', 'phase', 'character varying'],
             ['tasks', 'source_object_id', 'uuid'],
             ['tasks', 'created_at', 'timestamp with time zone'],
             ['tasks', 'updated_at', 'timestamp with time zone'],
             ['users', 'id', 'uuid'],
             ['users', 'created_at', 'timestamp with time zone'],
             ['users', 'updated_at', 'timestamp with time zone'],
             ['users', 'auth_issuer', 'character varying'],
             ['users', 'auth_subject', 'character varying'],
             ['users', 'deactivated_at', 'timestamp with time zone'],
             ['workspace_memberships', 'id', 'uuid'],
             ['workspace_memberships', 'workspace_id', 'uuid'],
             ['workspace_memberships', 'user_id', 'uuid'],
             ['workspace_memberships', 'role', 'character varying'],
             ['workspace_memberships', 'created_at', 'timestamp with time zone'],
             ['workspaces', 'id', 'uuid'],
             ['workspaces', 'name', 'character varying'],
             ['workspaces', 'owner_id', 'uuid'],
             ['workspaces', 'created_at', 'timestamp with time zone'],
             ['workspaces', 'updated_at', 'timestamp with time zone']],
 'foreign_keys': [['fk_agent_definitions_owner_id_users', 'agent_definitions', 'users'],
                  ['fk_agent_definitions_workspace_id_workspaces',
                   'agent_definitions',
                   'workspaces'],
                  ['fk_audit_records_workspace_id_workspaces',
                   'audit_records',
                   'workspaces'],
                  ['fk_enterprise_objects_owner_id_users', 'enterprise_objects', 'users'],
                  ['fk_enterprise_objects_workspace_id_workspaces',
                   'enterprise_objects',
                   'workspaces'],
                  ['fk_tasks_source_object_id_enterprise_objects',
                   'tasks',
                   'enterprise_objects'],
                  ['fk_tasks_workspace_id_workspaces', 'tasks', 'workspaces'],
                  ['fk_workspace_memberships_user_id_users',
                   'workspace_memberships',
                   'users'],
                  ['fk_workspace_memberships_workspace_id_workspaces',
                   'workspace_memberships',
                   'workspaces'],
                  ['fk_workspaces_owner_id_users', 'workspaces', 'users']],
 'indexes': [['agent_definitions',
              'ix_agent_definitions_owner_id',
              'CREATE INDEX ix_agent_definitions_owner_id ON public.agent_definitions '
              'USING btree (owner_id)'],
             ['agent_definitions',
              'ix_agent_definitions_workspace_id',
              'CREATE INDEX ix_agent_definitions_workspace_id ON '
              'public.agent_definitions USING btree (workspace_id)'],
             ['agent_definitions',
              'pk_agent_definitions',
              'CREATE UNIQUE INDEX pk_agent_definitions ON public.agent_definitions '
              'USING btree (id)'],
             ['alembic_version',
              'alembic_version_pkc',
              'CREATE UNIQUE INDEX alembic_version_pkc ON public.alembic_version USING '
              'btree (version_num)'],
             ['audit_records',
              'ix_audit_records_workspace_id',
              'CREATE INDEX ix_audit_records_workspace_id ON public.audit_records USING '
              'btree (workspace_id)'],
             ['audit_records',
              'pk_audit_records',
              'CREATE UNIQUE INDEX pk_audit_records ON public.audit_records USING btree '
              '(id)'],
             ['audit_records',
              'uq_audit_bootstrap_action',
              'CREATE UNIQUE INDEX uq_audit_bootstrap_action ON public.audit_records '
              'USING btree (action) WHERE ((action)::text = ANY '
              "((ARRAY['user.bootstrap_created'::character varying, "
              "'workspace.bootstrap_created'::character varying, "
              "'workspace_membership.bootstrap_created'::character varying])::text[]))"],
             ['audit_records',
              'uq_audit_bootstrap_workspace_action',
              'CREATE UNIQUE INDEX uq_audit_bootstrap_workspace_action ON '
              'public.audit_records USING btree (workspace_id, action) WHERE '
              "((action)::text = ANY ((ARRAY['user.bootstrap_created'::character "
              "varying, 'workspace.bootstrap_created'::character varying, "
              "'workspace_membership.bootstrap_created'::character varying])::text[]))"],
             ['enterprise_objects',
              'ix_enterprise_objects_owner_id',
              'CREATE INDEX ix_enterprise_objects_owner_id ON public.enterprise_objects '
              'USING btree (owner_id)'],
             ['enterprise_objects',
              'ix_enterprise_objects_workspace_id',
              'CREATE INDEX ix_enterprise_objects_workspace_id ON '
              'public.enterprise_objects USING btree (workspace_id)'],
             ['enterprise_objects',
              'pk_enterprise_objects',
              'CREATE UNIQUE INDEX pk_enterprise_objects ON public.enterprise_objects '
              'USING btree (id)'],
             ['tasks',
              'ix_tasks_source_object_id',
              'CREATE INDEX ix_tasks_source_object_id ON public.tasks USING btree '
              '(source_object_id)'],
             ['tasks',
              'ix_tasks_workspace_id',
              'CREATE INDEX ix_tasks_workspace_id ON public.tasks USING btree '
              '(workspace_id)'],
             ['tasks',
              'pk_tasks',
              'CREATE UNIQUE INDEX pk_tasks ON public.tasks USING btree (id)'],
             ['users',
              'pk_users',
              'CREATE UNIQUE INDEX pk_users ON public.users USING btree (id)'],
             ['users',
              'uq_users_auth_issuer_auth_subject',
              'CREATE UNIQUE INDEX uq_users_auth_issuer_auth_subject ON public.users '
              'USING btree (auth_issuer, auth_subject)'],
             ['workspace_memberships',
              'ix_workspace_memberships_user_id',
              'CREATE INDEX ix_workspace_memberships_user_id ON '
              'public.workspace_memberships USING btree (user_id)'],
             ['workspace_memberships',
              'ix_workspace_memberships_workspace_id',
              'CREATE INDEX ix_workspace_memberships_workspace_id ON '
              'public.workspace_memberships USING btree (workspace_id)'],
             ['workspace_memberships',
              'pk_workspace_memberships',
              'CREATE UNIQUE INDEX pk_workspace_memberships ON '
              'public.workspace_memberships USING btree (id)'],
             ['workspace_memberships',
              'uq_workspace_memberships_workspace_id',
              'CREATE UNIQUE INDEX uq_workspace_memberships_workspace_id ON '
              'public.workspace_memberships USING btree (workspace_id, user_id)'],
             ['workspaces',
              'ix_workspaces_owner_id',
              'CREATE INDEX ix_workspaces_owner_id ON public.workspaces USING btree '
              '(owner_id)'],
             ['workspaces',
              'pk_workspaces',
              'CREATE UNIQUE INDEX pk_workspaces ON public.workspaces USING btree (id)']],
 'revisions': ['adw02_02'],
 'tables': ['agent_definitions',
            'alembic_version',
            'audit_records',
            'enterprise_objects',
            'tasks',
            'users',
            'workspace_memberships',
            'workspaces']}
CONTEXT_NAMES = (
    "GITHUB_REPOSITORY", "GITHUB_REPOSITORY_OWNER", "GITHUB_WORKFLOW_REF",
    "GITHUB_JOB", "GITHUB_EVENT_NAME", "GITHUB_REF", "GITHUB_BASE_REF",
    "GITHUB_HEAD_REF", "BIZZI_EVENT_HEAD_REPOSITORY", "BIZZI_EVENT_HEAD_SHA",
    "BIZZI_CHECKOUT_SHA", "GITHUB_ACTIONS", "RUNNER_ENVIRONMENT",
    "GITHUB_SHA", "BIZZI_PUSH_BEFORE", "BIZZI_PUSH_AFTER",
    "BIZZI_PUSH_FORCED", "BIZZI_PUSH_DELETED",
)
QUERIES = {
    "identity": "SELECT current_database(), current_user",
    "system_identifier": "SELECT system_identifier::text FROM pg_control_system()",
    "psql_address": "SELECT host(inet_server_addr()), inet_server_port()",
    "tables": "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename",
    "revisions": "SELECT version_num FROM alembic_version ORDER BY version_num",
    "columns": ("SELECT table_name,column_name,data_type FROM information_schema.columns "
                "WHERE table_schema='public' ORDER BY table_name,ordinal_position"),
    "indexes": ("SELECT tablename,indexname,indexdef FROM pg_indexes "
                "WHERE schemaname='public' ORDER BY tablename,indexname"),
    "foreign_keys": ("SELECT conname,conrelid::regclass::text,confrelid::regclass::text "
                     "FROM pg_constraint WHERE contype='f' "
                     "AND connamespace='public'::regnamespace ORDER BY conname"),
}
FIELDS = {"status", "reason", "repository", "event", "pr", "head_sha", "checkout_sha",
          "checkout_tree", "run_id", "attempt", "job", "runner_environment", "image",
          "container_id", "project", "network", "storage_kind", "system_identifier",
          "host", "port", "database", "role", "migration_revision", "schema_sha256",
          "schema_match", "table_counts", "health_status", "intake_unavailable",
          "observed_utc", "disposal_basis", "push_before", "push_after",
          "push_forced", "push_deleted"}


# Public error vocabulary is closed; arbitrary exception text never becomes a reason.
FAILURE_REASONS = frozenset({
    "context", "checkout", "summary-fields", "summary-value", "rows",
    "fresh-evidence", "command", "metadata", "container", "storage", "destination",
    "fresh-project", "fresh-schema", "schema", "health", "intake",
})


class EvidenceRefused(ValueError):
    """Only a fixed safe reason code is public."""


def need(value: object, reason: str) -> None:
    if not value:
        raise EvidenceRefused(reason)


def canonical_schema(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def validate_context(env: dict[str, str]) -> dict[str, str]:
    need(not any(k in env for k in ("BIZZI_PR_HEAD_SHA", "BIZZI_PR_HEAD_REPOSITORY")), "context")
    ref = env.get("GITHUB_REF", "")
    sha = env.get("BIZZI_EVENT_HEAD_SHA", "")
    fixed = {"GITHUB_REPOSITORY": REPOSITORY, "GITHUB_REPOSITORY_OWNER": "ArtheosClub",
             "GITHUB_JOB": "compose-e2e", "GITHUB_ACTIONS": "true",
             "RUNNER_ENVIRONMENT": "github-hosted"}
    need(all(env.get(k) == v for k, v in fixed.items()), "context")
    event = env.get("GITHUB_EVENT_NAME")
    if event == "pull_request":
        need(env.get("GITHUB_BASE_REF") == "main" and
             env.get("GITHUB_HEAD_REF") == "feat/wp15-bounded-task-service" and
             env.get("BIZZI_EVENT_HEAD_REPOSITORY") == REPOSITORY and
             re.fullmatch(r"refs/pull/[1-9][0-9]*/merge", ref), "context")
        need(not any(env.get(k) for k in
             ("BIZZI_PUSH_BEFORE", "BIZZI_PUSH_AFTER", "BIZZI_PUSH_FORCED", "BIZZI_PUSH_DELETED")),
             "context")
    elif event == "push":
        need(ref == "refs/heads/main" and not any(env.get(k) for k in
             ("GITHUB_BASE_REF", "GITHUB_HEAD_REF", "BIZZI_EVENT_HEAD_REPOSITORY")), "context")
        need(env.get("GITHUB_SHA") == env.get("BIZZI_PUSH_AFTER") == sha and
             re.fullmatch(r"[0-9a-f]{40}", env.get("BIZZI_PUSH_BEFORE", "")) and
             env.get("BIZZI_PUSH_FORCED") in {"true", "false"} and
             env.get("BIZZI_PUSH_DELETED") == "false", "context")
    else:
        raise EvidenceRefused("context")
    need(env.get("GITHUB_WORKFLOW_REF") ==
         f"{REPOSITORY}/.github/workflows/backend-ci.yml@{ref}", "context")
    need(re.fullmatch(r"[0-9a-f]{40}", sha) and env.get("BIZZI_CHECKOUT_SHA") == sha, "checkout")
    for name in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT"):
        need(re.fullmatch(r"[1-9][0-9]*", env.get(name, "")), "context")
    return {k: env.get(k, "") for k in CONTEXT_NAMES}


def validate_summary(value: dict[str, Any]) -> None:
    need(set(value) == FIELDS, "summary-fields")
    fixed = {"status": "PASS", "reason": "verified", "repository": REPOSITORY,
             "job": "compose-e2e", "runner_environment": "github-hosted",
             "image": "postgres:18.4-alpine", "storage_kind": "tmpfs",
             "host": "postgres-test", "port": 5432, "database": "bizzi_test", "role": "bizzi",
             "migration_revision": "adw02_02", "schema_sha256": SCHEMA_SHA256,
             "schema_match": True, "health_status": 200, "intake_unavailable": True,
             "disposal_basis": "github-hosted-vm-platform-disposal"}
    need(
        all(type(value[k]) is type(v) and value[k] == v for k, v in fixed.items()),
        "summary-value",
    )
    for name, pattern in {
        "head_sha": r"[0-9a-f]{40}", "checkout_sha": r"[0-9a-f]{40}",
        "checkout_tree": r"[0-9a-f]{40}", "container_id": r"[0-9a-f]{64}",
        "system_identifier": r"[0-9]{1,20}", "project": r"bizzi-ci-[1-9][0-9]*-[1-9][0-9]*",
        "network": r"bizzi-ci-[1-9][0-9]*-[1-9][0-9]*_default",
    }.items():
        need(
            isinstance(value[name], str) and re.fullmatch(pattern, str(value[name])),
            "summary-value",
        )
    need(value["checkout_sha"] == value["head_sha"], "checkout")
    if value["event"] == "pull_request":
        need(type(value["pr"]) is int and value["pr"] > 0 and
             all(value[k] is None for k in
                 ("push_before", "push_after", "push_forced", "push_deleted")), "summary-value")
    elif value["event"] == "push":
        need(value["pr"] is None and
             isinstance(value["push_before"], str) and
             re.fullmatch(r"[0-9a-f]{40}", value["push_before"]) and
             value["push_after"] == value["head_sha"] and
             type(value["push_forced"]) is bool and value["push_deleted"] is False, "summary-value")
    else:
        raise EvidenceRefused("summary-value")
    for name in ("run_id", "attempt"):
        need(type(value[name]) is int and int(str(value[name])) > 0, "summary-value")
    counts = value["table_counts"]
    need(type(counts) is dict and set(counts) == set(TABLES), "rows")
    need(all(type(v) is int and v == 0 for v in counts.values()), "rows")
    need(isinstance(value["observed_utc"], str), "summary-value")
    stamp = datetime.fromisoformat(str(value["observed_utc"]))
    need(stamp.utcoffset() == UTC.utcoffset(stamp), "summary-value")
    need(value["project"] == f"bizzi-ci-{value['run_id']}-{value['attempt']}" and
         value["network"] == f"{value['project']}_default", "summary-value")


class Collector:
    def __init__(self, root: Path, env: dict[str, str]) -> None:
        self.context = validate_context(env)
        need(root.is_absolute() and not root.exists(), "fresh-evidence")
        root.mkdir()
        self.root = root
        self.env = env
        self.project = f"bizzi-ci-{env['GITHUB_RUN_ID']}-{env['GITHUB_RUN_ATTEMPT']}"
        self.prefix = ["docker", "compose", "-f", "docker-compose.ci.yml", "-p", self.project]
        self.sequence = 0

    def command(self, argv: list[str], *, input_text: str | None = None) -> str:
        self.sequence += 1
        try:
            result = subprocess.run(argv, input=input_text, capture_output=True, text=True,
                                    timeout=300, check=False)
        except (OSError, subprocess.TimeoutExpired):
            raise EvidenceRefused("command") from None
        (self.root / f"command-{self.sequence}.stdout").write_text(result.stdout)
        (self.root / f"command-{self.sequence}.stderr").write_text(result.stderr)
        need(result.returncode == 0, "command")
        return result.stdout

    def rows(self, statement: str) -> list[list[Any]]:
        # Role is the synthetic image superuser; read-only is the transaction, not role ACL.
        query = "BEGIN READ ONLY; SELECT COALESCE(json_agg(row_to_json(q)), '[]'::json) FROM ("
        query += statement + ") q; ROLLBACK;"
        raw = self.command(self.prefix + ["exec", "-T", "-e",
            "PGOPTIONS=-c default_transaction_read_only=on", "postgres-test", "psql",
            "-X", "-h", "127.0.0.1", "-U", "bizzi", "-d", "bizzi_test",
            "-v", "ON_ERROR_STOP=1", "-qAt", "-c", query])
        data = json.loads(raw)
        need(type(data) is list and all(type(row) is dict for row in data), "metadata")
        return [list(row.values()) for row in data]

    def inspect(self, service: str) -> dict[str, Any]:
        cid = self.command(self.prefix + ["ps", "-q", service]).strip()
        need(re.fullmatch(r"[0-9a-f]{64}", cid), "container")
        values = json.loads(self.command(["docker", "inspect", cid]))
        need(type(values) is list and len(values) == 1, "container")
        obj: dict[str, Any] = values[0]
        labels = obj["Config"]["Labels"]
        need(labels.get("com.docker.compose.project") == self.project and
             labels.get("com.docker.compose.service") == service, "container")
        need(obj["Id"] == cid and obj["State"]["Running"], "container")
        need(set(obj["NetworkSettings"]["Networks"]) == {self.project + "_default"}, "container")
        mounts = obj["Mounts"]
        if service == "postgres-test":
            need(obj["Config"]["Image"] == "postgres:18.4-alpine", "container")
            need(len(mounts) == 1 and mounts[0]["Type"] == "tmpfs" and
                 mounts[0]["Destination"] == "/var/lib/postgresql", "storage")
        else:
            need(mounts == [], "storage")
            forwarded = dict(item.split("=", 1) for item in obj["Config"]["Env"] if "=" in item)
            need(all(forwarded.get(k) == v for k, v in self.context.items()), "context")
            need(forwarded.get("SYNTHETIC_EXECUTION_PROFILE") == "ci_compose" and
                 forwarded.get("DATABASE_URL") ==
                 "postgresql+psycopg://bizzi:bizzi@postgres-test:5432/bizzi_test", "destination")
            need(not any(k.startswith("PG") or k in {"GITHUB_TOKEN", "GH_TOKEN"}
                         for k in forwarded), "context")
        return obj

    def collect(self) -> dict[str, object]:
        need(not self.command(self.prefix + ["ps", "-aq"]).strip(), "fresh-project")
        sha = self.command(["git", "--no-optional-locks", "rev-parse", "HEAD"]).strip()
        tree = self.command(["git", "--no-optional-locks", "rev-parse", "HEAD^{tree}"]).strip()
        need(sha == self.context["BIZZI_EVENT_HEAD_SHA"] and
             re.fullmatch(r"[0-9a-f]{40}", tree), "checkout")
        self.command(self.prefix + ["up", "-d", "--wait", "--wait-timeout", "180", "postgres-test"])
        db = self.inspect("postgres-test")
        need(self.rows(QUERIES["tables"]) == [], "fresh-schema")
        need(self.rows(QUERIES["identity"]) == [["bizzi_test", "bizzi"]], "destination")
        system = str(self.rows(QUERIES["system_identifier"])[0][0])
        address = self.rows(QUERIES["psql_address"])
        need(address == [["127.0.0.1", 5432]], "destination")
        self.command(
            self.prefix + ["up", "--build", "-d", "--wait", "--wait-timeout", "180", "api"]
        )
        self.inspect("api")
        need(self.inspect("postgres-test")["Id"] == db["Id"], "container")
        need(str(self.rows(QUERIES["system_identifier"])[0][0]) == system, "container")
        schema: dict[str, Any] = {key: self.rows(QUERIES[key]) for key in
                  ("columns", "indexes", "foreign_keys")}
        schema["tables"] = [v[0] for v in self.rows(QUERIES["tables"])]
        schema["revisions"] = [v[0] for v in self.rows(QUERIES["revisions"])]
        need(schema == EXPECTED_SCHEMA and canonical_schema(schema) == SCHEMA_SHA256, "schema")
        counts = {name: self.rows("SELECT count(*) FROM " + name)[0][0] for name in TABLES}
        need(all(type(v) is int and v == 0 for v in counts.values()), "rows")
        # Only status codes and fixed health shape are public, never raw response text.
        with urlopen("http://127.0.0.1:8000/health", timeout=10) as response:
            health = response.status
            need(json.loads(response.read(4096)) == {"status": "ok"}, "health")
        need(health == 200, "health")
        try:
            with urlopen(Request("http://127.0.0.1:8000/business-requests", data=b"{}",
                                 headers={"Content-Type": "application/json"}), timeout=10):
                raise EvidenceRefused("intake")
        except HTTPError as error:
            need(error.code == 404, "intake")
        summary: dict[str, Any] = {
            "status": "PASS", "reason": "verified", "repository": REPOSITORY,
            "event": self.context["GITHUB_EVENT_NAME"],
            "pr": (int(self.context["GITHUB_REF"].split("/")[2])
                   if self.context["GITHUB_EVENT_NAME"] == "pull_request" else None),
            "push_before": self.context["BIZZI_PUSH_BEFORE"] or None,
            "push_after": self.context["BIZZI_PUSH_AFTER"] or None,
            "push_forced": (self.context["BIZZI_PUSH_FORCED"] == "true"
                            if self.context["GITHUB_EVENT_NAME"] == "push" else None),
            "push_deleted": (self.context["BIZZI_PUSH_DELETED"] == "true"
                             if self.context["GITHUB_EVENT_NAME"] == "push" else None),
            "head_sha": sha, "checkout_sha": sha, "checkout_tree": tree,
            "run_id": int(self.env["GITHUB_RUN_ID"]),
            "attempt": int(self.env["GITHUB_RUN_ATTEMPT"]),
            "job": "compose-e2e", "runner_environment": "github-hosted",
            "image": "postgres:18.4-alpine", "container_id": db["Id"],
            "project": self.project, "network": self.project + "_default", "storage_kind": "tmpfs",
            "system_identifier": system, "host": "postgres-test", "port": 5432,
            "database": "bizzi_test", "role": "bizzi", "migration_revision": "adw02_02",
            "schema_sha256": SCHEMA_SHA256, "schema_match": True, "table_counts": counts,
            "health_status": health, "intake_unavailable": True,
            "observed_utc": datetime.now(UTC).isoformat(),
            "disposal_basis": "github-hosted-vm-platform-disposal",
        }
        validate_summary(summary)
        self.command(["git", "--no-optional-locks", "diff", "--exit-code", "HEAD", "--"])
        (self.root / "PUBLIC_SUMMARY.json").write_text(json.dumps(summary, sort_keys=True) + "\n")
        return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    try:
        summary = Collector(args.evidence, dict(os.environ)).collect()
    except EvidenceRefused as error:
        # Select an exact closed code, never echo unrecognised exception text.
        reason = str(error) if str(error) in FAILURE_REASONS else "unexpected"
        print(json.dumps({"status": "FAIL", "reason": reason}))
        return 1
    except Exception:
        print(json.dumps({"status": "FAIL", "reason": "unexpected"}))
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
