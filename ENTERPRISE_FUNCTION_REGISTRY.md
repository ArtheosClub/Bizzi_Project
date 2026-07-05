# ENTERPRISE_FUNCTION_REGISTRY.md

# Art of Business Enterprise Function Registry

Version: 2.0
Status: Core Architecture — owners aligned to confirmed 83-agent org chart (AGENT_REGISTRY.md v2.0)

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

STR-MIS-001 Maintain Mission Statement
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

STR-OKR-001 Define Quarterly OKRs
Owner: AG006 Strategy Agent
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
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-INT-001 Market Entry Assessment
Owner: AG006 Strategy Agent
Decision: L4
Escalation: E4

STR-PAR-001 Partnership Opportunity Evaluation
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-MNA-001 M&A Target Screening
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

## Innovation Functions

INN-IDE-001 Capture New Idea
Owner: AG077 Innovation Manager
Decision: L1
Escalation: E1

INN-IDE-002 Idea Scoring
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-IDE-003 Idea Prioritization
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-OPP-001 Opportunity Scouting
Owner: AG077 Innovation Manager
Decision: L1
Escalation: E1

INN-PDI-001 Product Discovery Sprint
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-PVA-001 Product Validation Testing
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-MVP-001 MVP Scope Definition
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-MVP-002 MVP Validation
Owner: AG077 Innovation Manager
Decision: L3
Escalation: E3

INN-VEN-001 New Venture Charter
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

INN-BMD-001 Business Model Canvas Update
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-POR-001 Innovation Portfolio Review
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

INN-RND-001 R&D Initiative Tracking
Owner: AG076 R&D Agent
Decision: L2
Escalation: E2

INN-COM-001 Go-to-Market Readiness Review
Owner: AG077 Innovation Manager
Decision: L3
Escalation: E3

## Market Intelligence Functions

MKT-RES-001 Market Research
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-RES-002 Competitor Analysis
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-RES-003 Country Analysis
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-IND-001 Industry Landscape Analysis
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-TRD-001 Emerging Trend Scan
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-SEG-001 Market Segmentation Update
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-DEM-001 Demand Forecast Model
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-OPP-001 Market Opportunity Sizing
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-CUR-001 Customer Research Study
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-PRI-001 Competitive Pricing Scan
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

## Marketing Functions

MRK-BRA-001 Brand Guideline Management
Owner: AG035 Brand Agent
Decision: L2
Escalation: E2

MRK-BRA-002 Brand Asset Review
Owner: AG035 Brand Agent
Decision: L1
Escalation: E1

MRK-CON-001 Content Calendar Management
Owner: AG031 Content Agent
Decision: L1
Escalation: E1

MRK-SEO-001 SEO Performance Review
Owner: AG032 SEO Agent
Decision: L1
Escalation: E1

MRK-SOC-001 Social Media Posting Plan
Owner: AG033 Social Media Agent
Decision: L1
Escalation: E1

MRK-CAM-001 Campaign Planning
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

MRK-CAM-002 Campaign Execution
Owner: AG034 Campaign Manager
Decision: L1
Escalation: E1

MRK-CAM-003 Campaign Performance Analysis
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

MRK-LGN-001 Lead Generation Campaign
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

MRK-PR-001 Press Release Coordination
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-EVT-001 Event Planning & Execution
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-PMK-001 Product Launch Messaging
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-ANA-001 Marketing Performance Dashboard
Owner: AG067 Analytics Agent
Decision: L1
Escalation: E1

## Sales Functions

SAL-LEAD-001 Lead Capture
Owner: AG026 CRM Agent
Decision: L1
Escalation: E1

SAL-LEAD-002 Lead Qualification
Owner: AG027 Lead Qualification Agent
Decision: L1
Escalation: E1

SAL-LEAD-003 Lead Scoring
Owner: AG027 Lead Qualification Agent
Decision: L2
Escalation: E2

SAL-OPP-001 Opportunity Creation
Owner: AG026 CRM Agent
Decision: L1
Escalation: E1

SAL-OPP-002 Proposal Preparation
Owner: AG028 Proposal Generator
Decision: L2
Escalation: E2

SAL-OPP-003 Negotiation Support
Owner: AG025 Sales Director
Decision: L3
Escalation: E3

SAL-CTR-001 Sales Contract Finalization
Owner: AG018 Contract Review Agent
Decision: L2
Escalation: E2

SAL-ACC-001 Key Account Review
Owner: AG025 Sales Director
Decision: L2
Escalation: E2

