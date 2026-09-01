# Q2-ST Audit Trigger — Execution Pointer

**Status:** Active planning pointer  
**Date:** 2026-08-30  
**Applies to:** WP14 deferred runtime/service remainder; WP19 AuditRecord implementation; later audited service WPs  
**Authority:** None in this file. Canonical authority is `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.

## Purpose

This file exists only to make the accepted Q2-ST AuditRecord subject-kind reopen trigger visible from the implementation-planning layer where it can first become operative. It does not duplicate, amend, or supersede the canonical authority.

## WP14 pointer

Before any deferred WP14 runtime/repository/service/API work introduces an auditable `AgentDefinition` mutation, consult the canonical Q2-ST decision. Standalone `AgentDefinition` is not automatically covered by the existing `EnterpriseObject` AuditRecord subject kind. If its persisted identity form is not already covered by accepted AuditRecord subject-kind and canonical persisted subject-identity authority, subject-kind/mapping authority must reopen before implementation.

This pointer does not authorize WP14 runtime/repository/service/API work and does not alter ADR-0015.

## WP19 pointer

Before WP19 model/migration/service implementation proceeds, consult the canonical Q2-ST decision in addition to the final Q2 persisted-representation authority. Any subject identity form used by the selected representation must be covered by an accepted AuditRecord subject kind and canonical persisted subject-identity contract, or subject-kind/mapping authority must reopen first.

WP19 remains **BLOCKED / UNAUTHORIZED** until the separate persisted Q2 representation decision is accepted.

## Later service-layer WPs

The same pointer applies to WP17, WP23, and any later Work Package at the point it first introduces an auditable mutation for a persisted subject identity form not already covered by accepted AuditRecord subject authority.

## Non-effects

This pointer does not:

- create a new subject kind;
- create a mapping exception;
- change WP dependencies or readiness markers;
- select BR1–BR5 or N1–N5;
- authorize implementation;
- close ADW-07.
