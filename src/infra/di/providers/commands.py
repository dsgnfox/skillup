from dishka import Provider, Scope, provide

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
