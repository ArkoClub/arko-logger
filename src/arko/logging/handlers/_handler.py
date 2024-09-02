from typing import Literal

from rich.console import Console
from rich.theme import Theme

from arko.logging._level import LogLevel
from arko.logging._style import ARKO_STYLE
from arko.logging.handlers._abc import AbstractHandler
from arko.logging.handlers._handler_file import AbstractHandlerFile, DefaultHandlerFile


class Handler(AbstractHandler):
    def __init__(
        self,
        level: int | str | LogLevel = LogLevel.INFO,
        *,
        name: str | None = None,
        color_system: (
            Literal["auto", "standard", "256", "truecolor", "windows"] | None
        ) = "auto",
        theme: Theme | None = None,
        width: int | None = None,
        file: AbstractHandlerFile | None = None,
        level_icon: bool = True,
    ):
        super().__init__(level)
        self._name = name
        self._console = Console(
            color_system=color_system,
            width=width,
            theme=theme or ARKO_STYLE,
            file=file or DefaultHandlerFile(),
        )

    def start(self) -> None:
        """开始"""

    def stop(self) -> None:
        self._console.file.close()


class FileHandler(Handler): ...
