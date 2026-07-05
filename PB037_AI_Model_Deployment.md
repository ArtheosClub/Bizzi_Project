# PB037 AI Model Deployment & Retraining

Version: 1.0
Status: Active Playbook
Related Capability: C13 Technology
Related Functions: TEC-AIP-001, TEC-MLO-001, TEC-MLO-001-002
Owner Agent: AG056 AI Trainer
Escalation Path: AG056 → AG009 Enterprise Architect → AG003 AI Auditor
(для моделей, влияющих на Decision Level L3+)

## Purpose

Playbook описывает жизненный цикл AI/ML моделей, используемых агентами
предприятия — от развёртывания новой версии до планового переобучения
при деградации качества.

## Trigger Conditions

- Новая версия модели готова к развёртыванию
- Плановая проверка деградации модели (model drift)
- Существенное изменение входных данных, влияющих на релевантность модели

## Stage 1 — Idea (Model Readiness Check)

**Owner:** AG056 AI Trainer
**Decision Level:** L2

Действия:
1. Подтвердить, что новая модель прошла валидацию на тестовом наборе данных
2. Сравнить метрики новой модели с текущей production-версией

## Stage 2 — Analysis (Performance Evaluation)

**Function:** TEC-AIP-001 AI Model Performance Review
**Owner:** AG055 Model Evaluation Agent
**Decision Level:** L2

Действия:
1. Провести независимую оценку модели (не тем же агентом, что обучал —
   разделение ролей для объективности)
2. Проверить на bias и edge cases, релевантные для функций, которые модель
   будет поддерживать

## Stage 3 — Risk Review

**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Оценить, для каких Decision Level функций используется модель — при
   поддержке решений L3+ требуется более строгая проверка
2. Проверить соответствие принципам AI Governance (GOVERNANCE_MODEL.md,
   см. PB022)

## Stage 4 — Decision (Deployment Approval)

**Owner:** AG009 Enterprise Architect (AG003 AI Auditor — для моделей,
влияющих на решения L3+)
**Decision Level:** L2 (L3-L4 в зависимости от критичности применения)

Критерии:
- Новая модель показывает улучшение или как минимум не хуже текущей по
  ключевым метрикам
- Риски (bias, edge cases) задокументированы и приемлемы

## Stage 5 — Execution (Deployment)

**Function:** TEC-DEV-001 Deployment Pipeline Health Check (используется
как транспорт)
**Owner:** AG064 DevOps Agent
**Decision Level:** L1

Действия:
1. Развернуть модель поэтапно (canary/staged rollout, не сразу на 100%
   трафика)
2. Мониторить метрики в реальном времени во время rollout

## Stage 6 — Audit

**Function:** TEC-MLO-001 Model Retraining Schedule
**Owner:** AG056 AI Trainer
**Decision Level:** L2

Действия:
1. Установить график мониторинга деградации (model drift detection)
2. При обнаружении деградации ниже порога — инициировать цикл заново
   (Stage 1) для переобучения

## Stage 7 — Knowledge Capture

**Function:** TEC-MLO-001-002 Model Retraining Schedule Review
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать версию модели, дату развёртывания, ключевые метрики
2. Зафиксировать паттерны деградации для улучшения будущих циклов
   переобучения

## KPIs

- Model Performance Delta (новая версия vs предыдущая)
- Time to Detect Model Drift
- Deployment Rollback Rate (% развёртываний, потребовавших отката)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (TEC-AIP, TEC-MLO, TEC-DEV)
- PB022_AI_Governance_Review.md (проверка соответствия принципам)
- PB038_Deployment_Pipeline_Health.md (механизм развёртывания)
- AGENT_REGISTRY.md (AG056, AG055, AG009, AG003, AG064)
