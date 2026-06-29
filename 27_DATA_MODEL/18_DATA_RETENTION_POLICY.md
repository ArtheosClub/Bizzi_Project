# 18_DATA_RETENTION_POLICY.md

# Bizzi Platform

## Data Retention Policy

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Governance Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md through 17_DATABASE_MIGRATION_STRATEGY.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the initial data retention policy for Bizzi Platform.

It establishes how long different categories of Bizzi data should be retained, when data should be archived, when data may be deleted, and how retention rules should preserve workspace isolation, auditability, AI governance and product safety.

Core question:

```text
How should Bizzi retain, archive and delete platform data without losing business continuity, audit evidence or governance control?
```

---

# 2. Policy Role

The Data Retention Policy provides rules for:

- active operating data;
- archived operating data;
- audit records;
- runtime events;
- memory entries;
- integration data;
- export files;
- dashboard snapshots;
- security records;
- deletion requests;
- workspace closure;
- future compliance hardening.

This document is a product and engineering policy, not a jurisdiction-specific legal policy.

---

# 3. Retention Principles

## 3.1 Retain Business Memory by Default

Bizzi is designed to preserve company operating knowledge.

Rule:

```text
Important business context should be archived, not silently deleted.
```

## 3.2 Audit Evidence Must Be Preserved

Audit records support trust, governance and accountability.

Rule:

```text
Audit events should not be deleted through normal product workflows.
```

## 3.3 Runtime Noise Can Expire

Not all runtime events need permanent retention.

Rule:

```text
Operational runtime events may have shorter retention than audit events or confirmed business records.
```

## 3.4 Workspace Scope Applies to Retention

Retention actions must operate within one workspace boundary unless explicitly global.

Rule:

```text
Retention jobs must always filter by workspace_id when operating on workspace data.
```

## 3.5 Secrets Must Never Be Retained in Runtime Tables

Raw secrets should never be stored in normal database tables.

Rule:

```text
Credential values belong in secure secret storage, not in Bizzi runtime data.
```

---

# 4. Data Classes

Bizzi data is grouped into retention classes:

```text
identity_data
workspace_data
operating_data
execution_data
memory_data
audit_data
runtime_event_data
integration_data
security_data
dashboard_data
export_data
system_metadata
```

Each class may have different retention and archival rules.

---

# 5. Identity Data Retention

Applies to:

```text
users
sessions
workspace_access
```

Recommended policy:

```text
users: retained while account exists; archived or anonymized after account closure where required
sessions: short-term retention only
workspace_access: retained while workspace exists; revoked records retained for access history
```

Suggested MVP retention:

```text
sessions: 30-90 days after expiration or revocation
workspace_access revoked records: retain with workspace audit history
```

Governance note:

```text
User deletion and anonymization should be handled by future privacy and compliance policy.
```

---

# 6. Workspace Data Retention

Applies to:

```text
company_workspaces
workspace_settings
workspace_profiles
```

Recommended policy:

```text
active workspaces: retain indefinitely
paused workspaces: retain indefinitely unless account closure occurs
archived workspaces: retain according to workspace closure policy
```

Workspace archival should preserve:

```text
workspace record
settings
operating map
functions
tasks
decisions
memory
audit history
exports metadata
```

Rule:

```text
Workspace archival should not immediately delete operating history.
```

---

# 7. Operating Data Retention

Applies to:

```text
operating_maps
operating_gaps
functions
responsibilities
ownership_gaps
processes
process_steps
```

Recommended policy:

```text
active records: retain while workspace is active
archived records: retain as operating history
resolved gaps: retain for learning and audit context
old operating map versions: retain for change history
```

Default behavior:

```text
archive, do not hard delete
```

Allowed hard deletion:

```text
accidental duplicate records during early MVP
test data
records created in error before confirmation
```

Hard deletion should be restricted and audited.

---

# 8. Execution Data Retention

Applies to:

```text
tasks
decisions
agent_recommendations
agent_action_drafts
```

Recommended policy:

```text
completed tasks: retain as operating history
archived tasks: retain unless workspace deletion policy applies
confirmed decisions: retain indefinitely while workspace exists
rejected AI recommendations: retain for limited review period or archive
unapplied drafts: expire or archive after defined period
```

