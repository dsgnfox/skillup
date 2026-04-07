from aiogram import Bot, Router, types
from aiogram.filters import Command
from dishka.integrations.aiogram import FromDishka, inject
from src.application.commands.user_register_via_telegram import (
    IRegisterUserViaTelegramCommand,
    RegisterUserViaTelegramPayload,
)
from src.domain.exceptions.telegram_already_added import TelegramAlreadyAdded


class TelegramControllerStart:
    """
    Контроллер запуска бота
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.router = Router()

        self.router.message.register(self.handle_start, Command("start"))

    @inject
    async def handle_start(
        self,
        message: types.Message,
        register_cmd: FromDishka[IRegisterUserViaTelegramCommand],
    ):
        user_data = message.from_user
        if not user_data:
            return

        payload = RegisterUserViaTelegramPayload(
            telegram_id=user_data.id,
            first_name=user_data.first_name,
            username=user_data.username,
        )

        try:
            user = await register_cmd.execute(payload)
            await message.answer(f"Привет, {user.name}! Вы успешно зарегистрированы.")
        except TelegramAlreadyAdded:
            await message.answer("Вы уже зарегистрированы!")
