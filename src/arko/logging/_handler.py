import logging

from rich.console import Console

from arko.logging._config import LoggerTracebackConfig


class Handler(logging.Handler):
    def __init__(
        self,
        level: int | str = 0,
        *,
        console: Console | None,
        omit_repeated_times: bool = True,
        show_path: bool = True,
        enable_link_path: bool = True,
        markup: bool = False,
        keywords: list[str] | None = None,
        time_format: str | None = None,
        rich_tracebacks: bool = True,
        traceback_configs: LoggerTracebackConfig | None = None,
    ) -> None:
        super().__init__(level)
        self._console = console
