from typing import TYPE_CHECKING

from rich.logging import RichHandler

from arko_logger._context import LoggerConfigContextVar
from arko_logger._render import Render
from arko_logger._sink import Sink

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    pass

__all__ = ("Handler",)


class Handler(RichHandler):
    sinks: list[Sink] = []

    def __init__(self) -> None:
        config = LoggerConfigContextVar.get()
        super().__init__(level=config.level)
        self.log_render = Render(True, True, True, config.time_format, True, 8)
