import logging
from dataclasses import dataclass
from multiprocessing import RLock as Lock
from typing import Mapping, Optional, TYPE_CHECKING

from rich.console import Console
from rich.theme import Theme
from typing_extensions import Self

from arko.logging._config import LoggerConfig
from arko.logging._style import LOGGER_STYLE
from arko.logging._typed import ExcInfoType

if TYPE_CHECKING:
    from multiprocessing.synchronize import RLock as LockType

logging.addLevelName(25, "SUCCESS")


class LoggerMeta(type):
    _lock: "LockType" = Lock()
    _instance: Optional["Logger"] = None

    def __call__(cls, *args, **kwargs) -> "Logger":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LoggerMeta, cls).__call__(*args, **kwargs)
            else:
                cls._instance.warning("A Logger instance already exists.")
        return cls._instance


class LoggerCore:
    """The Core of the Logger."""

    def __init__(
        self,
        level: str | int | None = None,
        width: int = 180,
        keywords: list[str] | None = None,
        time_format: str = "[%Y-%m-%d %X]",
    ):
        ...


@dataclass
class LoggerTracebackConfig:
    max_frames: int = 20
    trace_locals_max_depth: int | None = None
    trace_locals_max_length: int = 10
    trace_locals_max_string: int = 80


class Logger(logging.Logger, metaclass=LoggerMeta):
    """只能有一个实例的 Logger"""

    _core: LoggerCore

    def __init__(
        self,
        name: str | None = None,
        level: str | int | None = None,
        *,
        config: LoggerConfig = LoggerConfig(),
    ):
        """Initialization Logger"""
        super().__init__(
            name or config.name or "arko-logger",
            logging.getLevelName(level or config.level or "INFO"),
        )
        self._console = Console(
            color_system=config.color_system,
            theme=Theme(LOGGER_STYLE),
            width=config.width,
        )
        self.handlers = []

    def opt(self, markup: bool | None = None, depth: int | None = None) -> Self:
        return self

    def success(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        if self.isEnabledFor(25):
            self._log(
                25,
                msg,
                args,
                exc_info=exc_info,
                stack_info=stack_info,
                stacklevel=stacklevel,
                extra=extra,
            )
