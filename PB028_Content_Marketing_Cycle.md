# PB028 Content Marketing Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C04 Marketing
Related Functions: MRK-CON-001, MRK-CON-002, MRK-SEO-001, MRK-ANA-001
Owner Agent: AG031 Content Agent
Escalation Path: AG031 → AG030 Marketing Manager → AG035 Brand Agent
(для вопросов бренд-соответствия)

## Purpose

Playbook описывает регулярный цикл производства контента — от планирования
календаря до анализа эффективности опубликованных материалов.

## Trigger Conditions

- Плановый цикл (обычно еженедельный/двухнедельный контент-календарь)
- Запрос на контент от другого playbook (например, PB027 Product Launch,
  PB025 Partnership)

## Stage 1 — Idea (Content Calendar Planning)

**Function:** MRK-CON-001 Content Calendar Management
**Owner:** AG031 Content Agent
**Decision Level:** L1

Действия:
1. Собрать входящие запросы на контент от других доменов
2. Сформировать календарь на период с учётом SEO-приоритетов
   (MRK-SEO-001 SEO Performance Review) и трендов (MKT-TRD-001)
3. Распределить темы по форматам (статьи, видео, кейсы)

## Stage 2 — Analysis (Content Creation)

**Owner:** AG031 Content Agent
**Decision Level:** L1

Действия:
1. Подготовить черновики согласно плану
2. Оптимизировать под SEO (ключевые слова, структура) совместно с
   AG032 SEO Agent

## Stage 3 — Risk Review

**Owner:** AG035 Brand Agent
**Decision Level:** L1

Действия:
1. Проверить соответствие тона и стиля бренд-гайдлайнам (MRK-BRA-001)
2. Проверить фактическую точность (особенно для контента о продукте/данных)

## Stage 4 — Decision (Publication Approval)

**Owner:** AG030 Marketing Manager
**Decision Level:** L1 (L2 для контента, затрагивающего юридические темы —
эскалация к AG017 Legal Counsel)

Критерии:
- Контент соответствует бренд-гайдлайнам
- Фактическая точность подтверждена
- SEO-оптимизация выполнена

## Stage 5 — Execution (Publishing & Distribution)

**Owner:** AG031 Content Agent (публикация), AG033 Social Media Agent
(дистрибуция)
**Decision Level:** L1

Действия:
1. Опубликовать на выбранных каналах (блог, соцсети — MRK-SOC-001)
2. Обновить внутреннюю Knowledge Base при релевантности для Support
   (KNW-KB-001)

## Stage 6 — Audit

**Function:** MRK-CON-002 Content Calendar Management Exception Handling
**Owner:** AG067 Analytics Agent
**Decision Level:** L1

Действия:
1. Отследить выполнение календаря (публикации в срок)
2. Проверить, не было ли пропущенных проверок Stage 3

## Stage 7 — Knowledge Capture

**Function:** MRK-ANA-001 Marketing Performance Dashboard
**Owner:** AG067 Analytics Agent
**Decision Level:** L1

Действия:
1. Собрать метрики по опубликованному контенту (трафик, вовлечённость,
   конверсия)
2. Передать в KNW-LES-001, какие темы/форматы работают лучше всего
3. Использовать данные для корректировки следующего цикла планирования

## KPIs

- Content Calendar Adherence Rate
- Organic Traffic Growth
- Content-to-Lead Conversion Rate (связь с MRK-LGN-001)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (MRK-CON, MRK-SEO, MRK-SOC, MRK-ANA, MRK-BRA)
- PB029_Campaign_Planning.md (контент как часть более широких кампаний)
- AGENT_REGISTRY.md (AG031, AG032, AG033, AG035, AG030, AG067)
