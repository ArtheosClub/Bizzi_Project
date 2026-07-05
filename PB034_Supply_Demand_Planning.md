# PB034 Supply & Demand Planning

Version: 1.0
Status: Active Playbook
Related Capability: C08 Supply Chain
Related Functions: SCM-SUP-001, SCM-DMP-001, SCM-DMP-001-002
Owner Agent: AG040 Logistics Manager
Escalation Path: AG040 → AG007 Operations Manager → AG012 CFO Agent
(для решений, влияющих на оборотный капитал)

## Purpose

Playbook описывает цикл согласования прогноза спроса с планом поставок —
чтобы избежать как дефицита (упущенные продажи), так и избытка (замороженный
капитал в запасах).

## Trigger Conditions

- Плановый ежемесячный S&OP (Sales & Operations Planning) цикл
- Существенное отклонение фактического спроса от прогноза

## Stage 1 — Idea (Demand Forecast Input)

**Function:** SCM-DMP-001 Demand Plan Reconciliation
**Owner:** AG040 Logistics Manager
**Decision Level:** L2

Действия:
1. Собрать прогноз спроса от AG084 Market Intelligence Analyst (MKT-DEM-001)
   и фактические данные продаж (SAL-OPP-001 pipeline)
2. Сверить с историческими паттернами потребления

## Stage 2 — Analysis (Supply Plan Development)

**Function:** SCM-SUP-001 Supply Plan Update
**Owner:** AG040 Logistics Manager
**Decision Level:** L2

Действия:
1. Рассчитать требуемый объём закупок/производства на основе согласованного
   прогноза спроса
2. Учесть текущие запасы (SCM-INV-001 Inventory Reconciliation) и lead time
   поставщиков

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Оценить риск дефицита при недооценке спроса (упущенная выручка)
2. Оценить риск избыточных запасов при переоценке (замороженный капитал,
   складские расходы)
3. Проверить зависимость от единственного поставщика (концентрационный риск)

## Stage 4 — Decision (S&OP Plan Approval)

**Owner:** AG007 Operations Manager (AG012 CFO Agent — при существенном
влиянии на оборотный капитал)
**Decision Level:** L2 (L3 при крупных объёмах)

Критерии:
- План поставок покрывает прогнозируемый спрос с разумным буфером
- Влияние на оборотный капитал в рамках бюджета (FIN-TRE-001 Cash Position)

## Stage 5 — Execution (Procurement Trigger)

**Owner:** AG039 Purchasing Agent
**Decision Level:** L1

Действия:
1. Инициировать закупки согласно утверждённому плану через
   PB010_Procurement_Request_to_Pay.md
2. Скоординировать сроки поставки с логистикой (SCM-LOG-001)

## Stage 6 — Audit

**Function:** SCM-DMP-001-002 Demand Plan Reconciliation Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Сравнить фактический спрос и фактические поставки с планом по итогам
   периода
2. Зафиксировать процент избытка/дефицита для калибровки следующего цикла

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать точность прогноза спроса по категориям товаров/услуг
2. Обновить модели прогнозирования при систематических отклонениях

## KPIs

- Forecast Accuracy (спрос: прогноз vs факт)
- Stockout Rate (случаи дефицита)
- Inventory Turnover Ratio
- Days of Supply on Hand

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SCM-SUP, SCM-DMP, SCM-INV, MKT-DEM)
- PB010_Procurement_Request_to_Pay.md (исполнение плана закупок)
- PB009_Vendor_Onboarding.md (диверсификация поставщиков при концентрационном риске)
- AGENT_REGISTRY.md (AG040, AG007, AG012, AG039, AG005)
