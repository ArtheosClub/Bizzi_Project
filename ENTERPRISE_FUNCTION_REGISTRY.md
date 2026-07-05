# ENTERPRISE_FUNCTION_REGISTRY.md

# Art of Business Enterprise Function Registry

Version: 1.1
Status: Core Architecture

## Purpose
Function Registry является единым реестром функций предприятия.

Каждая функция должна иметь:
- Function ID
- Capability
- Function Name
- Owner Agent
- Decision Level
- Escalation Route
- KPI
- Related Playbooks

Owner Agent указывается в виде Agent ID из AGENT_REGISTRY.md.

## Function Classification

### Level 1 — Capability
FIN Finance

### Level 2 — Function Group
FIN-BUD Budgeting

### Level 3 — Function
FIN-BUD-001 Budget Planning

## Strategy Functions

STR-VIS-001 Maintain Corporate Vision
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-VIS-002 Vision Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-PLN-001 Annual Strategic Planning
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-PLN-002 Quarterly Strategic Review
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

## Innovation Functions

INN-IDE-001 Capture New Idea
Owner: AG007 Innovation Manager
Decision: L1
Escalation: E1

INN-IDE-002 Idea Scoring
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-IDE-003 Idea Prioritization
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-MVP-001 MVP Scope Definition
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-MVP-002 MVP Validation
Owner: AG007 Innovation Manager
Decision: L3
Escalation: E3

## Market Intelligence Functions

MKT-RES-001 Market Research
Owner: AG008 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-RES-002 Competitor Analysis
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-RES-003 Country Analysis
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

## Sales Functions

SAL-LEAD-001 Lead Capture
Owner: AG010 Sales Manager
Decision: L1
Escalation: E1

SAL-LEAD-002 Lead Qualification
Owner: AG010 Sales Manager
Decision: L1
Escalation: E1

SAL-LEAD-003 Lead Scoring
Owner: AG010 Sales Manager
Decision: L2
Escalation: E2

SAL-OPP-001 Opportunity Creation
Owner: AG010 Sales Manager
Decision: L1
Escalation: E1

SAL-OPP-002 Proposal Preparation
Owner: AG010 Sales Manager
Decision: L2
Escalation: E2

SAL-OPP-003 Negotiation Support
Owner: AG010 Sales Manager
Decision: L3
Escalation: E3

## Marketing Functions

MRK-BRA-001 Brand Guideline Management
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-BRA-002 Brand Asset Review
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

MRK-CAM-001 Campaign Planning
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-CAM-002 Campaign Execution
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

MRK-CAM-003 Campaign Performance Analysis
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

## Customer Success Functions

CUS-ONB-001 Onboarding Plan Creation
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

CUS-ONB-002 Onboarding Completion Tracking
Owner: AG011 Customer Success Manager
Decision: L1
Escalation: E1

CUS-HLT-001 Customer Health Scoring
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

CUS-HLT-002 Churn Risk Detection
Owner: AG011 Customer Success Manager
Decision: L3
Escalation: E3

CUS-ESC-001 Escalation Handling
Owner: AG011 Customer Success Manager
Decision: L3
Escalation: E3

## Operations Functions

OPS-PRO-001 Process Documentation
Owner: AG012 Operations Manager
Decision: L1
Escalation: E1

OPS-PRO-002 Process Optimization
Owner: AG012 Operations Manager
Decision: L2
Escalation: E2

OPS-QUA-001 Quality Audit
Owner: AG012 Operations Manager
Decision: L2
Escalation: E2

OPS-PER-001 Operational KPI Monitoring
Owner: AG012 Operations Manager
Decision: L1
Escalation: E1

## Supply Chain Functions

SCM-PRC-001 Purchase Requisition
Owner: AG022 Procurement Agent
Decision: L1
Escalation: E1

SCM-PRC-002 Supplier Evaluation
Owner: AG023 Vendor Management Agent
Decision: L2
Escalation: E2

SCM-LOG-001 Shipment Tracking
Owner: AG013 Supply Chain Manager
Decision: L1
Escalation: E1

SCM-INV-001 Inventory Reconciliation
Owner: AG013 Supply Chain Manager
Decision: L2
Escalation: E2

## Finance Functions

