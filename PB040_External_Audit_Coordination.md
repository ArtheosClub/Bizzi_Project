# PB040 External Audit Coordination

Version: 1.0
Status: Active Playbook
Related Capability: C09 Finance
Related Functions: FIN-AUD-001, FIN-AUD-001-002
Owner Agent: AG012 CFO Agent
Escalation Path: AG012 → AG001 CEO Agent (для существенных находок аудита)

## Purpose

Playbook описывает координацию годового внешнего финансового аудита —
от подготовки документов до закрытия рекомендаций аудитора.

## Trigger Conditions

- Плановый годовой внешний аудит
- Аудит, требуемый инвестором/грантодателем (см. FIN-GRA-004 Grant Reporting)

## Stage 1 — Idea (Audit Scope & Timeline)

**Owner:** AG012 CFO Agent
**Decision Level:** L3

Действия:
1. Согласовать с внешним аудитором объём и сроки проверки
2. Сформировать список требуемых документов (PBC list — prepared-by-client)

## Stage 2 — Analysis (Documentation Preparation)

**Function:** FIN-AUD-001 External Audit Coordination
**Owner:** AG013 Accounting Agent
**Decision Level:** L2

Действия:
1. Собрать финансовую отчётность за период (12 месяцев из PB008)
2. Подготовить подтверждающие документы (контракты — PB013, договоры
   с поставщиками — PB009, налоговые декларации — PB039)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Провести внутреннюю предварительную проверку на предмет очевидных
   несоответствий до начала внешнего аудита
2. Оценить риск существенных находок по проблемным областям (если известны
   заранее)

## Stage 4 — Decision (PBC Package Approval)

**Owner:** AG012 CFO Agent
**Decision Level:** L3

Критерии:
- Пакет документов полон и соответствует запросу аудитора
- Предварительная внутренняя проверка не выявила критичных проблем

## Stage 5 — Execution (Audit Fieldwork Support)

**Owner:** AG013 Accounting Agent
**Decision Level:** L2

Действия:
1. Обеспечивать оперативные ответы на запросы аудитора в ходе проверки
2. Координировать доступ аудитора к системам/данным через
   AG081 Authorization Manager

## Stage 6 — Audit (Findings Resolution)

**Function:** FIN-AUD-001-002 External Audit Coordination Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3 (L4 для существенных находок)

Действия:
1. Классифицировать находки аудитора по критичности
2. Разработать план устранения для каждой находки (аналогично PB014
   Compliance Monitoring)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать находки и их устранение для предотвращения повторения
2. Обновить внутренние процедуры контроля (SOP) при системных находках

## KPIs

- Audit Preparation Time
- Number of Material Findings
- Finding Remediation Time

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (FIN-AUD, GOV-AUD)
- PB008_Monthly_Financial_Close.md, PB039_Tax_Filing_Cycle.md (источники данных)
- PB014_Compliance_Monitoring.md (аналогичный процесс устранения находок)
- AGENT_REGISTRY.md (AG012, AG013, AG005, AG003)
