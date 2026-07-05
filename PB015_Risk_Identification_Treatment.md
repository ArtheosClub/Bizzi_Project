# PB015 Risk Identification & Treatment

Version: 1.0
Status: Active Playbook
Related Capability: C11 Risk Management
Related Functions: RSK-ERM-001, RSK-ERM-002, RSK-ERM-003
Owner Agent: AG005 Risk Manager
Escalation Path: AG005 → AG002 Chief Orchestrator → AG001 CEO Agent
(для рисков "High"/"Critical")

## Purpose

Playbook описывает сквозной цикл управления рисками предприятия — от
выявления до реализации плана обработки, применимый к любому типу риска
(финансовому, операционному, юридическому, киберрискам и др.).

## Trigger Conditions

- Плановый ежеквартальный risk review
- Сигнал из любого домена (например, RSK-CYB-001, SCM-SRK-001, RSK-FIN-001)
- Инцидент, выявивший ранее неучтённый риск

## Stage 1 — Idea (Risk Identification)

**Function:** RSK-ERM-001 Risk Identification
**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Собрать сигналы риска из доменных функций (Finance, Legal, Technology,
   Supply Chain и др.)
2. Зафиксировать риск в Risk Register с описанием и предполагаемым источником
3. Присвоить предварительную категорию (Strategic/Financial/Operational/
   Legal/Cyber/Reputation/Country — см. GOVERNANCE_MODEL.md п.11)

## Stage 2 — Analysis (Risk Assessment)

**Function:** RSK-ERM-002 Risk Assessment
**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить вероятность и потенциальное влияние (Impact × Likelihood)
2. Рассчитать риск-рейтинг (Low/Medium/High/Critical)
3. Определить владельца домена, к которому относится риск

## Stage 3 — Risk Review (Cross-Domain Validation)

**Owner:** AG005 Risk Manager (совместно с владельцем затронутого домена)
**Decision Level:** L3

Действия:
1. Подтвердить оценку с владельцем домена (например, AG012 CFO Agent для
   финансовых рисков, AG049 Information Security Agent для киберрисков)
2. Проверить, не пересекается ли риск с уже зарегистрированными

## Stage 4 — Decision (Treatment Strategy Approval)

**Owner:** AG005 Risk Manager (AG001 CEO Agent — для риска "High"/"Critical")
**Decision Level:** L3 (L4-L5 для критичных рисков)

Критерии выбора стратегии обработки:
- **Avoid** — прекратить деятельность, порождающую риск
- **Mitigate** — снизить вероятность/влияние
- **Transfer** — страхование, контрактные условия
- **Accept** — осознанное принятие при низком риск-рейтинге

**Human Override:** обязателен для рисков "Critical" (см. Human Sovereignty,
GOVERNANCE_MODEL.md п.9).

## Stage 5 — Execution (Treatment Plan Implementation)

**Function:** RSK-ERM-003 Risk Treatment Plan
**Owner:** владелец домена, где локализован риск
**Decision Level:** L2

Действия:
1. Реализовать выбранные меры (например, RSK-BCP-001 для непрерывности
   бизнеса, TEC-SEC-001 для кибербезопасности)
2. Назначить сроки и контрольные точки
3. AG005 Risk Manager отслеживает статус выполнения

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Проверить, что план обработки выполнен в срок
2. Переоценить риск-рейтинг после реализации мер (остаточный риск)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Обновить Risk Register с итоговым статусом (закрыт/остаточный риск принят)
2. Зафиксировать эффективные меры обработки для похожих будущих рисков

## KPIs

- Risk Register Coverage (% доменов с актуальной оценкой риска)
- Average Time to Treatment (от идентификации до реализации плана)
- Residual Risk Reduction (снижение риск-рейтинга после обработки)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (RSK-ERM, RSK-FIN, RSK-CYB, RSK-BCP)
- GOVERNANCE_MODEL.md (Risk Governance, п.11)
- PB016_Cyber_Incident_Response.md, PB017_Crisis_Management.md (специализированные подпроцессы)
- AGENT_REGISTRY.md (AG005, AG001, AG003)
