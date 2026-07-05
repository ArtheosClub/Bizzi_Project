# PB013 Contract Review & Approval

Version: 1.0
Status: Active Playbook
Related Capability: C10 Legal & Compliance
Related Functions: LEG-CON-001, LEG-CON-002, LEG-CON-003, LEG-CON-002-002
Owner Agent: AG018 Contract Review Agent
Escalation Path: AG018 → AG017 Legal Counsel → AG001 CEO Agent (для контрактов
с обязательствами выше установленного лимита)

## Purpose

Playbook описывает цикл рассмотрения и утверждения любого контракта
(с клиентом, поставщиком или партнёром), поступающего из любого департамента
(Sales, Procurement, Partnerships).

## Trigger Conditions

- Запрос на контракт от AG025 Sales Director (SAL-CTR-001)
- Запрос от AG036 Procurement Manager / AG018 (SCM-CSU-001)
- Запрос на партнёрское соглашение от AG006 Strategy Agent (STR-PAR-001)

## Stage 1 — Idea (Intake & Drafting)

**Function:** LEG-CON-001 Contract Drafting
**Owner:** AG018 Contract Review Agent
**Decision Level:** L2

Действия:
1. Получить запрос с базовыми условиями (стороны, предмет, сумма, срок)
2. Подобрать применимый шаблон контракта из Knowledge Base (KNW-KB-001)
3. Подготовить черновик

**Output:** Draft Contract

## Stage 2 — Analysis (Legal Review)

**Function:** LEG-CON-002 Contract Review
**Owner:** AG018 Contract Review Agent
**Decision Level:** L3

Действия:
1. Проверить черновик на соответствие стандартным условиям компании
2. Выявить нестандартные пункты (нетиповые условия ответственности, IP,
   расторжения)
3. При обнаружении нестандартных условий — передать на Stage 3

## Stage 3 — Risk Review

**Function:** LEG-CON-002-002 Contract Review Exception Handling
**Owner:** AG017 Legal Counsel
**Decision Level:** L3

Действия:
1. Оценить риски нестандартных условий (RSK-LEG-001 Legal Risk Review)
2. При конфликте с IP компании — привлечь AG020 IP Agent (LEG-IP-001)
3. Вынести рекомендацию: Approve as-is / Approve with redlines / Reject

## Stage 4 — Decision (Approval)

**Function:** LEG-CON-003 Contract Approval
**Owner:** AG017 Legal Counsel (AG001 CEO Agent — для контрактов выше лимита
обязательств, установленного Governance Model)
**Decision Level:** L4

Критерии:
- Все нестандартные условия явно одобрены или удалены
- Risk rating не выше "Medium" (либо одобрено CEO при "High")
- Финансовые условия согласованы с AG012 CFO Agent (для контрактов,
  влияющих на бюджет)

**Human Override:** обязателен для контрактов с обязательствами выше лимита
или содержащих нестандартные условия ответственности.

## Stage 5 — Execution (Signing & Filing)

**Owner:** AG018 Contract Review Agent
**Decision Level:** L1

Действия:
1. Направить финальную версию на подпись сторонам
2. Зарегистрировать подписанный контракт в Records (ADM-REC-001)
3. Установить напоминания о ключевых датах (продление, окончание срока)
   через AG075 Calendar Agent

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что контракт прошёл все обязательные этапы ревью
2. Сверить фактические условия с одобренными на Stage 4

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. При повторяющихся нестандартных условиях — обновить стандартный шаблон
2. Зафиксировать типовые redlines для ускорения будущих ревью

## KPIs

- Contract Turnaround Time: время от Draft до подписания
- Exception Rate: % контрактов с нестандартными условиями
- Redline Cycles: среднее число раундов правок до утверждения

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (LEG-CON, RSK-LEG, LEG-IP)
- PB004_Lead_to_Contract.md (источник запросов из Sales)
- AGENT_REGISTRY.md (AG018, AG017, AG020, AG001, AG012)
