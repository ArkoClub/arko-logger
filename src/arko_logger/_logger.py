import logging
from contextlib import contextmanager
from threading import RLock
from types import TracebackType
from typing import ClassVar, Mapping, TYPE_CHECKING, Union

from typing_extensions import Self, TypeAlias

from arko_logger._config import LoggerConfig
from arko_logger._sink import Sink

if TYPE_CHECKING:
    from threading import RLock as LockType

__all__ = ("Logger",)

_SysExcInfoType: TypeAlias = Union[
    tuple[type[BaseException], BaseException, TracebackType | None],
    tuple[None, None, None],
]
_ExcInfoType: TypeAlias = None | bool | _SysExcInfoType | BaseException
_Level: TypeAlias = int | str


class Logger(logging.Logger):
    _lock: ClassVar["LockType"] = RLock()
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> "Logger":
        with cls._lock:
            if cls._instance is None:
                result = super(Logger, cls).__new__(cls)
                cls._instance = result
        return cls._instance

    def __init__(self, config: LoggerConfig | None = None) -> None:
        super().__init__(config.name, config.level)
        self._config = config

    def add(self, sink: Sink) -> Self:
        ...

    def _update(self) -> None:
        self.name = self._config.name
        self.level = self._config.level
        logging.basicConfig(datefmt=self._config.time_format, format="%(record)%")

    @contextmanager
    def _use_config(self, config: LoggerConfig) -> None:
        old_config = self._config
        try:
            self._config = config
            self._update()
            yield
        finally:
            self._config = old_config
            self._update()

    def opt(self, config: LoggerConfig | None = None, **kwargs) -> Self:
        config = LoggerConfig.parse_obj((config or self._config).dict().update(kwargs))
        with self._use_config(config):
            return self

    def success(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(25, msg, args, exc_info, extra, stack_info, stacklevel)

    def setLevel(self, level: _Level) -> None:
        super().setLevel(level)
        self._config.level = self.level


handlers = []

logging.basicConfig(handlers=handlers)
