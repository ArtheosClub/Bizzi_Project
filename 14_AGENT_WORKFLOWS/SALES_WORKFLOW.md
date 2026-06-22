# SALES_WORKFLOW.md

# Art of Business

## Sales Agent Workflow v1.0

**Status:** Canonical Agent Workflow Specification  
**Workflow Domain:** Sales  
**Business Process:** 13_BUSINESS_PROCESSES/SALES_PROCESS.md  
**Primary Application Services:** CRM_SERVICE, LEAD_MANAGEMENT_SERVICE, OPPORTUNITY_SERVICE, SALES_PIPELINE_SERVICE  
**Workflow Owner:** AG020_Head_of_Sales  
**Architecture Owner:** AG054_Enterprise_Architect  
**Operational Owner:** AG013_Revenue_Operations_Manager  
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

Sales Agent Workflow defines how AI agents and human owners execute the Sales Process from lead intake to revenue handoff.

---

# 2. Mission

Convert sales process architecture into executable agent behavior with clear routing, decision points, controls, audit events, and service interactions.

---

# 3. Workflow Position

```text
Business Process
↓
Agent Workflow
↓
Application Services
↓
Platform Services
↓
Actions
↓
Results
```

---

# 4. Trigger

The workflow starts when a lead, customer expansion signal, partner referral, campaign response, or strategic sales opportunity is detected.

---

# 5. Participating Agents

- AG010_CRM_Manager
- AG011_Lead_Manager
- AG012_Opportunity_Manager
- AG013_Revenue_Operations_Manager
- AG020_Head_of_Sales
- AG030_CFO
- AG003_AI_Auditor

---

# 6. Services Used

Application Services:

- CRM_SERVICE.md
- LEAD_MANAGEMENT_SERVICE.md
- OPPORTUNITY_SERVICE.md
- SALES_PIPELINE_SERVICE.md
- FINANCE_SERVICE.md

Platform Services:

- Agent Registry Service
- Context Service
- Knowledge Graph Service
- Memory Service
- Reasoning Service
- Decision Service
- Execution Service
- Audit Logging Service
- Observability Service

---

# 7. Workflow Flow

```text
Lead Signal Received
↓
Context Loaded
↓
Lead Record Created or Matched
↓
Lead Enriched
↓
Lead Scored
↓
Qualification Decision Requested
↓
Opportunity Created
↓
Opportunity Managed
↓
Pipeline Updated
↓
Deal Closed / Lost / Archived
↓
Finance Handoff Completed
```

---

# 8. Agent Responsibilities

## AG011_Lead_Manager

- create or validate lead record;
- enrich lead profile;
- score lead;
- recommend qualification result.

## AG012_Opportunity_Manager

- create opportunity;
- manage opportunity stage;
- analyze opportunity risk;
- recommend next action.

## AG013_Revenue_Operations_Manager

- update pipeline;
- generate forecast;
- detect pipeline gaps;
- prepare pipeline review.

## AG020_Head_of_Sales

- approve strategic opportunities;
- approve escalations;
- accept revenue commitments.

## AG003_AI_Auditor

- verify traceability;
- validate audit coverage;
- detect policy violations.

---

# 9. Human Approval Points

Human approval is required for:

- strategic opportunity creation;
- non-standard pricing;
- executive commitment;
- high-risk deal progression;
- final revenue handoff exceptions.

---

# 10. Decision Routing

```text
Lead Qualification → Decision Service
Strategic Opportunity → Head of Sales
Pricing Exception → Head of Sales + Finance
Revenue Commitment → Revenue Operations
Audit Exception → AI Auditor
```

---

# 11. Data Inputs

- lead data;
- customer record;
- account record;
- contact record;
- interaction history;
- opportunity data;
- pipeline data;
- forecast data.

---

# 12. Data Outputs

- qualified lead;
- opportunity record;
- pipeline update;
- forecast update;
- sales task;
- audit record;
- finance handoff record.

---

# 13. Controls

- lead ownership required;
- opportunity ownership required;
- stage transition must be logged;
- decision rationale must be recorded;
- revenue handoff must be auditable.

---

# 14. Audit Events

- Workflow Started
- Lead Created
- Lead Qualified
- Opportunity Created
- Stage Changed
- Forecast Updated
- Deal Closed
- Finance Handoff Completed
- Workflow Completed

---

# 15. Observability

Metrics:

- workflow completion rate;
- lead processing time;
- qualification time;
- opportunity conversion rate;
- forecast update frequency;
- exception count.

---

# 16. Exception Handling

Exceptions:

- duplicate lead;
- missing customer information;
- failed qualification;
- stalled opportunity;
- pricing exception;
- audit gap.

Exception routing:

```text
Operational Exception → AG013_Revenue_Operations_Manager
Commercial Exception → AG020_Head_of_Sales
Financial Exception → AG030_CFO
Audit Exception → AG003_AI_Auditor
```

---

# 17. Completion Criteria

The workflow is complete when the deal is closed, lost, or archived; pipeline state is updated; finance handoff is complete when applicable; and audit trail is complete.

---

# 18. KPIs

- Lead Response Time
- Lead Qualification Rate
- Opportunity Conversion Rate
- Sales Cycle Time
- Forecast Accuracy
- Revenue Handoff Accuracy

---

# 19. Governance

AG020_Head_of_Sales owns sales workflow governance.

AG013_Revenue_Operations_Manager owns operational workflow execution.

AG003_AI_Auditor owns audit validation and traceability.

---

# 20. Architectural Role

Sales Agent Workflow transforms the Sales Process into coordinated agent execution.

```text
Sales Process
↓
Sales Agent Workflow
↓
Sales Application Services
↓
Revenue Result
```
