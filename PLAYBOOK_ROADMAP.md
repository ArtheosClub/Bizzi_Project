# PLAYBOOK_ROADMAP.md

# Art of Business Playbook Roadmap

Version: 2.0
Status: COMPLETE — все 50 целевых playbooks написаны ✅✅✅✅✅

## Purpose

Единый реестр всех 50 playbooks. Каждый playbook привязан к Capability
домену и конкретным Function ID из ENTERPRISE_FUNCTION_REGISTRY.md, следует
7-стадийной Decision Architecture (Idea → Analysis → Risk Review → Decision
→ Execution → Audit → Knowledge Capture) из GOVERNANCE_MODEL.md.

## Done (50/50) — 100% Complete

### Priority 1 — Core Revenue & Operations (14)

| ID | Название | Домен |
|---|---|---|
| PB001 | Grant Acquisition | C09 Finance |
| PB002 | Budget Planning & Approval | C09 Finance |
| PB003 | Customer Onboarding | C06 Customer Success |
| PB004 | Lead-to-Contract (Sales Cycle) | C05 Sales |
| PB005 | Renewal & Retention Cycle | C05/C06 |
| PB006 | Upsell & Cross-Sell Motion | C05 Sales |
| PB007 | Support Ticket Escalation | C06 Customer Success |
| PB008 | Monthly Financial Close | C09 Finance |
| PB009 | Vendor Onboarding & Evaluation | C08 Supply Chain |
| PB010 | Procurement Request-to-Pay | C08 Supply Chain |
| PB011 | Employee Onboarding | C12 People |
| PB012 | Recruitment Cycle | C12 People |
| PB013 | Contract Review & Approval | C10 Legal |
| PB014 | Compliance Monitoring Cycle | C10 Legal |

### Priority 2 — Governance & Risk (8)

| ID | Название | Домен |
|---|---|---|
| PB015 | Risk Identification & Treatment | C11 Risk |
| PB016 | Cyber Incident Response | C11/C13 |
| PB017 | Crisis Management Activation | C11 Risk |
| PB018 | Agent Performance Review | C15 Governance |
| PB019 | Decision Audit Cycle | C15 Governance |
| PB020 | Agent Lifecycle (Onboarding/Retirement) | C15 Governance |
| PB021 | Escalation Handling Protocol | C15 Governance |
| PB022 | AI Governance Compliance Review | C15 Governance |

### Priority 3 — Growth & Innovation (8)

| ID | Название | Домен |
|---|---|---|
| PB023 | Idea-to-MVP Pipeline | C02 Innovation |
| PB024 | Market Entry Assessment | C01/C03 |
| PB025 | Partnership Opportunity Evaluation | C01 Strategy |
| PB026 | M&A Target Screening | C01 Strategy |
| PB027 | Product Launch (Go-to-Market) | C02/C04 |
| PB028 | Content Marketing Cycle | C04 Marketing |
| PB029 | Campaign Planning & Execution | C04 Marketing |
| PB030 | Event Planning & Execution | C04 Marketing |

### Priority 4 — Operations & Technology (8)

| ID | Название | Домен |
|---|---|---|
| PB031 | Quality Audit Cycle | C07 Operations |
| PB032 | Process Optimization Review | C07 Operations |
| PB033 | Resource Capacity Planning | C07 Operations |
| PB034 | Supply & Demand Planning | C08 Supply Chain |
| PB035 | Import/Export & Customs Compliance | C08 Supply Chain |
| PB036 | System Integration Rollout | C13 Technology |
| PB037 | AI Model Deployment & Retraining | C13 Technology |
| PB038 | Deployment Pipeline Health Check | C13 Technology |

### Priority 5 — Finance, People, Knowledge (12)

| ID | Название | Домен |
|---|---|---|
| PB039 | Tax Filing Cycle | C09 Finance |
| PB040 | External Audit Coordination | C09 Finance |
| PB041 | Investor Relations Update | C09 Finance |
| PB042 | Capital Structure Review | C09 Finance |
| PB043 | Compensation Benchmarking Cycle | C12 People |
| PB044 | Talent Review & Succession Planning | C12 People |
| PB045 | Leadership Development Program | C12 People |
| PB046 | Knowledge Base Quality Audit | C14 Knowledge |
| PB047 | SOP Drafting & Approval | C14 Knowledge |
| PB048 | Policy Document Lifecycle | C14/C15 |
| PB049 | Data Privacy Impact Assessment | C10 Legal |
| PB050 | Litigation Case Management | C10 Legal |

## Coverage Summary

- **Все 16 Capability доменов** имеют минимум один playbook
- **Cross-referencing:** playbooks ссылаются друг на друга как источники/
  получатели (например, PB004 Lead-to-Contract → PB003 Customer Onboarding
  → PB005 Renewal → PB006 Upsell, замкнутый цикл клиента)
- **Мета-playbooks:** PB021 (Escalation Protocol) и PB038 (Deployment
  Pipeline) работают как общие сервисы, на которые ссылаются другие
  playbooks вместо дублирования логики
- **Границы автоматизации честно обозначены:** PB026 (M&A) и PB050
  (Litigation) явно указывают, что финальная часть процесса ведётся людьми
  и внешними советниками вне Decision Architecture

## How to add a new Playbook (для будущего расширения за пределы 50)

1. Определить Capability домен и Function ID, которые playbook покрывает
2. Использовать PLAYBOOK_TEMPLATE.md как основу
3. Пройти все 7 стадий Decision Architecture
4. Указать Related Documents — связи с существующими playbooks/функциями
5. Добавить запись в этот файл
6. Обновить счётчик в README.md
