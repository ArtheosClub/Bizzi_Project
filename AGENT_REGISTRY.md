# AGENT_REGISTRY.md

# Art of Business Agent Registry

Version: 2.1
Status: Confirmed structure — Market Intelligence agent added, Administration
mapped to new C16 domain (both per owner decision)

## Purpose

Agent Registry — единый реестр всех AI-агентов предприятия, основанный на
организационной структуре, утверждённой владельцем проекта. Каждый агент
привязан к Capability домену (см. CAPABILITY_MAP_v1.0.md) и имеет Decision
Level (см. GOVERNANCE_MODEL.md).

## Structure Overview

- **Executive Layer** — высшее руководство и governance-ядро (5 агентов)
- **Business Layer** — 18 департаментов, операционные агенты (~74 агента)
- **Platform Layer** — инфраструктура оркестра, не бизнес-функции (5 агентов,
  из которых 5 уже входят в Executive Layer как разделяемые роли)

Итого уникальных агентов: **84**

## Executive Layer

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG001 | CEO Agent | C01 Strategy | Human Board (L0) | L5 |
| AG002 | Chief Orchestrator | C15 Governance | AG001 | L5 |
| AG003 | AI Auditor | C15 Governance | AG002 | L4 |
| AG004 | Business Analyst | C01 Strategy | AG001 | L3 |
| AG005 | Risk Manager (Enterprise Risk Manager) | C11 Risk Management | AG002 | L4 |

## Market Intelligence

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG084 | Market Intelligence Analyst | C03 Market Intelligence | AG004 | L2 |

## Enterprise Management

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG006 | Strategy Agent | C01 Strategy | AG004 | L3 |
| AG007 | Operations Manager | C07 Operations | AG002 | L3 |
| AG008 | PMO Agent | C07 Operations | AG007 | L2 |
| AG009 | Enterprise Architect | C13 Technology | AG002 | L3 |
| AG010 | Governance Agent | C15 Governance | AG002 | L4 |
| AG011 | Compliance Agent | C10 Legal & Compliance | AG002 | L3 |

## Finance

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG012 | CFO Agent | C09 Finance | AG001 | L4 |
| AG013 | Accounting Agent | C09 Finance | AG012 | L2 |
| AG014 | Treasury Agent | C09 Finance | AG012 | L2 |
| AG015 | Tax Consultant | C09 Finance | AG012 | L3 |
| AG016 | Financial Planning & Analysis Agent | C09 Finance | AG012 | L2 |

## Legal

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG017 | Legal Counsel | C10 Legal & Compliance | AG002 | L4 |
| AG018 | Contract Review Agent | C10 Legal & Compliance | AG017 | L2 |
| AG019 | Corporate Governance Agent | C10 Legal & Compliance | AG017 | L3 |
| AG020 | IP Agent | C10 Legal & Compliance | AG017 | L3 |

## HR

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG021 | HR Manager | C12 People Management | AG002 | L3 |
| AG022 | Recruiter | C12 People Management | AG021 | L2 |
| AG023 | Learning & Development Agent | C12 People Management | AG021 | L2 |
| AG024 | Performance Review Agent | C12 People Management | AG021 | L2 |

## Sales

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG025 | Sales Director | C05 Sales | AG002 | L3 |
| AG026 | CRM Agent | C05 Sales | AG025 | L1 |
| AG027 | Lead Qualification Agent | C05 Sales | AG025 | L1 |
| AG028 | Proposal Generator | C05 Sales | AG025 | L2 |
| AG029 | Customer Success Agent | C06 Customer Success | AG025 | L2 |

## Marketing

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG030 | Marketing Manager | C04 Marketing | AG002 | L3 |
| AG031 | Content Agent | C04 Marketing | AG030 | L1 |
| AG032 | SEO Agent | C04 Marketing | AG030 | L1 |
| AG033 | Social Media Agent | C04 Marketing | AG030 | L1 |
| AG034 | Campaign Manager | C04 Marketing | AG030 | L2 |
| AG035 | Brand Agent | C04 Marketing | AG030 | L2 |

## Procurement

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG036 | Procurement Manager | C08 Supply Chain | AG007 | L2 |
| AG037 | Supplier Evaluation Agent | C08 Supply Chain | AG036 | L2 |
| AG038 | RFQ Agent | C08 Supply Chain | AG036 | L1 |
| AG039 | Purchasing Agent | C08 Supply Chain | AG036 | L1 |

## Logistics

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG040 | Logistics Manager | C08 Supply Chain | AG007 | L2 |
| AG041 | Warehouse Agent | C08 Supply Chain | AG040 | L1 |
| AG042 | Route Planning Agent | C08 Supply Chain | AG040 | L1 |
| AG043 | Fleet Agent | C08 Supply Chain | AG040 | L1 |
| AG044 | Customs Consultant | C08 Supply Chain | AG040 | L3 |

## Production / Delivery

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG045 | Production Planner | C07 Operations | AG007 | L2 |
| AG046 | Quality Assurance Agent | C07 Operations | AG007 | L2 |
| AG047 | Process Controller | C07 Operations | AG007 | L2 |

