class DefaultException(Exception):
    """Базовое исключение"""

    _message: str | None

    def __init__(self, message: str | None, *args: object) -> None:
        super().__init__(*args)
        self._message = message

    @property
    def message(self) -> str | None:
        return self._message
