# PB035 Import/Export & Customs Compliance

Version: 1.0
Status: Active Playbook
Related Capability: C08 Supply Chain
Related Functions: SCM-IMX-001, SCM-CUS-001, SCM-CUS-001-002
Owner Agent: AG044 Customs Consultant
Escalation Path: AG044 → AG040 Logistics Manager → AG011 Compliance Agent
(для регуляторных вопросов)

## Purpose

Playbook описывает оформление трансграничных поставок — от подготовки
документации до подтверждения таможенной очистки, минимизируя риск
задержек и штрафов.

## Trigger Conditions

- Плановая международная поставка (импорт сырья/товаров, экспорт продукции)
- Изменение таможенного регулирования в стране операций (LEG-REG-001)

## Stage 1 — Idea (Shipment Documentation Planning)

**Function:** SCM-IMX-001 Import/Export Documentation
**Owner:** AG044 Customs Consultant
**Decision Level:** L2

Действия:
1. Определить применимые торговые режимы и требуемые документы
   (инвойс, сертификат происхождения, лицензии)
2. Проверить актуальность HS-кодов для товарной категории

## Stage 2 — Analysis (Compliance Check)

**Function:** SCM-CUS-001 Customs Compliance Check
**Owner:** AG044 Customs Consultant
**Decision Level:** L3

Действия:
1. Проверить соответствие поставки актуальным таможенным требованиям
   страны отправления и назначения
2. Рассчитать применимые пошлины и налоги
3. Проверить санкционные ограничения (LEG-AML-001 AML Screening для
   контрагентов)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить риск задержки на таможне и его влияние на SLA поставки
2. Оценить финансовый риск от изменения пошлин/тарифов

## Stage 4 — Decision (Shipment Approval)

**Owner:** AG040 Logistics Manager (AG011 Compliance Agent — при
неоднозначности регуляторных требований)
**Decision Level:** L2 (L3 при высоком риске)

Критерии:
- Вся необходимая документация подготовлена и проверена
- Расчёт пошлин учтён в стоимости поставки

## Stage 5 — Execution (Customs Clearance)

**Owner:** AG044 Customs Consultant
**Decision Level:** L2

Действия:
1. Подать документы на таможенное оформление
2. Координировать с логистическим партнёром (AG043 Fleet Agent /
   внешний перевозчик) сроки прохождения таможни
3. Отслеживать статус через SCM-LOG-001 Shipment Tracking

## Stage 6 — Audit

**Function:** SCM-CUS-001-002 Customs Compliance Check Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить фактическое время таможенной очистки против ожидаемого
2. Зафиксировать любые расхождения в расчёте пошлин или документации

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Обновить справочник HS-кодов и требований по странам
2. Зафиксировать типовые причины задержек на конкретных маршрутах/границах

## KPIs

- Customs Clearance Time
- Documentation Error Rate (требующий повторной подачи)
- Duty & Tax Accuracy (расчёт vs фактически уплаченное)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SCM-IMX, SCM-CUS, LEG-AML)
- PB034_Supply_Demand_Planning.md (источник плановых международных поставок)
- AGENT_REGISTRY.md (AG044, AG040, AG011, AG005)
