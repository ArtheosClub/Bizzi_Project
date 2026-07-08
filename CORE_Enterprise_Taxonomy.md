# CORE Enterprise Taxonomy

Version: 1.0
Status: Information Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Object_Registry.md
- CORE_Enterprise_Metadata_Standard.md

Primary Owner:
- AG009 Enterprise Architect

Knowledge Owner:
- AG053 Knowledge Curator

Governance Owner:
- AG002 Chief Orchestrator

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Enterprise Taxonomy defines the shared language of Bizzi.

It standardizes the terms, categories, relationships, and classification logic used across capabilities, functions, agents, playbooks, objects, workflows, decisions, events, KPIs, knowledge, and integrations.

Core principle:

```text
A digital enterprise cannot reason consistently without a shared vocabulary.
```

---

## 01. Purpose

This document defines:

- common enterprise terms;
- object categories;
- relationship categories;
- classification dimensions;
- taxonomy governance;
- integration with metadata, registry, memory, and search.

---

## 02. Taxonomy Domains

Bizzi taxonomy is organized into domains:

| Domain | Purpose |
|---|---|
| Capability Taxonomy | Classifies enterprise capabilities |
| Function Taxonomy | Classifies responsibilities and functions |
| Agent Taxonomy | Classifies agent roles and authority |
| Process Taxonomy | Classifies processes and workflows |
| Object Taxonomy | Classifies managed objects |
| Decision Taxonomy | Classifies decisions and authority levels |
| Event Taxonomy | Classifies enterprise events |
| KPI Taxonomy | Classifies metrics and performance indicators |
| Risk Taxonomy | Classifies risk types |
| Knowledge Taxonomy | Classifies memory, lessons, and patterns |
| Integration Taxonomy | Classifies APIs, tools, and system links |

---

## 03. Core Classification Dimensions

Common classification dimensions:

- capability;
- function;
- process;
- agent;
- object type;
- lifecycle state;
- decision level;
- risk rating;
- confidence level;
- governance class;
- data sensitivity;
- business criticality;
- operational domain;
- knowledge type;
- event type.

---

## 04. Relationship Vocabulary

Standard relationship names:

| Relationship | Meaning |
|---|---|
| owns | Has responsibility for |
| executes | Performs or carries out |
| governs | Sets rules for |
| approves | Authorizes |
| audits | Reviews or validates |
| depends_on | Requires another object |
| produces | Creates output |
| consumes | Uses input |
| triggers | Causes workflow or event |
| updates | Changes state or content |
| supersedes | Replaces older version |
| references | Links to supporting material |
| validates | Confirms correctness or effect |
| escalates_to | Routes to higher authority |
| belongs_to | Is part of a larger domain |

---

## 05. Term Quality Rules

A taxonomy term should have:

- clear definition;
- owner;
- domain;
- allowed values where applicable;
- relationship to existing terms;
- lifecycle status;
- usage examples;
- deprecated synonyms where relevant.

---

## 06. Controlled Vocabulary Examples

### Decision Levels

- L1 Routine
- L2 Operational
- L3 Cross-functional
- L4 High-impact / regulated
- L5 Strategic / Human Board

### Confidence Levels

- Low
- Medium
- High
- Verified

### Risk Ratings

- Low
- Medium
- High
- Critical

### Object Status

- Draft
- Under Review
- Approved
- Active
- Superseded
- Deprecated
- Archived

---

## 07. Taxonomy Governance

Taxonomy governance requirements:

- new core terms require architecture review;
- duplicate terms must be merged or mapped;
- deprecated terms remain as aliases;
- term changes must be versioned;
- taxonomy updates must not break object registry consistency;
- taxonomy must remain agent-readable and human-readable.

---

## 08. Enterprise Ontology Direction

The taxonomy should evolve into an enterprise ontology.

Taxonomy defines terms.
Ontology defines relationships and reasoning rules.

Example:

```text
Agent owns Function
Function executes Capability
Playbook implements Function
Event triggers Workflow
Decision approves Transition
Audit validates Outcome
Knowledge stores Lesson
```

---

## 09. Integration

The Enterprise Taxonomy supports:

- Object Registry;
- Metadata Standard;
- Enterprise Memory;
- Knowledge Graph;
- Search;
- Reporting;
- Workflow routing;
- Decision routing;
- KPI classification.

---

## 10. Success Criteria

This specification is successful if Bizzi can:

- classify objects consistently;
- avoid terminology drift;
- support search and reasoning;
- connect objects into a knowledge graph;
- map legacy terms to canonical terms;
- provide a shared vocabulary for all agents.

---

## 11. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Enterprise Taxonomy foundation specification |
