# PB017 Crisis Management Activation

Version: 1.0
Status: Active Playbook
Related Capability: C11 Risk Management
Related Functions: RSK-CRI-001, RSK-BCP-001, RSK-BCP-002
Owner Agent: AG001 CEO Agent
Escalation Path: AG005 Risk Manager → AG001 CEO Agent → Human Board
(немедленно, без промежуточных уровней)

## Purpose

Playbook описывает активацию режима кризисного управления при событиях,
угрожающих непрерывности бизнеса (не путать с обычным Risk Treatment —
PB015 — который работает на превентивном/плановом горизонте).

## Trigger Conditions

- Критичный инцидент кибербезопасности (эскалация из PB016)
- Форс-мажор (отказ ключевой инфраструктуры, отказ ключевого поставщика,
  внешнее событие)
- Репутационный кризис, требующий немедленной реакции

## Stage 1 — Idea (Crisis Declaration)

**Function:** RSK-CRI-001 Crisis Response Activation
**Owner:** AG005 Risk Manager (инициирует), AG001 CEO Agent (подтверждает)
**Decision Level:** L5

Действия:
1. Зафиксировать событие как кризис (порог: угроза непрерывности бизнеса
   или существенный финансовый/репутационный ущерб)
2. Немедленно уведомить AG001 CEO Agent и Human Board — в обход обычной
   иерархии эскалации

**Human Override:** обязателен на этом этапе — кризис не может быть объявлен
или снят без подтверждения человека.

## Stage 2 — Analysis (Impact Assessment)

**Owner:** AG005 Risk Manager
**Decision Level:** L5

Действия:
1. Быстро оценить масштаб: какие домены/системы/клиенты затронуты
2. Определить, требуется ли активация Business Continuity Plan (RSK-BCP-001)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager + AG048 Security Officer (при применимости)
**Decision Level:** L5

Действия:
1. Определить наихудший и наиболее вероятный сценарий развития
2. Оценить необходимость внешней коммуникации (клиенты, регулятор, инвесторы —
   FIN-IR-001 Investor Update Preparation при необходимости)

## Stage 4 — Decision (Crisis Response Plan Approval)

**Owner:** AG001 CEO Agent (совместно с Human Board)
**Decision Level:** L5

Критерии:
- План покрывает непрерывность критичных функций (см. Business Continuity)
- Назначен единый ответственный (Incident Commander) на время кризиса
- Определён план коммуникации (внутренний и внешний)

**Human Override:** обязателен — кризисное управление всегда находится под
прямым контролем человека, автономные решения агентов ограничены операционным
уровнем в рамках уже утверждённого плана.

## Stage 5 — Execution (Business Continuity Activation)

**Function:** RSK-BCP-001 Business Continuity Plan Test
**Owner:** AG051 Business Continuity Agent
**Decision Level:** L3 (в рамках утверждённого на Stage 4 плана)

Действия:
1. Активировать резервные процессы/системы для критичных функций
2. Координировать работу затронутых доменов через AG002 Chief Orchestrator
3. Регулярно (каждые несколько часов, в зависимости от критичности) обновлять
   AG001 CEO Agent и Human Board о статусе

## Stage 6 — Audit

**Function:** RSK-BCP-002 Business Continuity Plan Test Review
**Owner:** AG003 AI Auditor
**Decision Level:** L4

Действия:
1. После разрешения кризиса — задокументировать полный таймлайн событий
   и принятых решений
2. Оценить, соответствовало ли фактическое время реагирования плану

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Провести post-mortem с участием всех затронутых владельцев доменов
2. Обновить Business Continuity Plan и Crisis Response Plan на основе
   полученного опыта

## KPIs

- Time to Declare Crisis (от события до формальной активации)
- Time to Business Continuity Activation
- Critical Function Uptime During Crisis
- Post-Crisis Recovery Time

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (RSK-CRI, RSK-BCP, FIN-IR)
- PB016_Cyber_Incident_Response.md (частый источник эскалации)
- GOVERNANCE_MODEL.md (Human Override, п.9)
- AGENT_REGISTRY.md (AG001, AG005, AG051, AG048, AG002)