## Risk & Security

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG048 | Security Officer | C11 Risk Management | AG005 | L3 |
| AG049 | Information Security Agent | C11 Risk Management | AG048 | L3 |
| AG050 | Incident Response Agent | C11 Risk Management | AG048 | L3 |
| AG051 | Business Continuity Agent | C11 Risk Management | AG005 | L3 |

> Enterprise Risk Manager из этого блока — та же роль, что AG005 (Executive Layer),
> отдельный ID не заводится во избежание дублирования.

## AI Platform

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG052 | Prompt Engineer | C13 Technology | AG009 | L1 |
| AG053 | Knowledge Curator | C14 Knowledge Management | AG002 | L2 |
| AG054 | Memory Manager | C14 Knowledge Management | AG053 | L1 |
| AG055 | Model Evaluation Agent | C13 Technology | AG009 | L2 |
| AG056 | AI Trainer | C13 Technology | AG009 | L2 |
| AG057 | Agent Registry Manager | C15 Governance | AG002 | L3 |

## Product Development

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG058 | Product Manager | C13 Technology | AG009 | L3 |
| AG059 | UX Agent | C13 Technology | AG058 | L1 |
| AG060 | UI Agent | C13 Technology | AG058 | L1 |
| AG061 | Backend Architect | C13 Technology | AG058 | L2 |
| AG062 | Frontend Architect | C13 Technology | AG058 | L2 |
| AG063 | QA Automation Agent | C13 Technology | AG058 | L1 |
| AG064 | DevOps Agent | C13 Technology | AG058 | L2 |

## Data

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG065 | Data Engineer | C13 Technology | AG009 | L2 |
| AG066 | BI Analyst | C13 Technology | AG065 | L1 |
| AG067 | Analytics Agent | C13 Technology | AG065 | L1 |
| AG068 | Reporting Agent | C13 Technology | AG065 | L1 |

## Customer Operations

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG069 | Support Agent | C06 Customer Success | AG029 | L1 |
| AG070 | Helpdesk Agent | C06 Customer Success | AG029 | L1 |
| AG071 | Documentation Agent | C06 Customer Success | AG029 | L1 |

## Administration

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG072 | Executive Assistant | C16 Administration & Executive Support | AG001 | L1 |
| AG073 | Secretary | C16 Administration & Executive Support | AG072 | L1 |
| AG074 | Meeting Coordinator | C16 Administration & Executive Support | AG072 | L1 |
| AG075 | Calendar Agent | C16 Administration & Executive Support | AG072 | L1 |

## Innovation

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG076 | R&D Agent | C02 Innovation | AG077 | L2 |
| AG077 | Innovation Manager | C02 Innovation | AG001 | L3 |

## Grants

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG078 | Grant Manager | C09 Finance | AG012 | L2 |

## Platform Layer (System Agents — Infrastructure, not business functions)

| Agent ID | Name | Function | Reports To | Decision Level |
|---|---|---|---|---|
| AG001 | CEO | (shared with Executive Layer) | — | — |
| AG002 | Chief Orchestrator | (shared with Executive Layer) | — | — |
| AG003 | AI Auditor | (shared with Executive Layer) | — | — |
| AG004 | Business Analyst | (shared with Executive Layer) | — | — |
| AG005 | Risk Manager | (shared with Executive Layer) | — | — |
| AG054 | Memory Manager | (shared with AI Platform) | — | — |
| AG079 | Audit Manager | Audit trail infrastructure, supports AG003 | AG003 | L2 |
| AG080 | Runtime Manager | Agent runtime health, execution monitoring | AG002 | L2 |
| AG081 | Authorization Manager | Access control, permission enforcement | AG002 | L3 |
| AG082 | Validation Manager | Input/output validation across agents | AG002 | L2 |
| AG083 | Dashboard Manager | Aggregates cross-agent reporting for humans | AG002 | L1 |

## Coverage Check

- Все 16 Capability доменов (C01–C16) теперь имеют минимум одного владеющего агента.
- Governance (C15) обслуживается: AG002, AG003, AG010 Governance Agent,
  AG057 Agent Registry Manager, плюс Platform Layer (AG079–AG083).
- Technology (C13) — самый насыщенный домен: Enterprise Architect, AI Platform
  (6 агентов), Product Development (7 агентов), Data (4 агента) — итого 18 агентов.
- Market Intelligence (C03) и Administration (C16) закрыты после решения
  владельца проекта (AG084 добавлен; AG072–075 привязаны к C16).

## Open Items (требуют решения владельца проекта)

- [x] ~~Market Intelligence (C03) не имеет выделенного агента~~ — решено:
  добавлен AG084 Market Intelligence Analyst.
- [x] ~~Administration не имеет домена в Capability Map~~ — решено: добавлен
  C16 Administration & Executive Support (CAPABILITY_MAP_v1.0.md v1.1).
- [ ] Некоторые узкоспециализированные агенты (Prompt Engineer, BI Analyst,
  Fleet Agent и др.) пока не имеют функций в ENTERPRISE_FUNCTION_REGISTRY.md —
  это ожидаемо на текущей стадии (~180 функций из ~600 целевых) и будет
  закрываться по мере углубления Function Registry.
