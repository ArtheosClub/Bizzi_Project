# PB047 SOP Drafting & Approval

Version: 1.0
Status: Active Playbook
Related Capability: C14 Knowledge Management
Related Functions: KNW-SOP-001, KNW-SOP-002
Owner Agent: AG053 Knowledge Curator
Escalation Path: AG053 → AG002 Chief Orchestrator → владелец домена
(для утверждения)

## Purpose

Playbook описывает создание и утверждение стандартных операционных
процедур (SOP) — формализованных версий того, как выполняется конкретная
функция, часто рождающихся из PB031/PB032 (Quality Audit / Process
Optimization) или из нового playbook, требующего документированной
процедуры.

## Trigger Conditions

- Новая функция в ENTERPRISE_FUNCTION_REGISTRY.md без документированной
  процедуры
- Изменение процесса по итогам PB032 Process Optimization Review
- Повторяющаяся ошибка, указывающая на отсутствие чёткой процедуры

## Stage 1 — Idea (SOP Need Identification)

**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Определить, для какой функции/процесса требуется SOP
2. Собрать вводные данные от владельца функции (Agent ID из
   ENTERPRISE_FUNCTION_REGISTRY.md)

## Stage 2 — Analysis (Drafting)

**Function:** KNW-SOP-001 SOP Drafting
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Задокументировать процедуру шаг за шагом (аналогично структуре
   PLAYBOOK_TEMPLATE.md, но для более гранулярного уровня, чем playbook)
2. Указать роли, инструменты, ожидаемые результаты каждого шага

## Stage 3 — Risk Review

**Owner:** владелец домена (Agent ID функции, для которой пишется SOP)
**Decision Level:** L2

Действия:
1. Проверить черновик на техническую точность
2. Убедиться, что SOP не противоречит существующим SOP или Governance Model

## Stage 4 — Decision (SOP Approval)

**Function:** KNW-SOP-002 SOP Review & Approval
**Owner:** AG002 Chief Orchestrator
**Decision Level:** L3

Критерии:
- SOP технически точен и проверен владельцем домена
- Не создаёт противоречий с другими SOP/playbooks в репозитории

## Stage 5 — Execution (Publication)

**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Опубликовать SOP в Knowledge Base
2. Уведомить всех агентов, для которых процедура релевантна (через
   AG002 Chief Orchestrator)
3. Связать SOP с соответствующей Function ID для быстрого доступа

## Stage 6 — Audit

**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Периодически проверять, следуют ли агенты опубликованному SOP на
   практике (сверка с фактическим выполнением функции)
2. Выявить расхождения между SOP и реальной практикой

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. При обнаружении расхождений (Stage 6) — обновить SOP, чтобы отражать
   лучшую текущую практику, либо скорректировать выполнение
2. Зафиксировать эффективность SOP в снижении ошибок/вариативности

## KPIs

- SOP Coverage (% функций из Function Registry, имеющих документированный SOP)
- SOP Adherence Rate (по итогам аудита Stage 6)
- Time to Draft & Approve

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (все функции — потенциальные объекты SOP)
- PB032_Process_Optimization.md (частый источник новых/обновлённых SOP)
- PLAYBOOK_TEMPLATE.md (более крупноформатный аналог для целых процессов)
- AGENT_REGISTRY.md (AG053, AG002, AG003)
