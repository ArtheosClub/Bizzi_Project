# PB003 Customer Onboarding

Version: 1.0
Status: Active Playbook
Related Capability: C06 Customer Success
Related Functions: CUS-ONB-001, CUS-ONB-002, CUS-ADO-001, CUS-SPL-001
Owner Agent: AG011 Customer Success Manager
Escalation Path: AG011 → AG012 Operations Manager → AG002 Chief Orchestrator

## Purpose

Playbook описывает передачу клиента от Sales к Customer Success и доведение
его до состояния устойчивого использования продукта/услуги.

## Trigger Conditions

- Подписан контракт (SAL-CTR-001 Sales Contract Finalization завершён)
- Автоматическое уведомление из Sales pipeline о статусе "Closed Won"

## Stage 1 — Idea (Handoff Intake)

**Function:** CUS-ONB-001 Onboarding Plan Creation
**Owner:** AG011 Customer Success Manager
**Decision Level:** L2

Действия:
1. Получить от AG010 Sales Manager пакет передачи: контракт, ожидания клиента,
   ключевые заинтересованные лица
2. Проверить полноту данных (SAL-ACC-001 Key Account Review как источник)
3. Сформировать первичный Onboarding Plan с контрольными точками

**Output:** Onboarding Plan (сроки, ответственные, критерии успеха)

## Stage 2 — Analysis (Success Criteria Definition)

**Function:** CUS-SPL-001 Customer Success Plan
**Owner:** AG011 Customer Success Manager
**Decision Level:** L2

Действия:
1. Определить метрики успеха для конкретного клиента (что считается "успешным onboarding")
2. Согласовать План с клиентом (стартовая встреча)
3. Оценить риски срыва сроков (нехватка ресурсов, сложность интеграции)

## Stage 3 — Risk Review

**Function:** RSK-OPR-001 Operational Risk Assessment
**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Проверить, не превышает ли клиент текущую операционную ёмкость команды
   (см. OPS-RES-001 Resource Capacity Planning)
2. При высокой сложности — запросить дополнительные ресурсы у AG012

## Stage 4 — Decision (Onboarding Kickoff Approval)

**Owner:** AG011 Customer Success Manager
**Decision Level:** L2 (эскалация к AG012 при нехватке ресурсов — L3)

Критерии:
- Onboarding Plan согласован с клиентом
- Ресурсы подтверждены
- Риск-рейтинг не выше "Medium"

## Stage 5 — Execution (Onboarding Delivery)

**Function:** CUS-ONB-002 Onboarding Completion Tracking
**Owner:** AG011 Customer Success Manager
**Decision Level:** L1

Действия:
1. Выполнить шаги Onboarding Plan (настройка, обучение, интеграция)
2. Отслеживать прогресс по контрольным точкам
3. Параллельно отслеживать CUS-ADO-001 Feature Adoption Tracking —
   ранние признаки использования продукта клиентом

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить соответствие фактических сроков onboarding плановым
2. Зафиксировать причины отклонений (если есть)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG026 Knowledge Manager
**Decision Level:** L1

Действия:
1. Зафиксировать типовые препятствия onboarding для конкретного сегмента клиентов
2. Обновить шаблон Onboarding Plan при выявлении системных проблем
3. Передать клиента в постоянное сопровождение — переход к отслеживанию
   CUS-HLT-001 Customer Health Scoring и CUS-RET-001 Retention Risk Intervention

## KPIs

- Time to Value: время от подписания контракта до первого использования продукта
- Onboarding Completion Rate: % клиентов, завершивших план в срок
- Early Churn Rate: % клиентов, отменивших подписку в первые 90 дней

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (CUS-ONB, CUS-ADO, CUS-SPL, CUS-HLT, CUS-RET)
- PB004_Lead_to_Contract.md (предыдущий этап — передача из Sales)
- AGENT_REGISTRY.md (AG011, AG010, AG012, AG005)