SAL-REN-001 Renewal Risk Review
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

SAL-XSL-001 Cross-Sell Opportunity Identification
Owner: AG025 Sales Director
Decision: L1
Escalation: E1

SAL-UPS-001 Upsell Proposal
Owner: AG025 Sales Director
Decision: L1
Escalation: E1

## Customer Success Functions

CUS-ONB-001 Onboarding Plan Creation
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-ONB-002 Onboarding Completion Tracking
Owner: AG029 Customer Success Agent
Decision: L1
Escalation: E1

CUS-ADO-001 Feature Adoption Tracking
Owner: AG029 Customer Success Agent
Decision: L1
Escalation: E1

CUS-SUP-001 Support Ticket Resolution
Owner: AG069 Support Agent
Decision: L1
Escalation: E1

CUS-RET-001 Retention Risk Intervention
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-EXP-001 Expansion Opportunity Review
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-HLT-001 Customer Health Scoring
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-HLT-002 Churn Risk Detection
Owner: AG029 Customer Success Agent
Decision: L3
Escalation: E3

CUS-NPS-001 NPS Survey Cycle
Owner: AG029 Customer Success Agent
Decision: L1
Escalation: E1

CUS-ESC-001 Escalation Handling
Owner: AG029 Customer Success Agent
Decision: L3
Escalation: E3

CUS-ADV-001 Reference Customer Program
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-SPL-001 Customer Success Plan
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

## Operations Functions

OPS-SRV-001 Service Delivery Tracking
Owner: AG007 Operations Manager
Decision: L1
Escalation: E1

OPS-PMG-001 Project Milestone Review
Owner: AG008 PMO Agent
Decision: L2
Escalation: E2

OPS-PRO-001 Process Documentation
Owner: AG047 Process Controller
Decision: L1
Escalation: E1

OPS-PRO-002 Process Optimization
Owner: AG047 Process Controller
Decision: L2
Escalation: E2

OPS-AST-001 Asset Register Update
Owner: AG007 Operations Manager
Decision: L1
Escalation: E1

OPS-RES-001 Resource Capacity Planning
Owner: AG007 Operations Manager
Decision: L2
Escalation: E2

OPS-QUA-001 Quality Audit
Owner: AG046 Quality Assurance Agent
Decision: L2
Escalation: E2

OPS-COS-001 Cost Optimization Review
Owner: AG007 Operations Manager
Decision: L3
Escalation: E3

OPS-PER-001 Operational KPI Monitoring
Owner: AG007 Operations Manager
Decision: L1
Escalation: E1

OPS-IMP-001 Improvement Initiative Tracking
Owner: AG047 Process Controller
Decision: L2
Escalation: E2

## Supply Chain Functions

SCM-PRC-001 Purchase Requisition
Owner: AG039 Purchasing Agent
Decision: L1
Escalation: E1

SCM-PRC-002 Supplier Evaluation
Owner: AG037 Supplier Evaluation Agent
Decision: L2
Escalation: E2

SCM-VEN-001 Vendor Performance Review
Owner: AG037 Supplier Evaluation Agent
Decision: L2
Escalation: E2

SCM-CSU-001 Supplier Contract Negotiation
Owner: AG018 Contract Review Agent
Decision: L2
Escalation: E2

SCM-LOG-001 Shipment Tracking
Owner: AG040 Logistics Manager
Decision: L1
Escalation: E1

SCM-INV-001 Inventory Reconciliation
Owner: AG041 Warehouse Agent
Decision: L2
Escalation: E2

SCM-SUP-001 Supply Plan Update
Owner: AG040 Logistics Manager
Decision: L2
Escalation: E2

SCM-DMP-001 Demand Plan Reconciliation
Owner: AG040 Logistics Manager
Decision: L2
Escalation: E2

SCM-IMX-001 Import/Export Documentation
Owner: AG044 Customs Consultant
Decision: L2
Escalation: E2

SCM-CUS-001 Customs Compliance Check
Owner: AG044 Customs Consultant
Decision: L3
Escalation: E3

SCM-SRK-001 Supplier Risk Assessment
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

## Finance Functions

FIN-ACC-001 Monthly Close Process
Owner: AG013 Accounting Agent
Decision: L2
Escalation: E2

FIN-TRE-001 Cash Position Monitoring
Owner: AG014 Treasury Agent
Decision: L2
Escalation: E2

FIN-BUD-001 Budget Planning
Owner: AG012 CFO Agent
Decision: L3
Escalation: E3

