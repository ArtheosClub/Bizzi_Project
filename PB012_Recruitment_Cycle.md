# PB012 Recruitment Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C12 People Management
Related Functions: PEO-REC-001, PEO-REC-002, PEO-WFP-001
Owner Agent: AG022 Recruiter
Escalation Path: AG022 → AG021 HR Manager → AG001 CEO Agent (для C-level позиций)

## Purpose

Playbook описывает цикл найма — от открытия позиции до принятия оффера
кандидатом, после чего управление передаётся в PB011_Employee_Onboarding.md.

## Trigger Conditions

- Утверждённая открытая позиция в headcount plan (PEO-WFP-001)
- Замена уволившегося сотрудника

## Stage 1 — Idea (Job Requisition)

**Function:** PEO-REC-001 Job Requisition
**Owner:** AG022 Recruiter
**Decision Level:** L2

Действия:
1. Получить заявку на позицию от руководителя департамента
2. Согласовать с AG021 HR Manager соответствие headcount plan и бюджету
   (PEO-WFP-001)
3. Подготовить описание вакансии и разместить на площадках

## Stage 2 — Analysis (Candidate Screening)

**Function:** PEO-REC-002 Candidate Screening
**Owner:** AG022 Recruiter
**Decision Level:** L1

Действия:
1. Собрать входящие отклики
2. Провести первичный скрининг по формальным критериям (опыт, навыки)
3. Сформировать short-list для интервью с руководителем

## Stage 3 — Risk Review

**Function:** LEG-KYC-001 KYC Verification (для ролей с расширенным доступом)
**Owner:** AG011 Compliance Agent
**Decision Level:** L2

Действия:
1. Для ролей, дающих доступ к финансам, данным клиентов или governance-функциям —
   предварительная проверка репутационных рисков
2. Для остальных ролей — этап пропускается

## Stage 4 — Decision (Offer Decision)

**Owner:** AG021 HR Manager (AG001 CEO Agent — для C-level и ролей уровня L4-L5)
**Decision Level:** L2 (L4 для руководящих позиций)

Критерии:
- Кандидат прошёл интервью с руководителем департамента
- Компенсация в рамках диапазона (PEO-COM-001 Compensation Benchmarking)
- Compliance check пройден (если применимо)

## Stage 5 — Execution (Offer & Negotiation)

**Owner:** AG022 Recruiter
**Decision Level:** L1

Действия:
1. Подготовить и направить оффер кандидату
2. Провести переговоры по условиям при необходимости
3. При принятии оффера — инициировать PB011_Employee_Onboarding.md

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить соответствие предложенной компенсации утверждённому диапазону
2. Зафиксировать длительность цикла найма для анализа эффективности

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать эффективные источники кандидатов по типам позиций
2. Обновить шаблоны описаний вакансий при необходимости

## KPIs

- Time to Fill: дни от Job Requisition до принятия оффера
- Offer Acceptance Rate
- Source Effectiveness (какие каналы дают лучших кандидатов)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (PEO-REC, PEO-WFP, PEO-COM)
- PB011_Employee_Onboarding.md (следующий этап)
- AGENT_REGISTRY.md (AG022, AG021, AG011, AG001)
