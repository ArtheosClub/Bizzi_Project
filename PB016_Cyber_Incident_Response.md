# PB016 Cyber Incident Response

Version: 1.0
Status: Active Playbook
Related Capability: C11 Risk Management / C13 Technology
Related Functions: RSK-CYB-001, TEC-SEC-001, RSK-CYB-002
Owner Agent: AG050 Incident Response Agent
Escalation Path: AG050 → AG048 Security Officer → AG005 Risk Manager →
AG001 CEO Agent (для инцидентов с утечкой данных клиентов)

## Purpose

Playbook описывает обнаружение, локализацию и устранение инцидентов
кибербезопасности, в обход стандартного SLA поддержки (см. PB007) ввиду
критичности временного фактора.

## Trigger Conditions

- Автоматическое обнаружение аномалии системой мониторинга (TEC-INF-001)
- Тикет от AG069 Support Agent, классифицированный как security incident
  (см. PB007_Support_Escalation.md, Stage 3)
- Внешнее уведомление (bug bounty, партнёр, регулятор)

## Stage 1 — Idea (Detection & Triage)

**Function:** RSK-CYB-001 Cyber Risk Assessment
**Owner:** AG049 Information Security Agent
**Decision Level:** L3

Действия:
1. Подтвердить, что событие является реальным инцидентом (не ложным
   срабатыванием)
2. Классифицировать по типу (утечка данных, DDoS, несанкционированный доступ,
   вредоносное ПО) и серьёзности

## Stage 2 — Analysis (Containment Planning)

**Function:** TEC-SEC-001 Security Incident Response
**Owner:** AG050 Incident Response Agent
**Decision Level:** L4

Действия:
1. Определить масштаб воздействия (какие системы/данные затронуты)
2. Разработать план локализации (изоляция систем, отзыв доступов через
   AG081 Authorization Manager)

## Stage 3 — Risk Review

**Owner:** AG048 Security Officer
**Decision Level:** L4

Действия:
1. Оценить, затронуты ли данные клиентов (требует LEG-DPR-001 Data Privacy
   Impact Assessment и, возможно, регуляторного уведомления)
2. Оценить репутационный риск (RSK-REP-001)

## Stage 4 — Decision (Response Activation)

**Owner:** AG005 Risk Manager (AG001 CEO Agent — при утечке данных клиентов
или необходимости публичного раскрытия)
**Decision Level:** L4 (L5 при критичном инциденте)

Критерии:
- План локализации минимизирует дальнейший ущерб
- Определена необходимость внешнего уведомления (клиенты, регулятор,
  партнёры)

**Human Override:** обязателен перед любым внешним/публичным уведомлением
об инциденте.

## Stage 5 — Execution (Containment & Remediation)

**Owner:** AG050 Incident Response Agent
**Decision Level:** L2

Действия:
1. Выполнить локализацию (изоляция, патчинг уязвимости)
2. Восстановить затронутые системы из чистых бэкапов при необходимости
   (RSK-BCP-001 Business Continuity Plan Test как справочная база)
3. Уведомить затронутые стороны согласно решению Stage 4

## Stage 6 — Audit

**Function:** RSK-CYB-002 Cyber Risk Assessment Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Провести post-incident review: что сработало, что нет, время реакции
2. Зафиксировать root cause и таймлайн инцидента для регуляторной отчётности
   при необходимости

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Обновить процедуры реагирования на основе выявленных пробелов
2. Передать структурные уязвимости в TEC-домен для устранения (TEC-APP-001,
   TEC-INT-001)

## KPIs

- Mean Time to Detect (MTTD)
- Mean Time to Contain (MTTC)
- Mean Time to Resolve (MTTR)
- Post-Incident Action Item Closure Rate

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (RSK-CYB, TEC-SEC, LEG-DPR)
- PB007_Support_Escalation.md (источник инцидентов через support-канал)
- PB017_Crisis_Management.md (эскалация при критичном масштабе)
- AGENT_REGISTRY.md (AG050, AG049, AG048, AG005, AG001)
