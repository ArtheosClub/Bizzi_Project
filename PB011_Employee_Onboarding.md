# PB011 Employee Onboarding

Version: 1.0
Status: Active Playbook
Related Capability: C12 People Management
Related Functions: PEO-ONB-001, PEO-ONB-002, PEO-WFP-001, PEO-CUL-001
Owner Agent: AG021 HR Manager
Escalation Path: AG021 → AG002 Chief Orchestrator (для доступа к системам) →
AG001 CEO Agent (для C-level найма)

## Purpose

Playbook описывает цикл выхода нового сотрудника на работу — от подтверждения
оффера до полной интеграции в команду и системы компании.

## Trigger Conditions

- Кандидат принял оффер (после PB012 Recruitment Cycle)
- Подтверждена дата выхода на работу

## Stage 1 — Idea (Onboarding Plan Setup)

**Function:** PEO-WFP-001 Headcount Planning
**Owner:** AG021 HR Manager
**Decision Level:** L2

Действия:
1. Подтвердить открытую позицию соответствует утверждённому headcount plan
2. Определить департамент, руководителя, необходимое оборудование/доступы
3. Создать чек-лист онбординга (документы, IT-доступы, обучение)

## Stage 2 — Analysis (Access & Resource Planning)

**Owner:** AG021 HR Manager
**Decision Level:** L2

Действия:
1. Запросить у AG081 Authorization Manager необходимые уровни доступа
   (соответствующие роли — см. AGENT_REGISTRY.md для человеческих аналогов
   ролей агентов, если сотрудник курирует agent-функции)
2. Запросить оборудование через AG039 Purchasing Agent при необходимости
3. Согласовать дату первого дня с руководителем департамента

## Stage 3 — Risk Review

**Function:** LEG-KYC-001 KYC Verification (для ролей с финансовым доступом)
**Owner:** AG011 Compliance Agent
**Decision Level:** L2

Действия:
1. Проверить необходимость дополнительных проверок (NDA, non-compete,
   background check) в зависимости от роли
2. Для ролей с доступом к финансам/данным клиентов — расширенная проверка

## Stage 4 — Decision (Onboarding Kickoff Approval)

**Owner:** AG021 HR Manager
**Decision Level:** L1 (L3 для C-level или ролей с широким доступом)

Критерии:
- Все документы подписаны (оффер, NDA)
- Доступы одобрены Authorization Manager
- Compliance check пройден

## Stage 5 — Execution (Onboarding Delivery)

**Function:** PEO-ONB-001 New Hire Onboarding
**Owner:** AG021 HR Manager
**Decision Level:** L1

Действия:
1. Первый день: welcome-пакет, знакомство с командой, настройка рабочего места
2. Провести ознакомление с Vision.md, GOVERNANCE_MODEL.md (для понимания
   принципов работы AI-агентов, с которыми сотрудник будет взаимодействовать)
3. Назначить онбординг-buddy из департамента
4. Запланировать обучение через AG023 Learning & Development Agent (PEO-LRN-001)

## Stage 6 — Audit

**Function:** PEO-ONB-002 New Hire Onboarding Exception Handling
**Owner:** AG021 HR Manager
**Decision Level:** L1

Действия:
1. Проверить на 30/60/90 день, что чек-лист онбординга полностью закрыт
2. Зафиксировать отклонения (например, задержка выдачи оборудования)
   и эскалировать к ответственному департаменту

## Stage 7 — Knowledge Capture

**Function:** PEO-CUL-001 Culture Survey
**Owner:** AG021 HR Manager
**Decision Level:** L1

Действия:
1. Собрать обратную связь нового сотрудника об опыте онбординга (30 день)
2. Обновить чек-лист онбординга при выявлении системных проблем
3. Зафиксировать в KNW-LES-001, если обнаружен повторяющийся паттерн

## KPIs

- Time to Productivity: время до первого самостоятельного вклада
- Onboarding Completion Rate: % закрытых пунктов чек-листа к 30 дню
- New Hire Satisfaction Score (по итогам опроса на 30 день)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (PEO-ONB, PEO-WFP, PEO-CUL, PEO-LRN)
- PB012_Recruitment_Cycle.md (предыдущий этап)
- AGENT_REGISTRY.md (AG021, AG011, AG081, AG023)
