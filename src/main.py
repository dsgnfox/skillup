import asyncio
from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka
from src.infra.di.main import init_container
from src.infra.logger import ILogger
from src.infra.views.telegram.controller import TelegramController
from src.infra.views.telegram.plan_create.plan_create_controller import (
    TelegramControllerPlanCreate,
)
from src.infra.views.telegram.start.start_controller import TelegramControllerStart


async def main():
    container = init_container()

    logger = await container.get(ILogger)

    bot = await container.get(Bot)
    dp = Dispatcher()

    setup_dishka(container=container, router=dp)

    controller_start = await container.get(TelegramControllerStart)
    controller_plan_create = await container.get(TelegramControllerPlanCreate)

    dp.include_router(controller_start.router)
    dp.include_router(controller_plan_create.router)

    try:
        logger.info("APP RUNNING")
        await dp.start_polling(bot)
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
