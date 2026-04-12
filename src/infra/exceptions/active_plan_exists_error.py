from src.infra.exceptions.infra_exception import InfraException


class ActivePlanExistsError(InfraException):
    """Ошибка, возникающая при попытке создать новый план обучения, когда уже существует активный план"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__("Active plan already exists for user")