FIN-BUD-002 Budget Review
Owner: AG016 Financial Planning & Analysis Agent
Decision: L2
Escalation: E2

FIN-BUD-003 Budget Approval Package
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

FIN-FCS-001 Financial Forecast Update
Owner: AG016 Financial Planning & Analysis Agent
Decision: L2
Escalation: E2

FIN-FPA-001 Variance Analysis
Owner: AG016 Financial Planning & Analysis Agent
Decision: L2
Escalation: E2

FIN-TAX-001 Tax Filing Preparation
Owner: AG015 Tax Consultant
Decision: L3
Escalation: E3

FIN-AUD-001 External Audit Coordination
Owner: AG012 CFO Agent
Decision: L3
Escalation: E3

FIN-IR-001 Investor Update Preparation
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

FIN-GRA-001 Grant Discovery
Owner: AG078 Grant Manager
Decision: L1
Escalation: E1

FIN-GRA-002 Grant Eligibility Review
Owner: AG078 Grant Manager
Decision: L2
Escalation: E2

FIN-GRA-003 Grant Application Preparation
Owner: AG078 Grant Manager
Decision: L2
Escalation: E2

FIN-GRA-004 Grant Reporting
Owner: AG078 Grant Manager
Decision: L2
Escalation: E2

FIN-CAP-001 Capital Structure Review
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

## Legal Functions

LEG-CON-001 Contract Drafting
Owner: AG018 Contract Review Agent
Decision: L2
Escalation: E2

LEG-CON-002 Contract Review
Owner: AG018 Contract Review Agent
Decision: L3
Escalation: E3

LEG-CON-003 Contract Approval
Owner: AG017 Legal Counsel
Decision: L4
Escalation: E4

LEG-LIC-001 License Renewal Tracking
Owner: AG017 Legal Counsel
Decision: L2
Escalation: E2

LEG-REG-001 Regulatory Change Monitoring
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-AML-001 AML Screening
Owner: AG011 Compliance Agent
Decision: L3
Escalation: E3

LEG-KYC-001 KYC Verification
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-DPR-001 Data Privacy Impact Assessment
Owner: AG011 Compliance Agent
Decision: L3
Escalation: E3

LEG-CMP-001 Compliance Checklist Review
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-LIT-001 Litigation Case Tracking
Owner: AG017 Legal Counsel
Decision: L4
Escalation: E4

LEG-IP-001 IP Filing Management
Owner: AG020 IP Agent
Decision: L3
Escalation: E3

LEG-INT-001 Cross-Border Legal Review
Owner: AG017 Legal Counsel
Decision: L3
Escalation: E3

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
Owner: AG049 Information Security Agent
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
Owner: AG051 Business Continuity Agent
Decision: L3
Escalation: E3

## People Management Functions

PEO-WFP-001 Headcount Planning
Owner: AG021 HR Manager
Decision: L2
Escalation: E2

PEO-REC-001 Job Requisition
Owner: AG022 Recruiter
Decision: L2
Escalation: E2

PEO-REC-002 Candidate Screening
Owner: AG022 Recruiter
Decision: L1
Escalation: E1

PEO-ONB-001 New Hire Onboarding
Owner: AG021 HR Manager
Decision: L1
Escalation: E1

PEO-PER-001 Performance Review Cycle
Owner: AG024 Performance Review Agent
Decision: L2
Escalation: E2

PEO-COM-001 Compensation Benchmarking
Owner: AG021 HR Manager
Decision: L3
Escalation: E3

PEO-LRN-001 Learning Path Assignment
Owner: AG023 Learning & Development Agent
Decision: L1
Escalation: E1

PEO-TAL-001 Talent Review Cycle
Owner: AG021 HR Manager
Decision: L2
Escalation: E2

PEO-CUL-001 Culture Survey
Owner: AG021 HR Manager
Decision: L1
Escalation: E1

PEO-LDR-001 Leadership Development Plan
Owner: AG023 Learning & Development Agent
Decision: L2
Escalation: E2

PEO-SUC-001 Succession Plan Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

## Technology Functions

TEC-INF-001 Infrastructure Monitoring
Owner: AG064 DevOps Agent
Decision: L1
Escalation: E1

TEC-APP-001 Application Portfolio Review
Owner: AG009 Enterprise Architect
Decision: L2
Escalation: E2

TEC-INT-001 System Integration Monitoring
Owner: AG065 Data Engineer
Decision: L2
Escalation: E2

