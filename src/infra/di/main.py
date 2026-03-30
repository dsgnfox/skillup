from dishka import make_async_container

from src.infra.di.providers import providers


def init_container():
    return make_async_container(*providers)
