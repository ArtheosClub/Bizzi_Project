# PB049 Data Privacy Impact Assessment

Version: 1.0
Status: Active Playbook
Related Capability: C10 Legal & Compliance
Related Functions: LEG-DPR-001, LEG-DPR-001-002
Owner Agent: AG011 Compliance Agent
Escalation Path: AG011 → AG017 Legal Counsel → AG001 CEO Agent (для
существенных изменений в обработке данных клиентов)

## Purpose

Playbook описывает оценку рисков конфиденциальности данных перед запуском
новой функции/интеграции, обрабатывающей персональные данные — превентивная
мера, в отличие от PB016 (реактивное реагирование на инцидент).

## Trigger Conditions

- Новая интеграция, обрабатывающая персональные данные (см. PB036 System
  Integration Rollout)
- Новая функция продукта, собирающая дополнительные данные пользователей
- Изменение регулирования о защите данных (LEG-REG-001)

## Stage 1 — Idea (Trigger Identification)

**Owner:** AG011 Compliance Agent
**Decision Level:** L2

Действия:
1. Определить, обрабатывает ли новая инициатива персональные данные
2. Классифицировать тип данных (обычные / чувствительные категории)

## Stage 2 — Analysis (Impact Assessment)

**Function:** LEG-DPR-001 Data Privacy Impact Assessment
**Owner:** AG011 Compliance Agent
**Decision Level:** L3

Действия:
1. Задокументировать поток данных (откуда собираются, где хранятся, кто
   имеет доступ, куда передаются)
2. Оценить необходимость данных (data minimization — собираем ли мы
   больше, чем нужно)
3. Проверить правовое основание обработки (согласие, законный интерес)

## Stage 3 — Risk Review

**Owner:** AG049 Information Security Agent + AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить технические меры защиты (шифрование, контроль доступа —
   AG081 Authorization Manager)
2. Оценить риск при утечке (severity), опираясь на тип данных

## Stage 4 — Decision (Processing Approval)

**Owner:** AG017 Legal Counsel (AG001 CEO Agent — при обработке
чувствительных категорий данных в большом масштабе)
**Decision Level:** L3 (L4 для высокого риска)

Критерии:
- Правовое основание обработки задокументировано
- Технические меры защиты соответствуют уровню риска
- Data minimization принцип соблюдён

## Stage 5 — Execution (Implementation with Safeguards)

**Owner:** AG065 Data Engineer (техническая реализация)
**Decision Level:** L2

Действия:
1. Внедрить согласованные технические и организационные меры защиты
2. Обновить публичную политику конфиденциальности при необходимости
   (KNW-POL-001, см. PB048)

## Stage 6 — Audit

**Function:** LEG-DPR-001-002 Data Privacy Impact Assessment Review
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Периодически проверять, что фактическая обработка данных соответствует
   задокументированной в DPIA
2. Проверить своевременность реагирования на запросы субъектов данных
   (доступ, удаление)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать типовые паттерны обработки данных для ускорения будущих
   DPIA
2. Обновить чек-лист DPIA при изменении регулирования

## KPIs

- DPIA Completion Rate (% новых инициатив с обработкой данных, прошедших
  оценку до запуска)
- Data Subject Request Response Time
- Time to Complete DPIA

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (LEG-DPR, TEC-SEC, KNW-POL)
- PB036_System_Integration_Rollout.md (частый триггер)
- PB016_Cyber_Incident_Response.md (реактивный аналог при инциденте)
- AGENT_REGISTRY.md (AG011, AG017, AG049, AG005, AG065)
