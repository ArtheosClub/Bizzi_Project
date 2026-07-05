# PB044 Talent Review & Succession Planning

Version: 1.0
Status: Active Playbook
Related Capability: C12 People Management
Related Functions: PEO-TAL-001, PEO-SUC-001, PEO-SUC-001-002
Owner Agent: AG021 HR Manager
Escalation Path: AG021 → AG001 CEO Agent → Human Board (для succession
на позиции C-level)

## Purpose

Playbook описывает ежегодную оценку талантов и планирование преемственности
для ключевых позиций — снижение риска зависимости от конкретных людей
(в том числе людей-руководителей доменов, курирующих AI-агентов).

## Trigger Conditions

- Плановый ежегодный talent review
- Незапланированный уход ключевого сотрудника (реактивный триггер)

## Stage 1 — Idea (Talent Pool Assessment)

**Function:** PEO-TAL-001 Talent Review Cycle
**Owner:** AG021 HR Manager
**Decision Level:** L2

Действия:
1. Собрать данные по производительности (PEO-PER-001) и потенциалу
   сотрудников
2. Построить 9-box grid (performance × potential) для ключевых ролей

## Stage 2 — Analysis (Critical Role Identification)

**Owner:** AG021 HR Manager
**Decision Level:** L3

Действия:
1. Определить критичные позиции (высокий риск при уходе — C-level,
   уникальная экспертиза)
2. Для каждой критичной позиции — определить готовность потенциальных
   преемников (Ready Now / 1-2 года / 3+ года)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить риск отсутствия преемника для каждой критичной позиции
2. Приоритизировать позиции без готового преемника как "Critical Gap"

## Stage 4 — Decision (Succession Plan Approval)

**Function:** PEO-SUC-001 Succession Plan Review
**Owner:** AG001 CEO Agent (Human Board — для позиции CEO)
**Decision Level:** L4

Критерии:
- Каждая критичная позиция имеет хотя бы одного преемника в горизонте
  3 лет
- План развития преемников конкретен и измерим

## Stage 5 — Execution (Development Plan Implementation)

**Owner:** AG023 Learning & Development Agent
**Decision Level:** L2

Действия:
1. Разработать индивидуальные планы развития для потенциальных преемников
   (PEO-LDR-001 Leadership Development Plan)
2. Обеспечить ротацию/расширение обязанностей для ускорения готовности

## Stage 6 — Audit

**Function:** PEO-SUC-001-002 Succession Plan Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить прогресс преемников против плана развития
2. Зафиксировать позиции, остающиеся "Critical Gap" более одного цикла

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать критичные знания уходящих ключевых сотрудников
   (Corporate Memory — KNW-MEM-001) до их ухода
2. Обновить критерии готовности преемников

## KPIs

- Succession Coverage Rate (% критичных позиций с готовым преемником)
- Internal Promotion Rate для критичных позиций
- Time to Fill критичной позиции при незапланированном уходе

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (PEO-TAL, PEO-SUC, PEO-LDR, KNW-MEM)
- PB045_Leadership_Development.md (реализация планов развития)
- AGENT_REGISTRY.md (AG021, AG005, AG023, AG001)
