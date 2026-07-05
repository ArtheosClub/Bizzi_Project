# PB043 Compensation Benchmarking Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C12 People Management
Related Functions: PEO-COM-001, PEO-COM-002
Owner Agent: AG021 HR Manager
Escalation Path: AG021 → AG012 CFO Agent (влияние на бюджет) → AG001 CEO
Agent (для изменений компенсационной политики)

## Purpose

Playbook описывает периодическую сверку компенсаций компании с рынком
и корректировку диапазонов для обеспечения конкурентоспособности.

## Trigger Conditions

- Плановый ежегодный benchmarking цикл
- Рост текучести кадров, указывающий на неконкурентную компенсацию

## Stage 1 — Idea (Market Data Collection)

**Owner:** AG021 HR Manager
**Decision Level:** L2

Действия:
1. Собрать рыночные данные по компенсациям для каждой роли (внешние
   источники, отраслевые отчёты)
2. Сопоставить с текущими диапазонами компании

## Stage 2 — Analysis (Compensation Benchmarking)

**Function:** PEO-COM-001 Compensation Benchmarking
**Owner:** AG021 HR Manager
**Decision Level:** L3

Действия:
1. Рассчитать позиционирование компании относительно рынка (percentile)
   по каждой роли/уровню
2. Выявить роли с существенным отставанием от рынка

## Stage 3 — Risk Review

**Owner:** AG012 CFO Agent
**Decision Level:** L3

Действия:
1. Оценить финансовое влияние корректировки диапазонов на общий payroll
   бюджет (FIN-BUD-002)
2. Приоритизировать корректировки по риску удержания (retention risk)

## Stage 4 — Decision (Range Adjustment Approval)

**Owner:** AG001 CEO Agent (для изменения общей компенсационной политики)
**Decision Level:** L4

Критерии:
- Корректировки в рамках утверждённого бюджета
- Приоритет отдан ролям с наивысшим риском текучести

## Stage 5 — Execution (Rollout)

**Owner:** AG021 HR Manager
**Decision Level:** L2

Действия:
1. Обновить диапазоны компенсации в системах
2. Применить индивидуальные корректировки при следующем цикле
   PEO-PER-001 Performance Review Cycle
3. Использовать актуальные диапазоны в PB012_Recruitment_Cycle.md для
   новых офферов

## Stage 6 — Audit

**Function:** PEO-COM-002 Compensation Benchmarking Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить на внутреннюю справедливость (pay equity) — отсутствие
   необоснованных различий в оплате за аналогичные роли
2. Сверить фактические выплаты с обновлёнными диапазонами

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать корреляцию между компенсационными корректировками и
   изменением текучести кадров
2. Обновить источники рыночных данных при выявлении неточностей

## KPIs

- Compensation Competitiveness (% ролей на целевом percentile рынка)
- Voluntary Turnover Rate (до/после корректировки)
- Pay Equity Score

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (PEO-COM, PEO-PER, FIN-BUD)
- PB012_Recruitment_Cycle.md (применение актуальных диапазонов)
- AGENT_REGISTRY.md (AG021, AG012, AG001, AG003)
