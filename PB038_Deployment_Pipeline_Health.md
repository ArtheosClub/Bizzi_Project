# PB038 Deployment Pipeline Health Check

Version: 1.0
Status: Active Playbook
Related Capability: C13 Technology
Related Functions: TEC-DEV-001, TEC-DEV-002, TEC-INF-001
Owner Agent: AG064 DevOps Agent
Escalation Path: AG064 → AG009 Enterprise Architect → AG050 Incident
Response Agent (при сбое production)

## Purpose

Playbook описывает мониторинг и поддержание работоспособности CI/CD
pipeline — механизма, через который любой код, интеграция или AI-модель
попадает в production (используется как общий сервис для PB036 и PB037).

## Trigger Conditions

- Плановая ежедневная проверка состояния pipeline
- Сбой при развёртывании (failed deployment)
- Запрос на развёртывание от Product Development (PB023, PB027) или
  AI Platform (PB037)

## Stage 1 — Idea (Deployment Request Intake)

**Owner:** AG064 DevOps Agent
**Decision Level:** L1

Действия:
1. Получить запрос на развёртывание (код, конфигурация, модель)
2. Проверить, что все обязательные проверки пройдены (тесты — AG063 QA
   Automation Agent, security scan)

## Stage 2 — Analysis (Pipeline Health Check)

**Function:** TEC-DEV-001 Deployment Pipeline Health Check
**Owner:** AG064 DevOps Agent
**Decision Level:** L1

Действия:
1. Проверить состояние инфраструктуры pipeline (TEC-INF-001 Infrastructure
   Monitoring)
2. Убедиться, что предыдущие развёртывания завершились успешно (нет
   незакрытых инцидентов)

## Stage 3 — Risk Review

**Owner:** AG049 Information Security Agent
**Decision Level:** L2

Действия:
1. Для изменений, затрагивающих продакшн-данные или безопасность —
   дополнительная проверка
2. Оценить, требуется ли staged rollout (canary) вместо полного
   развёртывания

## Stage 4 — Decision (Deployment Go/No-Go)

**Owner:** AG064 DevOps Agent (AG009 Enterprise Architect — для
архитектурно значимых изменений)
**Decision Level:** L1 (L2 для значимых изменений)

Критерии:
- Все автоматические проверки (тесты, security scan) пройдены
- Pipeline здоров (нет открытых инцидентов инфраструктуры)

## Stage 5 — Execution (Deployment)

**Owner:** AG064 DevOps Agent
**Decision Level:** L1

Действия:
1. Выполнить развёртывание согласно выбранной стратегии (blue-green,
   canary, rolling)
2. Мониторить ключевые метрики (error rate, latency) в реальном времени
3. При обнаружении аномалии — автоматический откат (rollback)

## Stage 6 — Audit

**Function:** TEC-DEV-002 Deployment Pipeline Health Check Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. При сбое — провести post-mortem (что пошло не так, почему проверки
   Stage 2-3 не поймали проблему)
2. Зафиксировать частоту откатов по типу изменений

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Обновить чек-лист автоматических проверок при выявлении пробелов
2. Задокументировать паттерны успешных/неуспешных развёртываний

## KPIs

- Deployment Frequency
- Deployment Success Rate (без отката)
- Mean Time to Recovery (MTTR) при сбое
- Change Failure Rate

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (TEC-DEV, TEC-INF, TEC-SEC)
- PB036_System_Integration_Rollout.md, PB037_AI_Model_Deployment.md (используют этот pipeline)
- PB016_Cyber_Incident_Response.md (эскалация при security-related сбое)
- AGENT_REGISTRY.md (AG064, AG009, AG049, AG050, AG063)
