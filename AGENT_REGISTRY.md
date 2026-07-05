# AGENT_REGISTRY.md

# Art of Business Agent Registry

Version: 1.0 (draft reconstruction)
Status: Proposed — requires human review and confirmation

## Purpose

Agent Registry — единый реестр всех AI-агентов предприятия. Каждый агент привязан
к одной или нескольким Capability (см. CAPABILITY_MAP_v1.0.md) и имеет чётко
определённый уровень принятия решений (см. GOVERNANCE_MODEL.md, Decision Levels L0–L5).

> ⚠️ **Примечание о происхождении:** в предыдущей версии GOVERNANCE_MODEL.md
> были явно перечислены только AG001–AG005 и AG026 — 22 агента (AG006–AG025, AG027–AG028)
> отсутствовали в репозитории. Список ниже — реконструкция, построенная по аналогии
> с уже существующей логикой (1–2 агента на Capability домен), а не восстановление
> оригинальных данных. Требует вашей проверки и корректировки ролей/названий.

## Agent Classification

Каждый агент описывается полями:
- Agent ID
- Name
- Owned Capability (домен из Capability Map)
- Reports To (вышестоящий агент/человек)
- Decision Level (L0–L5, см. Governance Model)

## Full Registry (28 Agents)

| Agent ID | Name | Capability | Reports To | Decision Level |
|---|---|---|---|---|
| AG001 | CEO Agent | C01 Strategy | Human Board (L0) | L5 |
| AG002 | Chief Orchestrator | C15 Governance | AG001 | L5 |
| AG003 | AI Auditor | C15 Governance | AG002 | L4 |
| AG004 | Business Analyst | C01 Strategy | AG001 | L3 |
| AG005 | Risk Manager | C11 Risk Management | AG002 | L4 |
| AG006 | Strategic Planning Agent | C01 Strategy | AG004 | L3 |
| AG007 | Innovation Manager | C02 Innovation | AG001 | L3 |
| AG008 | Market Intelligence Analyst | C03 Market Intelligence | AG004 | L2 |
| AG009 | Marketing Manager | C04 Marketing | AG002 | L3 |
| AG010 | Sales Manager | C05 Sales | AG002 | L3 |
| AG011 | Customer Success Manager | C06 Customer Success | AG002 | L3 |
| AG012 | Operations Manager | C07 Operations | AG002 | L3 |
| AG013 | Supply Chain Manager | C08 Supply Chain | AG012 | L2 |
| AG014 | Finance Manager (CFO Agent) | C09 Finance | AG001 | L4 |
| AG015 | Legal Counsel Agent | C10 Legal & Compliance | AG002 | L4 |
| AG016 | Compliance Officer | C10 Legal & Compliance | AG015 | L3 |
| AG017 | HR Manager (People Agent) | C12 People Management | AG002 | L3 |
| AG018 | Technology Manager (CTO Agent) | C13 Technology | AG001 | L4 |
| AG019 | Data Platform Agent | C13 Technology | AG018 | L2 |
| AG020 | Cybersecurity Agent | C11 Risk Management | AG005 | L3 |
| AG021 | Automation & MLOps Agent | C13 Technology | AG018 | L2 |
| AG022 | Procurement Agent | C08 Supply Chain | AG013 | L2 |
| AG023 | Vendor Management Agent | C08 Supply Chain | AG013 | L2 |
| AG024 | Contract Management Agent | C10 Legal & Compliance | AG015 | L2 |
| AG025 | Grant & Funding Agent | C09 Finance | AG014 | L2 |
| AG026 | Knowledge Manager | C14 Knowledge Management | AG002 | L3 |
| AG027 | Talent Acquisition Agent | C12 People Management | AG017 | L2 |
| AG028 | Escalation & Audit Support Agent | C15 Governance | AG003 | L2 |

## Coverage Check

- Все 15 Capability доменов (C01–C15) имеют минимум одного владеющего агента.
- Governance (C15) обслуживается тремя агентами (AG002, AG003, AG028) — соответствует
  критичности слоя согласно Governance Model.
- Finance (C09) — два агента (AG014, AG025), так как Grant Acquisition (PB001)
  требует отдельного владельца по объёму работы.

## Open Items

- [ ] Подтвердить/скорректировать названия ролей AG006–AG025, AG027–AG028 с владельцем проекта
- [ ] Добавить KPI для каждого агента (сейчас есть только в Function Registry на уровне функций)
- [ ] Связать Agent ID с конкретными Function ID из ENTERPRISE_FUNCTION_REGISTRY.md (Owner Agent column)
