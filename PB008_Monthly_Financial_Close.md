# PB008 Monthly Financial Close

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-ACC-001, FIN-ACC-002, FIN-FPA-001
Owner Agent: AG013 Accounting Agent
Escalation Path: AG013 → AG012 CFO Agent → AG001 CEO Agent (при существенных
расхождениях)

## Purpose

Playbook описывает ежемесячный цикл закрытия финансового периода —
от сверки транзакций до публикации отчётности для руководства.

## Trigger Conditions

- Плановое ежемесячное закрытие (обычно 1-5 рабочих дней после конца месяца)
- Внеплановое закрытие перед due diligence/аудитом

## Stage 1 — Idea (Transaction Reconciliation)

**Function:** FIN-ACC-001 Monthly Close Process
**Owner:** AG013 Accounting Agent
**Decision Level:** L2

Действия:
1. Собрать все транзакции периода из систем (банк, CRM, ERP)
2. Сверить банковские выписки с внутренними записями
3. Зафиксировать незакрытые статьи (pending invoices, accruals)

## Stage 2 — Analysis (Variance Check)

**Function:** FIN-FPA-001 Variance Analysis
**Owner:** AG016 Financial Planning & Analysis Agent
**Decision Level:** L2

Действия:
1. Сравнить фактические показатели с бюджетом (см. PB002_Budget_Approval.md)
2. Выявить отклонения выше порогового значения (обычно 10%)
3. Запросить объяснения у владельцев соответствующих Capability доменов

## Stage 3 — Risk Review

**Function:** RSK-FIN-001 Financial Risk Monitoring
**Owner:** AG005 Risk Manager
**Decision Level:** L2 (эскалация к L3 при существенных отклонениях)

Действия:
1. Оценить, не указывают ли отклонения на системную проблему (кассовый разрыв,
   ошибка в прогнозе)
2. При обнаружении риска — эскалация к AG012 CFO Agent

## Stage 4 — Decision (Close Approval)

**Owner:** AG012 CFO Agent
**Decision Level:** L3

Критерии:
- Все транзакции сверены, расхождений нет или они объяснены
- Отчётность соответствует требованиям учётной политики
- Существенные отклонения (>10%) прокомментированы

## Stage 5 — Execution (Reporting)

**Owner:** AG013 Accounting Agent
**Decision Level:** L1

Действия:
1. Сформировать финальные отчёты (P&L, Balance Sheet, Cash Flow)
2. Опубликовать для AG001 CEO Agent и владельцев доменов через AG083
   Dashboard Manager
3. Архивировать документы периода (ADM-REC-001 Records Retention Management)

## Stage 6 — Audit

**Function:** FIN-ACC-002 Monthly Close Process Review
**Owner:** AG012 CFO Agent
**Decision Level:** L2

Действия:
1. Проверить своевременность закрытия (соответствие SLA в днях)
2. Зафиксировать в GOV-AUD-002 Compliance Audit для регуляторных целей

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать повторяющиеся источники расхождений
2. Обновить чек-лист закрытия при выявлении узких мест в процессе

## KPIs

- Days to Close: количество рабочих дней на закрытие периода
- Reconciliation Accuracy: % транзакций без расхождений при первой сверке
- Variance Explanation Rate: % отклонений с задокументированным объяснением

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-ACC, FIN-FPA, RSK-FIN)
- PB002_Budget_Approval.md (источник планового бюджета для сравнения)
- AGENT_REGISTRY.md (AG013, AG016, AG012, AG005)
