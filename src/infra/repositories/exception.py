from src.infra.exceptions.infra_exception import InfraException


class RepositoryException(InfraException):
    """Исключение репозиторий"""


class NotFoundElement(RepositoryException):
    """Элемент не найден"""
