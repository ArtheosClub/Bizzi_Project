# PB033 Resource Capacity Planning

Version: 1.0
Status: Active Playbook
Related Capability: C07 Operations
Related Functions: OPS-RES-001, OPS-RES-001-002, PEO-WFP-001
Owner Agent: AG007 Operations Manager
Escalation Path: AG007 → AG002 Chief Orchestrator → AG001 CEO Agent
(для решений о найме/инвестициях в capacity)

## Purpose

Playbook описывает планирование операционной ёмкости — как человеческих
ресурсов (через связь с PEO-WFP-001), так и вычислительных/агентских
ресурсов — чтобы гарантировать, что домены могут выполнять взятые на себя
обязательства (например, onboarding новых клиентов из PB003 или PB009).

## Trigger Conditions

- Плановое ежеквартальное планирование ёмкости
- Сигнал перегрузки от любого домена (например, рост очереди в PB007
  Support Ticket Escalation)
- Запуск нового крупного клиента/проекта, требующего дополнительных ресурсов

## Stage 1 — Idea (Demand Signal Collection)

**Owner:** AG007 Operations Manager
**Decision Level:** L2

Действия:
1. Собрать прогноз спроса на ресурсы из доменов (Sales pipeline — SAL-OPP,
   ожидаемый onboarding — CUS-ONB, рост поддержки — CUS-SUP)
2. Сопоставить с текущей доступной ёмкостью (человеческие агенты, часы
   AI-агентов, вычислительные ресурсы)

## Stage 2 — Analysis (Capacity Gap Analysis)

**Function:** OPS-RES-001 Resource Capacity Planning
**Owner:** AG007 Operations Manager
**Decision Level:** L2

Действия:
1. Рассчитать разрыв между прогнозируемым спросом и текущей ёмкостью
2. Определить, где разрыв критичен (риск нарушения SLA) vs допустим

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Оценить риск нарушения обязательств перед клиентами при сохранении
   текущей ёмкости
2. Оценить риск избыточных затрат при чрезмерном расширении ёмкости

## Stage 4 — Decision (Capacity Plan Approval)

**Owner:** AG002 Chief Orchestrator (AG001 CEO Agent — для решений о найме
или значительных инвестициях)
**Decision Level:** L3 (L4 при существенных инвестициях)

Варианты решения:
- Перераспределение существующих ресурсов между доменами
- Расширение через PEO-WFP-001 Headcount Planning → PB012 Recruitment Cycle
- Временное снижение SLA в некритичных областях

## Stage 5 — Execution (Capacity Adjustment)

**Owner:** AG007 Operations Manager
**Decision Level:** L2

Действия:
1. Реализовать выбранное решение
2. При необходимости найма — инициировать PB012_Recruitment_Cycle.md
3. Обновить SLA-ожидания в затронутых доменах при временных корректировках

## Stage 6 — Audit

**Function:** OPS-RES-001-002 Resource Capacity Planning Review
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, устранён ли фактический разрыв ёмкости
2. Сверить фактическую загрузку с прогнозом для калибровки будущих циклов

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать точность прогноза спроса по доменам
2. Обновить модели прогнозирования ёмкости

## KPIs

- Capacity Utilization Rate по доменам
- SLA Breach Rate (связанный с нехваткой ёмкости)
- Forecast Accuracy (прогноз спроса vs факт)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (OPS-RES, PEO-WFP)
- PB012_Recruitment_Cycle.md (при решении о расширении через найм)
- PB007_Support_Escalation.md (частый источник сигналов перегрузки)
- AGENT_REGISTRY.md (AG007, AG002, AG005, AG001)