FIN-BUD-001 Budget Planning
Owner: AG014 Finance Manager
Decision: L3
Escalation: E3

FIN-BUD-002 Budget Review
Owner: AG014 Finance Manager
Decision: L2
Escalation: E2

FIN-BUD-003 Budget Approval Package
Owner: AG014 Finance Manager
Decision: L4
Escalation: E4

FIN-GRA-001 Grant Discovery
Owner: AG025 Grant & Funding Agent
Decision: L1
Escalation: E1

FIN-GRA-002 Grant Eligibility Review
Owner: AG025 Grant & Funding Agent
Decision: L2
Escalation: E2

FIN-GRA-003 Grant Application Preparation
Owner: AG025 Grant & Funding Agent
Decision: L2
Escalation: E2

FIN-GRA-004 Grant Reporting
Owner: AG025 Grant & Funding Agent
Decision: L2
Escalation: E2

## Legal Functions

LEG-CON-001 Contract Drafting
Owner: AG024 Contract Management Agent
Decision: L2
Escalation: E2

LEG-CON-002 Contract Review
Owner: AG015 Legal Counsel Agent
Decision: L3
Escalation: E3

LEG-CON-003 Contract Approval
Owner: AG015 Legal Counsel Agent
Decision: L4
Escalation: E4

## Risk Functions

RSK-ERM-001 Risk Identification
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-ERM-002 Risk Assessment
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

RSK-ERM-003 Risk Treatment Plan
Owner: AG005 Risk Manager
Decision: L4
Escalation: E4

## People Management Functions

PEO-REC-001 Job Requisition
Owner: AG027 Talent Acquisition Agent
Decision: L2
Escalation: E2

PEO-REC-002 Candidate Screening
Owner: AG027 Talent Acquisition Agent
Decision: L1
Escalation: E1

PEO-PER-001 Performance Review Cycle
Owner: AG017 HR Manager
Decision: L2
Escalation: E2

PEO-LRN-001 Learning Path Assignment
Owner: AG017 HR Manager
Decision: L1
Escalation: E1

## Technology Functions

TEC-INF-001 Infrastructure Monitoring
Owner: AG019 Data Platform Agent
Decision: L1
Escalation: E1

TEC-SEC-001 Security Incident Response
Owner: AG020 Cybersecurity Agent
Decision: L4
Escalation: E4

TEC-AUT-001 Workflow Automation Deployment
Owner: AG021 Automation & MLOps Agent
Decision: L2
Escalation: E2

TEC-DAT-001 Data Pipeline Management
Owner: AG019 Data Platform Agent
Decision: L2
Escalation: E2

## Knowledge Management Functions

KNW-KB-001 Knowledge Base Article Creation
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

KNW-SOP-001 SOP Drafting
Owner: AG026 Knowledge Manager
Decision: L2
Escalation: E2

KNW-SOP-002 SOP Review & Approval
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

KNW-LES-001 Lessons Learned Capture
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

## Governance Functions

GOV-ORC-001 Task Routing
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-ORC-002 Agent Assignment
Owner: AG002 Chief Orchestrator
Decision: L2
Escalation: E2

GOV-ORC-003 Escalation Management
Owner: AG002 Chief Orchestrator
Decision: L4
Escalation: E4

GOV-AUD-001 Decision Audit
Owner: AG003 AI Auditor
Decision: L3
Escalation: E3

GOV-AUD-002 Compliance Audit
Owner: AG003 AI Auditor
Decision: L3
Escalation: E3

## Summary

Capabilities: 15 (15/15 have at least one documented Function Group — was 8/15)
Function Groups: 20 documented (was 12)
Functions documented: 62 (was ~40) — Target: ~600
Agents: 28 — full mapping in AGENT_REGISTRY.md
Playbooks: 1 documented (PB001) — Target: 50+

Changelog v1.0 → v1.1:
- Added Owner/Decision/Escalation to Innovation, Market Intelligence, Sales, Legal,
  Risk, Governance functions (previously listed without these fields)
- Added Marketing, Customer Success, Operations, Supply Chain, People Management,
  Technology, Knowledge Management function groups (7 domains, 30 functions)
- All Owner Agent fields now reference Agent IDs from AGENT_REGISTRY.md
