# PB006 Upsell & Cross-Sell Motion

Version: 1.0
Status: Active Playbook
Related Capability: C05 Sales
Related Functions: SAL-XSL-001, SAL-UPS-001, SAL-UPS-001-002, CUS-EXP-001
Owner Agent: AG025 Sales Director
Escalation Path: AG025 → AG012 CFO Agent (для нестандартного pricing)

## Purpose

Playbook описывает выявление и реализацию возможностей расширения контракта
с существующим клиентом (upsell — больше того же продукта/тарифа, cross-sell —
другой продукт).

## Trigger Conditions

- Клиент со статусом "Healthy" по Customer Health Score (см. PB005)
- Признаки роста использования, приближающиеся к лимитам текущего тарифа
- Плановый квартальный обзор ключевых аккаунтов (SAL-ACC-001)

## Stage 1 — Idea (Opportunity Identification)

**Function:** CUS-EXP-001 Expansion Opportunity Review
**Owner:** AG029 Customer Success Agent
**Decision Level:** L2

Действия:
1. Проанализировать паттерны использования клиента на предмет приближения
   к лимитам тарифа
2. Выявить неиспользуемые модули/функции, релевантные бизнесу клиента
3. Передать список возможностей AG025 Sales Director

## Stage 2 — Analysis (Cross-Sell Fit Assessment)

**Function:** SAL-XSL-001 Cross-Sell Opportunity Identification
**Owner:** AG025 Sales Director
**Decision Level:** L1

Действия:
1. Оценить, какие дополнительные продукты релевантны профилю клиента
2. Проверить бюджетный цикл клиента (когда логично выходить с предложением)

## Stage 3 — Risk Review

**Function:** RSK-FIN-001 Financial Risk Monitoring
**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Для крупных upsell-сделок — проверить платёжную историю клиента
2. Оценить риск перегрузки клиента (слишком агрессивный upsell может повредить
   отношениям — см. CUS-RET-001)

## Stage 4 — Decision (Offer Approval)

**Owner:** AG025 Sales Director
**Decision Level:** L1 (L2 при нестандартном pricing)

Критерии:
- Предложение соответствует реальной потребности клиента (не навязывание)
- Ценообразование в рамках стандартных правил или согласовано с AG012 CFO Agent

## Stage 5 — Execution (Upsell/Cross-Sell Delivery)

**Function:** SAL-UPS-001 Upsell Proposal
**Owner:** AG025 Sales Director
**Decision Level:** L1

Действия:
1. Подготовить и представить предложение клиенту (через AG028 Proposal Generator)
2. При согласии — оформить изменение контракта через PB013_Contract_Review_Approval.md
3. Передать обновлённые условия AG029 Customer Success Agent для актуализации
   Customer Success Plan (CUS-SPL-001)

## Stage 6 — Audit

**Function:** SAL-UPS-001-002 Upsell Proposal Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить соответствие фактической скидки утверждённым лимитам
2. Зафиксировать случаи отказа клиента и причины

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать, какие триггеры использования лучше всего предсказывают
   готовность к upsell
2. Обновить шаблоны предложений по сегментам

## KPIs

- Expansion Revenue (% от общей выручки, пришедший от upsell/cross-sell)
- Offer Acceptance Rate
- Average Expansion Deal Size

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SAL-XSL, SAL-UPS, CUS-EXP)
- PB005_Renewal_Retention.md (источник "Healthy" клиентов)
- PB013_Contract_Review_Approval.md (оформление изменения контракта)
- AGENT_REGISTRY.md (AG025, AG029, AG005, AG012)
