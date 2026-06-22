# HIRING_WORKFLOW.md

# Art of Business

## Hiring Agent Workflow v1.0

**Status:** Canonical Agent Workflow Specification  
**Workflow Domain:** Human Resources  
**Business Process:** 13_BUSINESS_PROCESSES/HIRING_PROCESS.md  
**Primary Application Services:** HR_SERVICE, COMPLIANCE_SERVICE, FINANCE_SERVICE  
**Workflow Owner:** AG050_Chief_People_Officer  
**Architecture Owner:** AG054_Enterprise_Architect  
**Operational Owner:** AG051_HR_Manager  
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

Hiring Agent Workflow defines how agents and human owners execute hiring needs from role request to onboarding handoff.

---

# 2. Mission

Convert the Hiring Process into a governed, auditable, AI-enabled workflow that aligns workforce needs with enterprise capability requirements.

---

# 3. Workflow Position

```text
Workforce Need
↓
Hiring Process
↓
Hiring Agent Workflow
↓
HR / Finance / Compliance Services
↓
Onboarding Handoff
```

---

# 4. Trigger

The workflow starts when a new role, replacement need, capacity gap, or capability gap is approved for hiring evaluation.

---

# 5. Participating Agents

- AG050_Chief_People_Officer
- AG051_HR_Manager
- Hiring Manager
- Department Owner
- AG030_CFO
- AG060_Chief_Compliance_Officer
- AG003_AI_Auditor

---

# 6. Services Used

Application Services:

- HR_SERVICE.md
- COMPLIANCE_SERVICE.md
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
Workforce Need Received
↓
Context Loaded
↓
Hiring Request Created
↓
Role Profile Drafted
↓
Budget Checked
↓
Candidate Pipeline Created
↓
Candidates Screened
↓
Interview Summaries Generated
↓
Hiring Decision Routed
↓
Offer Approval Completed
↓
Onboarding Handoff Created
↓
Workflow Closed
```

---

# 8. Agent Responsibilities

## AG051_HR_Manager

- create hiring request;
- draft role profile;
- coordinate candidate flow;
- prepare hiring summaries;
- create onboarding handoff.

## Hiring Manager

- validate role requirements;
- review candidate summaries;
- recommend candidate selection.

## AG030_CFO

- validate budget availability;
- approve compensation exceptions.

## AG060_Chief_Compliance_Officer

- review compliance-sensitive hiring cases;
- ensure hiring controls are followed.

## AG003_AI_Auditor

- verify hiring workflow traceability;
- validate personal-data access controls.

---

# 9. Human Approval Points

Human approval is required for:

- role opening;
- budget exceptions;
- final candidate selection;
- compensation exceptions;
- offer issuance;
- onboarding acceptance.

---

# 10. Decision Routing

```text
Role Approval → Department Owner + HR
Budget Approval → CFO
Candidate Selection → Hiring Manager + HR
Compliance Review → Compliance Officer
Audit Exception → AI Auditor
```

---

# 11. Data Inputs

- workforce plan;
- role requirements;
- budget reference;
- candidate profiles;
- interview notes;
- evaluation records;
- compliance requirements.

---

# 12. Data Outputs

- hiring request;
- role profile;
- candidate shortlist;
- evaluation summary;
- hiring decision record;
- offer approval record;
- onboarding handoff.

---

# 13. Controls

- role owner required;
- budget validation required;
- candidate evaluation record required;
- final decision rationale required;
- personal-data access must be controlled;
- onboarding handoff must be recorded.

---

# 14. Audit Events

- Workflow Started
- Hiring Request Created
- Role Approved
- Candidate Screened
- Interview Completed
- Candidate Selected
- Offer Approved
- Onboarding Handoff Completed
- Workflow Completed

---

# 15. Observability

Metrics:

- time to role approval;
- time to shortlist;
- interview completion rate;
- approval latency;
- workflow completion rate;
- exception count.

---

# 16. Exception Handling

Exceptions:

- missing role definition;
- missing budget;
- candidate withdrawal;
- delayed approval;
- incomplete evaluation;
- compliance concern.

Exception routing:

```text
Role Exception → HR Manager
Budget Exception → CFO
Candidate Exception → Hiring Manager
Compliance Exception → Compliance Officer
Audit Exception → AI Auditor
```

---

# 17. Completion Criteria

The workflow is complete when the candidate is hired or the role is closed, onboarding handoff is complete, and the audit trail is complete.

---

# 18. KPIs

- Time to Hire
- Offer Acceptance Rate
- Candidate Quality Score
- Approval Completion Rate
- Onboarding Handoff Accuracy
- Audit Coverage

---

# 19. Governance

AG050_Chief_People_Officer owns hiring workflow governance.

AG051_HR_Manager owns operational execution.

AG003_AI_Auditor owns traceability and control validation.

---

# 20. Architectural Role

Hiring Agent Workflow transforms workforce needs into approved organizational capability.

```text
Hiring Process
↓
Hiring Agent Workflow
↓
HR Service
↓
Onboarding / Capability Result
```
