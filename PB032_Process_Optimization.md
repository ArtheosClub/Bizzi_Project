# PB032 Process Optimization Review

Version: 1.1
Status: Active Playbook
Related Capability: C07 Operations
Related Functions: OPS-PRO-002, OPS-IMP-001, OPS-IMP-002, OPS-COS-001, OPS-PER-001
Owner Agent: AG047 Process Controller
Escalation Path: AG047 Process Controller → AG007 Operations Manager → AG002 Chief Orchestrator
(для изменений, затрагивающих несколько доменов, полномочия агентов или operating model)

---

## Purpose

Playbook описывает управляемый цикл выявления, анализа, утверждения, внедрения
и проверки улучшений операционных процессов.

PB032 нужен для того, чтобы оптимизация процессов не превращалась в хаотичное
"улучшательство", а проходила через измеримый контур:

Signal → Diagnosis → Redesign → Risk Review → Decision → Rollout → Audit → Knowledge Capture

Playbook применяется как реактивно — по итогам PB031 Quality Audit Cycle, жалоб,
ошибок, задержек и роста затрат, так и проактивно — через регулярный анализ
операционной эффективности.

Главный принцип PB032:

> Процесс можно менять только тогда, когда понятны причина, ожидаемый эффект,
> риски перехода, владелец изменения и способ проверки результата.

---

## Scope

PB032 покрывает:

- Улучшение существующих операционных процессов
- Сокращение времени цикла
- Снижение операционных затрат
- Уменьшение ошибок, переделок и ручных действий
- Устранение повторяющихся проблем качества
- Упрощение workflow между агентами
- Обновление SOP после изменения процесса
- Проверку фактического эффекта после внедрения

PB032 не покрывает:

- Создание нового продукта или MVP — см. PB023 Idea-to-MVP Pipeline
- Изменение состава агентов — см. PB020 Agent Lifecycle
- Кризисное управление — см. PB017 Crisis Management Activation
- Технический deployment программных систем — см. PB036/PB038
- Исправление единичной ошибки без системной причины — обрабатывается в доменном процессе

---

## Trigger Conditions

Playbook запускается при одном или нескольких условиях:

- Системная проблема, выявленная в PB031 Quality Audit Cycle
- Повторяющаяся ошибка в одном и том же процессе
- Плановый ежеквартальный process review
- Рост стоимости операций — OPS-COS-001 Cost Optimization Review
- Ухудшение операционных KPI — OPS-PER-001 Operational KPI Monitoring
- Увеличение cycle time, backlog, delay или rework
- Жалобы клиентов, указывающие на процессную причину
- Конфликт между агентами из-за неясного workflow
- Ручная операция, которую можно стандартизировать или автоматизировать
- Появление нового инструмента, делающего старый процесс неэффективным

---

## Inputs

Для запуска PB032 должны быть собраны доступные входные данные:

- Описание текущего процесса / SOP
- Метрики процесса: cycle time, cost, error rate, backlog, throughput
- Источник сигнала: аудит, KPI, жалоба, инцидент, наблюдение агента
- Список затронутых агентов и функций
- Текущие ограничения: legal, compliance, budget, capacity, technology
- Предварительная гипотеза проблемы
- История предыдущих изменений этого процесса

Если входных данных недостаточно, AG047 фиксирует это как Discovery Gap и
проводит короткий сбор фактов до перехода к Stage 2.

---

## Outputs

Результатом PB032 должны быть:

- Process Optimization Brief
- Root Cause Analysis
- Proposed Future-State Process
- Impact & Risk Assessment
- Decision Record
- Rollout Plan
- Updated SOP / workflow documentation
- Post-Implementation Audit Report
- Lessons Learned entry в Corporate Memory

---

## Roles & Responsibilities

| Role | Agent | Responsibility |
|---|---|---|
| Process Owner | AG047 Process Controller | Ведёт playbook, анализирует процесс, готовит redesign |
| Operations Approver | AG007 Operations Manager | Утверждает изменения внутри C07 Operations |
| Cross-Domain Coordinator | AG002 Chief Orchestrator | Утверждает/координирует изменения, затрагивающие несколько доменов |
| Risk Reviewer | AG005 Risk Manager | Проверяет transition risk, compliance risk, continuity risk |
| Auditor | AG003 AI Auditor | Проверяет фактический эффект и корректность decision trail |
| Knowledge Owner | AG053 Knowledge Curator | Обновляет SOP, lessons learned и process benchmark |
| Data Support | AG066 BI Analyst / AG067 Analytics Agent | Помогают с метриками, если требуется quantitative analysis |

---

## Stage 1 — Idea (Improvement Opportunity Identification)

**Function:** OPS-IMP-001 Improvement Initiative Tracking  
**Owner:** AG047 Process Controller  
**Decision Level:** L2

Действия:

1. Зафиксировать источник сигнала: audit finding, KPI deviation, complaint,
   cost increase, delay, manual bottleneck или agent conflict.
2. Описать текущий процесс в формате:
   - Trigger
   - Inputs
   - Steps
   - Owner agents
   - Outputs
   - Known pain points
