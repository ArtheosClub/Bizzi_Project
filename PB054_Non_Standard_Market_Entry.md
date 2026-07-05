# PB054 Non-Standard Market Entry

Version: 1.0
Status: Active Playbook — Flagship
Related Capability: C01 Strategy / C03 Market Intelligence
Related Functions: STR-DIG-001, STR-LIC-001, STR-CHM-001, STR-DIA-001,
STR-TCK-001, LEG-SBX-001
Owner Agent: AG006 Strategy Agent
Escalation Path: AG006 → AG001 CEO Agent (для выбора между лёгким и
традиционным путём входа)

## Purpose

PB024_Market_Entry_Assessment.md описывает оценку рынка вообще. Этот
playbook — конкретно про выбор МЕТОДА входа, когда цель — скорость и
низкий риск капитала, а не полноценное развёртывание с первого дня.
Разница подхода: вместо "открыть юрлицо → нанять команду → локализовать
продукт → запустить" — "проверить спрос за недели → найти локального
партнёра/champion → расти без прямых инвестиций в инфраструктуру, пока
гипотеза не подтверждена деньгами реальных клиентов".

## Trigger Conditions

- PB024 определил рынок как перспективный, но с высокой неопределённостью
  (не хотим сразу вкладываться в полноценный вход)
- Ограниченный капитал/время для классического выхода
- Открылась нестандартная возможность (диаспора, sandbox-программа,
  доступная для tuck-in компания)

## Stage 1 — Idea (Method Screening)

**Function:** STR-DIG-001 Digital-First Market Testing
**Owner:** AG006 Strategy Agent
**Decision Level:** L2

Действия:
1. Запустить минимальное цифровое присутствие (лендинг, реклама, локальный
   контент) без физического присутствия — проверить реальный спрос за
   недели, не месяцы
2. Параллельно просканировать нестандартные пути: диаспора-сообщества
   (STR-DIA-001), regulatory sandbox программы (LEG-SBX-001), доступные для
   tuck-in локальные игроки (STR-TCK-001)

## Stage 2 — Analysis (Method Selection)

**Owner:** AG006 Strategy Agent
**Decision Level:** L3

Действия:
1. Сравнить методы по трём осям: скорость, требуемый капитал, риск
2. Для B2B с длинным циклом продаж — рассмотреть Local Champion model
   (STR-CHM-001): партнёр с локальными связями продаёт от имени компании
   за долю выручки, без найма локальной команды
3. Для продуктов, требующих локальной адаптации, — Licensing/Franchise-Light
   (STR-LIC-001): передать право использования бренда/продукта локальному
   оператору

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Для Local Champion/Licensing — оценить риск потери контроля над брендом
   и качеством
2. Для Tuck-In — оценить риск интеграции (аналогично PB026 M&A Target
   Screening, но на меньшем масштабе — "acqui-hire" локального присутствия)
3. Для Regulatory Sandbox — уточнить временные ограничения программы и
   план перехода к полноценной лицензии

## Stage 4 — Decision (Entry Method Approval)

**Owner:** AG001 CEO Agent
**Decision Level:** L4

Критерии:
- Метод соответствует уровню неопределённости (чем выше неопределённость
  спроса — тем легче должен быть метод входа)
- Риск потери контроля (для partner-based методов) явно принят или
  митигирован договорными условиями

## Stage 5 — Execution (Lightweight Launch)

**Owner:** зависит от метода — AG025 Sales Director (Local Champion),
AG017 Legal Counsel (Licensing/Sandbox), AG001 CEO Agent (Tuck-In)
**Decision Level:** L2

Действия:
1. Запустить выбранный метод с минимальными необратимыми инвестициями
2. Установить чёткие контрольные точки для решения "инвестировать больше"
   vs "закрыть эксперимент" (см. PB053 Blameless Retrospective — Fail-Fast
   логика применима и здесь)
3. При успехе на лёгком методе — рассмотреть переход к полноценному входу
   через PB024

## Stage 6 — Audit

**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Сверить фактическую скорость и стоимость входа с традиционным методом
   (сколько сэкономлено времени/капитала)
2. Оценить, оправдались ли риски, принятые на Stage 3 (потеря контроля,
   качество через партнёра)

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Зафиксировать, какой нестандартный метод сработал для какого типа
   рынка/продукта — построить библиотеку паттернов входа
2. При неудаче — передать в PB053_Blameless_Retrospective_Pivot.md для
   системного разбора

## KPIs

- Time to Market Validation (недели, не месяцы)
- Capital at Risk (сравнение с гипотетическим традиционным входом)
- Conversion to Full Entry Rate (% лёгких тестов, переросших в полноценный
  вход через PB024)

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (Non-Standard International Expansion layer)
- PB024_Market_Entry_Assessment.md (традиционная оценка входа)
- PB026_MA_Target_Screening.md (Tuck-In как облегчённая версия M&A)
- PB053_Blameless_Retrospective_Pivot.md (разбор неудачных экспериментов входа)
- AGENT_REGISTRY.md (AG006, AG005, AG001, AG025, AG017, AG084)
