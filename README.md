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
| `AGENT_REGISTRY.md` | 84 AI-агента, их зона ответственности и подчинённость |
| `GOVERNANCE_MODEL.md` | Конституционные принципы, уровни решений, эскалация, аудит |
| `PB001`–`PB050` | 50 playbooks — полные операционные процессы по всем доменам |
| `PLAYBOOK_ROADMAP.md` | Реестр всех 50 playbooks с привязкой к доменам |
| `PLAYBOOK_TEMPLATE.md` | Шаблон для создания новых playbooks сверх 50 |

## Как читать документацию

Рекомендуемый порядок для нового участника:
1. `Vision.md` — зачем существует проект
2. `CAPABILITY_MAP_v1.0.md` — что предприятие умеет делать (16 доменов)
3. `GOVERNANCE_MODEL.md` — как принимаются решения
4. `AGENT_REGISTRY.md` — кто (какой агент) за что отвечает (84 агента)
5. `ENTERPRISE_FUNCTION_REGISTRY.md` — как способности превращаются в конкретные функции
6. `PLAYBOOK_ROADMAP.md` — навигация по всем 50 playbooks
7. Начать с любого playbook своего домена — все они следуют единой
   7-стадийной структуре (Idea → Analysis → Risk Review → Decision →
   Execution → Audit → Knowledge Capture)

## Статус проекта

Архитектурный каркас полностью выстроен и внутренне непротиворечив: все
домены, функции, агенты и все 50 playbooks ссылаются друг на друга по
единым ID без разрывов.

Текущий охват:
- **Capabilities: 16/16** — все 160 под-способностей имеют Function Group
  (включая C16 Administration & Executive Support)
- **Functions: 300 из целевых ~600** (ровно половина). Каждая Function
  Group имеет минимум 2 функции (основное действие + Review или Exception
  Handling)
- **Agents: 84/84** — полная организационная структура, подтверждённая
  владельцем проекта, все агенты привязаны к Capability доменам
- **Playbooks: 50/50 — 100% ЗАВЕРШЕНО** ✅ Все 5 приоритетных волн
  реализованы: revenue & operations, governance & risk, growth & innovation
  (включая весь Marketing), operations & technology, finance/people/knowledge

### Что дальше (после 50/50 playbooks)

Единственный незакрытый количественный разрыв — функции: 300 из ~600.
Следующий шаг для дальнейшего углубления — расширение каждой Function
Group сверх текущих 2 функций (добавление узкоспециализированных
вариантов: например, отдельная функция для каждого типа исключения,
а не одна общая "Exception Handling").

Все 50 playbooks образуют связный граф — например, полный цикл клиента
проходит через PB004 (Lead-to-Contract) → PB003 (Onboarding) → PB005
(Renewal) ↔ PB006 (Upsell) ↔ PB007 (Support), с общими сервисами
PB021 (Escalation Protocol) и PB038 (Deployment Pipeline), на которые
ссылаются остальные playbooks вместо дублирования логики.

## Contributing

Проект находится в приватной разработке ArtheosClub. Изменения в
CAPABILITY_MAP, GOVERNANCE_MODEL и AGENT_REGISTRY требуют согласования
с владельцем проекта, так как эти файлы — источник истины для остальной
архитектуры. Изменения состава агентов проводятся через процедуру
PB020_Agent_Lifecycle.md. Новые playbooks создавайте по
PLAYBOOK_TEMPLATE.md и добавляйте в PLAYBOOK_ROADMAP.md.
