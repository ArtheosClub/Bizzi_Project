# PB026 M&A Target Screening

Version: 1.0
Status: Active Playbook
Related Capability: C01 Strategy
Related Functions: STR-MNA-001, STR-MNA-002, STR-CAP-001
Owner Agent: AG001 CEO Agent
Escalation Path: AG006 Strategy Agent → AG012 CFO Agent → AG001 CEO Agent →
Human Board (для завершения сделки)

## Purpose

Playbook описывает выявление и первичную оценку потенциальных целей для
приобретения (M&A) — до этапа полноценного due diligence, который выходит
за рамки типового цикла и ведётся отдельным проектом с внешними советниками.

## Trigger Conditions

- Стратегическая инициатива неорганического роста (STR-GRW-001)
- Входящее предложение о продаже от потенциальной цели
- Результат PB024, где M&A выбран как стратегия входа на рынок

## Stage 1 — Idea (Target Identification)

**Owner:** AG006 Strategy Agent
**Decision Level:** L3

Действия:
1. Сформировать критерии целевой компании (размер, технология, клиентская
   база, география)
2. Составить long-list потенциальных целей (совместно с AG084 Market
   Intelligence Analyst)

## Stage 2 — Analysis (Preliminary Screening)

**Function:** STR-MNA-001 M&A Target Screening
**Owner:** AG006 Strategy Agent
**Decision Level:** L3

Действия:
1. Сузить long-list до short-list по стратегическому соответствию
2. Оценить примерную стоимость (публичные данные, отраслевые мультипликаторы)
3. Оценить синергетический эффект (доступ к клиентам, технологии, команде)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L4

Действия:
1. Оценить риски интеграции (культурные, технологические, юридические)
2. Предварительная проверка на регуляторные ограничения (антимонопольные
   и др. — LEG-REG-001)

## Stage 4 — Decision (Approach Approval)

**Owner:** AG001 CEO Agent
**Decision Level:** L4

Критерии:
- Цель соответствует стратегическим критериям Stage 1
- Предварительная оценка стоимости в рамках доступного капитала
  (STR-CAP-001 Capital Allocation Decision)

**Human Override:** обязателен — решение о выходе на переговоры с целью
поглощения требует прямого утверждения Human Board.

## Stage 5 — Execution (Initial Approach & Due Diligence Kickoff)

**Owner:** AG001 CEO Agent (с привлечением внешних M&A советников —
за пределами предприятия Art of Business)
**Decision Level:** L2 (в рамках утверждённого на Stage 4 мандата)

Действия:
1. Инициировать контакт с целью (через AG006 или напрямую AG001)
2. При взаимном интересе — передать в формальный due diligence процесс
   (ведётся вне рамок этого playbook, с участием внешних юристов/аудиторов)
3. AG012 CFO Agent координирует финансовую часть due diligence

## Stage 6 — Audit

**Function:** STR-MNA-002 M&A Target Screening Review
**Owner:** AG003 AI Auditor
**Decision Level:** L4

Действия:
1. Зафиксировать процесс отбора цели для последующего аудита сделки
2. Проверить соответствие процесса screening утверждённым критериям

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Зафиксировать критерии и процесс отбора для будущих M&A инициатив
2. При завершении сделки (успешной или нет) — задокументировать факторы
   успеха/провала

## KPIs

- Long-list to Short-list Conversion Rate
- Time to Initial Approach
- Strategic Fit Score точность (по итогам постфактум-анализа завершённых сделок)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (STR-MNA, STR-CAP, RSK-LEG)
- PB024_Market_Entry_Assessment.md (M&A как одна из стратегий входа)
- AGENT_REGISTRY.md (AG001, AG006, AG012, AG005)

> Примечание: полный due diligence и закрытие сделки M&A выходят за рамки
> стандартной Decision Architecture предприятия и ведутся как отдельный
> проект с участием людей и внешних советников — данный playbook покрывает
> только этап до формального due diligence.