Suggested MVP values:

```text
completed tasks: retain indefinitely
confirmed decisions: retain indefinitely
rejected recommendations: retain 180-365 days
stale drafts: archive after 90-180 days
```

Rule:

```text
Confirmed decisions should not be hard deleted through normal workflows.
```

---

# 9. Memory Data Retention

Applies to:

```text
memory_entries
memory_sources
memory_usage
memory_reviews
```

Recommended policy:

```text
active memory: retain while useful and valid
archived memory: retain for history unless sensitive or obsolete
memory candidates: delete or archive if rejected
expired memory: archive when valid_until passes
```

Suggested MVP values:

```text
candidate memory: review within 30-90 days
rejected memory: archive or delete after 180 days
active memory: retained indefinitely until archived
archived memory: retained with workspace history
```

AI rule:

```text
Archived or expired memory must not be used as active AI context.
```

---

# 10. Audit Data Retention

Applies to:

```text
audit_events
audit_exports
```

Recommended policy:

```text
audit_events: retain for the life of the workspace or longer if required
audit_exports: retain metadata; exported files may expire separately
```

MVP retention:

```text
audit_events: retain indefinitely while workspace exists
```

Rule:

```text
Audit events should be append-oriented and protected from normal deletion.
```

Exception:

```text
Legal, privacy or security processes may require redaction or restricted access rather than deletion.
```

---

# 11. Runtime Event Retention

Applies to:

```text
runtime_events
event_failures
event_handler_runs
```

Recommended policy:

```text
processed informational events: retain for limited operational period
failed or critical events: retain longer
runtime events linked to audit or memory: retain as long as linked evidence is needed
```

Suggested MVP values:

```text
processed runtime events: 180-365 days
failed runtime events: 365 days or until resolved plus review period
critical runtime events: retain with audit history
```

Rule:

```text
Runtime events may be compacted or archived after operational usefulness expires.
```

---

# 12. Integration Data Retention

Applies to:

```text
integrations
integration_sync_jobs
integration_scopes
integration_credential_references
integration_mappings
```

Recommended policy:

```text
active integrations: retain while connected
revoked integrations: retain metadata and audit history
sync jobs: retain operational history for limited period
credential references: retain only while valid or needed for audit metadata
raw credentials: never stored in runtime tables
```

Suggested MVP values:

```text
integration_sync_jobs: 180-365 days
revoked integration metadata: retain with workspace history
credential references: revoke and remove access immediately when disconnected
```

---

# 13. Security Data Retention

Applies to:

```text
security_policies
security_events
workspace_access
sessions
access denied audit events
```

Recommended policy:

```text
active security policies: retain while active
archived security policies: retain as policy history
access denied events: retain for security review
sessions: short-term retention
```

Suggested MVP values:

```text
sessions: 30-90 days after expiration
access denied events: 365 days
security policy history: retain with workspace history
```

Rule:

```text
Security data should be retained long enough to investigate access and AI context issues.
```

---

# 14. Dashboard Data Retention

Applies to:

```text
dashboard_metrics
dashboard_snapshots
dashboard_insights
dashboard_alerts
```

Recommended policy:

```text
current dashboard metrics: retain while current
stale dashboard metrics: refresh, archive or delete
snapshots: retain only if used for reports or history
alerts: retain until resolved plus review period
```

Suggested MVP values:

```text
dashboard_metrics: retain current state and recent history
resolved alerts: retain 180-365 days
snapshots: optional; retain according to report needs
```

MVP note:

```text
Many dashboard values may be computed dynamically and not require long-term retention.
```

---

# 15. Export Data Retention

Applies to:

```text
export_jobs
export_files
file_reference
```

Recommended policy:

```text
export job metadata: retain for audit and user history
export files: expire after defined download/access period
sensitive exports: shorter file retention
```

Suggested MVP values:

```text
export_jobs metadata: retain with workspace history
export files: expire after 7-30 days by default
sensitive audit exports: expire after 7 days unless configured otherwise
```

Rule:

