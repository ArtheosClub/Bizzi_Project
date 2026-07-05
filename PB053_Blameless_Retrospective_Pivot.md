# PB053 Blameless Retrospective & Pivot Engine

Version: 1.0
Status: Active Playbook — Flagship
Related Capability: C15 Governance / C14 Knowledge Management
Related Functions: GOV-RET-001, KNW-FAIL-001, STR-PIV-001, MRK-REC-001,
INN-MIS-001, GOV-LRN-001
Owner Agent: AG053 Knowledge Curator
Escalation Path: AG053 → AG002 Chief Orchestrator → AG001 CEO Agent
(для решений о пивоте)

## Purpose

Большинство компаний либо игнорируют неудачи (повторяют одну и ту же
ошибку в разных доменах), либо зацикливаются на поиске виноватого вместо
извлечения пользы. Этот playbook формализует третий путь: системное,
безоценочное (blameless) извлечение уроков из ЛЮБОЙ неудачи — провалившейся
кампании (PB029), потерянного клиента (PB005), неудачного MVP (PB023),
проигранной сделки (PB004) — с явной целью найти, какую возможность
открывает конкретная неудача, а не просто "закрыть инцидент".

## Trigger Conditions

- Любой playbook в репозитории завершился с результатом хуже ожидаемого
  (потеря клиента, провал кампании, неудачный запуск, проигранный тендер)
- Накопление похожих мелких неудач, указывающее на системный паттерн
  (KNW-FAIL-001)

## Stage 1 — Idea (Blameless Intake)

**Function:** GOV-RET-001 Blameless Retrospective Engine
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Зафиксировать неудачу с фактами, без указания "кто виноват" — фокус на
   "что произошло" и "какие условия это допустили"
2. Собрать данные от всех агентов/доменов, участвовавших в исходном
   playbook

## Stage 2 — Analysis (Pattern Matching)

**Function:** KNW-FAIL-001 Failure Pattern Library & Cross-Domain Matching
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Сверить с библиотекой ранее зафиксированных паттернов неудач — не
   повторяется ли это в третий раз в разных доменах под разными масками
2. Классифицировать первопричину: процессная, человеческая (в случае
   людей-сотрудников), внешняя (рыночная), архитектурная (пробел в
   Function Registry/Agent Registry)

## Stage 3 — Risk Review (Opportunity Scan)

**Function:** MRK-REC-001 Crisis-to-Opportunity Reframing (для
внешне-заметных неудач), INN-MIS-001 Mistake-Derived Innovation Capture
(для внутренних)
**Owner:** AG030 Marketing Manager / AG077 Innovation Manager (в зависимости
от типа)
**Decision Level:** L3

Действия:
1. Явно задать вопрос: "какую возможность открывает эта неудача?" —
   например, публичный провал конкурента в той же нише — это наш momentum;
   потеря клиента из-за отсутствия фичи — это valid product insight
2. Не ограничиваться "как не повторить" — искать "что теперь можно сделать,
   чего не могли раньше"

## Stage 4 — Decision (Response Classification)

**Owner:** AG002 Chief Orchestrator (AG001 CEO Agent — для решений уровня
пивота)
**Decision Level:** L3 (L4-L5 для пивота)

Варианты решения:
- **Fix & Continue** — устранить первопричину, процесс/продукт продолжается
  без изменений
- **Adjust** — скорректировать стратегию домена (новый playbook/функция)
- **Pivot** — STR-PIV-001 Pivot Decision Framework, для случаев, когда
  накопленные сигналы указывают на неверную базовую гипотезу, а не
  единичную ошибку исполнения

## Stage 5 — Execution

**Owner:** зависит от решения — владелец домена (Fix/Adjust) или AG001 CEO
Agent (Pivot)
**Decision Level:** L2-L5

Действия:
1. Для Fix — обновить SOP через PB047, обновить соответствующий playbook
2. Для Adjust — инициировать PB032 Process Optimization или новую функцию
   в Function Registry
3. Для Pivot — задействовать полную Decision Architecture стратегического
   уровня (аналогично PB024/PB026)

## Stage 6 — Audit

**Function:** GOV-LRN-001 Learning Velocity Tracking
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Измерить время от неудачи до внедрённого исправления/решения
   (Learning Velocity — ключевая метрика агрессивно растущей компании)
2. Проверить, действительно ли похожая неудача не повторилась в других
   доменах после обновления Pattern Library

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Обновить Failure Pattern Library новым паттерном (или подтверждением
   существующего)
2. Если неудача превратилась в реальную возможность (Stage 3) —
   задокументировать это как success story для внутренней культуры —
   ошибки становятся видимым источником побед, а не тем, что скрывают

## KPIs

- Learning Velocity (среднее время от неудачи до внедрённого исправления)
- Repeat Failure Rate (% неудач, повторяющих уже известный паттерн —
  должен снижаться со временем)
- Opportunity Conversion Rate (% неудач, из которых извлечена явная новая
  возможность, а не только "не повторять")

## Why This Playbook Matters

Скорость реакции на рынок (PB051) — это одна сторона агрессивного роста.
Другая — скорость обучения на собственных ошибках. Компании, которые
масштабируются быстро, не совершают меньше ошибок — они на порядок быстрее
извлекают из них пользу и на порядок реже повторяют одну и ту же ошибку
дважды. Blameless-подход — не про "мягкость", а про то, что поиск
виноватого замедляет как раз то самое обучение, ради которого затевается
разбор.

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (Adaptive Learning & Failure-to-Opportunity layer)
- PB051_Rapid_Market_Response.md (симметричный playbook — скорость реакции на рынок)
- PB024_Market_Entry_Assessment.md, PB026_MA_Target_Screening.md (куда ведёт Pivot)
- AGENT_REGISTRY.md (AG053, AG002, AG001, AG030, AG077, AG003)
