import sys
from functools import cached_property, lru_cache
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseSettings as Settings

try:
    import ujson as json
except ImportError:
    import json

if TYPE_CHECKING:
    from rich.console import Console
    from arko_logger._render import Render

__all__ = ("LoggerConfig",)

PROJECT_ROOT = Path(sys.modules["__main__"].__file__).parent.resolve()


class BaseSettings(Settings):
    class Config(Settings.Config):
        json_loads = json.loads
        json_dumps = json.dumps


class TracebackConfig(BaseSettings):
    max_frames: int = 20
    locals_max_depth: int | None = None
    locals_max_length: int = 10
    locals_max_string: int = 80

    class Config(BaseSettings.Config):
        env_prefix = "logger_traceback_"


class LoggerConfig(BaseSettings):
    name: str = "arko-logger"
    level: str | int | None = None

    debug: bool = False
    width: int = 180
    keywords: list[str] = []

    time_format: str = "%Y-%m-%d %X"
    capture_warnings: bool = True

    log_path: PathLike | str = "./logs"
    project_root: PathLike | str = PROJECT_ROOT
    max_log_file_size: str = "1M"

    class Config(BaseSettings.Config):
        env_prefix = "logger_"

    traceback: TracebackConfig = TracebackConfig()

    @cached_property
    def log_render(self) -> "Render":
        from arko_logger._render import Render

        return Render(time_format=self.time_format, show_level=True)

    @lru_cache
    def console(self, level: str | int | None = None) -> "Console":
        from rich.console import Console
        from rich.theme import Theme
        from arko_logger._style import DEFAULT_STYLE

        return Console(
            color_system="truecolor",
            theme=Theme(DEFAULT_STYLE),
            width=None if level is None else self.width,
        )
