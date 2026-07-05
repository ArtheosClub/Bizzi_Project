# PB041 Investor Relations Update

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-IR-001, FIN-IR-001-002
Owner Agent: AG012 CFO Agent
Escalation Path: AG012 → AG001 CEO Agent → Human Board (для существенной
негативной информации)

## Purpose

Playbook описывает подготовку регулярных обновлений для инвесторов
(quarterly update, board deck) и ad-hoc коммуникацию при существенных
событиях.

## Trigger Conditions

- Плановый квартальный investor update
- Существенное событие, требующее ad-hoc уведомления (крупная сделка,
  кризис — см. PB017)

## Stage 1 — Idea (Content Planning)

**Owner:** AG012 CFO Agent
**Decision Level:** L3

Действия:
1. Определить ключевые метрики периода (выручка, рост, runway)
2. Собрать операционные highlights от владельцев доменов (через
   AG083 Dashboard Manager)

## Stage 2 — Analysis (Financial Narrative)

**Function:** FIN-IR-001 Investor Update Preparation
**Owner:** AG012 CFO Agent
**Decision Level:** L4

Действия:
1. Подготовить финансовую часть (P&L, cash position — FIN-TRE-001)
2. Сформировать нарратив: что сработало, что нет, следующие шаги
3. Подготовить материалы совместно с AG031 Content Agent (формат, дизайн)

## Stage 3 — Risk Review

**Owner:** AG017 Legal Counsel
**Decision Level:** L4

Действия:
1. Проверить на предмет forward-looking statements и раскрытия
   конфиденциальной информации
2. Убедиться в соответствии обязательствам перед инвесторами (условия
   инвестиционного соглашения)

## Stage 4 — Decision (Update Approval)

**Owner:** AG001 CEO Agent
**Decision Level:** L4

Критерии:
- Финансовые данные точны и сверены с закрытым периодом
- Нарратив честно отражает ситуацию (включая негативные моменты)

**Human Override:** обязателен — коммуникация с инвесторами всегда
проходит через прямое утверждение человеком.

## Stage 5 — Execution (Distribution)

**Owner:** AG012 CFO Agent
**Decision Level:** L2

Действия:
1. Направить обновление инвесторам по согласованному каналу
2. Подготовиться к возможным вопросам (FAQ)

## Stage 6 — Audit

**Function:** FIN-IR-001-002 Investor Update Preparation Review
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить консистентность цифр с официальной финансовой отчётностью
2. Зафиксировать историю коммуникаций для будущих раундов финансирования

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать вопросы инвесторов для подготовки к будущим обновлениям
2. Обновить шаблон investor update при необходимости

## KPIs

- Update Timeliness (в срок согласно инвестиционному соглашению)
- Investor Response/Engagement Rate
- Consistency Score (соответствие официальной отчётности)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-IR, FIN-TRE, LEG-CON)
- PB008_Monthly_Financial_Close.md (источник финансовых данных)
- PB017_Crisis_Management.md (источник ad-hoc коммуникаций)
- AGENT_REGISTRY.md (AG012, AG001, AG017)
