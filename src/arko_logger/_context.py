from contextvars import ContextVar

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arko_logger._config import LoggerConfig

__all__ = ("LoggerConfigContextVar",)


LoggerConfigContextVar: ContextVar["LoggerConfig"] = ContextVar("LoggerConfig")
