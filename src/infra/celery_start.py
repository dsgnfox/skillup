from src.infra.celery_app import celery_app
from src.infra.di.main import init_container
from dishka.integrations.celery import setup_dishka

container = init_container()
setup_dishka(container, celery_app)  # type: ignore
