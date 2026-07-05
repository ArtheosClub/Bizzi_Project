# ENTERPRISE_FUNCTION_REGISTRY.md

# Art of Business Enterprise Function Registry

Version: 1.2
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

## Strategy Functions (continued)

STR-MIS-001 Maintain Mission Statement
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-OKR-001 Define Quarterly OKRs
Owner: AG006 Strategic Planning Agent
Decision: L3
Escalation: E3

STR-POR-001 Strategic Portfolio Review
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

STR-CAP-001 Capital Allocation Decision
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-GRW-001 Growth Strategy Formulation
Owner: AG006 Strategic Planning Agent
Decision: L3
Escalation: E3

STR-INT-001 Market Entry Assessment
Owner: AG006 Strategic Planning Agent
Decision: L4
Escalation: E4

STR-PAR-001 Partnership Opportunity Evaluation
Owner: AG006 Strategic Planning Agent
Decision: L3
Escalation: E3

STR-MNA-001 M&A Target Screening
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

## Innovation Functions (continued)

INN-OPP-001 Opportunity Scouting
Owner: AG007 Innovation Manager
Decision: L1
Escalation: E1

INN-PDI-001 Product Discovery Sprint
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-PVA-001 Product Validation Testing
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-VEN-001 New Venture Charter
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

INN-BMD-001 Business Model Canvas Update
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-POR-001 Innovation Portfolio Review
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

INN-RND-001 R&D Initiative Tracking
Owner: AG007 Innovation Manager
Decision: L2
Escalation: E2

INN-COM-001 Go-to-Market Readiness Review
Owner: AG007 Innovation Manager
Decision: L3
Escalation: E3

## Market Intelligence Functions (continued)

MKT-IND-001 Industry Landscape Analysis
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-TRD-001 Emerging Trend Scan
Owner: AG008 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-SEG-001 Market Segmentation Update
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-DEM-001 Demand Forecast Model
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-OPP-001 Market Opportunity Sizing
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-CUR-001 Customer Research Study
Owner: AG008 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-PRI-001 Competitive Pricing Scan
Owner: AG008 Market Intelligence Analyst
Decision: L2
Escalation: E2

## Marketing Functions (continued)

MRK-CON-001 Content Calendar Management
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

MRK-SEO-001 SEO Performance Review
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

MRK-SOC-001 Social Media Posting Plan
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

MRK-LGN-001 Lead Generation Campaign
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-PR-001 Press Release Coordination
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-EVT-001 Event Planning & Execution
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-PMK-001 Product Launch Messaging
Owner: AG009 Marketing Manager
Decision: L2
Escalation: E2

MRK-ANA-001 Marketing Performance Dashboard
Owner: AG009 Marketing Manager
Decision: L1
Escalation: E1

## Sales Functions (continued)

SAL-CTR-001 Sales Contract Finalization
Owner: AG024 Contract Management Agent
Decision: L2
Escalation: E2

SAL-ACC-001 Key Account Review
Owner: AG010 Sales Manager
Decision: L2
Escalation: E2

SAL-REN-001 Renewal Risk Review
Owner: AG010 Sales Manager
Decision: L2
Escalation: E2

SAL-XSL-001 Cross-Sell Opportunity Identification
Owner: AG010 Sales Manager
Decision: L1
Escalation: E1

SAL-UPS-001 Upsell Proposal
Owner: AG010 Sales Manager
Decision: L1
Escalation: E1

## Customer Success Functions (continued)

CUS-ADO-001 Feature Adoption Tracking
Owner: AG011 Customer Success Manager
Decision: L1
Escalation: E1

CUS-SUP-001 Support Ticket Resolution
Owner: AG011 Customer Success Manager
Decision: L1
Escalation: E1

CUS-RET-001 Retention Risk Intervention
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

CUS-EXP-001 Expansion Opportunity Review
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

CUS-NPS-001 NPS Survey Cycle
Owner: AG011 Customer Success Manager
Decision: L1
Escalation: E1

CUS-ADV-001 Reference Customer Program
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

CUS-SPL-001 Customer Success Plan
Owner: AG011 Customer Success Manager
Decision: L2
Escalation: E2

## Operations Functions (continued)

OPS-SRV-001 Service Delivery Tracking
Owner: AG012 Operations Manager
Decision: L1
Escalation: E1

OPS-PMG-001 Project Milestone Review
Owner: AG012 Operations Manager
Decision: L2
Escalation: E2

