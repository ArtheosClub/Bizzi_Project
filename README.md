# Art of Business

AI-Orchestrated Enterprise Framework — операционная система для цифрового
двойника малого и среднего бизнеса, управляемая сетью AI-агентов под
контролем человека.

## Что это

Art of Business — архитектурная спецификация предприятия, в котором:
- Бизнес-процессы разложены на измеримые **функции** (Function Registry)
- Каждой функцией владеет конкретный **AI-агент** (Agent Registry)
- Решения принимаются по чётким **уровням** (Governance Model, L0–L5)
- Повторяемые процессы описаны как **playbooks** (пошаговые сценарии)

Человек сохраняет право вето на критические и стратегические решения
(см. GOVERNANCE_MODEL.md, п.9 Human Override).

## Структура репозитория

| Файл | Назначение |
|---|---|
| `Vision.md` | Миссия и долгосрочное видение проекта |
| `CAPABILITY_MAP_v1.0.md` | 16 бизнес-доменов (C01–C16), 160 базовых способностей |
| `ENTERPRISE_FUNCTION_REGISTRY.md` | Реестр функций: Function ID, Owner Agent, Decision Level, Escalation |
| `AGENT_REGISTRY.md` | 28 AI-агентов, их зона ответственности и подчинённость |
| `GOVERNANCE_MODEL.md` | Конституционные принципы, уровни решений, эскалация, аудит |
| `PB001_Grant_Acquisition.md` | Playbook: полный цикл получения гранта |
| `PB002_Budget_Approval.md` | Playbook: годовой/квартальный цикл бюджетирования |
| `PB003_Customer_Onboarding.md` | Playbook: передача клиента из Sales в Customer Success |
| `PB004_Lead_to_Contract.md` | Playbook: полный цикл продажи от лида до контракта |
| `PB008_Monthly_Financial_Close.md` | Playbook: ежемесячное закрытие финансового периода |
| `PB011_Employee_Onboarding.md` | Playbook: онбординг нового сотрудника |
| `PB012_Recruitment_Cycle.md` | Playbook: цикл найма от заявки до оффера |
| `PB013_Contract_Review_Approval.md` | Playbook: ревью и утверждение контрактов |
| `PLAYBOOK_ROADMAP.md` | Backlog всех 50 целевых playbooks со статусами |
| `PLAYBOOK_TEMPLATE.md` | Шаблон для создания новых playbooks в единой структуре |

## Как читать документацию

Рекомендуемый порядок для нового участника:
1. `Vision.md` — зачем существует проект
2. `CAPABILITY_MAP_v1.0.md` — что предприятие умеет делать
3. `GOVERNANCE_MODEL.md` — как принимаются решения
4. `AGENT_REGISTRY.md` — кто (какой агент) за что отвечает
5. `ENTERPRISE_FUNCTION_REGISTRY.md` — как способности превращаются в конкретные функции
6. `PB001`–`PB004` — примеры полных playbooks в разных доменах
7. `PLAYBOOK_ROADMAP.md` — что предстоит сделать дальше

## Статус проекта

Архитектурный каркас выстроен и внутренне непротиворечив: все домены, функции,
агенты и playbooks ссылаются друг на друга по единым ID.

Текущий охват:
- Capabilities: 16/16, все 160 под-способностей имеют Function Group
  (включая C16 Administration & Executive Support)
- Functions: 300 документировано из целевых ~600 — ровно половина. Каждая
  Function Group теперь имеет минимум 2 функции (основное действие + Review
  или Exception Handling)
- Agents: 84/84 определены и полностью привязаны к Capability доменам
- Playbooks: 38/50 написаны полностью (76%) — Priority 1-4 закрыты
  (revenue & operations, governance & risk, growth & innovation, operations
  & technology). Осталось 12 в Priority 5 (finance, people, knowledge),
  см. PLAYBOOK_ROADMAP.md

## Contributing

Проект находится в приватной разработке ArtheosClub. Изменения в
CAPABILITY_MAP, GOVERNANCE_MODEL и AGENT_REGISTRY требуют согласования
с владельцем проекта, так как эти файлы — источник истины для остальной
архитектуры. Новые playbooks создавайте по PLAYBOOK_TEMPLATE.md и добавляйте
в PLAYBOOK_ROADMAP.md.
