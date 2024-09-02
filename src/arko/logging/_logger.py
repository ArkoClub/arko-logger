import logging
from contextlib import contextmanager
from multiprocessing import RLock as Lock
from typing import Mapping, Optional, TYPE_CHECKING, TypedDict

from typing_extensions import Self

from arko.logging._config import LoggerConfig
from arko.logging._typed import ArgsType, ExcInfoType

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


class LoggerExtra(TypedDict):
    markup: bool
    depth: int
    keywords: list[str]


class Logger(logging.Logger, metaclass=LoggerMeta):
    """只能有一个实例的 Logger"""

    _extra: LoggerExtra

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
        self.handlers = []
        self._extra = LoggerExtra(
            markup=config.markup,
            depth=config.traceback.locals.max_depth,
            keywords=config.keywords,
        )
        self._config = config

    @contextmanager
    def _opt(
        self,
        markup: bool | None = None,
        depth: int | None = None,
        keywords: list[str] | None = None,
    ):
        old_extra = self._extra
        self._extra = {
            "markup": markup if markup is not None else self._extra["markup"],
            "depth": depth if depth is not None else self._extra["depth"],
            "keywords": keywords if keywords is not None else self._extra["keywords"],
        }
        try:
            yield
        finally:
            self._extra = old_extra

    def opt(
        self,
        markup: bool | None = None,
        depth: int | None = None,
        keywords: list[str] | None = None,
    ) -> Self:
        with self._opt(markup=markup, depth=depth, keywords=keywords):
            return self

    def _log(
        self,
        level: int,
        msg: object,
        args: ArgsType,
        exc_info: ExcInfoType | None = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        extra = self._extra | (extra or {})
        self.extras = None
        # noinspection PyProtectedMember
        return super()._log(level, msg, args, exc_info, extra, stack_info)

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
