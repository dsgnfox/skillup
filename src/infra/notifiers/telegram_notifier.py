from aiogram import Bot
from src.domain.models.user import UserID
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.user_notifier import IUserNotifier


class TelegramNotifier(IUserNotifier):
    """Сервис уведомлений в телеграм"""

    def __init__(self, bot: Bot, telegram_user_repo: ITelegramUserRepository):
        self.bot = bot
        self.telegram_user_repo = telegram_user_repo

    async def notify(self, user_id: UserID, message: str):
        telegram_user = await self.telegram_user_repo.get_by_user_id(user_id)

        if telegram_user is None:
            return

        await self.bot.send_message(chat_id=telegram_user.telegram_id, text=message)
