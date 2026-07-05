# PLAYBOOK_TEMPLATE.md

Используйте эту структуру для каждого нового playbook. Она обеспечивает
согласованность и совместимость с Governance Model и Agent Registry.

---

# PBxxx <Название Playbook>

Version: 1.0
Status: Draft | Active Playbook
Related Capability: <Cxx Domain Name>
Related Functions: <Function ID список>
Owner Agent: <Agent ID и имя из AGENT_REGISTRY.md>
Escalation Path: <Owner> → <следующий уровень> → ... (по Escalation Framework)

## Purpose
Краткое описание, зачем нужен этот playbook и какую проблему решает.

## Trigger Conditions
Список событий/условий, запускающих playbook.

## Stage 1 — Idea
**Function:** <Function ID>
**Owner:** <Agent ID>
**Decision Level:** <L0-L5>
Действия (нумерованный список)
**Output:** что получается на выходе стадии

## Stage 2 — Analysis
(аналогично)

## Stage 3 — Risk Review
**Function:** обычно RSK-* функция
**Owner:** AG005 Risk Manager (или домен-специфичный)
Действия + критерий эскалации

## Stage 4 — Decision
**Owner:** <Agent ID, соответствующий Decision Level>
Критерии принятия решения (список условий Approve/Reject)
**Human Override:** указать, обязателен ли (для L4-L5 решений — как правило да)

## Stage 5 — Execution
**Function:** <Function ID>
**Owner:** <Agent ID>
Действия по выполнению

## Stage 6 — Audit
**Function:** обычно GOV-AUD-001 или GOV-AUD-002
**Owner:** AG003 AI Auditor
Что проверяется постфактум

## Stage 7 — Knowledge Capture
**Function:** KNW-LES-001 (или другая KNW-* функция)
**Owner:** AG026 Knowledge Manager
Что фиксируется в базе знаний

## KPIs
Список из 2-4 измеримых метрик успеха playbook'а

## Related Documents
Ссылки на связанные Function Registry записи, другие playbooks, Agent Registry
