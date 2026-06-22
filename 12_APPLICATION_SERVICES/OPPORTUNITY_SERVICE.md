# OPPORTUNITY_SERVICE.md

# Art of Business

## Opportunity Service v1.0

**Status:** Canonical Application Service Specification
**Domain:** Sales Domain
**Service Owner:** AG020_Head_of_Sales
**Architecture Owner:** AG054_Enterprise_Architect
**Operational Owner:** AG012_Opportunity_Manager
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

Opportunity Service manages qualified business opportunities from initial qualification through deal closure.

It converts sales potential into measurable revenue outcomes.

---

# 2. Mission

Provide a governed opportunity management system that maximizes conversion rates, revenue predictability, and sales execution effectiveness.

---

# 3. Architectural Position

```text
Lead
↓
Qualified Lead
↓
Opportunity
↓
Deal
↓
Revenue
```

Opportunity Service bridges Lead Management and Sales Pipeline Services.

---

# 4. Business Domain

Sales Domain

Primary responsibilities:

- Opportunity Management
- Deal Qualification
- Deal Progression
- Revenue Forecasting
- Win/Loss Management

---

# 5. Service Responsibilities

- opportunity creation;
- opportunity qualification;
- opportunity ownership;
- opportunity progression;
- deal tracking;
- forecast generation;
- win/loss tracking;
- opportunity closure.

---

# 6. Opportunity Domain Model

Core business objects:

```text
Opportunity
Deal
Opportunity Owner
Opportunity Stage
Forecast
Proposal
Contract
```

---

# 7. Opportunity Lifecycle Model

```text
Qualified Opportunity
↓
Discovery
↓
Proposal
↓
Negotiation
↓
Commit
↓
Won
```

Alternative outcomes:

```text
Lost
Cancelled
Deferred
Archived
```

---

# 8. Opportunity Identity Model

Opportunity attributes:

```text
Opportunity ID
Customer
Account
Owner
Estimated Value
Probability
Stage
Status
```

Opportunity identity must be unique.

---

# 9. Opportunity Classification Model

Examples:

```text
New Business
Upsell
Cross-Sell
Renewal
Strategic Deal
Enterprise Deal
Partner Deal
```

---

# 10. Deal Value Model

Tracked metrics:

```text
Expected Revenue
Projected Revenue
Contract Value
Recurring Revenue
Margin
Strategic Value
```

---

# 11. Opportunity Stage Model

Stages:

```text
Discovery
Qualification
Proposal
Negotiation
Commit
Closed Won
Closed Lost
```

Stage transitions must be auditable.

---

# 12. Opportunity Ownership Model

Every opportunity must have:

```text
Opportunity Owner
Sales Manager
Executive Sponsor
```

Ownership accountability is mandatory.

---

# 13. Opportunity Relationship Model

Relationships tracked:

```text
Opportunity ↔ Customer
Opportunity ↔ Account
Opportunity ↔ Contact
Opportunity ↔ Proposal
Opportunity ↔ Contract
Opportunity ↔ Agent
```

Stored in the Enterprise Knowledge Graph.

---

# 14. Opportunity Activity Model

Tracked activities:

```text
Meetings
Calls
Presentations
Demos
Negotiations
Proposals
Reviews
```

---

# 15. Revenue Forecast Model

Forecast dimensions:

```text
Revenue
Probability
Expected Close Date
Risk Level
Confidence Level
```

Forecasts support executive planning.

---

# 16. Agent Interaction Model

Agents may:

```text
Create Opportunity
Update Opportunity
Advance Stage
Generate Forecast
Analyze Risk
Recommend Actions
Close Opportunity
```

---

# 17. Process Integration

Supported processes:

```text
Opportunity Management
Deal Qualification
Proposal Management
Revenue Forecasting
Deal Closure
```

---

# 18. Function Mapping

Mapped functions:

```text
Sales
Business Development
Revenue Operations
Executive Sales Management
```

---

# 19. Capability Mapping

Mapped capabilities:

```text
Opportunity Management
Revenue Generation
Forecasting
Deal Management
Pipeline Growth
```

---

# 20. CRM Integration

CRM Service provides:

```text
Customer Data
Account Data
Contact Data
Relationship Data
```

---

# 21. Lead Management Integration

Opportunity Service receives:

```text
Qualified Leads
Lead Scores
Qualification Records
Lead History
```

Lead conversion creates opportunities.

---

# 22. Knowledge Graph Integration

Opportunity entities become graph nodes.

Examples:

```text
Opportunity
Deal
Proposal
Contract
Customer
```

---

# 23. Memory Integration

Contributes:

```text
Opportunity Memory
Deal Memory
Negotiation Memory
Forecast Memory
```

---

# 24. Decision Integration

Supports decisions:

```text
Deal Prioritization
Resource Allocation
Forecast Approval
Commit Approval
Risk Escalation
```

---

# 25. Execution Integration

Execution Service supports:

```text
Deal Workflows
Proposal Workflows
Negotiation Tasks
Forecast Processes
```

---

# 26. MCP Integration

External integrations:

```text
Opportunity Service
↓
Execution Service
↓
MCP Gateway Service
↓
MCP Tools
```

Examples:

- CRM Systems
- ERP Systems
- Contract Systems
- Communication Systems

---

# 27. Digital Twin Integration

Updates:

```text
Pipeline State
Revenue State
Forecast State
Sales State
```

---

# 28. API Model

Supported APIs:

```text
Create Opportunity
Read Opportunity
Update Opportunity
Advance Stage
Generate Forecast
Close Opportunity
Search Opportunity
```

---

# 29. Security Model

Opportunity Service enforces:

- RBAC;
- ABAC;
- opportunity ownership controls;
- forecast controls;
- approval controls.

---

# 30. Audit Model

Audited events:

```text
Opportunity Created
Opportunity Updated
Stage Changed
Forecast Updated
Opportunity Won
Opportunity Lost
```

Audit records are immutable.

---

# 31. Observability Model

Metrics:

```text
Opportunity Count
Pipeline Value
Win Rate
Loss Rate
Forecast Accuracy
Average Deal Size
```

---

# 32. Governance

AG020_Head_of_Sales owns opportunity governance.

AG012_Opportunity_Manager owns operational opportunity management.

AG054_Enterprise_Architect owns architecture consistency.

AG003_AI_Auditor owns traceability and controls.

---

# 33. KPIs

Opportunity KPIs:

- Win Rate
- Average Deal Size
- Forecast Accuracy
- Revenue Conversion Rate
- Sales Cycle Duration
- Pipeline Coverage
- Revenue Growth

---

# 34. Future Evolution

Future capabilities:

- AI deal scoring;
- predictive forecasting;
- autonomous opportunity progression;
- negotiation intelligence;
- opportunity digital twins;
- autonomous revenue optimization.

---

# 35. Architectural Role

Opportunity Service is the revenue generation engine of the Sales Domain.

```text
Qualified Lead
↓
Opportunity
↓
Deal
↓
Pipeline
↓
Revenue
```

It bridges Lead Management Service and Sales Pipeline Service.
