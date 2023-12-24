import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings as _BaseSettings, SettingsConfigDict

__all__ = ["LoggerConfig", "LoggerTracebackConfig"]


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


class LoggerTracebackConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="logger_traceback_")

    class LoggerTraceLocalsConfig(BaseSettings):
        enable: bool = True
        max_depth: int | None = None
        max_length: int = 10
        max_string: int = 80

    max_frames: int = 20
    word_wrap: bool = False
    suppress: list[str] = []
    locals: LoggerTraceLocalsConfig = LoggerTraceLocalsConfig()


class LoggerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="logger_")

    name: str = "arko-logger"
    level: str | int | None = None

    multiprocess: bool = False

    color_system: Literal["auto", "standard", "256", "truecolor", "windows"] = "auto"
    width: int = 180
    keywords: list[str] = []
    time_format: str = "[%Y-%m-%d %X]"
    capture_warnings: bool = True

    default_log_path: str | Path = "./logs"

    log_path: str | Path = "./logs"
    project_root: str | Path = Path(os.curdir).resolve()
    max_log_file_size: int | None = 1000000

    traceback: LoggerTracebackConfig = LoggerTracebackConfig()
