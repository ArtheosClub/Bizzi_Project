# PB005 Renewal & Retention Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C05 Sales / C06 Customer Success
Related Functions: SAL-REN-001, SAL-REN-001-002, CUS-RET-001, CUS-HLT-001, CUS-HLT-002
Owner Agent: AG029 Customer Success Agent
Escalation Path: AG029 → AG025 Sales Director (для коммерческих условий) →
AG012 CFO Agent (для скидок на renewal выше лимита)

## Purpose

Playbook описывает цикл продления контракта клиента — от раннего выявления
риска оттока до подписания renewal или управляемого расставания с клиентом.

## Trigger Conditions

- Приближение даты окончания контракта (за 90/60/30 дней — по календарю
  из PB013_Contract_Review_Approval.md)
- Падение Customer Health Score ниже порога (CUS-HLT-001)

## Stage 1 — Idea (Health Check)

**Function:** CUS-HLT-001 Customer Health Scoring
**Owner:** AG029 Customer Success Agent
**Decision Level:** L2

Действия:
1. Собрать метрики здоровья клиента: adoption (CUS-ADO-001), тикеты (CUS-SUP-001),
   NPS (CUS-NPS-001)
2. Рассчитать композитный Health Score
3. Классифицировать: Healthy / At Risk / Critical

## Stage 2 — Analysis (Churn Risk Detection)

**Function:** CUS-HLT-002 Churn Risk Detection
**Owner:** AG029 Customer Success Agent
**Decision Level:** L3

Действия:
1. Для клиентов "At Risk"/"Critical" — определить конкретные причины
   (низкое использование, нерешённые тикеты, смена контактного лица)
2. Оценить commercial value клиента (SAL-ACC-001 Key Account Review)
3. Сформировать renewal-стратегию: Standard Renewal / Save Play / Managed Exit

## Stage 3 — Risk Review

**Function:** SAL-REN-001 Renewal Risk Review
**Owner:** AG029 Customer Success Agent
**Decision Level:** L2

Действия:
1. Оценить финансовое влияние потери клиента на выручку
2. При высоком риске и высокой ценности клиента — эскалация к AG025 Sales Director

## Stage 4 — Decision (Renewal Strategy Approval)

**Owner:** AG025 Sales Director (AG012 CFO Agent — при скидке выше лимита)
**Decision Level:** L2 (L3 при нестандартных условиях)

Критерии:
- Стратегия (Standard/Save Play/Managed Exit) соответствует ценности клиента
- Предлагаемые условия (скидка, доп. услуги) в рамках утверждённых лимитов

## Stage 5 — Execution (Renewal Outreach)

**Owner:** AG029 Customer Success Agent
**Decision Level:** L1

Действия:
1. Связаться с клиентом заранее (не позднее чем за 60 дней до окончания)
2. Для "Save Play" — устранить конкретные болевые точки перед предложением renewal
3. Подготовить renewal-контракт через PB013_Contract_Review_Approval.md
4. При решении клиента не продлевать — задокументировать причину (Managed Exit)

## Stage 6 — Audit

**Function:** SAL-REN-001-002 Renewal Risk Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что все клиенты с приближающейся датой окончания были
   своевременно охвачены (не пропущены)
2. Зафиксировать причины оттока для потерянных клиентов

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать эффективные Save Play тактики по сегментам клиентов
2. Обновить пороги Health Score при систематических ложных срабатываниях

## KPIs

- Net Revenue Retention (NRR)
- Renewal Rate (% продлённых контрактов от общего числа due)
- Early Warning Lead Time (за сколько дней до оттока клиент был выявлен как "At Risk")

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SAL-REN, CUS-HLT, CUS-RET)
- PB013_Contract_Review_Approval.md (оформление renewal-контракта)
- PB006_Upsell_Cross_Sell.md (альтернативный путь для "Healthy" клиентов)
- AGENT_REGISTRY.md (AG029, AG025, AG012)
