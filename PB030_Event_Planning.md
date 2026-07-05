# PB030 Event Planning & Execution

Version: 1.0
Status: Active Playbook
Related Capability: C04 Marketing
Related Functions: MRK-EVT-001, MRK-EVT-002
Owner Agent: AG030 Marketing Manager
Escalation Path: AG030 → AG012 CFO Agent (для бюджета выше лимита) →
AG074 Meeting Coordinator (для логистики)

## Purpose

Playbook описывает организацию мероприятий (вебинары, конференции, стенды
на выставках) — от планирования до пост-события анализа лидов.

## Trigger Conditions

- Плановое участие в отраслевом мероприятии
- Организация собственного мероприятия (вебинар, meetup)

## Stage 1 — Idea (Event Selection/Concept)

**Owner:** AG030 Marketing Manager
**Decision Level:** L2

Действия:
1. Определить цель мероприятия (lead gen, brand awareness, удержание
   клиентов)
2. Оценить соответствие целевой аудитории мероприятия сегментам компании
   (MKT-SEG-001)

## Stage 2 — Analysis (Planning)

**Function:** MRK-EVT-001 Event Planning & Execution
**Owner:** AG030 Marketing Manager
**Decision Level:** L2

Действия:
1. Определить бюджет (участие, стенд, материалы, travel)
2. Спланировать логистику совместно с AG074 Meeting Coordinator и
   AG072 Executive Assistant (при участии руководства)
3. Подготовить материалы (AG031 Content Agent) и брендинг (AG035 Brand Agent)

## Stage 3 — Risk Review

**Owner:** AG012 CFO Agent
**Decision Level:** L2

Действия:
1. Проверить бюджет мероприятия против утверждённого маркетингового
   бюджета
2. Оценить ROI прошлых аналогичных мероприятий (если применимо)

## Stage 4 — Decision (Event Approval)

**Owner:** AG030 Marketing Manager (AG012 CFO Agent — при бюджете выше
лимита)
**Decision Level:** L2 (L3 для крупных мероприятий)

Критерии:
- Ожидаемое количество квалифицированных контактов оправдывает бюджет
- Логистика подтверждена (travel, стенд, материалы)

## Stage 5 — Execution (Event Delivery)

**Owner:** AG030 Marketing Manager (на площадке) + AG074 Meeting Coordinator
(логистика)
**Decision Level:** L1

Действия:
1. Провести мероприятие согласно плану
2. Собрать контакты участников (визитки, сканирование бейджей, регистрации
   на вебинаре)
3. Передать собранные контакты в AG026 CRM Agent как лиды (SAL-LEAD-001)

## Stage 6 — Audit

**Function:** MRK-EVT-002 Event Planning & Execution Review
**Owner:** AG067 Analytics Agent
**Decision Level:** L2

Действия:
1. Сверить фактический бюджет с планом
2. Оценить количество и качество собранных лидов против ожиданий

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать ROI мероприятия для решения об участии в будущем
2. Обновить чек-лист логистики при выявлении организационных проблем

## KPIs

- Cost Per Lead from Event
- Lead Volume and Quality (сравнение с MRK-LGN-001 из digital-кампаний)
- Event ROI

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (MRK-EVT, ADM-TRV, ADM-MTG)
- PB029_Campaign_Planning.md (координация с общим маркетинговым планом)
- PB004_Lead_to_Contract.md (получатель собранных лидов)
- AGENT_REGISTRY.md (AG030, AG074, AG072, AG012, AG026)
