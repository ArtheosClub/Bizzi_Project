# PB018 Agent Performance Review

Version: 1.0
Status: Active Playbook
Related Capability: C15 Governance
Related Functions: GOV-PRF-001, GOV-PRF-002
Owner Agent: AG002 Chief Orchestrator
Escalation Path: AG002 → AG001 CEO Agent (для решений о замене/расширении
полномочий агента)

## Purpose

Playbook описывает периодическую оценку эффективности каждого из 84 агентов
предприятия — насколько хорошо агент выполняет свои функции из
ENTERPRISE_FUNCTION_REGISTRY.md.

## Trigger Conditions

- Плановый ежеквартальный цикл оценки (для всех агентов)
- Сигнал о систематических проблемах (частые эскалации, ошибки, задержки)

## Stage 1 — Idea (Metrics Collection)

**Owner:** AG083 Dashboard Manager
**Decision Level:** L1

Действия:
1. Собрать метрики выполнения функций по каждому агенту: completion rate,
   среднее время выполнения, частота эскалаций
2. Сопоставить с KPI, определёнными в соответствующих playbooks

## Stage 2 — Analysis (Performance Assessment)

**Function:** GOV-PRF-001 Agent Performance Review
**Owner:** AG002 Chief Orchestrator
**Decision Level:** L3

Действия:
1. Оценить каждого агента по: точность выполнения, соблюдение Decision Level
   (не превышает ли агент свои полномочия), частота обоснованных эскалаций
2. Выявить агентов с систематически низкой производительностью

## Stage 3 — Risk Review

**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить, не связаны ли проблемы производительности с некорректно
   настроенными полномочиями (см. GOV-AUT-001 Authority Matrix Review)
2. Оценить риск для бизнеса от продолжения работы агента без изменений

## Stage 4 — Decision (Action Plan Approval)

**Owner:** AG002 Chief Orchestrator (AG001 CEO Agent — для замены агента
или существенного изменения полномочий)
**Decision Level:** L3 (L4 для структурных изменений)

Варианты решения:
- Agent Retraining — донастройка промптов/параметров (AG056 AI Trainer)
- Authority Adjustment — изменение Decision Level или Reports To
- Agent Retirement — вывод агента из эксплуатации (см. PB020)
- No Action — производительность в норме

## Stage 5 — Execution

**Owner:** зависит от решения (AG056 AI Trainer / AG081 Authorization Manager
/ AG057 Agent Registry Manager)
**Decision Level:** L2

Действия:
1. Реализовать выбранное действие
2. Обновить AGENT_REGISTRY.md при изменении полномочий или ролей
3. Установить период наблюдения для оценки эффекта изменений

## Stage 6 — Audit

**Function:** GOV-PRF-002 Agent Performance Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить, что изменения были внесены корректно и задокументированы
2. Отследить метрики агента в следующем цикле для подтверждения улучшения

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать паттерны, приводящие к низкой производительности агентов
   (например, недостаточно чёткие Function definitions)
2. Использовать для улучшения ENTERPRISE_FUNCTION_REGISTRY.md формулировок

## KPIs

- % агентов, соответствующих целевым KPI своих функций
- Среднее время между выявлением проблемы и её устранением
- Escalation Rate по агенту (не должен систематически расти)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (GOV-PRF, GOV-AUT)
- PB020_Agent_Lifecycle.md (для случаев Agent Retirement)
- AGENT_REGISTRY.md (полный список агентов для оценки)
