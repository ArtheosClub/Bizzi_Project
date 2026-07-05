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

## Summary

Capabilities: 16/16 — все 160 под-способностей (включая новый C16) имеют Function Group
Function Groups: ~35 documented
Functions documented: 181 — Target: ~600
Agents: 84 (см. AGENT_REGISTRY.md v2.1) — Owner-поля во всех функциях выше
приведены в соответствие с подтверждённым org chart
Playbooks: 4 documented (PB001-004), roadmap на 50 в PLAYBOOK_ROADMAP.md

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
