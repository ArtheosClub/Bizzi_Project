# PB050 Litigation Case Management

Version: 1.0
Status: Active Playbook
Related Capability: C10 Legal & Compliance
Related Functions: LEG-LIT-001, LEG-LIT-002
Owner Agent: AG017 Legal Counsel
Escalation Path: AG017 → AG001 CEO Agent → Human Board (для существенных
исков)

## Purpose

Playbook описывает управление судебными и претензионными делами — от
получения претензии/иска до разрешения, с учётом того, что фактическое
судебное представительство ведётся внешними юристами, а роль внутренних
агентов — координация и управление информацией.

## Trigger Conditions

- Получена претензия или судебный иск (входящий)
- Решение об инициировании иска компанией (исходящий, реже)

## Stage 1 — Idea (Case Intake)

**Owner:** AG017 Legal Counsel
**Decision Level:** L3

Действия:
1. Зафиксировать претензию/иск с ключевыми деталями (стороны, предмет,
   сумма требований, сроки ответа)
2. Определить связанные внутренние документы (контракт — PB013, инцидент —
   PB016, если применимо)

## Stage 2 — Analysis (Case Assessment)

**Function:** LEG-LIT-001 Litigation Case Tracking
**Owner:** AG017 Legal Counsel
**Decision Level:** L4

Действия:
1. Оценить обоснованность претензии/иска
2. Оценить потенциальный финансовый и репутационный ущерб (RSK-LEG-001,
   RSK-REP-001)
3. Определить необходимость привлечения внешних юристов

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L4

Действия:
1. Оценить вероятность неблагоприятного исхода и диапазон возможного
   ущерба
2. Проверить наличие страхового покрытия для данного типа риска

## Stage 4 — Decision (Strategy Approval)

**Owner:** AG001 CEO Agent (Human Board — для исков с существенной суммой
требований)
**Decision Level:** L5

Варианты стратегии:
- Settle — досудебное урегулирование
- Defend — судебная защита
- Counter-claim — встречный иск (для исходящих ситуаций)

**Human Override:** обязателен — судебные споры относятся к решениям,
требующим прямого утверждения человеком ввиду финансовых и репутационных
последствий.

## Stage 5 — Execution (Case Management)

**Owner:** AG017 Legal Counsel (координация с внешними юристами)
**Decision Level:** L2 (в рамках утверждённого на Stage 4 мандата)

Действия:
1. Координировать сбор документов и данных, запрашиваемых в рамках
   разбирательства
2. Регулярно информировать AG001 CEO Agent о статусе дела
3. При необходимости — привлечь AG012 CFO Agent для финансового
   резервирования (provisions)

## Stage 6 — Audit

**Function:** LEG-LIT-002 Litigation Case Tracking Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L4

Действия:
1. После завершения дела — задокументировать итог и фактические затраты
   против первоначальной оценки
2. Проверить, соответствовал ли процесс управления делом установленной
   стратегии

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Зафиксировать первопричину спора (например, неясная формулировка в
   типовом контракте — обратная связь в PB013_Contract_Review_Approval.md)
2. Обновить шаблоны контрактов/процессов для предотвращения аналогичных
   споров в будущем

## KPIs

- Case Resolution Time
- Settlement vs Litigation Cost Ratio
- Recurring Dispute Rate (споры с одинаковой первопричиной)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (LEG-LIT, RSK-LEG, RSK-REP)
- PB013_Contract_Review_Approval.md (частый источник первопричины спора)
- PB016_Cyber_Incident_Response.md (источник для исков, связанных с утечками данных)
- AGENT_REGISTRY.md (AG017, AG001, AG005, AG012)

> Примечание: фактическое судебное представительство ведётся внешними
> юристами вне рамок Decision Architecture предприятия — данный playbook
> покрывает внутреннюю координацию и управление информацией по делу.
