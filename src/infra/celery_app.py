from celery import Celery

celery_app = Celery(
    "skillup",
    broker="redis://localhost:6379/0",
    include=["src.infra.background_tasks.generate_plan"],
)
