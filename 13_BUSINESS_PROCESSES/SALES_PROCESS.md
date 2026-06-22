# SALES_PROCESS.md

# Art of Business

## Sales Process v1.0

**Status:** Canonical Business Process Specification  
**Process Domain:** Sales  
**Process Owner:** AG020_Head_of_Sales  
**Architecture Owner:** AG054_Enterprise_Architect  
**Operational Owner:** AG013_Revenue_Operations_Manager  
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

Sales Process defines how the enterprise converts market interest into qualified opportunities, managed pipeline, closed deals, and revenue.

---

# 2. Mission

Create a repeatable, auditable, AI-enabled sales execution process connecting CRM, lead management, opportunity management, pipeline governance, and finance handoff.

---

# 3. Process Position

```text
Market
↓
Lead
↓
Opportunity
↓
Sales Pipeline
↓
Deal
↓
Revenue
↓
Finance
```

---

# 4. Trigger Events

- New lead received
- Existing customer expansion identified
- Partner referral received
- Campaign response received
- Strategic account opportunity identified

---

# 5. Process Scope

Included:

- lead intake
- lead qualification
- opportunity creation
- opportunity progression
- proposal preparation
- negotiation support
- deal closure
- revenue handoff

Excluded:

- accounting recognition
- fulfillment execution
- customer support operations

---

# 6. Process Participants

- AG020_Head_of_Sales
- AG010_CRM_Manager
- AG011_Lead_Manager
- AG012_Opportunity_Manager
- AG013_Revenue_Operations_Manager
- AG030_CFO
- AG003_AI_Auditor

---

# 7. Application Services Used

- CRM_SERVICE.md
- LEAD_MANAGEMENT_SERVICE.md
- OPPORTUNITY_SERVICE.md
- SALES_PIPELINE_SERVICE.md
- FINANCE_SERVICE.md

---

# 8. Platform Services Used

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

# 9. Process Flow

```text
Lead Captured
↓
Lead Validated
↓
Lead Scored
↓
Lead Qualified
↓
Opportunity Created
↓
Opportunity Managed
↓
Pipeline Reviewed
↓
Proposal / Negotiation
↓
Deal Closed
↓
Finance Handoff
```

---

# 10. Decision Points

- Is the lead valid?
- Is the lead qualified?
- Should an opportunity be created?
- Is executive approval required?
- Is the deal ready to close?
- Should the deal be escalated?

---

# 11. Data Objects

- Lead
- Account
- Contact
- Customer
- Opportunity
- Proposal
- Deal
- Forecast
- Revenue Handoff Record

---

# 12. Agent Responsibilities

Agents may:

- enrich leads
- score leads
- recommend qualification outcomes
- generate follow-up tasks
- analyze opportunity risk
- prepare pipeline reports
- recommend next actions

---

# 13. Human Responsibilities

Humans approve:

- strategic opportunity acceptance
- commercial terms
- non-standard discounts
- final deal commitment
- executive escalations

---

# 14. Controls

- lead ownership required
- opportunity ownership required
- stage changes are auditable
- deal approval thresholds enforced
- all revenue handoffs recorded

---

# 15. Audit Events

- Lead Created
- Lead Qualified
- Opportunity Created
- Stage Changed
- Forecast Updated
- Deal Closed
- Finance Handoff Completed

---

# 16. KPIs

- Lead Conversion Rate
- Opportunity Win Rate
- Sales Cycle Time
- Forecast Accuracy
- Pipeline Coverage
- Revenue Growth

---

# 17. Exception Handling

Exceptions include:

- duplicate lead
- missing customer data
- stalled opportunity
- approval delay
- contract risk
- forecast discrepancy

---

# 18. Completion Criteria

Sales Process is complete when:

- deal is won, lost, or archived;
- revenue handoff is recorded;
- audit trail is complete;
- pipeline state is updated.

---

# 19. Governance

AG020_Head_of_Sales owns sales process governance.

AG013_Revenue_Operations_Manager owns operational execution.

AG003_AI_Auditor owns traceability and control validation.

---

# 20. Architectural Role

Sales Process connects customer acquisition with revenue generation.

```text
Application Services
↓
Sales Process
↓
Revenue
↓
Finance Process
```
