from dishka import Provider, Scope, provide

from src.application.commands.plan_create import CreatePlanCommand, ICreatePlanCommand
from src.application.commands.plan_creation_complete import (
    IPlanCreationCompleteCommand,
    PlanCreationCompleteCommand,
)
from src.application.commands.user_register_via_telegram import (
    IRegisterUserViaTelegramCommand,
    RegisterUserViaTelegramCommand,
)


class CommandProvider(Provider):
    """Провайдер команд"""

    scope = Scope.REQUEST

    register_user_via_telegram = provide(
        RegisterUserViaTelegramCommand, provides=IRegisterUserViaTelegramCommand
    )

    plan_create = provide(CreatePlanCommand, provides=ICreatePlanCommand)

    plan_creation_complete = provide(
        PlanCreationCompleteCommand, provides=IPlanCreationCompleteCommand
    )
