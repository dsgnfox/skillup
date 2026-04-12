import asyncio
import uuid
from dishka.integrations.celery import DishkaTask
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from src.domain.events.plan_creation_complete import (
    PlanCreationCompleteEvent,
    PlanCreationCompleteStep,
)
from src.domain.ports.event_bus import IEventBus
from src.infra.config.ai import AiConfig
from src.infra.celery_app import celery_app


class Topic(BaseModel):
    title: str = Field(description="Название темы или модуля")
    description: str = Field(description="Краткое содержание темы")
    hours: int = Field(description="Примерное количество часов на изучение")


class StructuredPlanResponse(BaseModel):
    plan_title: str = Field(description="Общее название сгенерированного плана")
    summary: str = Field(description="Краткое резюме по плану")
    steps: list[Topic] = Field(description="Список последовательных шагов/тем обучения")


@celery_app.task(name="tasks.generate_plan_celery_task")
def generate_plan_celery_task(request_data: dict):
    from src.infra.celery_start import container

    return asyncio.run(_generate_plan_logic(request_data, container))


async def _generate_plan_logic(request_data: dict, container):
    async with container() as request_container:
        # Получаем зависимости напрямую
        event_bus = await request_container.get(IEventBus)
        config_ai = await request_container.get(AiConfig)

        try:
            plan_request_id = uuid.UUID(request_data.get("id"))
            user_request_text = request_data.get("request")
            user_id = uuid.UUID(request_data.get("user_id"))

            if plan_request_id is None or user_request_text is None or user_id is None:
                raise ValueError()

            ai_client = AsyncOpenAI(
                api_key=config_ai.token, base_url=config_ai.base_url
            )

            SYSTEM_PROMPT = (
                "Ты профессиональный методист и эксперт по составлению индивидуальных планов обучения. "
                "Твоя задача — составить пошаговый и логичный план на основе запроса пользователя. "
                "Будь точен, избегай 'воды'"
                "Разбей план обучения на три равномерных шага"
            )

            response = await ai_client.beta.chat.completions.parse(
                model=config_ai.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Запрос пользователя: {user_request_text}",
                    },
                ],
                response_format=StructuredPlanResponse,  # Гарантирует структуру ответа
                timeout=120.0,  # Защита от долгого ожидания ИИ
            )

            ai_structured_result = response.choices[0].message.parsed

            if ai_structured_result is None:
                return

            steps = ai_structured_result.steps
            is_success = True
            error = None

        except Exception as e:
            is_success = False
            steps: list[Topic] = []
            error = str(e)

        await event_bus.publish(
            PlanCreationCompleteEvent(
                user_id=user_id,
                plan_request_id=plan_request_id,
                steps=[
                    PlanCreationCompleteStep(
                        title=step.title, description=step.description
                    )
                    for step in steps
                ],
                is_success=is_success,
                error=error,
            )
        )
