from src.application.commands.plan_creation_complete import (
    IPlanCreationCompleteCommand,
    PlanCreationCompletePayload,
    StepItem,
)
from src.domain.events.plan_creation_complete import PlanCreationCompleteEvent
from src.domain.ports.user_notifier import IUserNotifier
from src.infra.exceptions.active_plan_exists_error import ActivePlanExistsError


class PlanCreationCompleteHandler:
    """Обработчик события завершения создания плана обучения"""

    def __init__(
        self,
        plan_creation_complete_cmd: IPlanCreationCompleteCommand,
        notifier: IUserNotifier,
    ):
        self.plan_creation_complete_cmd = plan_creation_complete_cmd
        self.notifier = notifier

    async def handle(self, event: PlanCreationCompleteEvent) -> None:
        payload = PlanCreationCompletePayload(
            plan_request_id=event.plan_request_id,
            steps=[
                StepItem(title=step.title, description=step.description)
                for step in event.steps
            ],
            is_success=event.is_success,
            error=event.error,
        )

        try:
            await self.plan_creation_complete_cmd.execute(payload)
            """
            fixme:
            по хорошему логику формирования текста сообщения нужно перенести в конкретную имплементацию notify
            """
            await self.notifier.notify(
                event.user_id, f"Учебный план создан. Можете его начать"
            )
        except ActivePlanExistsError as e:
            await self.notifier.notify(
                event.user_id,
                "Вы уже имеете активный учебный план. Завершите его перед созданием нового.",
            )

        except Exception as e:
            await self.notifier.notify(
                event.user_id,
                f"Произошла ошибка при создании учебного плана: {str(e)}",
            )
