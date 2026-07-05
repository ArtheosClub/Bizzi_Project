# PB039 Tax Filing Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-TAX-001, FIN-TAX-002
Owner Agent: AG015 Tax Consultant
Escalation Path: AG015 → AG012 CFO Agent → AG001 CEO Agent (для существенных
налоговых позиций/споров)

## Purpose

Playbook описывает цикл подготовки и подачи налоговой отчётности по всем
юрисдикциям присутствия компании.

## Trigger Conditions

- Плановый налоговый период (месячный НДС, квартальный, годовой)
- Изменение налогового законодательства (LEG-REG-001)

## Stage 1 — Idea (Filing Calendar Check)

**Owner:** AG015 Tax Consultant
**Decision Level:** L2

Действия:
1. Проверить календарь налоговых обязательств по всем юрисдикциям
2. Собрать исходные данные из закрытого финансового периода (FIN-ACC-001,
   см. PB008_Monthly_Financial_Close.md)

## Stage 2 — Analysis (Tax Calculation)

**Function:** FIN-TAX-001 Tax Filing Preparation
**Owner:** AG015 Tax Consultant
**Decision Level:** L3

Действия:
1. Рассчитать налоговые обязательства по каждому применимому налогу
2. Проверить применимость льгот/вычетов
3. Подготовить черновик декларации

## Stage 3 — Risk Review

**Owner:** AG011 Compliance Agent
**Decision Level:** L3

Действия:
1. Проверить декларацию на соответствие актуальному законодательству
2. Оценить риск налогового спора при использовании неоднозначных трактовок

## Stage 4 — Decision (Filing Approval)

**Owner:** AG012 CFO Agent
**Decision Level:** L3 (L4 для существенных или спорных налоговых позиций)

Критерии:
- Расчёт проверен и не содержит ошибок
- Спорные позиции задокументированы с обоснованием

## Stage 5 — Execution (Filing & Payment)

**Owner:** AG015 Tax Consultant
**Decision Level:** L2

Действия:
1. Подать декларацию в установленный срок
2. Инициировать оплату через AG014 Treasury Agent (FIN-TRE-001)
3. Архивировать поданные документы (ADM-REC-001)

## Stage 6 — Audit

**Function:** FIN-TAX-002 Tax Filing Preparation Review
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить своевременность подачи (нет штрафов за просрочку)
2. Сверить фактически уплаченное с расчётом

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать изменения в законодательстве для следующего цикла
2. Обновить шаблоны расчётов по юрисдикциям

## KPIs

- On-time Filing Rate (100% — целевое значение)
- Tax Calculation Accuracy
- Effective Tax Rate по юрисдикциям

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-TAX, FIN-TRE, LEG-REG)
- PB008_Monthly_Financial_Close.md (источник финансовых данных)
- AGENT_REGISTRY.md (AG015, AG012, AG011, AG014)
