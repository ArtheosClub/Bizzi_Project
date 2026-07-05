# PB009 Vendor Onboarding & Evaluation

Version: 1.0
Status: Active Playbook
Related Capability: C08 Supply Chain
Related Functions: SCM-VEN-001, SCM-VEN-001-002, SCM-CSU-001, SCM-SRK-001
Owner Agent: AG037 Supplier Evaluation Agent
Escalation Path: AG037 → AG036 Procurement Manager → AG005 Risk Manager
(для высокорисковых поставщиков)

## Purpose

Playbook описывает процесс проверки, онбординга и периодической оценки
поставщиков — от первичной заявки до включения в утверждённый список
(Approved Vendor List).

## Trigger Conditions

- Заявка от любого департамента на нового поставщика
- Плановая периодическая переоценка существующего поставщика (ежегодно)

## Stage 1 — Idea (Vendor Intake)

**Owner:** AG037 Supplier Evaluation Agent
**Decision Level:** L1

Действия:
1. Получить заявку с базовой информацией о поставщике (услуга/товар, объём,
   ориентировочная стоимость)
2. Проверить, нет ли уже одобренного поставщика с аналогичным предложением
   в Approved Vendor List

## Stage 2 — Analysis (Supplier Evaluation)

**Function:** SCM-PRC-002 Supplier Evaluation
**Owner:** AG037 Supplier Evaluation Agent
**Decision Level:** L2

Действия:
1. Запросить у поставщика документы (реквизиты, референсы, сертификаты)
2. Оценить по критериям: цена, качество, надёжность поставки, финансовая
   устойчивость
3. Для критичных категорий — запросить RFQ через AG038 RFQ Agent

## Stage 3 — Risk Review

**Function:** SCM-SRK-001 Supplier Risk Assessment
**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Проверить репутационные и финансовые риски поставщика
2. Для поставщиков из стран с повышенным страновым риском — RSK-CTR-001
   Country Risk Rating
3. Проверить на санкционные списки (LEG-AML-001 AML Screening при необходимости)

## Stage 4 — Decision (Vendor Approval)

**Owner:** AG036 Procurement Manager (AG005 Risk Manager — при высоком риске)
**Decision Level:** L2 (L3 при высоком риске)

Критерии:
- Оценка поставщика выше порогового значения
- Risk rating не выше "Medium" (либо одобрено Risk Manager при "High" с
  компенсирующими мерами)
- Соответствие условиям compliance (LEG-KYC-001 при необходимости)

## Stage 5 — Execution (Onboarding & Contracting)

**Function:** SCM-CSU-001 Supplier Contract Negotiation
**Owner:** AG018 Contract Review Agent
**Decision Level:** L2

Действия:
1. Согласовать коммерческие условия и SLA
2. Оформить контракт через PB013_Contract_Review_Approval.md
3. Добавить поставщика в Approved Vendor List
4. Настроить периодическое напоминание о переоценке (AG075 Calendar Agent)

## Stage 6 — Audit

**Function:** SCM-VEN-001-002 Vendor Performance Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что все этапы оценки пройдены и задокументированы
2. Периодически (ежеквартально) проверять фактическую performance
   поставщика против SLA (SCM-VEN-001 Vendor Performance Review)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать типовые red flags, выявленные при оценке
2. Обновить критерии оценки при системных проблемах с определённой категорией
   поставщиков

## KPIs

- Vendor Onboarding Time (от заявки до включения в Approved Vendor List)
- Vendor Risk Distribution (% поставщиков по уровням риска)
- On-time Delivery Rate по действующим поставщикам

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SCM-VEN, SCM-CSU, SCM-SRK, SCM-PRC)
- PB010_Procurement_Request_to_Pay.md (использует Approved Vendor List)
- PB013_Contract_Review_Approval.md (оформление контракта с поставщиком)
- AGENT_REGISTRY.md (AG037, AG036, AG005, AG018, AG038)