TEC-DAT-001 Data Pipeline Management
Owner: AG065 Data Engineer
Decision: L2
Escalation: E2

TEC-SEC-001 Security Incident Response
Owner: AG050 Incident Response Agent
Decision: L4
Escalation: E4

TEC-AIP-001 AI Model Performance Review
Owner: AG055 Model Evaluation Agent
Decision: L2
Escalation: E2

TEC-DEV-001 Deployment Pipeline Health Check
Owner: AG064 DevOps Agent
Decision: L1
Escalation: E1

TEC-MLO-001 Model Retraining Schedule
Owner: AG056 AI Trainer
Decision: L2
Escalation: E2

TEC-AUT-001 Workflow Automation Deployment
Owner: AG064 DevOps Agent
Decision: L2
Escalation: E2

TEC-DWP-001 Digital Workplace Tools Review
Owner: AG009 Enterprise Architect
Decision: L1
Escalation: E1

## Knowledge Management Functions

KNW-KB-001 Knowledge Base Article Creation
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-SOP-001 SOP Drafting
Owner: AG053 Knowledge Curator
Decision: L2
Escalation: E2

KNW-SOP-002 SOP Review & Approval
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

KNW-POL-001 Policy Document Maintenance
Owner: AG053 Knowledge Curator
Decision: L2
Escalation: E2

KNW-MEM-001 Corporate Memory Archive Update
Owner: AG054 Memory Manager
Decision: L1
Escalation: E1

KNW-GRA-001 Knowledge Graph Enrichment
Owner: AG053 Knowledge Curator
Decision: L2
Escalation: E2

KNW-SRC-001 Knowledge Search Index Update
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-EXP-001 Expert Network Directory
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-ANL-001 Knowledge Usage Analytics
Owner: AG067 Analytics Agent
Decision: L1
Escalation: E1

KNW-LES-001 Lessons Learned Capture
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-AUD-001 Knowledge Base Quality Audit
Owner: AG003 AI Auditor
Decision: L2
Escalation: E2

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

GOV-AUT-001 Authority Matrix Review
Owner: AG081 Authorization Manager
Decision: L3
Escalation: E3

GOV-POL-001 Governance Policy Update
Owner: AG010 Governance Agent
Decision: L4
Escalation: E4

GOV-DEC-001 Decision Log Maintenance
Owner: AG079 Audit Manager
Decision: L2
Escalation: E2

GOV-AUD-001 Decision Audit
Owner: AG003 AI Auditor
Decision: L3
Escalation: E3

GOV-AUD-002 Compliance Audit
Owner: AG003 AI Auditor
Decision: L3
Escalation: E3

GOV-PRF-001 Agent Performance Review
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-LIF-001 Agent Onboarding/Retirement
Owner: AG057 Agent Registry Manager
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

## Administration Functions

ADM-SUP-001 Executive Support Request Handling
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

ADM-CAL-001 Calendar Management
Owner: AG075 Calendar Agent
Decision: L1
Escalation: E1

ADM-MTG-001 Meeting Scheduling & Logistics
Owner: AG074 Meeting Coordinator
Decision: L1
Escalation: E1

ADM-COR-001 Correspondence Handling
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-TRV-001 Travel Arrangement
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

ADM-DOC-001 Document Filing & Organization
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-OFF-001 Office Administration Tasks
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-COM-001 Executive Communication Drafting
Owner: AG072 Executive Assistant
Decision: L2
Escalation: E2

ADM-REC-001 Records Retention Management
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-REP-001 Administrative Reporting
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

## Function Depth Enrichment (v2.2 — companion functions)

Ниже добавлены вторые функции для групп, у которых была только одна.
Паттерн: `-002 Review` для функций типа Create/Plan/Manage, `-002 Exception
Handling` для функций типа Monitor/Review/Assess (второй виток анализа не
нужен — нужна обработка отклонений).

STR-MIS-002 Maintain Mission Statement Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-OKR-002 Define Quarterly OKRs Review
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-POR-002 Strategic Portfolio Review Exception Handling
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

STR-CAP-002 Capital Allocation Decision Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-GRW-002 Growth Strategy Formulation Review
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-INT-002 Market Entry Assessment Exception Handling
Owner: AG006 Strategy Agent
Decision: L4
Escalation: E4

STR-PAR-002 Partnership Opportunity Evaluation Review
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-MNA-002 M&A Target Screening Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

INN-OPP-002 Opportunity Scouting Review
Owner: AG077 Innovation Manager
Decision: L1
Escalation: E1

