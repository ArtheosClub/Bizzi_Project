# PB020 Agent Lifecycle (Onboarding / Retirement)

Version: 1.0
Status: Active Playbook
Related Capability: C15 Governance
Related Functions: GOV-LIF-001, GOV-LIF-001-002
Owner Agent: AG057 Agent Registry Manager
Escalation Path: AG057 → AG002 Chief Orchestrator → AG001 CEO Agent
(для новых доменов/существенных изменений структуры)

## Purpose

Playbook описывает добавление нового агента в AGENT_REGISTRY.md или вывод
существующего из эксплуатации — с сохранением целостности всех перекрёстных
ссылок (Function Registry, Governance Model, playbooks).

## Trigger Conditions

- Новая под-способность в Capability Map без владельца (как было с
  Market Intelligence и Administration — см. историю AGENT_REGISTRY.md)
- Решение о выводе агента (по итогам PB018 Agent Performance Review)
- Реорганизация департамента

## Stage 1 — Idea (Lifecycle Request)

**Owner:** AG057 Agent Registry Manager
**Decision Level:** L2

Действия:
1. Зафиксировать запрос: New Agent / Retire Agent / Merge Agents
2. Для New Agent — определить Capability домен, который останется без
   владельца, если агента не создать
3. Для Retire Agent — получить входные данные из PB018 (низкая
   производительность) или организационное решение

## Stage 2 — Analysis (Impact Assessment)

**Owner:** AG057 Agent Registry Manager
**Decision Level:** L3

Действия:
1. Для New Agent — определить Reports To, Decision Level, пересекающиеся
   функции с существующими агентами (избежать дублирования полномочий)
2. Для Retire Agent — найти все функции в ENTERPRISE_FUNCTION_REGISTRY.md,
   владельцем которых является агент, и определить нового владельца для
   каждой (по аналогии с переносом Market Intelligence на AG084)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить риск разрыва в покрытии функций на переходный период
2. Для Retire Agent — проверить, не остаётся ли Capability домен без
   владельца после вывода агента

## Stage 4 — Decision (Approval)

**Owner:** AG002 Chief Orchestrator (AG001 CEO Agent — для новых доменов
или структурных изменений уровня департамента)
**Decision Level:** L3 (L4 для структурных изменений)

Критерии:
- Ни один Capability домен и ни одна функция не остаются без владельца
- Reports To и Decision Level нового/изменённого агента непротиворечивы
  структуре AGENT_REGISTRY.md

## Stage 5 — Execution (Registry Update)

**Function:** GOV-LIF-001 Agent Onboarding/Retirement
**Owner:** AG057 Agent Registry Manager
**Decision Level:** L2

Действия:
1. Обновить AGENT_REGISTRY.md (добавить/удалить агента, обновить Reports To
   у затронутых агентов)
2. Обновить Owner-поля во всех затронутых функциях ENTERPRISE_FUNCTION_REGISTRY.md
3. Обновить ссылки на агента во всех playbooks, где он упоминается
4. Обновить GOVERNANCE_MODEL.md, если агент входит в Governance Core

## Stage 6 — Audit

**Function:** GOV-LIF-001-002 Agent Onboarding/Retirement Review
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить полноту обновления: ни одной "битой" ссылки на устаревший
   Agent ID не должно остаться ни в одном файле репозитория
2. Подтвердить, что все функции имеют действующего владельца

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать причину и процесс изменения в истории AGENT_REGISTRY.md
   (по аналогии с Changelog в других документах)
2. Обновить PLAYBOOK_TEMPLATE.md, если процесс выявил недостающие шаги

## KPIs

- Registry Consistency Rate (% функций с действующим, а не устаревшим владельцем)
- Time to Complete Lifecycle Change (от запроса до полного обновления всех файлов)
- Broken Reference Count после изменения (целевое значение — 0)

## Related Documents

- AGENT_REGISTRY.md (история изменений: добавление AG084, AG072-075→C16)
- ENTERPRISE_FUNCTION_REGISTRY.md (Owner-поля)
- PB018_Agent_Performance_Review.md (источник решений о retirement)
- CAPABILITY_MAP_v1.0.md (проверка покрытия доменов)
