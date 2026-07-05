# PB048 Policy Document Lifecycle

Version: 1.0
Status: Active Playbook
Related Capability: C14 Knowledge Management / C15 Governance
Related Functions: KNW-POL-001, GOV-POL-001, GOV-POL-001-002
Owner Agent: AG010 Governance Agent
Escalation Path: AG010 → AG002 Chief Orchestrator → AG001 CEO Agent
(для политик уровня предприятия)

## Purpose

Playbook описывает жизненный цикл корпоративных политик (в отличие от
SOP из PB047, политики задают правила и ограничения, а не пошаговые
инструкции) — от создания до планового пересмотра.

## Trigger Conditions

- Новое регуляторное требование (LEG-REG-001, см. PB014)
- Пробел, выявленный в PB022 AI Governance Compliance Review
- Плановый ежегодный пересмотр существующих политик

## Stage 1 — Idea (Policy Need Identification)

**Owner:** AG010 Governance Agent
**Decision Level:** L3

Действия:
1. Определить необходимость новой политики или пересмотра существующей
2. Собрать вводные требования (регуляторные, внутренние риски)

## Stage 2 — Analysis (Policy Drafting)

**Function:** KNW-POL-001 Policy Document Maintenance
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Подготовить черновик политики совместно с AG010 Governance Agent
2. Определить область применения (какие домены/агенты затрагивает)

## Stage 3 — Risk Review

**Owner:** AG017 Legal Counsel + AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Проверить соответствие законодательству (LEG-CMP-001)
2. Оценить операционное влияние на затрагиваемые домены (может ли политика
   создать конфликт с существующими SOP/playbooks)

## Stage 4 — Decision (Policy Approval)

**Function:** GOV-POL-001 Governance Policy Update
**Owner:** AG010 Governance Agent (AG001 CEO Agent — для политик уровня
предприятия, затрагивающих Governance Model)
**Decision Level:** L4

Критерии:
- Политика юридически корректна
- Не создаёт неразрешимых противоречий с существующими SOP/playbooks

**Human Override:** обязателен для политик, изменяющих Decision Levels
или Governance Core (см. PB022).

## Stage 5 — Execution (Rollout)

**Owner:** AG002 Chief Orchestrator
**Decision Level:** L2

Действия:
1. Довести политику до всех затронутых агентов
2. Обновить связанные SOP (PB047) для соответствия новой политике
3. Установить дату вступления в силу и переходный период при необходимости

## Stage 6 — Audit

**Function:** GOV-POL-001-002 Governance Policy Update Review
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить фактическое соблюдение политики затронутыми доменами
   (аналогично GOV-AUD-002 Compliance Audit)
2. Зафиксировать случаи несоблюдения для дальнейшей работы

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Установить дату планового пересмотра политики (обычно ежегодно)
2. Зафиксировать эффективность политики в снижении соответствующего риска

## KPIs

- Policy Compliance Rate
- Time from Need Identification to Rollout
- Policy Currency (% политик, пересмотренных в срок)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (KNW-POL, GOV-POL)
- PB014_Compliance_Monitoring.md, PB022_AI_Governance_Review.md (источники потребностей)
- PB047_SOP_Drafting_Approval.md (SOP как реализация политики на операционном уровне)
- AGENT_REGISTRY.md (AG010, AG053, AG017, AG005, AG001)