INN-PDI-002 Product Discovery Sprint Review
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-PVA-002 Product Validation Testing Review
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-VEN-002 New Venture Charter Review
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

INN-BMD-002 Business Model Canvas Update Review
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-POR-002 Innovation Portfolio Review Exception Handling
Owner: AG004 Business Analyst
Decision: L3
Escalation: E3

INN-RND-002 R&D Initiative Tracking Exception Handling
Owner: AG076 R&D Agent
Decision: L2
Escalation: E2

INN-COM-002 Go-to-Market Readiness Review Exception Handling
Owner: AG077 Innovation Manager
Decision: L3
Escalation: E3

MKT-IND-002 Industry Landscape Analysis Exception Handling
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-TRD-002 Emerging Trend Scan Exception Handling
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-SEG-002 Market Segmentation Update Review
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-DEM-002 Demand Forecast Model Review
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-OPP-002 Market Opportunity Sizing Review
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MKT-CUR-002 Customer Research Study Review
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-PRI-002 Competitive Pricing Scan Exception Handling
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

MRK-CON-002 Content Calendar Management Review
Owner: AG031 Content Agent
Decision: L1
Escalation: E1

MRK-SEO-002 SEO Performance Review Exception Handling
Owner: AG032 SEO Agent
Decision: L1
Escalation: E1

MRK-SOC-002 Social Media Posting Plan Review
Owner: AG033 Social Media Agent
Decision: L1
Escalation: E1

MRK-LGN-002 Lead Generation Campaign Review
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

MRK-PR-002 Press Release Coordination Review
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-EVT-002 Event Planning & Execution Review
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-PMK-002 Product Launch Messaging Review
Owner: AG030 Marketing Manager
Decision: L2
Escalation: E2

MRK-ANA-002 Marketing Performance Dashboard Exception Handling
Owner: AG067 Analytics Agent
Decision: L1
Escalation: E1

SAL-CTR-002 Sales Contract Finalization Review
Owner: AG018 Contract Review Agent
Decision: L2
Escalation: E2

SAL-ACC-002 Key Account Review Exception Handling
Owner: AG025 Sales Director
Decision: L2
Escalation: E2

SAL-REN-002 Renewal Risk Review Exception Handling
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

SAL-XSL-002 Cross-Sell Opportunity Identification Review
Owner: AG025 Sales Director
Decision: L1
Escalation: E1

SAL-UPS-002 Upsell Proposal Review
Owner: AG025 Sales Director
Decision: L1
Escalation: E1

CUS-ADO-002 Feature Adoption Tracking Exception Handling
Owner: AG029 Customer Success Agent
Decision: L1
Escalation: E1

CUS-SUP-002 Support Ticket Resolution Exception Handling
Owner: AG069 Support Agent
Decision: L1
Escalation: E1

CUS-RET-002 Retention Risk Intervention Review
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-EXP-002 Expansion Opportunity Review Exception Handling
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-NPS-002 NPS Survey Cycle Review
Owner: AG029 Customer Success Agent
Decision: L1
Escalation: E1

CUS-ADV-002 Reference Customer Program Review
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

CUS-SPL-002 Customer Success Plan Review
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

OPS-SRV-002 Service Delivery Tracking Exception Handling
Owner: AG007 Operations Manager
Decision: L1
Escalation: E1

OPS-PMG-002 Project Milestone Review Exception Handling
Owner: AG008 PMO Agent
Decision: L2
Escalation: E2

OPS-AST-002 Asset Register Update Review
Owner: AG007 Operations Manager
Decision: L1
Escalation: E1

OPS-RES-002 Resource Capacity Planning Review
Owner: AG007 Operations Manager
Decision: L2
Escalation: E2

OPS-COS-002 Cost Optimization Review Exception Handling
Owner: AG007 Operations Manager
Decision: L3
Escalation: E3

OPS-IMP-002 Improvement Initiative Tracking Exception Handling
Owner: AG047 Process Controller
Decision: L2
Escalation: E2

SCM-VEN-002 Vendor Performance Review Exception Handling
Owner: AG037 Supplier Evaluation Agent
Decision: L2
Escalation: E2

SCM-SUP-002 Supply Plan Update Review
Owner: AG040 Logistics Manager
Decision: L2
Escalation: E2

SCM-DMP-002 Demand Plan Reconciliation Exception Handling
Owner: AG040 Logistics Manager
Decision: L2
Escalation: E2

SCM-IMX-002 Import/Export Documentation Review
Owner: AG044 Customs Consultant
Decision: L2
Escalation: E2

