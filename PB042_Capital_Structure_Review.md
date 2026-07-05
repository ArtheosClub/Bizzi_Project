# PB042 Capital Structure Review

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-CAP-001, FIN-CAP-002, STR-CAP-001
Owner Agent: AG012 CFO Agent
Escalation Path: AG012 → AG001 CEO Agent → Human Board (для изменения
структуры капитала)

## Purpose

Playbook описывает периодическую оценку структуры капитала предприятия
(соотношение долга и капитала, стоимость капитала) и подготовку решений
о её изменении (привлечение долга, нового раунда, buyback).

## Trigger Conditions

- Плановый ежегодный обзор структуры капитала
- Потребность в капитале для роста (STR-GRW-001, STR-CAP-001) или M&A
  (PB026)

## Stage 1 — Idea (Capital Needs Assessment)

**Owner:** AG012 CFO Agent
**Decision Level:** L4

Действия:
1. Оценить текущую и прогнозную потребность в капитале (рост, M&A,
   операционные нужды)
2. Проанализировать текущую структуру (доля долга/капитала, стоимость
   каждого источника)

## Stage 2 — Analysis (Options Modeling)

**Function:** FIN-CAP-001 Capital Structure Review
**Owner:** AG016 Financial Planning & Analysis Agent
**Decision Level:** L3

Действия:
1. Смоделировать варианты (долговое финансирование, equity раунд,
   комбинация)
2. Рассчитать влияние каждого варианта на WACC (средневзвешенную стоимость
   капитала) и dilution для существующих акционеров

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L4

Действия:
1. Оценить риск избыточной долговой нагрузки (влияние на ликвидность —
   FIN-TRE-001)
2. Оценить рыночные условия для equity раунда (благоприятность момента)

## Stage 4 — Decision (Structure Approval)

**Owner:** AG001 CEO Agent + Human Board
**Decision Level:** L5

Критерии:
- Выбранная структура соответствует стратегическим потребностям в капитале
- Риск ликвидности и dilution приемлемы

**Human Override:** обязателен — изменение структуры капитала относится
к решениям, требующим прямого утверждения Human Board.

## Stage 5 — Execution (Capital Raise/Restructuring)

**Owner:** AG012 CFO Agent (с внешними финансовыми советниками, где
применимо — аналогично PB026 M&A, вне стандартной Decision Architecture
для этапа переговоров)
**Decision Level:** L2 (в рамках утверждённого мандата)

Действия:
1. Инициировать выбранный процесс (переговоры с банком, подготовка к
   equity раунду)
2. Координировать с AG017 Legal Counsel по документации

## Stage 6 — Audit

**Function:** FIN-CAP-002 Capital Structure Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L4

Действия:
1. Проверить, что итоговые условия соответствуют утверждённым на Stage 4
   параметрам
2. Обновить FIN-IR-001 Investor Update Preparation с новой структурой
   капитала

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Зафиксировать условия и итоги для будущих решений о капитале
2. Обновить модель WACC с актуальными параметрами

## KPIs

- Weighted Average Cost of Capital (WACC)
- Debt-to-Equity Ratio
- Time to Close (для привлечения капитала)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-CAP, STR-CAP, FIN-TRE)
- PB026_MA_Target_Screening.md (потребность в капитале для M&A)
- PB041_Investor_Relations_Update.md (коммуникация изменений)
- AGENT_REGISTRY.md (AG012, AG016, AG005, AG001, AG017)
