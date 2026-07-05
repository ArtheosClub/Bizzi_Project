# PB032 Process Optimization Review

Version: 1.0
Status: Active Playbook
Related Capability: C07 Operations
Related Functions: OPS-PRO-002, OPS-IMP-001, OPS-IMP-002
Owner Agent: AG047 Process Controller
Escalation Path: AG047 → AG007 Operations Manager → AG002 Chief Orchestrator
(для изменений, затрагивающих несколько доменов)

## Purpose

Playbook описывает цикл выявления и реализации улучшений операционных
процессов — как реактивно (по итогам PB031 Quality Audit), так и проактивно
(плановый анализ эффективности).

## Trigger Conditions

- Системная проблема, выявленная в PB031 Quality Audit Cycle
- Плановый ежеквартальный процессный ревью
- Рост стоимости операций (OPS-COS-001 Cost Optimization Review)

## Stage 1 — Idea (Improvement Opportunity Identification)

**Function:** OPS-IMP-001 Improvement Initiative Tracking
**Owner:** AG047 Process Controller
**Decision Level:** L2

Действия:
1. Собрать сигналы неэффективности (время выполнения, ошибки, стоимость)
   из доменных метрик
2. Приоритизировать по потенциальному эффекту и сложности реализации

## Stage 2 — Analysis (Root Cause & Redesign)

**Function:** OPS-PRO-002 Process Optimization
**Owner:** AG047 Process Controller
**Decision Level:** L2

Действия:
1. Провести анализ первопричины (5 Whys, process mapping)
2. Спроектировать улучшенный процесс
3. Оценить, какие агенты/функции затрагивает изменение

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Оценить риск нарушения работы во время перехода на новый процесс
2. Проверить, не создаёт ли изменение конфликт с Governance Model
   (например, изменение Decision Level без надлежащей процедуры — см. PB020)

## Stage 4 — Decision (Redesign Approval)

**Owner:** AG007 Operations Manager (AG002 Chief Orchestrator — для
кросс-доменных изменений)
**Decision Level:** L3

Критерии:
- Ожидаемый эффект (время/стоимость/качество) обоснован анализом
- План перехода минимизирует риск нарушения текущих операций

## Stage 5 — Execution (Rollout)

**Owner:** AG047 Process Controller
**Decision Level:** L2

Действия:
1. Внедрить изменение (пилотно на части операций, затем полностью)
2. Обновить SOP (KNW-SOP-001) и уведомить затронутых агентов через
   AG002 Chief Orchestrator

## Stage 6 — Audit

**Function:** OPS-IMP-002 Improvement Initiative Tracking Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Сравнить фактический эффект с прогнозом (Stage 2)
2. Зафиксировать отклонения — переоценка процесса при необходимости

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать методологию оптимизации для повторного использования
   в других доменах
2. Обновить бенчмарки эффективности процессов

## KPIs

- Process Cycle Time Reduction
- Improvement Initiative Success Rate (% давших ожидаемый эффект)
- Time from Identification to Rollout

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (OPS-PRO, OPS-IMP, OPS-COS, KNW-SOP)
- PB031_Quality_Audit_Cycle.md (частый источник инициатив)
- PB020_Agent_Lifecycle.md (если изменение требует изменения полномочий агента)
- AGENT_REGISTRY.md (AG047, AG007, AG005, AG002)
