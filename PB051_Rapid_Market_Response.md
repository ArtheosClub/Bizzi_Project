# PB051 Rapid Market Response (Growth War Room)

Version: 1.0
Status: Active Playbook — Flagship
Related Capability: C01 Strategy / C03 Market Intelligence / C04 Marketing / C05 Sales
Related Functions: MKT-RTM-001, MKT-ALT-001, STR-WAR-001, SAL-DYN-001,
GOV-SPD-001, GOV-KLL-001
Owner Agent: AG002 Chief Orchestrator (активирует), AG006 Strategy Agent
(ведёт разбор)
Escalation Path: AG084 → AG006 → AG002 → AG001 CEO Agent (немедленно, без
ожидания планового цикла)

## Purpose

Это не рутинный ежеквартальный playbook — это протокол мгновенной реакции
на существенное движение рынка (конкурент снизил цену, вышел с новым
продуктом, произошёл сдвиг спроса). Обычная Decision Architecture с
плановыми стадиями здесь заменяется на сжатый цикл, рассчитанный на часы,
а не недели, но БЕЗ отказа от Governance-дисциплины — просто на ускоренном
треке (GOV-SPD-001 Rapid Decision Fast-Track Protocol).

Разница с PB015 (Risk Identification & Treatment): PB015 — про управление
угрозами на плановом горизонте. PB051 — про рыночные возможности и угрозы,
требующие ответа до конца дня, а не по итогам квартального ревью.

## Trigger Conditions

- MKT-RTM-001 Real-Time Market Signal Monitoring зафиксировал аномалию
  (резкое изменение цены конкурента, вирусный запуск альтернативы, PR-кризис
  у конкурента, открывающий возможность)
- Внезапный всплеск/падение спроса, не объяснимый плановыми факторами
  (MKT-DEM-002 Real-Time Demand Sensing)

## Stage 1 — Idea (Signal Confirmation) — целевое время: до 2 часов

**Function:** MKT-RTM-001 Real-Time Market Signal Monitoring
**Owner:** AG084 Market Intelligence Analyst
**Decision Level:** L1

Действия:
1. Подтвердить, что сигнал реален, а не шум/единичная аномалия
2. Оценить масштаб и скорость изменения (насколько это движение уже
   ощущается в наших метриках — трафик, конверсия, отток)
3. Немедленно созвать "War Room" — не ждать планового совещания

## Stage 2 — Analysis (Rapid War-Gaming) — целевое время: до 6 часов

**Function:** STR-WAR-001 Competitive War-Gaming
**Owner:** AG006 Strategy Agent
**Decision Level:** L3

Действия:
1. Смоделировать 2-3 сценария ответа (игнорировать / зеркалировать /
   контр-ход) и их вероятные последствия
2. Оценить, требует ли ответ изменения цены (SAL-DYN-001), сообщения
   (MRK-*), продукта (INN-*) или комбинации
3. НЕ проводить полноценный многонедельный анализ — цель: достаточно
   хорошее решение быстро, а не идеальное решение поздно

## Stage 3 — Risk Review (Fast-Track) — целевое время: параллельно Stage 2

**Function:** RSK-OPP-001 Risk-to-Opportunity Conversion Review
**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Проверить только критичные ограничения (юридические, репутационные
   красные линии) — не полный Risk Treatment цикл из PB015
2. Явно указать, чего НЕ делать (например, демпинг ниже себестоимости)

## Stage 4 — Decision (Fast-Track Approval) — целевое время: в течение суток

**Function:** GOV-SPD-001 Rapid Decision Fast-Track Protocol
**Owner:** AG002 Chief Orchestrator (AG001 CEO Agent — для решений, меняющих
цену/позиционирование публично)
**Decision Level:** L4 (по ускоренному треку, не по плановому)

Критерии:
- Хотя бы один сценарий из Stage 2 однозначно лучше "ничего не делать"
- Red lines из Stage 3 не нарушены

**Human Override:** обязателен, но происходит в сжатые сроки (часы, не дни) —
Fast-Track Protocol не отменяет Human Sovereignty, а обеспечивает, что
человек получает решение к рассмотрению быстро и в готовом к принятию виде.

## Stage 5 — Execution (Immediate Action)

**Owner:** зависит от выбранного ответа — AG025 Sales Director (цена),
AG030 Marketing Manager (сообщение), AG077 Innovation Manager (продукт)
**Decision Level:** L2

Действия:
1. Реализовать выбранный ответ в течение согласованного окна (обычно
   часы, максимум 2-3 дня для более сложных изменений)
2. Коммуницировать изменение всем затронутым доменам одновременно через
   AG002 Chief Orchestrator (не последовательно — параллельно)

## Stage 6 — Audit

**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Отследить фактический эффект ответа в течение следующих 48-72 часов
   (метрики: доля рынка, конверсия, отток)
2. Задокументировать реальное время реакции (от Stage 1 до Stage 5) для
   калибровки будущих циклов

## Stage 7 — Knowledge Capture

**Function:** GOV-KLL-001 Portfolio Kill/Scale Gate Review
**Owner:** AG002 Chief Orchestrator
**Decision Level:** L3

Действия:
1. Если ответ сработал — рассмотреть INN-SCL-001 Rapid Scale Decision
   (удвоить ставку, а не просто вернуться к обычному режиму)
2. Если не сработал — зафиксировать причину и закрыть инициативу без
   долгих разборов (fail-fast — INN-FFL-001)
3. Обновить War-Gaming сценарии (Stage 2) с учётом реального исхода —
   библиотека сценариев растёт с каждым циклом

## KPIs

- Signal-to-Decision Time (от обнаружения до утверждённого решения —
  целевое значение: часы, не недели)
- Response Effectiveness (изменение ключевой метрики после ответа)
- False Alarm Rate (% сигналов, не потребовавших реального ответа)

## Why This Playbook Matters

Большинство enterprise-фреймворков оптимизированы под предсказуемость и
контроль — и правильно делают для 90% операций (см. PB001-PB050). Но
агрессивный рост требует ещё одного режима: способности сжать обычный
2-3-недельный цикл "заметили → проанализировали → согласовали →
отреагировали" до одного дня, не теряя Governance-дисциплину. Это то, что
реально отличает компанию, которая формирует рынок, от компании, которая
на него реагирует с опозданием.

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (Growth & Market Reactivity Functions layer)
- PB015_Risk_Identification_Treatment.md (плановый аналог для не-срочных рисков)
- PB021_Escalation_Protocol.md (базовый механизм, здесь ускоренный)
- AGENT_REGISTRY.md (AG084, AG006, AG005, AG002, AG001, AG025, AG030, AG077)
