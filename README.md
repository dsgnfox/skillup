# SkillUp

## Сервис пошагового обучения с ИИ ассистентом


#### Запуск для разработки

```
docker compose up -d
```
```
python3 -m src.main
celery -A src.infra.background_tasks.generate_plan worker
```