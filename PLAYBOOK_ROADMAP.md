# PLAYBOOK_ROADMAP.md

# Art of Business Playbook Roadmap

Version: 1.0
Status: Living Document — обновляется по мере создания новых playbooks

## Purpose

Единый backlog всех целевых playbooks (50+). Каждый playbook привязан к
Capability домену и конкретным Function ID из ENTERPRISE_FUNCTION_REGISTRY.md.
Статусы: **Done** (написан полностью), **Draft** (частично описан),
**Planned** (только определён, не начат).

## Done (8)

| ID | Название | Домен | Функции |
|---|---|---|---|
| PB001 | Grant Acquisition | C09 Finance | FIN-GRA-001..004 |
| PB002 | Budget Planning & Approval | C09 Finance | FIN-BUD-001..003 |
| PB003 | Customer Onboarding | C06 Customer Success | CUS-ONB-001..002 |
| PB004 | Lead-to-Contract (Sales Cycle) | C05 Sales | SAL-LEAD, SAL-OPP, SAL-CTR |
| PB008 | Monthly Financial Close | C09 Finance | FIN-ACC-001, FIN-FPA-001 |
| PB011 | Employee Onboarding | C12 People | PEO-ONB-001, PEO-WFP-001 |
| PB012 | Recruitment Cycle | C12 People | PEO-REC-001, PEO-REC-002 |
| PB013 | Contract Review & Approval | C10 Legal | LEG-CON-001..003 |

## Planned — Priority 1 (core revenue & operations cycle)

| ID | Название | Домен | Функции (основные) |
|---|---|---|---|
| PB005 | Renewal & Retention Cycle | C05/C06 | SAL-REN-001, CUS-RET-001 |
| PB006 | Upsell & Cross-Sell Motion | C05 Sales | SAL-XSL-001, SAL-UPS-001 |
| PB007 | Support Ticket Escalation | C06 Customer Success | CUS-SUP-001, CUS-ESC-001 |
| PB009 | Vendor Onboarding & Evaluation | C08 Supply Chain | SCM-VEN-001, SCM-CSU-001 |
| PB010 | Procurement Request-to-Pay | C08 Supply Chain | SCM-PRC-001, SCM-PRC-002 |
| PB014 | Compliance Monitoring Cycle | C10 Legal | LEG-CMP-001, LEG-REG-001 |

## Planned — Priority 2 (governance & risk)

| ID | Название | Домен | Функции (основные) |
|---|---|---|---|
| PB015 | Risk Identification & Treatment | C11 Risk | RSK-ERM-001..003 |
| PB016 | Cyber Incident Response | C11/C13 | RSK-CYB-001, TEC-SEC-001 |
| PB017 | Crisis Management Activation | C11 Risk | RSK-CRI-001, RSK-BCP-001 |
| PB018 | Agent Performance Review | C15 Governance | GOV-PRF-001 |
| PB019 | Decision Audit Cycle | C15 Governance | GOV-AUD-001..002 |
| PB020 | Agent Lifecycle (Onboarding/Retirement) | C15 Governance | GOV-LIF-001 |
| PB021 | Escalation Handling Protocol | C15 Governance | GOV-ORC-003 |
| PB022 | AI Governance Compliance Review | C15 Governance | GOV-AIG-001 |

## Planned — Priority 3 (growth & innovation)

| ID | Название | Домен | Функции (основные) |
|---|---|---|---|
| PB023 | Idea-to-MVP Pipeline | C02 Innovation | INN-IDE, INN-MVP |
| PB024 | Market Entry Assessment | C01/C03 | STR-INT-001, MKT-IND-001 |
| PB025 | Partnership Evaluation | C01 Strategy | STR-PAR-001 |
| PB026 | M&A Target Screening | C01 Strategy | STR-MNA-001 |
| PB027 | Product Launch (Go-to-Market) | C02/C04 | INN-COM-001, MRK-PMK-001 |
| PB028 | Content Marketing Cycle | C04 Marketing | MRK-CON-001, MRK-SEO-001 |
| PB029 | Campaign Planning & Execution | C04 Marketing | MRK-CAM-001..003 |
| PB030 | Event Planning & Execution | C04 Marketing | MRK-EVT-001 |

## Planned — Priority 4 (operations & technology)

| ID | Название | Домен | Функции (основные) |
|---|---|---|---|
| PB031 | Quality Audit Cycle | C07 Operations | OPS-QUA-001 |
| PB032 | Process Optimization Review | C07 Operations | OPS-PRO-002, OPS-IMP-001 |
| PB033 | Resource Capacity Planning | C07 Operations | OPS-RES-001 |
| PB034 | Supply & Demand Planning | C08 Supply Chain | SCM-SUP-001, SCM-DMP-001 |
| PB035 | Import/Export & Customs Compliance | C08 Supply Chain | SCM-IMX-001, SCM-CUS-001 |
| PB036 | System Integration Rollout | C13 Technology | TEC-INT-001 |
| PB037 | AI Model Deployment & Retraining | C13 Technology | TEC-AIP-001, TEC-MLO-001 |
| PB038 | Deployment Pipeline Health Check | C13 Technology | TEC-DEV-001 |

## Planned — Priority 5 (finance, people, knowledge)

| ID | Название | Домен | Функции (основные) |
|---|---|---|---|
| PB039 | Tax Filing Cycle | C09 Finance | FIN-TAX-001 |
| PB040 | External Audit Coordination | C09 Finance | FIN-AUD-001 |
| PB041 | Investor Relations Update | C09 Finance | FIN-IR-001 |
| PB042 | Capital Structure Review | C09 Finance | FIN-CAP-001 |
| PB043 | Compensation Benchmarking Cycle | C12 People | PEO-COM-001 |
| PB044 | Talent Review & Succession Planning | C12 People | PEO-TAL-001, PEO-SUC-001 |
| PB045 | Leadership Development Program | C12 People | PEO-LDR-001 |
| PB046 | Knowledge Base Quality Audit | C14 Knowledge | KNW-AUD-001 |
| PB047 | SOP Drafting & Approval | C14 Knowledge | KNW-SOP-001..002 |
| PB048 | Policy Document Lifecycle | C14/C15 | KNW-POL-001, GOV-POL-001 |
| PB049 | Data Privacy Impact Assessment | C10 Legal | LEG-DPR-001 |
| PB050 | Litigation Case Management | C10 Legal | LEG-LIT-001 |

## How to add a new Playbook

1. Взять следующий свободный ID из этого roadmap
2. Использовать PLAYBOOK_TEMPLATE.md как основу
3. Обязательно пройти все 7 стадий Decision Architecture (Idea → Analysis →
   Risk Review → Decision → Execution → Audit → Knowledge Capture)
4. Привязать к реальным Function ID из ENTERPRISE_FUNCTION_REGISTRY.md
5. Обновить статус в этом файле с Planned на Draft, затем на Done
6. Обновить счётчик в README.md
