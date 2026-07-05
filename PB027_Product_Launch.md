# PB027 Product Launch (Go-to-Market)

Version: 1.0
Status: Active Playbook
Related Capability: C02 Innovation / C04 Marketing
Related Functions: INN-COM-001, MRK-PMK-001, MRK-PMK-002
Owner Agent: AG030 Marketing Manager
Escalation Path: AG030 → AG077 Innovation Manager → AG001 CEO Agent
(для запуска флагманского продукта)

## Purpose

Playbook описывает вывод на рынок нового продукта или существенной фичи —
от подтверждения готовности до пост-запускового анализа. Стартует после
успешной валидации в PB023_Idea_to_MVP.md.

## Trigger Conditions

- MVP успешно валидирован (INN-PVA-001, см. PB023)
- Запланированный релиз существующего продукта (major version)

## Stage 1 — Idea (Launch Readiness Check)

**Function:** INN-COM-001 Go-to-Market Readiness Review
**Owner:** AG077 Innovation Manager
**Decision Level:** L3

Действия:
1. Подтвердить готовность продукта (AG058 Product Manager, AG063 QA
   Automation Agent)
2. Определить целевой сегмент запуска (полный рынок или ограниченный
   pilot)

## Stage 2 — Analysis (Messaging & Positioning)

**Function:** MRK-PMK-001 Product Launch Messaging
**Owner:** AG030 Marketing Manager
**Decision Level:** L2

Действия:
1. Разработать позиционирование и ключевые сообщения (с учётом
   MKT-SEG-001 Market Segmentation)
2. Подготовить материалы: лендинг, демо, кейсы (AG031 Content Agent)
3. Согласовать с AG035 Brand Agent на соответствие гайдлайнам (MRK-BRA-001)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Оценить риск преждевременного раскрытия информации конкурентам
2. Проверить готовность Support (AG069) к притоку запросов после запуска

## Stage 4 — Decision (Launch Approval)

**Owner:** AG030 Marketing Manager (AG001 CEO Agent — для флагманских
запусков)
**Decision Level:** L2 (L4 для крупных запусков)

Критерии:
- Продукт прошёл QA (OPS-QUA-001)
- Маркетинговые материалы готовы и одобрены
- Support-команда подготовлена (KNW-KB-001 обновлена статьями)

## Stage 5 — Execution (Launch Campaign)

**Function:** MRK-CAM-001 Campaign Planning, MRK-CAM-002 Campaign Execution
**Owner:** AG034 Campaign Manager
**Decision Level:** L1-L2

Действия:
1. Запустить многоканальную кампанию (контент, соцсети, PR, email)
2. Координировать одновременный запуск: продукт (AG058), продажи (AG025
   Sales Director), поддержка (AG069)
3. Мониторить первые метрики использования в реальном времени

## Stage 6 — Audit

**Function:** MRK-PMK-002 Product Launch Messaging Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Сверить фактические результаты запуска (adoption, конверсия) с планом
2. Зафиксировать отклонения и их причины

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Провести post-launch retrospective с участием Product, Marketing, Sales,
   Support
2. Обновить шаблон запуска для будущих продуктов

## KPIs

- Time to Launch (от Go-to-Market Readiness до публичного релиза)
- Launch Week Adoption Rate
- Launch Campaign ROI (MRK-CAM-003 Campaign Performance Analysis)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (INN-COM, MRK-PMK, MRK-CAM, MRK-BRA)
- PB023_Idea_to_MVP.md (предыдущий этап)
- PB028_Content_Marketing_Cycle.md, PB029_Campaign_Planning.md (поддерживающие процессы)
- AGENT_REGISTRY.md (AG030, AG077, AG034, AG058, AG025, AG069)
