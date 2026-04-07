import uuid
from celery import Celery
from dishka.integrations.celery import DishkaTask, FromDishka, inject, setup_dishka
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from src.application.commands.plan_creation_complete import IPlanCreationCompleteCommand
from src.infra.config.ai import AiConfig
from src.infra.di.main import init_container

app = Celery("plan_generator", broker="redis://localhost:6379/0")
container = init_container()

setup_dishka(container, app)  # type: ignore


class Topic(BaseModel):
    title: str = Field(description="Название темы или модуля")
    description: str = Field(description="Краткое содержание темы")
    hours: int = Field(description="Примерное количество часов на изучение")


class StructuredPlanResponse(BaseModel):
    plan_title: str = Field(description="Общее название сгенерированного плана")
    summary: str = Field(description="Краткое резюме по плану")
    steps: list[Topic] = Field(description="Список последовательных шагов/тем обучения")


@app.task(base=DishkaTask, name="tasks.generate_plan_celery_task")
@inject
async def generate_plan_celery_task(
    request_data: dict,
    command: FromDishka[IPlanCreationCompleteCommand],
    config_ai: FromDishka[AiConfig],
):
    try:
        uuid_obj = uuid.UUID(request_data.get("id"))
        user_request_text = request_data.get("request")

        if uuid_obj is None or user_request_text is None:
            raise ValueError()

        ai_client = AsyncOpenAI(api_key=config_ai.token, base_url=config_ai.base_url)

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
        steps = []
        error = str(e)

    await command.execute(
        payload={
            "steps": [
                {"title": step.title, "description": step.description} for step in steps
            ],
            "is_success": is_success,
            "error": error,
        }
    )
