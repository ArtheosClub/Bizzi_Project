# PB010 Procurement Request-to-Pay

Version: 1.0
Status: Active Playbook
Related Capability: C08 Supply Chain
Related Functions: SCM-PRC-001, SCM-PRC-002, FIN-ACC-001
Owner Agent: AG039 Purchasing Agent
Escalation Path: AG039 → AG036 Procurement Manager → AG012 CFO Agent
(для закупок выше лимита)

## Purpose

Playbook описывает полный цикл закупки — от заявки на покупку до оплаты
поставщику (Purchase-to-Pay), с использованием только поставщиков из
Approved Vendor List (см. PB009).

## Trigger Conditions

- Заявка на закупку от любого департамента
- Автоматический триггер по достижению порога запасов (SCM-INV-001)

## Stage 1 — Idea (Purchase Requisition)

**Function:** SCM-PRC-001 Purchase Requisition
**Owner:** AG039 Purchasing Agent
**Decision Level:** L1

Действия:
1. Получить заявку с описанием, количеством и обоснованием
2. Проверить наличие утверждённого бюджета в соответствующем домене
   (FIN-BUD-002 Budget Review)
3. Проверить, есть ли поставщик в Approved Vendor List (PB009); если нет —
   инициировать PB009_Vendor_Onboarding.md

## Stage 2 — Analysis (Quotation)

**Owner:** AG038 RFQ Agent
**Decision Level:** L1

Действия:
1. Для закупок выше порогового значения — запросить котировки у 2-3
   поставщиков из Approved Vendor List
2. Сравнить предложения по цене, срокам, условиям оплаты

## Stage 3 — Risk Review

**Owner:** AG036 Procurement Manager
**Decision Level:** L2

Действия:
1. Проверить, не превышает ли закупка лимиты для данной категории
2. Для нестандартных условий оплаты — проверить с AG014 Treasury Agent
   (FIN-TRE-001 Cash Position Monitoring)

## Stage 4 — Decision (Purchase Order Approval)

**Owner:** AG036 Procurement Manager (AG012 CFO Agent — выше установленного
лимита)
**Decision Level:** L2 (L4 для крупных закупок)

Критерии:
- Бюджет подтверждён
- Поставщик из Approved Vendor List
- Цена соответствует рыночной (по итогам RFQ) или обоснованное отклонение

## Stage 5 — Execution (Order & Payment)

**Owner:** AG039 Purchasing Agent
**Decision Level:** L1

Действия:
1. Выпустить Purchase Order поставщику
2. Отследить поставку (SCM-LOG-001 Shipment Tracking)
3. После подтверждения получения — передать в AG013 Accounting Agent для
   оплаты (FIN-ACC-001 Monthly Close Process учитывает данную транзакцию)

## Stage 6 — Audit

**Function:** SCM-PRC-002 Purchase Requisition Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить трёхстороннее соответствие: Purchase Order = Поставка = Счёт
   (three-way match)
2. Зафиксировать расхождения (цена, количество) для расследования

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать типовые задержки в цикле закупки для оптимизации процесса
2. Обновить пороговые значения для RFQ при необходимости

## KPIs

- Procurement Cycle Time (от заявки до оплаты)
- Three-Way Match Accuracy Rate
- Cost Savings from Competitive Quotation (RFQ)
- % закупок вне Approved Vendor List (должно стремиться к нулю)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SCM-PRC, FIN-ACC, FIN-TRE)
- PB009_Vendor_Onboarding.md (источник Approved Vendor List)
- PB008_Monthly_Financial_Close.md (учёт закупочных транзакций)
- AGENT_REGISTRY.md (AG039, AG038, AG036, AG012, AG013)
