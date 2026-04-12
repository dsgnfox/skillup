from aiogram import Bot, Router, types
from aiogram.filters import Command
from dishka.integrations.aiogram import FromDishka, inject
from src.application.commands.plan_create import (
    CreatePlanPayload,
    ICreatePlanCommand,
)

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.domain.exceptions.user_has_active_plan_request import UserHasActivePlanRequest
from src.domain.exceptions.user_has_in_process_plan import UserHasInProcessPlan
from src.domain.ports.telegram_user_repository import ITelegramUserRepository


class CreatePlanStates(StatesGroup):
    waiting_for_description = State()


class TelegramControllerPlanCreate:
    """
    Контроллер создания учебного плана
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.router = Router()
        self.router.message.register(self.handle_create_plan, Command("create_plan"))
        self.router.message.register(
            self.process_plan_text, CreatePlanStates.waiting_for_description
        )

    async def handle_create_plan(self, message: types.Message, state: FSMContext):
        await message.answer("Опишите, чему вы хотите научиться?")
        await state.set_state(CreatePlanStates.waiting_for_description)

    @inject
    async def process_plan_text(
        self,
        message: types.Message,
        state: FSMContext,
        create_plan_cmd: FromDishka[ICreatePlanCommand],
        telegram_user_repo: FromDishka[ITelegramUserRepository],
    ):
        request = message.text.strip() if message.text else ""
        user_data = message.from_user

        if not request:
            await message.answer("Запрос не может быть пустым")

        if not user_data:
            return

        telegram_user = await telegram_user_repo.get_by_telegram_id(user_data.id)

        if not telegram_user:
            return

        try:
            await create_plan_cmd.execute(
                CreatePlanPayload(user_id=telegram_user.user_id, request=request)
            )
            await message.answer(
                "План обучения создается. Мы сообщим, когда он будет готов"
            )
        except UserHasActivePlanRequest:
            await message.answer("У вас уже есть активный план обучения")
        except UserHasInProcessPlan:
            await message.answer("План обучения в процессе создания, ожидайте...")
        except:
            await message.answer("Непредвиденная ошибка, пожалуйста повторите запрос")

        await state.clear()
