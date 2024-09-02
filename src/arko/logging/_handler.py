import logging
import os
from datetime import datetime
from logging import LogRecord
from pathlib import Path
from types import TracebackType
from typing import AnyStr, IO, Iterable, Iterator, Literal, TYPE_CHECKING, Type

from arkowrapper import ArkoWrapper
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from arko.logging._config import LoggerTracebackConfig
from arko.logging._style import ARKO_STYLE
from arko.logging._traceback import Traceback
from arko.logging._utils import resolve_log_path

if TYPE_CHECKING:
    from rich.console import ConsoleRenderable, RenderableType


class HandlerIO(IO[str]):
    def close(self) -> None: ...

    @property
    def closed(self) -> bool:
        pass

    def fileno(self) -> int: ...

    def flush(self) -> None: ...

    def isatty(self) -> bool: ...

    def read(self, __n: int = -1) -> AnyStr: ...

    def readable(self) -> bool: ...

    def readline(self, __limit: int = -1) -> AnyStr: ...

    def readlines(self, __hint: int = -1) -> list[AnyStr]: ...

    def seek(self, __offset: int, __whence: int = 0) -> int: ...

    def seekable(self) -> bool: ...

    def tell(self) -> int: ...

    def truncate(self, __size: int | None = None) -> int: ...

    def writable(self) -> bool: ...

    def write(self, __s: AnyStr) -> int: ...

    def writelines(self, __lines: Iterable[AnyStr]) -> None: ...

    def __next__(self) -> AnyStr: ...

    def __iter__(self) -> Iterator[AnyStr]: ...

    def __enter__(self) -> IO[AnyStr]: ...

    def __exit__(
        self,
        __type: Type[BaseException] | None,
        __value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> None: ...


class Handler(logging.Handler):
    @property
    def console(self) -> Console:
        return self._console

    def __init__(
        self,
        level: int | str = 0,
        *,
        console: Console | None = None,
        width: int | None = None,
        color_system: Literal[
            "auto", "standard", "256", "truecolor", "windows"
        ] = "auto",
        omit_repeated_times: bool = True,
        show_path: bool = True,
        enable_link_path: bool = True,
        markup: bool = False,
        keywords: list[str] | None = None,
        time_format: str | None = None,
        rich_tracebacks: bool = True,
        traceback_configs: LoggerTracebackConfig | None = None,
        project_root: Path | None = None,
    ) -> None:
        super().__init__(level)
        self._console = console or Console(
            width=width,
            color_system=color_system,
            theme=Theme(ARKO_STYLE),
        )
        self.omit_repeated_times = omit_repeated_times
        self.show_path = show_path
        self.enable_link_path = enable_link_path
        self.markup = markup
        self.keywords = keywords
        self.time_format = time_format
        self.rich_tracebacks = rich_tracebacks
        self.traceback_configs = traceback_configs
        self.project_root = project_root or Path(os.curdir).resolve()

    def _get_message_renderable(self, record: LogRecord, message: str) -> Text:
        markup: bool = getattr(record, "markup", self.markup)
        keywords: list[str] = list(set(getattr(record, "keywords", []) + self.keywords))

        message_text = Text.from_markup(message) if markup else Text(message)

        if keywords:
            message_text.highlight_words(keywords, "logging.keyword")
        return message_text

    def render(
        self, record: LogRecord, message: str, traceback: Traceback | None
    ) -> "ConsoleRenderable":
        depth: int = getattr(record, "depth", self.traceback_configs.locals.max_depth)

        message_renderable = self._get_message_renderable(record, message)

        path = resolve_log_path(record.pathname, self.project_root)

        level_width = max(ArkoWrapper(logging.getLevelNamesMapping()).map(len))
        level_name = record.levelname
        level_text = Text.styled(
            level_name.ljust(level_width), f"logging.level.{level_name.lower()}"
        )

        logging.getLevelNamesMapping()
        time_format = None if self.formatter is None else self.formatter.datefmt
        log_time = datetime.fromtimestamp(record.created)

        renderables = [
            i for i in [message_renderable, traceback] if i is not None and i
        ]

        output = Table.grid(padding=(0, 1), expand=True)
        output.add_column(style="log.time")
        output.add_column(style="log.level", width=self.console.width)
        output.add_column(ratio=1, style="log.message", overflow="fold")
        output.add_column(style="log.path")
        output.add_column(style="log.line_no", width=4)

        row: list["RenderableType"] = []

    def emit(self, record: LogRecord) -> None:
        message = self.format(record)
        traceback = None
        if (
            self.rich_tracebacks
            and record.exc_info
            and record.exc_info != (None, None, None)
        ):
            exc_type, exc_value, exc_traceback = record.exc_info
            assert exc_type is not None
            assert exc_value is not None
            traceback = Traceback.from_exception(
                exc_type,
                exc_value,
                exc_traceback,
                width=None,
                word_wrap=self.traceback_configs.word_wrap,
                show_locals=self.traceback_configs.locals.enable,
                locals_max_length=self.traceback_configs.locals.max_length,
                locals_max_string=self.traceback_configs.locals.max_string,
                suppress=self.traceback_configs.suppress,
            )
            message = record.getMessage()
            if self.formatter:
                record.message = record.getMessage()
                formatter = self.formatter
                if hasattr(formatter, "usesTime") and formatter.usesTime():
                    record.asctime = formatter.formatTime(record, formatter.datefmt)
                message = formatter.formatMessage(record)

        log_renderable = self.render(
            record=record, message=message, traceback=traceback
        )

        # noinspection PyBroadException
        try:
            self.console.print(log_renderable)
        except Exception:
            self.handleError(record)
        return None

    def close(self) -> None:
        """"""