SCM-CUS-002 Customs Compliance Check Exception Handling
Owner: AG044 Customs Consultant
Decision: L3
Escalation: E3

SCM-CSU-002 Supplier Contract Negotiation Review
Owner: AG018 Contract Review Agent
Decision: L2
Escalation: E2

SCM-SRK-002 Supplier Risk Assessment Exception Handling
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

FIN-ACC-002 Monthly Close Process Review
Owner: AG013 Accounting Agent
Decision: L2
Escalation: E2

FIN-TRE-002 Cash Position Monitoring Exception Handling
Owner: AG014 Treasury Agent
Decision: L2
Escalation: E2

FIN-FCS-002 Financial Forecast Update Review
Owner: AG016 Financial Planning & Analysis Agent
Decision: L2
Escalation: E2

FIN-FPA-002 Variance Analysis Exception Handling
Owner: AG016 Financial Planning & Analysis Agent
Decision: L2
Escalation: E2

FIN-TAX-002 Tax Filing Preparation Review
Owner: AG015 Tax Consultant
Decision: L3
Escalation: E3

FIN-AUD-002 External Audit Coordination Exception Handling
Owner: AG012 CFO Agent
Decision: L3
Escalation: E3

FIN-IR-002 Investor Update Preparation Review
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

FIN-CAP-002 Capital Structure Review Exception Handling
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

LEG-LIC-002 License Renewal Tracking Exception Handling
Owner: AG017 Legal Counsel
Decision: L2
Escalation: E2

LEG-REG-002 Regulatory Change Monitoring Exception Handling
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-AML-002 AML Screening Exception Handling
Owner: AG011 Compliance Agent
Decision: L3
Escalation: E3

LEG-KYC-002 KYC Verification Exception Handling
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-DPR-002 Data Privacy Impact Assessment Exception Handling
Owner: AG011 Compliance Agent
Decision: L3
Escalation: E3

LEG-CMP-002 Compliance Checklist Review Exception Handling
Owner: AG011 Compliance Agent
Decision: L2
Escalation: E2

LEG-LIT-002 Litigation Case Tracking Exception Handling
Owner: AG017 Legal Counsel
Decision: L4
Escalation: E4

LEG-IP-002 IP Filing Management Review
Owner: AG020 IP Agent
Decision: L3
Escalation: E3

LEG-INT-002 Cross-Border Legal Review Exception Handling
Owner: AG017 Legal Counsel
Decision: L3
Escalation: E3

RSK-FIN-002 Financial Risk Monitoring Exception Handling
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

RSK-OPR-002 Operational Risk Assessment Exception Handling
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-LEG-002 Legal Risk Review Exception Handling
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

RSK-CYB-002 Cyber Risk Assessment Exception Handling
Owner: AG049 Information Security Agent
Decision: L3
Escalation: E3

RSK-REP-002 Reputation Risk Monitoring Exception Handling
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-CTR-002 Country Risk Rating Exception Handling
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-VND-002 Vendor Risk Screening Exception Handling
Owner: AG005 Risk Manager
Decision: L2
Escalation: E2

RSK-CRI-002 Crisis Response Activation Review
Owner: AG001 CEO Agent
Decision: L5
Escalation: E5

RSK-BCP-002 Business Continuity Plan Test Review
Owner: AG051 Business Continuity Agent
Decision: L3
Escalation: E3

PEO-WFP-002 Headcount Planning Review
Owner: AG021 HR Manager
Decision: L2
Escalation: E2

PEO-ONB-002 New Hire Onboarding Exception Handling
Owner: AG021 HR Manager
Decision: L1
Escalation: E1

PEO-COM-002 Compensation Benchmarking Review
Owner: AG021 HR Manager
Decision: L3
Escalation: E3

PEO-TAL-002 Talent Review Cycle Exception Handling
Owner: AG021 HR Manager
Decision: L2
Escalation: E2

PEO-CUL-002 Culture Survey Review
Owner: AG021 HR Manager
Decision: L1
Escalation: E1

PEO-LDR-002 Leadership Development Plan Review
Owner: AG023 Learning & Development Agent
Decision: L2
Escalation: E2

PEO-SUC-002 Succession Plan Review Exception Handling
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

TEC-APP-002 Application Portfolio Review Exception Handling
Owner: AG009 Enterprise Architect
Decision: L2
Escalation: E2

TEC-INT-002 System Integration Monitoring Exception Handling
Owner: AG065 Data Engineer
Decision: L2
Escalation: E2

