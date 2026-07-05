# PB036 System Integration Rollout

Version: 1.0
Status: Active Playbook
Related Capability: C13 Technology
Related Functions: TEC-INT-001, TEC-INT-001-002, TEC-APP-001
Owner Agent: AG065 Data Engineer
Escalation Path: AG065 → AG009 Enterprise Architect → AG002 Chief Orchestrator
(для интеграций, затрагивающих несколько доменов)

## Purpose

Playbook описывает подключение нового внешнего сервиса или внутренней
системы к экосистеме предприятия — от оценки совместимости до мониторинга
после запуска.

## Trigger Conditions

- Запрос от любого домена на интеграцию с новым инструментом (CRM, ERP,
  платёжная система и т.д.)
- Необходимость подключения нового источника данных для AI Platform

## Stage 1 — Idea (Integration Request)

**Owner:** AG065 Data Engineer
**Decision Level:** L2

Действия:
1. Получить запрос с описанием цели интеграции и требуемых данных
2. Оценить техническую совместимость (API, форматы данных, аутентификация)

## Stage 2 — Analysis (Architecture Design)

**Function:** TEC-APP-001 Application Portfolio Review
**Owner:** AG009 Enterprise Architect
**Decision Level:** L2

Действия:
1. Проверить, не дублирует ли новая интеграция существующий функционал
2. Спроектировать схему интеграции (API-first, webhook, batch sync)
3. Определить владельца данных и правила синхронизации

## Stage 3 — Risk Review

**Owner:** AG049 Information Security Agent
**Decision Level:** L3

Действия:
1. Проверить безопасность передачи данных (шифрование, хранение
   credentials — через AG081 Authorization Manager, не в открытом виде)
2. Оценить риск для непрерывности при отказе внешнего сервиса

## Stage 4 — Decision (Integration Approval)

**Owner:** AG009 Enterprise Architect (AG002 Chief Orchestrator — для
кросс-доменных интеграций)
**Decision Level:** L2 (L3 при затрагивании нескольких доменов)

Критерии:
- Архитектура соответствует стандартам безопасности
- Нет дублирования с существующими интеграциями

## Stage 5 — Execution (Build & Deploy)

**Function:** TEC-INT-001 System Integration Monitoring
**Owner:** AG065 Data Engineer (совместно с AG064 DevOps Agent)
**Decision Level:** L2

Действия:
1. Реализовать интеграцию в тестовой среде
2. Провести QA (AG063 QA Automation Agent)
3. Развернуть в production через стандартный deployment pipeline
   (TEC-DEV-001)

## Stage 6 — Audit

**Function:** TEC-INT-001-002 System Integration Monitoring Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Мониторить стабильность интеграции первые недели после запуска
2. Проверить логи на предмет ошибок синхронизации данных

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать архитектуру интеграции для будущих похожих запросов
2. Обновить Application Portfolio (TEC-APP-001)

## KPIs

- Integration Uptime
- Data Sync Accuracy
- Time to Integration (от запроса до production)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (TEC-INT, TEC-APP, TEC-DEV)
- PB038_Deployment_Pipeline_Health.md (используется для развёртывания)
- AGENT_REGISTRY.md (AG065, AG009, AG049, AG064, AG002)