3. Собрать первичные метрики: время, стоимость, ошибки, rework, SLA breaches.
4. Классифицировать инициативу:
   - Efficiency improvement
   - Quality improvement
   - Cost reduction
   - Control improvement
   - Automation candidate
   - Cross-domain workflow fix
5. Приоритизировать по трём параметрам:
   - Business impact
   - Urgency
   - Implementation complexity

**Output:** Improvement Opportunity Record

**Stage Gate:** переход к Stage 2 возможен, если проблема повторяется,
измерима или имеет значимый риск/стоимость для бизнеса.

---

## Stage 2 — Analysis (Root Cause & Redesign)

**Function:** OPS-PRO-002 Process Optimization  
**Owner:** AG047 Process Controller  
**Decision Level:** L2

Действия:

1. Провести root cause analysis:
   - 5 Whys
   - Process mapping
   - Bottleneck analysis
   - Failure mode review
   - Handoff analysis между агентами
2. Разделить симптомы и первопричины.
3. Построить Current-State Map.
4. Спроектировать Future-State Process.
5. Определить, какие элементы меняются:
   - sequence of steps
   - owner agent
   - decision level
   - data input/output
   - approval point
   - automation/tool usage
   - SOP / policy
6. Оценить ожидаемый эффект:
   - time saved
   - cost reduction
   - quality improvement
   - risk reduction
   - capacity increase
7. Проверить, не является ли изменение фактически изменением полномочий агента.
   Если да — инициировать связь с PB020 Agent Lifecycle.

**Output:** Root Cause Analysis + Proposed Future-State Process

**Stage Gate:** redesign не передаётся на решение, если не описаны baseline
metric, target metric и affected agents.

---

## Stage 3 — Risk Review

**Function:** RSK-OPS-001 Operational Risk Review (если отдельная функция не заведена — через AG005 Risk Manager)  
**Owner:** AG005 Risk Manager  
**Decision Level:** L2 / L3 для high-impact изменений

Действия:

1. Оценить transition risk: что может сломаться во время перехода.
2. Оценить continuity risk: сможет ли бизнес работать во время rollout.
3. Проверить compliance/legal ограничения.
4. Проверить governance conflict:
   - не меняется ли Decision Level без процедуры;
   - не передаётся ли агенту полномочие выше его уровня;
   - не исчезает ли контрольная точка audit или human override.
5. Определить rollback conditions.
6. Определить minimum safe pilot scope.

**Risk Rating:** Low / Medium / High / Critical

**Escalation Rules:**

- Low / Medium — остаётся у AG047 + AG007
- High — эскалация AG007 → AG002
- Critical — AG002 → AG001 CEO Agent / Human Board, если затронут L4-L5 контур

**Output:** Risk Review Note + Rollback Conditions

---

## Stage 4 — Decision (Redesign Approval)

**Owner:** AG007 Operations Manager  
**Secondary Owner:** AG002 Chief Orchestrator для cross-domain изменений  
**Decision Level:** L3

Критерии Approve:

- Проблема подтверждена данными или repeated pattern
- Root cause отделена от симптомов
- Предложенный future-state process описан достаточно чётко
- Есть baseline и target metric
- Затронутые агенты и функции перечислены
- Риски перехода оценены
- Rollback conditions определены
- SOP update включён в план

Критерии Reject / Rework:

- Нет измеримого эффекта
- Изменение решает симптом, но не причину
- Риск внедрения выше ожидаемого эффекта
- Изменение ломает Governance Model
- Неясен владелец будущего процесса

**Human Override:** не обязателен для L2-L3 process optimization. Обязателен,
если изменение затрагивает стратегические полномочия, юридические обязательства,
финансовый лимит L4-L5 или Human Board control point.

**Output:** Decision Record

---

## Stage 5 — Execution (Pilot & Rollout)

**Function:** OPS-IMP-001 Improvement Initiative Tracking  
**Owner:** AG047 Process Controller  
**Decision Level:** L2

Действия:

1. Подготовить Rollout Plan:
   - pilot scope
   - owner
   - start/end date
   - success metric
   - rollback condition
   - affected SOPs
2. Провести пилот на минимальном безопасном участке процесса.
3. Отслеживать pilot metrics ежедневно/еженедельно — в зависимости от процесса.
4. Собрать feedback от затронутых агентов.
5. Исправить workflow до масштабирования.
6. Внедрить изменение полностью после подтверждения pilot success.
7. Обновить SOP (KNW-SOP-001) и уведомить затронутых агентов через AG002 Chief Orchestrator.
8. Зафиксировать дату вступления нового процесса в силу.

**Output:** Rollout Completion Note + Updated SOP

---

## Stage 6 — Audit

**Function:** OPS-IMP-002 Improvement Initiative Tracking Exception Handling  
**Owner:** AG003 AI Auditor  
**Decision Level:** L2

Действия:

1. Сравнить фактический эффект с прогнозом Stage 2.
2. Проверить, были ли сохранены control points.
3. Проверить, не появились ли новые риски или скрытые издержки.
4. Проверить, обновлены ли SOP и knowledge base.
5. Зафиксировать один из audit outcomes:
   - Effective — target achieved
   - Partially Effective — target partly achieved, follow-up required
   - Ineffective — rollback or redesign required
   - Harmful — immediate escalation required
