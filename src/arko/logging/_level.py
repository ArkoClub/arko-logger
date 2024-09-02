import logging
from enum import Enum

__all__ = ("LogLevel",)


class LogLevel(Enum):
    num: int
    icon: str

    CRITICAL = (50, "\u2620\uFE0F")  # ☠️
    FATAL = CRITICAL
    ERROR = (40, "\u274C")  # ❌
    WARNING = (30, "\u26A0\uFE0F")  # ⚠️
    WARN = WARNING
    SUCCESS = (30, "\u2705")  # ✅
    INFO = (20, "\u2139\uFE0F")  # ℹ️
    DEBUG = (10, "\U0001F41E")  # 🐞
    NOTSET = (0, "\u270F\uFE0F")  # ✏️

    def __init__(self, num: int = logging.NOTSET, icon: str = "") -> None:
        self.num = num
        self.icon = icon