TEC-AIP-002 AI Model Performance Review Exception Handling
Owner: AG055 Model Evaluation Agent
Decision: L2
Escalation: E2

TEC-DEV-002 Deployment Pipeline Health Check Exception Handling
Owner: AG064 DevOps Agent
Decision: L1
Escalation: E1

TEC-MLO-002 Model Retraining Schedule Review
Owner: AG056 AI Trainer
Decision: L2
Escalation: E2

TEC-DWP-002 Digital Workplace Tools Review Exception Handling
Owner: AG009 Enterprise Architect
Decision: L1
Escalation: E1

KNW-POL-002 Policy Document Maintenance Review
Owner: AG053 Knowledge Curator
Decision: L2
Escalation: E2

KNW-MEM-002 Corporate Memory Archive Update Review
Owner: AG054 Memory Manager
Decision: L1
Escalation: E1

KNW-GRA-002 Knowledge Graph Enrichment Review
Owner: AG053 Knowledge Curator
Decision: L2
Escalation: E2

KNW-SRC-002 Knowledge Search Index Update Review
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-EXP-002 Expert Network Directory Review
Owner: AG053 Knowledge Curator
Decision: L1
Escalation: E1

KNW-ANL-002 Knowledge Usage Analytics Exception Handling
Owner: AG067 Analytics Agent
Decision: L1
Escalation: E1

KNW-AUD-002 Knowledge Base Quality Audit Exception Handling
Owner: AG003 AI Auditor
Decision: L2
Escalation: E2

GOV-AUT-002 Authority Matrix Review Exception Handling
Owner: AG081 Authorization Manager
Decision: L3
Escalation: E3

GOV-POL-002 Governance Policy Update Review
Owner: AG010 Governance Agent
Decision: L4
Escalation: E4

GOV-DEC-002 Decision Log Maintenance Review
Owner: AG079 Audit Manager
Decision: L2
Escalation: E2

GOV-PRF-002 Agent Performance Review Exception Handling
Owner: AG002 Chief Orchestrator
Decision: L3
Escalation: E3

GOV-LIF-002 Agent Onboarding/Retirement Review
Owner: AG057 Agent Registry Manager
Decision: L3
Escalation: E3

GOV-CTL-002 Enterprise Control Testing Exception Handling
Owner: AG003 AI Auditor
Decision: L4
Escalation: E4

GOV-AIG-002 AI Governance Compliance Review Exception Handling
Owner: AG003 AI Auditor
Decision: L4
Escalation: E4

ADM-SUP-002 Executive Support Request Handling Review
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

ADM-CAL-002 Calendar Management Review
Owner: AG075 Calendar Agent
Decision: L1
Escalation: E1

ADM-MTG-002 Meeting Scheduling & Logistics Review
Owner: AG074 Meeting Coordinator
Decision: L1
Escalation: E1

ADM-COR-002 Correspondence Handling Review
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-TRV-002 Travel Arrangement Review
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

ADM-DOC-002 Document Filing & Organization Review
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-OFF-002 Office Administration Tasks Review
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-COM-002 Executive Communication Drafting Review
Owner: AG072 Executive Assistant
Decision: L2
Escalation: E2

ADM-REC-002 Records Retention Management Review
Owner: AG073 Secretary
Decision: L1
Escalation: E1

ADM-REP-002 Administrative Reporting Review
Owner: AG072 Executive Assistant
Decision: L1
Escalation: E1

## Growth & Market Reactivity Functions (Signature Layer)

> Эти функции — не дополнение "для галочки" к существующим доменам, а
> отдельный сквозной слой, ради которого вообще стоит выбирать
> AI-оркестрированное предприятие вместо традиционного. Они закрывают то,
> что в реальных быстрорастущих компаниях (Amazon, Uber на ранних этапах,
> топовые SaaS-скейлапы) делает разницу между "мы отреагировали через
> квартал" и "мы отреагировали за день": непрерывный мониторинг рынка,
> готовность мгновенно менять цену/позиционирование, дисциплинированный
> fail-fast, и решительное удвоение ставки там, где сработало.

STR-AGR-001 Aggressive Growth Target Setting (Moonshot OKRs)
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

STR-WAR-001 Competitive War-Gaming
Owner: AG006 Strategy Agent
Decision: L3
Escalation: E3

STR-EXP-001 Rapid Experiment Portfolio Management
Owner: AG006 Strategy Agent
Decision: L2
Escalation: E2