OPS-AST-001 Asset Register Update
Owner: AG012 Operations Manager
Decision: L1
Escalation: E1

OPS-RES-001 Resource Capacity Planning
Owner: AG012 Operations Manager
Decision: L2
Escalation: E2

OPS-COS-001 Cost Optimization Review
Owner: AG012 Operations Manager
Decision: L3
Escalation: E3

OPS-IMP-001 Improvement Initiative Tracking
Owner: AG012 Operations Manager
Decision: L2
Escalation: E2

## Supply Chain Functions (continued)

SCM-VEN-001 Vendor Performance Review
Owner: AG023 Vendor Management Agent
Decision: L2
Escalation: E2

SCM-SUP-001 Supply Plan Update
Owner: AG013 Supply Chain Manager
Decision: L2
Escalation: E2

SCM-DMP-001 Demand Plan Reconciliation
Owner: AG013 Supply Chain Manager
Decision: L2
Escalation: E2

SCM-IMX-001 Import/Export Documentation
Owner: AG013 Supply Chain Manager
Decision: L2
Escalation: E2

SCM-CUS-001 Customs Compliance Check
Owner: AG013 Supply Chain Manager
Decision: L3
Escalation: E3

SCM-CSU-001 Supplier Contract Negotiation
Owner: AG024 Contract Management Agent
Decision: L2
Escalation: E2

SCM-SRK-001 Supplier Risk Assessment
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

## Finance Functions (continued)

FIN-ACC-001 Monthly Close Process
Owner: AG014 Finance Manager
Decision: L2
Escalation: E2

FIN-TRE-001 Cash Position Monitoring
Owner: AG014 Finance Manager
Decision: L2
Escalation: E2

FIN-FCS-001 Financial Forecast Update
Owner: AG014 Finance Manager
Decision: L2
Escalation: E2

FIN-FPA-001 Variance Analysis
Owner: AG014 Finance Manager
Decision: L2
Escalation: E2

FIN-TAX-001 Tax Filing Preparation
Owner: AG014 Finance Manager
Decision: L3
Escalation: E3

FIN-AUD-001 External Audit Coordination
Owner: AG014 Finance Manager
Decision: L3
Escalation: E3

FIN-IR-001 Investor Update Preparation
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

FIN-CAP-001 Capital Structure Review
Owner: AG014 Finance Manager
Decision: L4
Escalation: E4

## Legal Functions (continued)

LEG-LIC-001 License Renewal Tracking
Owner: AG015 Legal Counsel Agent
Decision: L2
Escalation: E2

LEG-REG-001 Regulatory Change Monitoring
Owner: AG016 Compliance Officer
Decision: L2
Escalation: E2

LEG-AML-001 AML Screening
Owner: AG016 Compliance Officer
Decision: L3
Escalation: E3

LEG-KYC-001 KYC Verification
Owner: AG016 Compliance Officer
Decision: L2
Escalation: E2

LEG-DPR-001 Data Privacy Impact Assessment
Owner: AG016 Compliance Officer
Decision: L3
Escalation: E3

LEG-CMP-001 Compliance Checklist Review
Owner: AG016 Compliance Officer
Decision: L2
Escalation: E2

LEG-LIT-001 Litigation Case Tracking
Owner: AG015 Legal Counsel Agent
Decision: L4
Escalation: E4

LEG-IP-001 IP Filing Management
Owner: AG015 Legal Counsel Agent
Decision: L3
Escalation: E3

LEG-INT-001 Cross-Border Legal Review
Owner: AG015 Legal Counsel Agent
Decision: L3
Escalation: E3

## Risk Functions (continued)

RSK-FIN-001 Financial Risk Monitoring
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

RSK-OPR-001 Operational Risk Assessment
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-LEG-001 Legal Risk Review
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

RSK-CYB-001 Cyber Risk Assessment
Owner: AG020 Cybersecurity Agent
Decision: L3
Escalation: E3

RSK-REP-001 Reputation Risk Monitoring
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-CTR-001 Country Risk Rating
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-VND-001 Vendor Risk Screening
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-CRI-001 Crisis Response Activation
Owner: AG001 CEO Agent
Decision: L5
Escalation: E5

RSK-BCP-001 Business Continuity Plan Test
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

## People Management Functions (continued)

PEO-WFP-001 Headcount Planning
Owner: AG017 HR Manager
Decision: L2
Escalation: E2

