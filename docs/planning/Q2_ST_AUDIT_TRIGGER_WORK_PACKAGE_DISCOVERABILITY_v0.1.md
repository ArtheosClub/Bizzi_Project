# Q2-ST Audit Trigger — Work-Package Discoverability v0.1

**Status:** Active planning synchronization note — non-authoritative  
**Date:** 2026-08-30  
**Scope:** WP14 / WP19 discoverability for the accepted Q2-ST AuditRecord subject-identity reopen trigger  
**Authority:** None. Canonical authority is `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## Purpose

Accepted Q2-ST-O2 establishes an AuditRecord-specific reopen trigger that is likely to fire during service-layer authorization rather than while ADW-07 documents are being read. This note places that trigger in the planning path for the Work Packages most likely to encounter it.

The trigger is normative only in the canonical Q2-ST authority named above. This file is pointer/discoverability support and does not duplicate or supersede that authority.

## WP19 — AuditRecord Model

WP19 is the Work Package that will implement the persisted AuditRecord subject-reference representation after final Q2 authority.

**Planning discoverability rule:** before WP19 representation/migration/service implementation is authorized, re-check the accepted Q2-ST authority for the AuditRecord subject-kind / canonical persisted subject-identity trigger. Any subject identity form used by WP19 must already be covered by an accepted AuditRecord subject kind and canonical persisted subject-identity contract, or the required subject-kind/mapping authority must be reopened first.

This note does not change WP19's current state: **BLOCKED / UNAUTHORIZED** pending final Q2 persisted-representation resolution.

## WP14 — AgentDefinition runtime/configuration remainder

WP14's schema foundation is already separate from its deferred runtime/configuration/service remainder. ADR-0015 gives AgentDefinition standalone persistence, with no corresponding `enterprise_objects` row.

**Planning discoverability rule:** before any later WP14 service/runtime work authorizes an auditable AgentDefinition mutation, re-check the accepted Q2-ST authority. Standalone AgentDefinition is not automatically covered by the existing `EnterpriseObject` AuditRecord subject kind merely because ADR-0013 classifies AgentDefinition as D02 EnterpriseObject.

If the persisted AgentDefinition identity is not already covered by the then-accepted AuditRecord subject-kind / canonical persisted subject-identity contract, subject-kind/mapping authority must reopen before the audited mutation is implemented.

This note does not change ADR-0015, does not declare AgentDefinition a sixth subject kind, and does not authorize WP14 repository/service/API work.

## Later service-layer WPs

The same check applies when WP17, WP23, or another later Work Package first authorizes an auditable service mutation for a persisted subject identity form not already covered by accepted AuditRecord subject authority.

## Direct-entry synchronization

The canonical WP entries currently live in `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` and `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`. The accepted trigger should be represented there as a pointer to the canonical Q2-ST authority, not by duplicating its normative text. This synchronization remains planning-only and must not change WP scope, readiness, dependencies, or implementation authorization.
