# PB014 Compliance Monitoring Cycle

Version: 1.0
Status: Active Playbook
Related Capability: C10 Legal & Compliance
Related Functions: LEG-CMP-001, LEG-CMP-001-002, LEG-REG-001
Owner Agent: AG011 Compliance Agent
Escalation Path: AG011 → AG017 Legal Counsel → AG001 CEO Agent (для
существенных нарушений)

## Purpose

Playbook описывает непрерывный цикл мониторинга регуляторных изменений
и внутреннего соответствия — от отслеживания изменений в законодательстве
до подтверждения устранения выявленных пробелов.

## Trigger Conditions

- Плановая периодическая проверка (ежеквартально)
- Уведомление об изменении регулирования, релевантного домену деятельности
- Результат внешнего аудита (FIN-AUD-001) выявил compliance-пробел

## Stage 1 — Idea (Regulatory Change Monitoring)

**Function:** LEG-REG-001 Regulatory Change Monitoring
**Owner:** AG011 Compliance Agent
**Decision Level:** L2

Действия:
1. Отслеживать изменения в применимом законодательстве (по юрисдикциям
   присутствия компании)
2. Оценить применимость изменения к текущей деятельности
3. При отсутствии изменений — переход сразу к плановой проверке (Stage 2)

## Stage 2 — Analysis (Compliance Checklist Review)

**Function:** LEG-CMP-001 Compliance Checklist Review
**Owner:** AG011 Compliance Agent
**Decision Level:** L2

Действия:
1. Пройти чек-лист соответствия по всем применимым областям (AML — LEG-AML-001,
   KYC — LEG-KYC-001, Data Privacy — LEG-DPR-001)
2. Выявить пробелы (gap analysis) между текущим состоянием и требованиями
3. Оценить критичность каждого пробела

## Stage 3 — Risk Review

**Function:** RSK-LEG-001 Legal Risk Review
**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Оценить последствия невыполнения (штрафы, репутационный риск,
   приостановка деятельности)
2. Приоритизировать пробелы по риск-рейтингу

## Stage 4 — Decision (Remediation Plan Approval)

**Owner:** AG017 Legal Counsel (AG001 CEO Agent — при риске "High" и выше)
**Decision Level:** L3 (L4-L5 при критичных нарушениях)

Критерии:
- План устранения покрывает все пробелы с риском "Medium" и выше
- Сроки устранения соответствуют регуляторным дедлайнам (если применимо)

**Human Override:** обязателен для нарушений с риском "High"/"Critical" —
требуется подтверждение человеком перед публичным раскрытием или уведомлением
регулятора, если это применимо.

## Stage 5 — Execution (Remediation)

**Owner:** AG011 Compliance Agent (совместно с владельцем затронутого домена)
**Decision Level:** L2

Действия:
1. Реализовать план устранения (обновление процессов, обучение, техническая
   доработка)
2. Задокументировать каждый шаг устранения для последующего аудита
3. Уведомить затронутые департаменты об изменениях в процессах

## Stage 6 — Audit

**Function:** LEG-CMP-001-002 Compliance Checklist Review Exception Handling
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Подтвердить, что все пункты плана устранения выполнены
2. Провести GOV-AUD-002 Compliance Audit для формальной фиксации закрытия

## Stage 7 — Knowledge Capture

**Function:** KNW-POL-001 Policy Document Maintenance
**Owner:** AG053 Knowledge Curator
**Decision Level:** L2

Действия:
1. Обновить внутренние политики и SOP с учётом новых требований
2. Зафиксировать пробел и его устранение в Corporate Memory (KNW-MEM-001)
   для будущих аудитов

## KPIs

- Compliance Gap Closure Rate
- Time to Remediate (по критичности)
- Regulatory Change Detection Lead Time (насколько заранее изменение было
  выявлено до вступления в силу)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (LEG-CMP, LEG-REG, RSK-LEG, LEG-AML, LEG-KYC, LEG-DPR)
- PB013_Contract_Review_Approval.md (compliance-проверка условий контрактов)
- AGENT_REGISTRY.md (AG011, AG017, AG005, AG001)
