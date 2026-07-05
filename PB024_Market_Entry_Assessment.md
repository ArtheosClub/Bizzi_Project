# PB024 Market Entry Assessment

Version: 1.0
Status: Active Playbook
Related Capability: C01 Strategy / C03 Market Intelligence
Related Functions: STR-INT-001, STR-INT-002, MKT-IND-001, MKT-OPP-001
Owner Agent: AG006 Strategy Agent
Escalation Path: AG006 → AG004 Business Analyst → AG001 CEO Agent

## Purpose

Playbook описывает оценку возможности выхода на новый географический рынок
или новый сегмент — от первичного анализа до рекомендации по стратегии входа.

## Trigger Conditions

- Стратегическая инициатива роста (STR-GRW-001 Growth Strategy Formulation)
- Сигнал возможности от AG084 Market Intelligence Analyst

## Stage 1 — Idea (Opportunity Framing)

**Owner:** AG006 Strategy Agent
**Decision Level:** L3

Действия:
1. Определить целевой рынок/сегмент и обоснование интереса
2. Сформулировать ключевые вопросы для анализа (размер рынка, конкуренция,
   регуляторные барьеры)

## Stage 2 — Analysis (Market & Country Analysis)

**Function:** MKT-IND-001 Industry Landscape Analysis, MKT-RES-003 Country Analysis
**Owner:** AG084 Market Intelligence Analyst
**Decision Level:** L2

Действия:
1. Оценить размер и динамику рынка (MKT-DEM-001 Demand Forecast Model)
2. Проанализировать конкурентную среду (MKT-RES-002 Competitor Analysis)
3. Оценить страновой риск (RSK-CTR-001 Country Risk Rating)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L4

Действия:
1. Оценить регуляторные барьеры входа (LEG-INT-001 Cross-Border Legal Review)
2. Оценить финансовый риск инвестиций в новый рынок (RSK-FIN-001)
3. Рассмотреть требования по локализации (валюта, налоги — FIN-TAX-001)

## Stage 4 — Decision (Entry Strategy Approval)

**Function:** STR-INT-001 Market Entry Assessment
**Owner:** AG001 CEO Agent
**Decision Level:** L4

Варианты стратегии входа:
- Прямой выход (собственная команда/юрлицо)
- Партнёрство (см. PB025_Partnership_Evaluation.md)
- Приобретение локального игрока (см. PB026_MA_Target_Screening.md)

Критерии:
- ROI обоснован анализом Stage 2
- Риск-рейтинг приемлем или есть план его снижения

**Human Override:** обязателен — вход на новый рынок относится к
стратегическим решениям уровня L4, требующим подтверждения человеком.

## Stage 5 — Execution (Entry Plan Implementation)

**Owner:** зависит от выбранной стратегии (AG006 для прямого входа,
AG025 Sales Director для коммерческого запуска)
**Decision Level:** L2

Действия:
1. Разработать детальный план запуска (юридическая структура, найм,
   локализация продукта)
2. Установить контрольные точки для оценки прогресса (обычно 6/12 месяцев)

## Stage 6 — Audit

**Function:** STR-INT-002 Market Entry Assessment Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. На контрольных точках сверить фактические результаты с прогнозом
2. При существенном отклонении — эскалация к AG001 для решения о продолжении/
   корректировке/выходе с рынка

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать точность прогноза размера рынка и рисков для улучшения
   будущих оценок
2. Обновить страновые профили в Knowledge Base

## KPIs

- Time to Market Entry Decision
- Forecast Accuracy (прогноз vs факт через 12 месяцев)
- Market Entry ROI

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (STR-INT, MKT-IND, MKT-RES, RSK-CTR, LEG-INT)
- PB025_Partnership_Evaluation.md, PB026_MA_Target_Screening.md (альтернативные пути входа)
- AGENT_REGISTRY.md (AG006, AG084, AG005, AG001)
