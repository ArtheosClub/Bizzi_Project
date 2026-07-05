# PB031 Quality Audit Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C07 Operations
Related Functions: OPS-QUA-001, OPS-QUA-002
Owner Agent: AG046 Quality Assurance Agent
Escalation Path: AG046 → AG007 Operations Manager → AG001 CEO Agent
(для системных проблем качества)

## Purpose

Playbook описывает регулярную проверку качества операционных процессов
и поставляемых продуктов/услуг — не путать с TEC-домен QA (AG063 QA
Automation Agent), который проверяет программный код.

## Trigger Conditions

- Плановый ежемесячный/ежеквартальный аудит качества
- Всплеск жалоб клиентов (CUS-SUP-001) или возвратов

## Stage 1 — Idea (Audit Scope Definition)

**Owner:** AG046 Quality Assurance Agent
**Decision Level:** L2

Действия:
1. Определить область проверки (конкретный процесс, продукт, департамент)
2. Собрать применимые стандарты качества (внутренние SOP — KNW-SOP-001)

## Stage 2 — Analysis (Quality Assessment)

**Function:** OPS-QUA-001 Quality Audit
**Owner:** AG046 Quality Assurance Agent
**Decision Level:** L2

Действия:
1. Провести проверку по чек-листу (выборочная или полная, в зависимости
   от критичности)
2. Зафиксировать несоответствия (non-conformances) с указанием серьёзности

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Оценить риск для клиентов/бизнеса от выявленных несоответствий
2. Приоритизировать по критичности (влияет на безопасность/финансы vs
   косметические отклонения)

## Stage 4 — Decision (Corrective Action Approval)

**Owner:** AG007 Operations Manager
**Decision Level:** L2 (L3 для системных проблем)

Критерии:
- План корректирующих действий покрывает все критичные несоответствия
- Установлены сроки устранения

## Stage 5 — Execution (Corrective Actions)

**Owner:** AG047 Process Controller
**Decision Level:** L2

Действия:
1. Реализовать корректирующие действия (обновление процесса, дообучение,
   изменение спецификации)
2. Задокументировать каждое действие для последующей верификации

## Stage 6 — Audit

**Function:** OPS-QUA-002 Quality Audit Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Провести повторную проверку после реализации корректирующих действий
   (verification of closure)
2. Зафиксировать, устранена ли первопричина, а не только симптом

## Stage 7 — Knowledge Capture

**Function:** KNW-SOP-001 SOP Drafting
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Обновить SOP при выявлении структурной причины несоответствия
2. Зафиксировать паттерн в Corporate Memory для предотвращения повторения
   в других доменах

## KPIs

- Non-Conformance Rate
- Corrective Action Closure Time
- Repeat Non-Conformance Rate (повторение той же проблемы — сигнал, что
  первопричина не устранена)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (OPS-QUA, KNW-SOP)
- PB032_Process_Optimization.md (для системных улучшений процесса)
- AGENT_REGISTRY.md (AG046, AG007, AG047, AG005)
