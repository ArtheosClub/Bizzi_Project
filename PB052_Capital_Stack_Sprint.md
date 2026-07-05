# PB052 Non-Dilutive & Alternative Capital Stack Sprint

Version: 1.0
Status: Active Playbook — Flagship
Related Capability: C09 Finance
Related Functions: FIN-ALT-001, FIN-STK-001, FIN-STR-001, FIN-BRG-001,
FIN-CRW-001, FIN-RUN-001, FIN-GRA-001..004
Owner Agent: AG012 CFO Agent
Escalation Path: AG012 → AG001 CEO Agent → Human Board (для комбинирования
источников, меняющих структуру капитала)

## Purpose

Большинство компаний, когда нужен капитал, идут по одному пути: equity
раунд. Это не единственный и часто не лучший вариант — особенно для
компании, которая хочет расти агрессивно, не размывая долю быстрее
необходимого. Этот playbook описывает систематический поиск и
комбинирование нескольких источников капитала одновременно — то, что
делают дисциплинированные растущие компании, но редко формализуют как
процесс.

## Trigger Conditions

- Потребность в капитале выявлена в PB042_Capital_Structure_Review.md
- Runway приближается к пороговому значению (FIN-RUN-001 сигнализирует)
- Возможность (не обязательно нужда) — благоприятные условия для конкретного
  источника капитала (например, открылась грантовая программа — см. PB001)

## Stage 1 — Idea (Capital Stack Mapping)

**Function:** FIN-STK-001 Non-Dilutive Funding Stack Optimization
**Owner:** AG078 Grant Manager (совместно с AG012 CFO Agent)
**Decision Level:** L3

Действия:
1. Составить полную карту доступных источников: гранты (PB001), venture
   debt, revenue-based financing, стратегические инвесторы, crowdfunding,
   bridge-финансирование от текущих инвесторов
2. Для каждого источника — оценить: скорость получения, стоимость
   (dilution/interest/revenue share), ограничения по использованию

## Stage 2 — Analysis (Stack Design)

**Function:** FIN-ALT-001 Alternative Financing Sourcing
**Owner:** AG012 CFO Agent
**Decision Level:** L3

Действия:
1. Спроектировать комбинацию источников под конкретную потребность
   (например: грант на R&D + revenue-based financing на масштабирование
   продаж + небольшой bridge на runway — вместо одного большого equity
   раунда)
2. Для стратегических инвесторов — оценить не только чек, но и доступ к
   рынку/экспертизе (FIN-STR-001 Strategic Investor Targeting)

## Stage 3 — Risk Review

**Owner:** AG005 Risk Manager
**Decision Level:** L3

Действия:
1. Проверить совместимость условий разных источников (например, некоторые
   venture debt соглашения ограничивают дальнейшее привлечение долга)
2. Оценить риск концентрации в одном источнике vs диверсификации

## Stage 4 — Decision (Stack Approval)

**Owner:** AG001 CEO Agent (Human Board — при существенном изменении
структуры капитала, см. PB042)
**Decision Level:** L4-L5

Критерии:
- Комбинация источников минимизирует dilution при сохранении необходимой
  скорости получения капитала
- Условия источников не создают конфликтующих обязательств

**Human Override:** обязателен для любого элемента, меняющего капитальную
структуру.

## Stage 5 — Execution (Parallel Sourcing)

**Owner:** AG012 CFO Agent + AG078 Grant Manager (параллельно, не
последовательно — это ключевое отличие от типового единственного раунда)
**Decision Level:** L2

Действия:
1. Запустить процессы по нескольким источникам одновременно (гранты через
   PB001, переговоры по venture debt, аутрич к стратегическим инвесторам)
2. Координировать сроки закрытия, чтобы избежать разрыва в финансировании

## Stage 6 — Audit

**Owner:** AG003 AI Auditor
**Decision Level:** L3

Действия:
1. Сверить фактическую стоимость капитала (blended cost) с изначальной
   оценкой Stage 2
2. Зафиксировать реальное время получения по каждому источнику для
   калибровки будущих циклов

## Stage 7 — Knowledge Capture

**Function:** KNW-LES-001 Lessons Learned Capture
**Owner:** AG053 Knowledge Curator
**Decision Level:** L1

Действия:
1. Задокументировать, какая комбинация источников оказалась эффективнее
   единственного equity-раунда (или наоборот)
2. Обновить карту источников капитала (Stage 1) для следующего цикла

## KPIs

- Blended Cost of Capital (средневзвешенная стоимость по всему стеку)
- Dilution Avoided (% доли, сохранённой относительно гипотетического
  единственного equity-раунда на ту же сумму)
- Time to Full Stack Close

## Related Documents

- ENTERPRISE_FUNCTION_REGISTRY.md (Growth Mechanics & Capital Agility layer)
- PB001_Grant_Acquisition.md, PB042_Capital_Structure_Review.md (источники и контекст)
- AGENT_REGISTRY.md (AG012, AG078, AG005, AG001, AG014)