6. При отклонении более 25% от expected benefit инициировать rework loop к Stage 2.

**Output:** Post-Implementation Audit Report

---

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture  
**Owner:** AG053 Knowledge Curator  
**Decision Level:** L1

Действия:

1. Задокументировать:
   - исходную проблему;
   - первопричину;
   - принятое изменение;
   - эффект;
   - ошибки внедрения;
   - reusable pattern.
2. Обновить process benchmark.
3. Обновить SOP и cross-links на связанные playbooks.
4. Добавить reusable optimization pattern в Corporate Memory.
5. Если изменение может быть применено в других доменах — создать recommendation для AG002.

**Output:** Lessons Learned Entry + Updated Process Benchmark

---

## Decision Levels

| Situation | Decision Level | Owner |
|---|---:|---|
| Minor step improvement внутри одного процесса | L2 | AG047 |
| Существенное изменение workflow внутри Operations | L3 | AG007 |
| Cross-domain process change | L3/L4 | AG002 |
| Изменение полномочий агента | по PB020 | AG002 / AG057 |
| Изменение, затрагивающее стратегию, legal exposure или major finance | L4/L5 | AG001 / Human Board |

---

## Escalation Criteria

Эскалация обязательна, если:

- Изменение затрагивает более одного Capability домена
- Меняется владелец функции или Decision Level
- Удаляется контрольная точка audit, risk review или approval
- Есть риск остановки критического процесса
- Ожидаемый financial impact превышает лимит L3
- Возникает конфликт между агентами-владельцами
- Pilot показывает ухудшение ключевой метрики
- Аудит классифицирует outcome как Harmful

---

## Control Points

| Control Point | Stage | Owner | Purpose |
|---|---|---|---|
| Baseline Metric Captured | Stage 1 | AG047 | Нельзя улучшать то, что не измерено |
| Root Cause Confirmed | Stage 2 | AG047 | Не лечить симптомы |
| Risk Review Completed | Stage 3 | AG005 | Защитить continuity и governance |
| Decision Record Created | Stage 4 | AG007/AG002 | Зафиксировать ответственность |
| Pilot Completed | Stage 5 | AG047 | Проверить изменение безопасно |
| Post-Implementation Audit | Stage 6 | AG003 | Подтвердить эффект |
| SOP Updated | Stage 7 | AG053 | Закрепить изменение в системе знаний |

---

## Anti-Patterns

PB032 должен предотвращать следующие ошибки:

- "Автоматизировать хаос" — автоматизация плохого процесса без redesign
- "Лечить симптом" — изменение шага без анализа первопричины
- "Срезать контроль" — ускорение за счёт удаления risk/audit gates
- "Оптимизация ради оптимизации" — отсутствие измеримого business impact
- "Silent rollout" — изменение процесса без уведомления затронутых агентов
- "Permanent pilot" — пилот без решения о масштабировании или закрытии
- "Metric gaming" — улучшение одной метрики с ухудшением другой
- "Ownerless process" — новый workflow без назначенного владельца

---

## KPIs

Primary KPIs:

- Process Cycle Time Reduction
- Improvement Initiative Success Rate (% инициатив, достигших target effect)
- Time from Identification to Rollout
- Cost per Process Instance Reduction

Quality & Control KPIs:

- Repeat Issue Rate after Optimization
- Rework Rate
- SOP Update Completion Rate
- Audit Confirmation Rate

Governance KPIs:

- % changes with complete Decision Record
- % cross-domain changes escalated correctly
- % initiatives with captured baseline and target metric

---

## Minimal Process Optimization Brief

Каждая инициатива PB032 должна иметь краткую карточку:

```markdown
# Process Optimization Brief

Process:
Owner Agent:
Trigger Source:
Current Pain:
Baseline Metric:
Root Cause:
Proposed Change:
Affected Agents:
Expected Effect:
Risk Rating:
Pilot Scope:
Success Metric:
Rollback Condition:
Decision Owner:
SOP Update Required: Yes/No
```

---

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (OPS-PRO, OPS-IMP, OPS-COS, OPS-PER, KNW-SOP)
- AGENT_REGISTRY.md (AG047, AG007, AG005, AG003, AG002, AG053)
- GOVERNANCE_MODEL.md (Decision Architecture, escalation, human override)
- PB020_Agent_Lifecycle.md (если изменение требует изменения полномочий агента)
- PB021_Escalation_Handling_Protocol.md (если возникает конфликт или high-risk change)
- PB031_Quality_Audit_Cycle.md (частый источник инициатив)
- PB036_System_Integration_Rollout.md (если процессное изменение требует системной интеграции)
- PB038_Deployment_Pipeline_Health_Check.md (если изменение связано с technical deployment)

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | Initial | Базовый playbook оптимизации процессов |
| 1.1 | 2026-07-08 | Усилен полный контур: scope, inputs/outputs, роли, stage gates, escalation, control points, anti-patterns, expanded KPIs |
