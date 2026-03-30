import asyncio
from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka
from src.infra.di.main import init_container
from src.infra.views.telegram.controller import TelegramController


async def main():
    container = init_container()

    bot = await container.get(Bot)
    dp = Dispatcher()

    setup_dishka(container=container, router=dp)

    controller = await container.get(TelegramController)

    dp.include_router(controller.router)

    try:
        print("=" * 20)
        print("✅ APP RUNNING")
        print("=" * 20)
        await dp.start_polling(bot)
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
