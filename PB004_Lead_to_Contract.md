# PB004 Lead-to-Contract (Sales Cycle)

Version: 1.0
Status: Active Playbook
Related Capability: C05 Sales
Related Functions: SAL-LEAD-001, SAL-LEAD-002, SAL-OPP-001, SAL-OPP-002, SAL-OPP-003, SAL-CTR-001
Owner Agent: AG025 Sales Director
Escalation Path: AG025 → AG012 CFO Agent (pricing) / AG017 Legal Counsel (contract terms) → AG001 CEO Agent

## Purpose

Playbook описывает полный цикл продажи — от захвата лида до подписания контракта
и передачи клиента в Customer Success (см. PB003_Customer_Onboarding.md).

## Trigger Conditions

- Новый лид получен через MRK-LGN-001 Lead Generation Campaign
- Входящий запрос от потенциального клиента

## Stage 1 — Idea (Lead Capture & Qualification)

**Functions:** SAL-LEAD-001 Lead Capture, SAL-LEAD-002 Lead Qualification
**Owner:** AG025 Sales Director
**Decision Level:** L1

Действия:
1. Зафиксировать лид со всеми доступными данными (источник, контакт, потребность)
2. Квалифицировать по базовым критериям (бюджет, потребность, полномочия, срок)
3. Отклонить или передать на этап Opportunity

## Stage 2 — Analysis (Opportunity Development)

**Function:** SAL-OPP-001 Opportunity Creation
**Owner:** AG025 Sales Director
**Decision Level:** L1

Действия:
1. Создать запись возможности (Opportunity) с оценкой суммы сделки
2. Определить требуемые ресурсы (демо, техническая консультация, custom pricing)
3. При нестандартных условиях — привлечь MKT-PRI-001 Competitive Pricing Scan

## Stage 3 — Risk Review (Deal Risk Assessment)

**Function:** RSK-FIN-001 Financial Risk Monitoring (при крупных сделках)
**Owner:** AG005 Risk Manager
**Decision Level:** L2

Действия:
1. Для сделок выше порогового значения — проверить кредитоспособность клиента
2. Оценить риск нестандартных договорных условий

**Escalation:** пропускается для типовых сделок ниже порога (эскалация E2+ только
для нестандартных условий или крупных сумм)

## Stage 4 — Decision (Proposal & Negotiation)

**Functions:** SAL-OPP-002 Proposal Preparation, SAL-OPP-003 Negotiation Support
**Owner:** AG025 Sales Director
**Decision Level:** L2 (скидки выше стандартного порога — L3, требуют AG012)

Действия:
1. Подготовить коммерческое предложение
2. Провести переговоры по условиям (цена, сроки, SLA)
3. При скидке выше установленного лимита — согласовать с AG012 CFO Agent

## Stage 5 — Execution (Contracting)

**Function:** SAL-CTR-001 Sales Contract Finalization
**Owner:** AG018 Contract Review Agent
**Decision Level:** L2

Действия:
1. Подготовить финальный контракт на основе согласованных условий
2. Направить на юридическое ревью (LEG-CON-002 Contract Review) при нестандартных пунктах
3. Получить подписи сторон
4. Передать пакет (контракт + ожидания клиента + ключевые лица) в AG029 Customer
   Success Manager — запуск PB003_Customer_Onboarding.md

## Stage 6 — Audit

**Function:** GOV-AUD-001 Decision Audit
**Owner:** AG003 AI Auditor
**Decision Level:** L2

Действия:
1. Проверить, что скидки и условия контракта соответствуют утверждённым лимитам
2. Зафиксировать полный путь сделки (Lead → Contract) для аудита

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать типовые возражения клиентов и успешные контраргументы
2. Обновить шаблоны коммерческих предложений

## KPIs

- Lead-to-Contract Conversion Rate
- Average Sales Cycle Length (дни от Lead Capture до подписи)
- Average Discount Given (% от стандартного прайса)
- Win Rate по сегментам

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (SAL-LEAD, SAL-OPP, SAL-CTR, LEG-CON, RSK-FIN)
- PB003_Customer_Onboarding.md (следующий этап после подписания контракта)
- AGENT_REGISTRY.md (AG025, AG018, AG012, AG005, AG017)
