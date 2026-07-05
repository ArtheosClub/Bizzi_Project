# PB001 Grant Acquisition

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-GRA-001, FIN-GRA-002, FIN-GRA-003, FIN-GRA-004
Owner Agent: AG025 Grant & Funding Agent
Escalation Path: AG025 → AG014 Finance Manager → AG001 CEO Agent (per Decision Architecture)

## Purpose

Playbook описывает полный жизненный цикл поиска, подачи заявки и отчётности
по грантам для цифрового предприятия. Следует Decision Architecture из
GOVERNANCE_MODEL.md: Idea → Analysis → Risk Review → Decision → Execution →
Audit → Knowledge Capture.

## Trigger Conditions

- Плановый ежеквартальный поиск грантов (STR-PLN-002 Quarterly Strategic Review)
- Ручной запрос от CEO Agent (AG001) или Business Analyst (AG004)
- Уведомление о новой грантовой программе от внешнего источника (RSS/API интеграция — TEC003)

## Stage 1 — Idea (Grant Discovery)

**Function:** FIN-GRA-001 Grant Discovery
**Owner:** AG025 Grant & Funding Agent
**Decision Level:** L1 (автономно)

Действия:
1. Сканировать источники грантовых программ (государственные, отраслевые, международные)
2. Отфильтровать по критериям: размер компании, отрасль, география, стадия проекта
3. Составить short-list из 3–5 наиболее релевантных программ
4. Передать short-list на этап Analysis

**Output:** Grant Shortlist (structured record: Grant ID, Name, Amount, Deadline, Source)

## Stage 2 — Analysis (Eligibility Review)

**Function:** FIN-GRA-002 Grant Eligibility Review
**Owner:** AG025 Grant & Funding Agent
**Decision Level:** L2 (требует подтверждения AG014)

Действия:
1. Проверить формальные критерии допуска (юрлицо, отрасль, размер выручки, регион)
2. Оценить требуемые документы и трудозатраты на подготовку заявки
3. Рассчитать ROI: (потенциальная сумма гранта) / (трудозатраты на подготовку)
4. Передать в Risk Review, если сумма гранта > установленного порога (см. Escalation Framework)

**Output:** Eligibility Report + Effort Estimate

## Stage 3 — Risk Review

**Function:** RSK-ERM-002 Risk Assessment
**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить репутационные и юридические риски (условия гранта, отчётные обязательства)
2. Проверить конфликт интересов и compliance-ограничения (LEG-CON программы)
3. Вынести рекомендацию: Proceed / Proceed with conditions / Reject

**Escalation:** при RSK rating "High" — эскалация к AG001 CEO Agent (E4)

## Stage 4 — Decision

**Owner:** AG014 Finance Manager (или AG001 CEO Agent при высокой сумме/риске)
**Decision Level:** L3–L4 в зависимости от суммы

Критерии принятия решения:
- ROI выше порогового значения
- Risk rating не выше "Medium" (либо одобрено CEO при "High")
- Трудозатраты на подготовку заявки согласованы с доступными ресурсами команды

**Human Override:** обязателен для грантов, требующих юридических обязательств
свыше установленного лимита (см. GOVERNANCE_MODEL.md, п.9 Human Override).

## Stage 5 — Execution (Application Preparation)

**Function:** FIN-GRA-003 Grant Application Preparation
**Owner:** AG025 Grant & Funding Agent
**Decision Level:** L2

Действия:
1. Собрать необходимые документы (финансовая отчётность, бизнес-план, устав)
2. Подготовить нарратив заявки, привязанный к Vision и Strategy (STR-PLN-001)
3. Направить черновик на ревью Legal (LEG-CON-002) при наличии договорных условий
4. Подать заявку через официальный канал программы
5. Зафиксировать дедлайны последующей отчётности

**Output:** Submitted Application + Confirmation Receipt

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить, что все этапы (Idea → Decision → Execution) задокументированы
2. Сверить фактические трудозатраты с оценкой из Stage 2
3. Зафиксировать Decision ID, Owner, Risk Rating, Audit Score в Audit Framework

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG026 Knowledge Manager
**Decision Level:** L1

Действия:
1. Зафиксировать исход заявки (одобрено/отклонено) и причины
2. Обновить Knowledge Base шаблонами успешных нарративов
3. При одобрении гранта — передать в FIN-GRA-004 Grant Reporting для дальнейшего
   сопровождения отчётности перед грантодателем

## Post-Award: Grant Reporting

**Function:** FIN-GRA-004 Grant Reporting
**Owner:** AG025 Grant & Funding Agent
**Decision Level:** L2

Периодическая отчётность перед грантодателем по установленному графику;
эскалация к AG014 при отклонениях от заявленного плана использования средств.

## KPIs

- Grant Discovery Rate: количество релевантных грантов, найденных за квартал
- Application Success Rate: % одобренных заявок от поданных
- Time to Submit: среднее время от Discovery до Submission
- ROI Realized: фактическая сумма полученных грантов / затраченные часы

## Related Documents

- CAPABILITY_MAP_v1.0.md (C09 Finance)
- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-GRA-001..004)
- GOVERNANCE_MODEL.md (Decision Architecture, Escalation Framework)
- AGENT_REGISTRY.md (AG025, AG014, AG005, AG003, AG026)
