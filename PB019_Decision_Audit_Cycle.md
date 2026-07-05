# PB019 Decision Audit Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C15 Governance
Related Functions: GOV-AUD-001, GOV-AUD-002, GOV-DEC-001
Owner Agent: AG003 AI Auditor
Escalation Path: AG003 → AG002 Chief Orchestrator → AG001 CEO Agent
(при выявлении системных нарушений)

## Purpose

Playbook описывает регулярный аудит принятых решений во всех доменах —
проверку того, что решения принимались агентами в рамках их полномочий
(Decision Level) и с соблюдением Decision Architecture.

## Trigger Conditions

- Плановый ежемесячный выборочный аудит решений
- Решение с Decision Level L4-L5 (всегда проверяется индивидуально)
- Жалоба или несоответствие, выявленное в другом playbook

## Stage 1 — Idea (Decision Log Collection)

**Function:** GOV-DEC-001 Decision Log Maintenance
**Owner:** AG079 Audit Manager
**Decision Level:** L2

Действия:
1. Собрать журнал решений за период из всех доменов (каждое решение должно
   быть залогировано согласно Decision Architecture: Idea → Analysis →
   Risk Review → Decision → Execution → Audit → Knowledge Capture)
2. Отфильтровать решения для проверки: 100% решений L4-L5, выборка (10-20%)
   решений L2-L3

## Stage 2 — Analysis (Compliance Check)

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить, что решение принято агентом с соответствующим Decision Level
   (см. AGENT_REGISTRY.md)
2. Проверить, что решение прошло все обязательные стадии (включая Human
   Override там, где требуется)
3. Проверить обоснованность решения относительно доступной на тот момент
   информации

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager (при выявлении потенциального нарушения)
**Decision Level:** L3

Действия:
1. Для решений с найденными несоответствиями — оценить фактические
   последствия (было ли решение по сути верным, несмотря на процессное
   нарушение)

## Stage 4 — Decision (Finding Classification)

**Owner:** AG003 AI Auditor (AG002 Chief Orchestrator — для системных находок)
**Decision Level:** L3

Классификация находок:
- **Compliant** — решение соответствует Governance Model
- **Minor Deviation** — процессное отклонение без материальных последствий
- **Major Violation** — превышение полномочий или пропуск обязательного
  Human Override

## Stage 5 — Execution (Remediation)

**Owner:** зависит от находки — AG057 Agent Registry Manager (для системных
проблем полномочий) или владелец домена (для единичных случаев)
**Decision Level:** L2-L3

Действия:
1. Для Major Violation — немедленная эскалация к AG001 CEO Agent
2. Для Minor Deviation — уведомление владельца агента, корректировка процесса
3. Обновить GOV-AUT-001 Authority Matrix при выявлении системных пробелов

## Stage 6 — Audit (Meta-Audit)

**Function:** GOV-CTL-001 Enterprise Control Testing
**Owner:** AG003 AI Auditor
**Decision Level:** L4

Действия:
1. Периодически (ежегодно) проверять эффективность самого процесса аудита
2. Убедиться, что выборка решений репрезентативна и находки действительно
   приводят к исправлениям

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать паттерны нарушений по доменам/агентам
2. Обновить GOVERNANCE_MODEL.md при выявлении неоднозначностей в определении
   Decision Level

## KPIs

- Audit Coverage (% решений L4-L5, проверенных за период — целевое значение 100%)
- Violation Rate (% решений с находками Major Violation)
- Time to Remediate Major Violation

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (GOV-AUD, GOV-DEC, GOV-CTL, GOV-AUT)
- GOVERNANCE_MODEL.md (Decision Architecture, Audit Framework, п.10)
- AGENT_REGISTRY.md (AG003, AG079, AG005, AG057)