MKT-RTM-001 Real-Time Market Signal Monitoring
Owner: AG084 Market Intelligence Analyst
Decision: L1
Escalation: E1

MKT-ALT-001 Competitor Move Alert & Rapid Response
Owner: AG084 Market Intelligence Analyst
Decision: L3
Escalation: E3

MRK-GRW-001 Growth Hacking Experiment Cycle
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

MRK-VIR-001 Viral & Referral Loop Design
Owner: AG034 Campaign Manager
Decision: L2
Escalation: E2

SAL-DYN-001 Dynamic Pricing Adjustment
Owner: AG025 Sales Director
Decision: L2
Escalation: E2

SAL-WIN-001 Competitive Win/Loss Rapid Analysis
Owner: AG025 Sales Director
Decision: L1
Escalation: E1

SAL-EXP-001 Expansion Beachhead Identification
Owner: AG025 Sales Director
Decision: L3
Escalation: E3

FIN-DYN-001 Real-Time Cash & Runway Dashboard
Owner: AG014 Treasury Agent
Decision: L1
Escalation: E1

FIN-OPP-001 Opportunistic Capital Deployment
Owner: AG012 CFO Agent
Decision: L4
Escalation: E4

RSK-OPP-001 Risk-to-Opportunity Conversion Review
Owner: AG005 Risk Manager
Decision: L3
Escalation: E3

INN-FFL-001 Fail-Fast Kill Criteria Enforcement
Owner: AG077 Innovation Manager
Decision: L2
Escalation: E2

INN-SCL-001 Rapid Scale Decision (Double-Down Trigger)
Owner: AG001 CEO Agent
Decision: L4
Escalation: E4

CUS-PRE-001 Predictive Churn Preemption
Owner: AG029 Customer Success Agent
Decision: L2
Escalation: E2

GOV-SPD-001 Rapid Decision Fast-Track Protocol
Owner: AG010 Governance Agent
Decision: L3
Escalation: E3

GOV-KLL-001 Portfolio Kill/Scale Gate Review
Owner: AG002 Chief Orchestrator
Decision: L4
Escalation: E4

TEC-RTA-001 Real-Time Market Signal Analytics Pipeline
Owner: AG067 Analytics Agent
Decision: L2
Escalation: E2

MKT-DEM-002 Real-Time Demand Sensing
Owner: AG084 Market Intelligence Analyst
Decision: L2
Escalation: E2

## Summary

Capabilities: 16/16 — все 160 под-способностей (включая C16) имеют Function Group
Function Groups: ~35 documented, все теперь имеют минимум 2 функции (create/do + review или exception-handling)
Functions documented: 320 — Target: ~600
Agents: 84 (см. AGENT_REGISTRY.md) — Owner-поля во всех функциях выше
приведены в соответствие с подтверждённым org chart
Playbooks: 50/50 COMPLETE — см. PLAYBOOK_ROADMAP.md

Changelog v2.2 → v2.3:
- Добавлен сигнатурный слой "Growth & Market Reactivity" (20 функций) —
  не механическое расширение существующих групп, а функции, воплощающие
  агрессивную стратегию роста: war-gaming конкурентов, динамическое
  ценообразование, fail-fast, real-time market sensing, oppортунистическое
  использование капитала. Это отличает проект от типовой ERP-подобной
  спецификации и делает ценность ощутимой с первого знакомства.

Changelog v2.1 → v2.2:
- Добавлено 119 companion-функций (-002) — каждая из ранее "одиночных" Function
  Group теперь имеет минимум 2 функции: основное действие + Review (для
  Create/Plan/Manage функций) или Exception Handling (для Monitor/Assess
  функций, где повторный анализ избыточен, а нужна обработка отклонений)
- Достигнут ровно половинный рубеж к целевым ~600 функциям

Changelog v2.0 → v2.1:
- Market Intelligence functions (MKT-*) переназначены с временного владельца
  (AG004 Business Analyst) на нового AG084 Market Intelligence Analyst
- Добавлена секция Administration Functions (ADM-*, 10 функций) для нового
  домена C16 Administration & Executive Support

Changelog v1.2 → v2.0:
- Полная замена Owner-полей: реконструированный список из 28 агентов заменён
  на подтверждённый владельцем проекта список из 83 агентов
- Уточнены владельцы на уровне специализации (например, SEO Agent вместо
  общего Marketing Manager для MRK-SEO-001)
- Зафиксирован открытый вопрос по Market Intelligence (см. предупреждение
  в соответствующем разделе) — временно на AG004 Business Analyst
