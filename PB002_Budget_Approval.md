# PB002 Budget Planning & Approval

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-BUD-001, FIN-BUD-002, FIN-BUD-003, FIN-FCS-001, FIN-FPA-001
Owner Agent: AG014 Finance Manager
Escalation Path: AG014 → AG001 CEO Agent (per Decision Architecture)

## Purpose

Playbook описывает годовой и квартальный цикл бюджетного планирования —
от первичного прогноза до финального утверждения человеком.

## Trigger Conditions

- Плановый годовой бюджетный цикл (обычно Q4 предыдущего года)
- Квартальный пересмотр бюджета (STR-PLN-002 Quarterly Strategic Review)
- Существенное отклонение факта от плана, инициирующее внеплановый пересмотр

## Stage 1 — Idea (Budget Framing)

**Function:** FIN-FCS-001 Financial Forecast Update
**Owner:** AG014 Finance Manager
**Decision Level:** L2

Действия:
1. Собрать исторические данные по расходам/доходам за предыдущий период
2. Получить стратегические приоритеты от AG001 CEO Agent (STR-PLN-001)
3. Сформировать черновой финансовый прогноз на следующий период

**Output:** Draft Forecast

## Stage 2 — Analysis (Budget Planning)

**Function:** FIN-BUD-001 Budget Planning
**Owner:** AG014 Finance Manager
**Decision Level:** L3

Действия:
1. Распределить бюджет по доменам (Capability) на основе стратегических приоритетов
2. Согласовать предварительные лимиты с владельцами доменов (Domain Manager Agents)
3. Рассчитать сценарии (базовый / оптимистичный / консервативный)

**Output:** Budget Draft by Capability Domain

## Stage 3 — Risk Review

**Function:** RSK-FIN-001 Financial Risk Monitoring
**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить риски излишней концентрации расходов в одном домене
2. Проверить соответствие бюджета лимитам Capital Allocation (STR-CAP-001)
3. Вынести рекомендацию: Approve / Approve with adjustments / Reject

## Stage 4 — Decision (Budget Approval)

**Function:** FIN-BUD-003 Budget Approval Package
**Owner:** AG001 CEO Agent
**Decision Level:** L4

Критерии:
- Бюджет соответствует стратегическим приоритетам (STR-PLN-001)
- Риск-рейтинг не выше "Medium"
- Резерв на непредвиденные расходы заложен (рекомендуется от 5%)

**Human Override:** обязателен — финальное утверждение бюджета всегда
подтверждается человеком (Human Sovereignty, GOVERNANCE_MODEL.md п.9).

## Stage 5 — Execution (Budget Distribution)

**Owner:** AG014 Finance Manager
**Decision Level:** L2

Действия:
1. Довести утверждённые лимиты до всех Domain Manager Agents
2. Настроить пороги оповещений о превышении бюджета по каждому домену
3. Зафиксировать бюджет как baseline для FIN-FPA-001 Variance Analysis

## Stage 6 — Audit (Ongoing Monitoring)

**Function:** FIN-FPA-001 Variance Analysis
**Owner:** AG014 Finance Manager
**Decision Level:** L2

Действия:
1. Ежемесячно сверять факт с планом (FIN-ACC-001 Monthly Close Process)
2. При отклонении > 10% — эскалация к AG005 Risk Manager
3. GOV-AUD-001 Decision Audit фиксирует само решение об утверждении бюджета

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG026 Knowledge Manager
**Decision Level:** L1

Действия:
1. Зафиксировать точность прогноза (план vs факт) для улучшения следующего цикла
2. Обновить шаблоны бюджетирования при обнаружении системных ошибок оценки

## KPIs

- Forecast Accuracy: отклонение факта от плана (%)
- Budget Cycle Time: время от Draft до Approval
- Reserve Utilization: % использования резерва на непредвиденные расходы

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-BUD, FIN-FCS, FIN-FPA, RSK-FIN)
- GOVERNANCE_MODEL.md (Human Override, Decision Architecture)
- AGENT_REGISTRY.md (AG014, AG001, AG005)
