# PB023 Idea-to-MVP Pipeline

Version: 1.0
Status: Active Playbook
Related Capability: C02 Innovation
Related Functions: INN-IDE-001..003, INN-OPP-001, INN-PDI-001, INN-PVA-001, INN-MVP-001..002
Owner Agent: AG077 Innovation Manager
Escalation Path: AG077 → AG004 Business Analyst → AG001 CEO Agent
(для запуска как отдельного venture)

## Purpose

Playbook описывает путь идеи от первичной фиксации до валидированного MVP,
готового к решению о дальнейшем развитии (масштабирование, venture, или
закрытие).

## Trigger Conditions

- Идея зафиксирована любым агентом или сотрудником (INN-IDE-001)
- Сигнал возможности от AG084 Market Intelligence Analyst (MKT-OPP-001)

## Stage 1 — Idea (Capture & Scoring)

**Function:** INN-IDE-001 Capture New Idea, INN-IDE-002 Idea Scoring
**Owner:** AG077 Innovation Manager
**Decision Level:** L1-L2

Действия:
1. Зафиксировать идею в едином реестре (проблема, гипотеза, целевой сегмент)
2. Оценить по критериям: соответствие стратегии (STR-GRW-001), размер рынка
   (MKT-OPP-001), техническая осуществимость
3. Присвоить приоритет (INN-IDE-003 Idea Prioritization)

## Stage 2 — Analysis (Discovery)

**Function:** INN-PDI-001 Product Discovery Sprint
**Owner:** AG077 Innovation Manager
**Decision Level:** L2

Действия:
1. Провести discovery-спринт: интервью с потенциальными пользователями,
   анализ конкурентов (MKT-RES-002)
2. Сформулировать Business Model Canvas (INN-BMD-001)
3. Определить минимальный набор функций для проверки гипотезы

## Stage 3 — Risk Review

**Owner:** AG004 Business Analyst
**Decision Level:** L3

Действия:
1. Оценить риск каннибализации существующих продуктов
2. Оценить требуемые инвестиции против размера возможности (INN-POR-001
   Innovation Portfolio Review)

## Stage 4 — Decision (MVP Go/No-Go)

**Owner:** AG004 Business Analyst (AG001 CEO Agent — при существенных
инвестициях)
**Decision Level:** L3 (L4 при запуске как отдельного venture)

Критерии:
- Discovery подтвердил наличие реальной потребности
- Ресурсы на MVP доступны без ущерба текущим приоритетам

## Stage 5 — Execution (MVP Build & Validation)

**Function:** INN-MVP-001 MVP Scope Definition, INN-MVP-002 MVP Validation
**Owner:** AG058 Product Manager (совместно с AG077)
**Decision Level:** L2

Действия:
1. Определить чёткий scope MVP (что входит, что сознательно исключено)
2. Реализовать через стандартный цикл разработки (AG061/AG062 Architects,
   AG063 QA Automation Agent)
3. Провести валидацию с реальными пользователями (INN-PVA-001 Product
   Validation Testing)

## Stage 6 — Audit

**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что MVP соответствует изначально определённому scope
   (не произошло неконтролируемое расширение — scope creep)
2. Зафиксировать фактические затраты против первоначальной оценки

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать результат валидации (подтверждена/опровергнута гипотеза)
2. При успехе — передать в INN-COM-001 Go-to-Market Readiness Review и
   PB027_Product_Launch.md
3. При неудаче — задокументировать причины для будущих discovery-циклов

## KPIs

- Idea-to-MVP Cycle Time
- Validation Success Rate (% MVP, подтвердивших гипотезу)
- Cost per Validated Learning

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (INN-IDE, INN-PDI, INN-MVP, INN-PVA)
- PB027_Product_Launch.md (следующий этап при успешной валидации)
- AGENT_REGISTRY.md (AG077, AG004, AG058, AG001)
