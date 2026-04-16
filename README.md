![SKILLUP](https://i-mg24.ru/images/041626101224-h89ey.png)

### Сервис пошагового обучения с ИИ ассистентом

---

#### Запуск для разработки

```
docker compose up -d
```
```
python3 -m src.main
celery -A src.infra.celery_start:celery_app worker --loglevel=info
```

Проект реализован в парадигме чистой архитектуры (Clean Architecture). Это позволило обеспечить независимость бизнес-логики от внешних механизмов доставки (Telegram, REST API), баз данных, шин сообщений и AI-сервисов.

Используется Event-driver подход. Доменные команды генерируют события в шину. Сервисы-обработчики слушают эти события и вызывают команды.

#### Организация потока данных

```mermaid
flowchart LR
    subgraph Infrastructure ["Infrastructure (View)"]
        View["View<br/>(REST / Bot / etc.)"]
    end

    subgraph Application ["Application Layer"]
        Command["Command<br/>(business logic use case)"]
        Handler["Event Handler"]
    end

    subgraph Domain ["Domain Layer"]
        Event["Domain Event"]
    end

    View -->|user request| Command
    Command -->|generates| Event
    Event -->|triggers| Handler
    Handler -->|calls| Command
```

#### Архитектурные слои:

Domain — модели, события, порты к моделям и протоколы сервисов

Application - обработчики событий, команды бизнес-логики

Infrastructure — реализации портов, доступ к данным, представления
