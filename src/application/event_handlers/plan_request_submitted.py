from src.domain.events.plan_request_submitted import PlanRequestSubmittedEvent
from src.domain.ports.plan_generator import IPlanGeneratorService


class PlanRequestSubmittedHandler:
    """Обработчик события принятия в обработку запроса на создание плана обучения"""

    def __init__(self, plan_generator: IPlanGeneratorService):
        self.plan_generator = plan_generator

    async def handle(self, event: PlanRequestSubmittedEvent) -> None:
        await self.plan_generator.generate(event.plan_request)
