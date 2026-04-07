import json
import sys
from typing import Optional, Protocol, Any
import logging


class ILogger(Protocol):
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def createScope(self, name: str) -> "ILogger": ...


class JsonArgsFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)

        if record.args:
            try:
                args_to_log = record.args
                if isinstance(args_to_log, dict):
                    payload = args_to_log
                elif isinstance(args_to_log, tuple) and len(args_to_log) == 1:
                    payload = args_to_log[0]
                else:
                    payload = args_to_log

                json_data = json.dumps(payload, ensure_ascii=False, default=str)
                return f"{log_message} | args: {json_data}"
            except (TypeError, ValueError):
                return f"{log_message} | args: {repr(record.args)}"

        return log_message


class StdlibLogger:
    def __init__(self, name: str, scope_name: Optional[str] = None) -> None:
        self._scope_name = scope_name
        self._logger = logging.getLogger(name)
        self._logger.propagate = False

        if not self._logger.handlers:
            formatter = JsonArgsFormatter(
                fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG)

    def _log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        current_scope = self._scope_name or "Global"
        scoped_msg = f"[{current_scope}] {msg}"
        self._logger.log(level, scoped_msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, *args, **kwargs)

    def createScope(self, name: str) -> "ILogger":
        return StdlibLogger(self._logger.name, scope_name=name)
