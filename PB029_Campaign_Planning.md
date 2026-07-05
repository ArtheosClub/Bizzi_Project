# PB029 Campaign Planning & Execution

Version: 1.0
Status: Active Playbook
Related Capability: C04 Marketing
Related Functions: MRK-CAM-001..003, MRK-LGN-001
Owner Agent: AG034 Campaign Manager
Escalation Path: AG034 → AG030 Marketing Manager → AG012 CFO Agent
(для бюджета выше лимита)

## Purpose

Playbook описывает планирование и проведение маркетинговых кампаний
(performance marketing, лидогенерация) — от постановки цели до анализа
результатов и передачи лидов в Sales.

## Trigger Conditions

- Плановый квартальный маркетинговый календарь
- Потребность в лидогенерации от AG025 Sales Director
- Поддержка запуска продукта (PB027) или события (PB030)

## Stage 1 — Idea (Campaign Brief)

**Owner:** AG034 Campaign Manager
**Decision Level:** L2

Действия:
1. Определить цель кампании (лидогенерация, awareness, конверсия) и
   целевой сегмент (MKT-SEG-001)
2. Оценить требуемый бюджет

## Stage 2 — Analysis (Campaign Planning)

**Function:** MRK-CAM-001 Campaign Planning
**Owner:** AG034 Campaign Manager
**Decision Level:** L2

Действия:
1. Выбрать каналы (платная реклама, email, соцсети, контент)
2. Спланировать креативы совместно с AG031 Content Agent и AG035 Brand Agent
3. Определить KPI и целевые показатели (CPL, CTR, конверсия)

## Stage 3 — Risk Review

**Owner:** AG012 CFO Agent (для бюджета выше лимита)
**Decision Level:** L2

Действия:
1. Проверить соответствие бюджета кампании утверждённому маркетинговому
   бюджету (FIN-BUD-002)
2. Оценить риск неэффективного расходования при новом канале/сегменте

## Stage 4 — Decision (Campaign Approval)

**Owner:** AG030 Marketing Manager (AG012 CFO Agent — при бюджете выше
лимита)
**Decision Level:** L2 (L3 для крупных бюджетов)

Критерии:
- Ожидаемый CAC (Customer Acquisition Cost) в рамках целевых показателей
- Бюджет утверждён в рамках Budget Approval

## Stage 5 — Execution (Campaign Execution)

**Function:** MRK-CAM-002 Campaign Execution, MRK-LGN-001 Lead Generation Campaign
**Owner:** AG034 Campaign Manager
**Decision Level:** L1

Действия:
1. Запустить кампанию по выбранным каналам
2. Мониторить показатели в реальном времени, корректировать таргетинг/бюджет
3. Передавать сгенерированные лиды в AG026 CRM Agent (SAL-LEAD-001 Lead Capture)

## Stage 6 — Audit

**Function:** MRK-CAM-003 Campaign Performance Analysis
**Owner:** AG067 Analytics Agent
**Decision Level:** L2

Действия:
1. Сверить фактические результаты (CPL, конверсия, ROI) с планом
2. Оценить качество переданных в Sales лидов (SAL-LEAD-002 Lead Qualification
   как обратная связь)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать наиболее эффективные каналы/креативы по сегментам
2. Обновить бенчмарки CPL/CAC для планирования будущих кампаний

## KPIs

- Cost Per Lead (CPL)
- Marketing Qualified Leads (MQL) Volume
- Campaign ROI
- Lead-to-Opportunity Conversion Rate (совместно с Sales)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (MRK-CAM, MRK-LGN, SAL-LEAD)
- PB004_Lead_to_Contract.md (получатель сгенерированных лидов)
- PB028_Content_Marketing_Cycle.md (источник креативов)
- AGENT_REGISTRY.md (AG034, AG030, AG012, AG026, AG067)