PEO-ONB-001 New Hire Onboarding
Owner: AG017 HR Manager
Decision: L1
Escalation: E1

PEO-COM-001 Compensation Benchmarking
Owner: AG017 HR Manager
Decision: L3
Escalation: E3

PEO-TAL-001 Talent Review Cycle
Owner: AG017 HR Manager
Decision: L2
Escalation: E2

PEO-CUL-001 Culture Survey
Owner: AG017 HR Manager
Decision: L1
Escalation: E1

PEO-LDR-001 Leadership Development Plan
Owner: AG017 HR Manager
Decision: L2
Escalation: E2

PEO-SUC-001 Succession Plan Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

## Technology Functions (continued)

TEC-APP-001 Application Portfolio Review
Owner: AG018 Technology Manager
Decision: L2
Escalation: E2

TEC-INT-001 System Integration Monitoring
Owner: AG019 Data Platform Agent
Decision: L2
Escalation: E2

TEC-AIP-001 AI Model Performance Review
Owner: AG021 Automation & MLOps Agent
Decision: L2
Escalation: E2

TEC-DEV-001 Deployment Pipeline Health Check
Owner: AG021 Automation & MLOps Agent
Decision: L1
Escalation: E1

TEC-MLO-001 Model Retraining Schedule
Owner: AG021 Automation & MLOps Agent
Decision: L2
Escalation: E2

TEC-DWP-001 Digital Workplace Tools Review
Owner: AG018 Technology Manager
Decision: L1
Escalation: E1

## Knowledge Management Functions (continued)

KNW-POL-001 Policy Document Maintenance
Owner: AG026 Knowledge Manager
Decision: L2
Escalation: E2

KNW-MEM-001 Corporate Memory Archive Update
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

KNW-GRA-001 Knowledge Graph Enrichment
Owner: AG026 Knowledge Manager
Decision: L2
Escalation: E2

KNW-SRC-001 Knowledge Search Index Update
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

KNW-EXP-001 Expert Network Directory
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

KNW-ANL-001 Knowledge Usage Analytics
Owner: AG026 Knowledge Manager
Decision: L1
Escalation: E1

KNW-AUD-001 Knowledge Base Quality Audit
Owner: AG003 AI Auditor
Decision: L2
Escalation: E2

## Governance Functions (continued)

GOV-AUT-001 Authority Matrix Review
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-POL-001 Governance Policy Update
Owner: AG002 Chief Orchestrator
Decision: L4
Escalation: E4

GOV-DEC-001 Decision Log Maintenance
Owner: AG003 AI Auditor
Decision: L2
Escalation: E2

GOV-PRF-001 Agent Performance Review
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-LIF-001 Agent Onboarding/Retirement
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-CTL-001 Enterprise Control Testing
Owner: AG003 AI Auditor
Decision: L4
Escalation: E4

GOV-AIG-001 AI Governance Compliance Review
Owner: AG003 AI Auditor
Decision: L4
Escalation: E4

## Summary

Capabilities: 15/15 — all sub-capabilities from Capability Map now have at least one Function Group (150/150 sub-capabilities mapped)
Function Groups: ~130 documented
Functions documented: 171 (was 62) — Target: ~600
Agents: 28 — full mapping in AGENT_REGISTRY.md
Playbooks: 1 documented (PB001), roadmap for 50 in PLAYBOOK_ROADMAP.md

Next iteration: deepen each Function Group from 1 function to 3-5 (adds review,
exception-handling, and reporting variants) to reach ~600 target.

Changelog v1.1 → v1.2:
- Mapped all 150 sub-capabilities from CAPABILITY_MAP_v1.0.md to Function Groups
  (was 40/150 — Strategy, Innovation, Market Intelligence, Marketing, Sales,
  Customer Success, Operations, Supply Chain, Finance, Legal, Risk, People,
  Technology, Knowledge, Governance all now have 100% sub-capability coverage)
- Added 109 new Level-3 functions, one representative function per previously
  unmapped sub-capability

Changelog v1.0 → v1.1:
- Added Owner/Decision/Escalation to Innovation, Market Intelligence, Sales, Legal,
  Risk, Governance functions (previously listed without these fields)
- Added Marketing, Customer Success, Operations, Supply Chain, People Management,
  Technology, Knowledge Management function groups (7 domains, 30 functions)
- All Owner Agent fields now reference Agent IDs from AGENT_REGISTRY.md
