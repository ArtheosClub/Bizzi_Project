# DECISION 0001 — MVP First & Architecture Freeze

Version: 1.0
Status: APPROVED
Class: Constitutional Decision
Owner: Chief Architect
Effective: Immediately

## Purpose

Establish the development strategy for Bizzi by prioritizing delivery of the first working product over architectural completeness.

## Decision

The Bizzi project adopts the MVP First principle.

The objective of the current phase is to build the first working version of the platform.

Architecture is considered sufficient when it enables implementation of the MVP.

Perfect architecture is not an objective of the MVP phase.

## Architecture Freeze

- No new architectural layers.
- No new governance models unless required for MVP implementation.
- No new foundational abstractions.
- No expansion of the agent ecosystem unless required by implementation.
- No architectural optimization without a concrete implementation need.

Ideas not required for MVP shall be recorded in the Post-MVP Backlog.

## Decision Rule

Every proposed change must answer one question:

> Is this required for the first working MVP?

If YES: Implement.

If NO: Move to the Post-MVP Backlog.

## MVP Scope

1. Workspace
2. Agent
3. Process
4. Task
5. Decision
6. Memory
7. Audit
8. Minimal User Interface
9. Execution Engine

Completeness of workflow is more important than completeness of features.

## Allowed Architectural Changes

Architecture may be modified only if the change removes a contradiction, fixes a critical design flaw, or is required to unblock MVP implementation.

## Definition of Done

The MVP phase is complete when Bizzi is capable of executing one complete business workflow from start to finish.

Only after MVP completion may the Architecture Freeze be lifted.

## Guiding Principle

Build.
Validate.
Learn.
Improve.

Do not perfect what has not yet been built.
