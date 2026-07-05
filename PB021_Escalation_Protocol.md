# PB021 Escalation Handling Protocol

Version: 1.0
Status: Active Playbook
Related Capability: C15 Governance
Related Functions: GOV-ORC-003, GOV-AUT-001
Owner Agent: AG002 Chief Orchestrator
Escalation Path: определяется динамически по Escalation Framework (E0-E5)

## Purpose

Мета-playbook, описывающий сам механизм эскалации — как любой агент должен
передавать вопрос выше по иерархии, когда он выходит за пределы его Decision
Level. Все остальные playbooks в этом репозитории ссылаются на этот протокол
вместо того, чтобы каждый раз описывать логику эскалации заново.

## Trigger Conditions

- Агент сталкивается с решением, требующим Decision Level выше его
  собственного
- Риск-рейтинг ситуации превышает порог, установленный для текущего
  Decision Level
- Два агента с равным уровнем полномочий не могут прийти к согласию

## Stage 1 — Idea (Escalation Trigger Detection)

**Owner:** инициирующий агент (любой из 84)
**Decision Level:** соответствует уровню агента

Действия:
1. Агент распознаёт, что задача превышает его Decision Level (см.
   AGENT_REGISTRY.md для собственного уровня)
2. Формирует пакет эскалации: контекст, что уже сделано, что требуется решить

## Stage 2 — Analysis (Routing)

**Function:** GOV-ORC-003 Escalation Management
**Owner:** AG002 Chief Orchestrator
**Decision Level:** L4

Действия:
1. Определить корректного получателя эскалации по Reports To цепочке
   агента (AGENT_REGISTRY.md)
2. Проверить, не является ли ситуация кросс-доменной (требует нескольких
   владельцев одновременно — например, финансовый + юридический риск)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager (при эскалациях, связанных с риском)
**Decision Level:** соответствует серьёзности ситуации

Действия:
1. Для эскалаций с потенциальным риском "High"/"Critical" — параллельное
   уведомление AG005, независимо от основного маршрута
2. Определить, требуется ли Human Override (см. GOVERNANCE_MODEL.md п.9)

## Stage 4 — Decision (Resolution at Escalated Level)

**Owner:** получатель эскалации (определяется на Stage 2)
**Decision Level:** соответствует уровню получателя (L3-L5)

Критерии для дальнейшей эскалации (эскалация "вверх по цепочке"):
- Получатель также не обладает достаточным Decision Level
- Ситуация требует Human Override, а получатель — не человек и не AG001

## Stage 5 — Execution (Communication Back)

**Owner:** AG002 Chief Orchestrator
**Decision Level:** L2

Действия:
1. Довести решение обратно до инициирующего агента
2. Разблокировать приостановленный процесс/playbook для продолжения

## Stage 6 — Audit

**Function:** GOV-DEC-001 Decision Log Maintenance
**Owner:** AG079 Audit Manager
**Decision Level:** L2

Действия:
1. Зафиксировать эскалацию в Decision Log: инициатор, получатель, время
   разрешения, итоговое решение
2. Отслеживать среднее время разрешения эскалаций по типу (E0-E5)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. При повторяющихся эскалациях одного типа — рассмотреть расширение
   Decision Level инициирующего агента (см. PB018 Agent Performance Review)
   вместо постоянной ручной эскалации
2. Обновить Authority Matrix (GOV-AUT-001) при выявлении системных пробелов
   в распределении полномочий

## KPIs

- Escalation Volume по уровням (E0-E5) — рост E4-E5 требует внимания
- Time to Resolution по типу эскалации
- Re-escalation Rate (эскалации, которые пришлось поднимать выше первого
  получателя)

## Related Documents

- GOVERNANCE_MODEL.md (Escalation Framework, Decision Levels, п.6-7)
- ENTERPRISE_FUNCTION_REGISTRY.md (GOV-ORC-003, GOV-AUT-001, GOV-DEC-001)
- Все остальные playbooks в репозитории ссылаются на этот протокол для
  описания шагов эскалации
- AGENT_REGISTRY.md (Reports To — основа маршрутизации)
