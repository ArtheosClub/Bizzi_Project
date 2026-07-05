# PB046 Knowledge Base Quality Audit

Version: 1.0
Status: Active Playbook
Related Capability: C14 Knowledge Management
Related Functions: KNW-AUD-001, KNW-AUD-001-002
Owner Agent: AG003 AI Auditor
Escalation Path: AG003 → AG053 Knowledge Curator → AG002 Chief Orchestrator
(для системных пробелов в Knowledge Base)

## Purpose

Playbook описывает периодическую проверку качества и актуальности
корпоративной базы знаний — устаревшая или неточная информация в Knowledge
Base напрямую влияет на качество работы всех 84 агентов, которые на неё
опираются (например, AG069 Support Agent через KNW-SRC-001).

## Trigger Conditions

- Плановый ежеквартальный аудит Knowledge Base
- Рост случаев, когда агенты не находят решение в KB и эскалируют
  (см. PB007 Support Ticket Escalation)

## Stage 1 — Idea (Content Inventory)

**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Собрать полный перечень статей/документов в Knowledge Base
2. Отметить дату последнего обновления каждой статьи

## Stage 2 — Analysis (Quality Assessment)

**Function:** KNW-AUD-001 Knowledge Base Quality Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить статьи старше порогового срока (например, 12 месяцев) на
   актуальность
2. Сверить с фактическими изменениями в продукте/процессах (не устарела
   ли информация)
3. Проверить usage-метрики (KNW-ANL-001) — какие статьи не используются
   вообще (кандидаты на архивацию)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Приоритизировать устаревшие статьи по риску (например, устаревшая
   информация о безопасности или compliance — критичнее, чем устаревший
   маркетинговый факт)

## Stage 4 — Decision (Remediation Plan)

**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Варианты:
- Update — обновить содержание
- Archive — вывести из активного использования
- Merge — объединить с дублирующей статьёй

## Stage 5 — Execution (Content Update)

**Owner:** AG053 Knowledge Curator (совместно с владельцем домена,
которому принадлежит тема статьи)
**Decision Level:** L1

Действия:
1. Обновить/архивировать/объединить статьи согласно плану
2. Обновить индекс поиска (KNW-SRC-001)

## Stage 6 — Audit

**Function:** KNW-AUD-001-002 Knowledge Base Quality Audit Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что обновления действительно устранили выявленные проблемы
2. Отследить снижение эскалаций, связанных с отсутствием актуальной
   информации в KB

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать паттерны устаревания (какие типы контента устаревают
   быстрее всего)
2. Установить более частый цикл проверки для быстро устаревающих категорий

## KPIs

- KB Freshness Score (% статей, обновлённых в пределах порогового срока)
- Self-Service Resolution Rate (связь с PB007 — должен расти при улучшении KB)
- Article Utilization Rate

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (KNW-AUD, KNW-SRC, KNW-ANL)
- PB007_Support_Escalation.md (потребитель качественной KB)
- AGENT_REGISTRY.md (AG003, AG053, AG005)