```text
Deleting an export file should not delete export job metadata.
```

---

# 16. Archive vs Delete

## Archive

Use archive for important business records:

```text
workspaces
operating maps
functions
processes
tasks
decisions
memory entries
integrations
security policies
```

Common archive fields:

```text
archived_at
archived_by
archive_reason
```

## Delete

Use delete for:

```text
expired sessions
expired export files
temporary drafts
test data
unconfirmed accidental records
runtime noise after retention window
```

Rule:

```text
Delete removes operational noise. Archive preserves business meaning.
```

---

# 17. Retention Job Requirements

Retention jobs must:

```text
run with explicit workspace scope where applicable
record audit events for sensitive retention actions
avoid deleting audit evidence through normal paths
avoid touching active AI memory without status check
respect export file expiration
preserve referential integrity
support dry-run mode before destructive action
```

Recommended retention job modes:

```text
dry_run
archive
delete
redact
```

---

# 18. Deletion Request Handling

Future deletion workflows should distinguish:

```text
user account deletion
workspace deletion
record deletion
export file deletion
integration disconnection
privacy redaction
```

MVP rule:

```text
Do not implement broad hard deletion until ownership, audit and backup rules are clear.
```

---

# 19. Redaction Strategy

Some data may need redaction instead of deletion.

Examples:

```text
personal data in audit metadata
sensitive integration payloads
private notes in memory entries
export file references
```

Redaction should preserve:

```text
audit event existence
object identity where safe
action history
workspace-level traceability
```

Rule:

```text
Redact sensitive content where deletion would destroy required evidence.
```

---

# 20. Backup and Restore Considerations

Retention policy must align with backup policy.

Important note:

```text
Deleted records may still exist in backups until backup expiration.
```

Future infrastructure policy should define:

```text
backup retention
restore windows
delete propagation to backups
legal hold behavior
disaster recovery requirements
```

---

# 21. Legal and Compliance Boundary

This document provides product-level retention architecture.

It does not define jurisdiction-specific legal retention obligations.

Future compliance layers should define:

```text
GDPR handling
customer data processing terms
legal hold
jurisdiction-specific retention
regulated industry requirements
privacy request handling
```

---

# 22. Retention Matrix

| Data Class | Default Action | Suggested MVP Retention |
|---|---|---|
| users | retain / anonymize later | account lifetime |
| sessions | delete | 30-90 days after expiration |
| workspaces | archive | workspace lifetime |
| operating data | archive | workspace lifetime |
| completed tasks | retain/archive | workspace lifetime |
| confirmed decisions | retain | workspace lifetime |
| active memory | retain | while valid/useful |
| rejected memory | archive/delete | 180 days |
| audit events | retain | workspace lifetime |
| processed runtime events | archive/delete | 180-365 days |
| failed runtime events | retain longer | 365 days |
| integration sync jobs | archive/delete | 180-365 days |
| security events | retain | 365 days or workspace lifetime |
| dashboard metrics | refresh/archive | current + recent history |
| export job metadata | retain | workspace lifetime |
| export files | delete/expire | 7-30 days |

---

# 23. Retention Anti-Patterns

Avoid:

```text
hard deleting confirmed decisions
hard deleting audit events through normal UI
using runtime events as permanent audit substitute
keeping export files forever by default
using archived memory as active AI context
retaining raw secrets in metadata
running retention jobs without workspace filters
performing destructive retention without dry-run
```

---

# 24. Acceptance Criteria

Data Retention Policy is ready when:

- data classes are defined;
- archive vs delete rules are clear;
- audit retention is protected;
- runtime event retention is differentiated;
- export file expiration is defined;
- memory usage rules are defined;
- security and integration retention are covered;
- retention job requirements are documented;
- legal/compliance boundary is stated.

Status:

```text
Accepted as Data Governance Standard
```

---

# 25. Final Statement

```text
Bizzi Data Retention Policy defines how platform data should be retained, archived, deleted, expired or redacted while preserving workspace isolation, operating continuity, auditability, AI safety and future compliance readiness.
```

This policy strengthens the `27_DATA_MODEL` layer as a governance-ready data architecture foundation.