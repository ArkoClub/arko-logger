from datetime import datetime
from datetime import datetime
from typing import (
    Callable,
    Iterable,
    List,
    Optional,
    TYPE_CHECKING,
    Union,
)

from rich.console import Console
from rich.logging import (
    LogRender as DefaultLogRender,
)
from rich.table import Table
from rich.text import (
    Text,
    TextType,
)

try:
    import ujson as json
    from ujson import JSONDecodeError
except ImportError:
    import json
    from json import JSONDecodeError

if TYPE_CHECKING:
    from rich.console import (  # pylint: disable=unused-import
        ConsoleRenderable,
        RenderableType,
    )

__all__ = ["LogRender"]

FormatTimeCallable = Callable[[datetime], Text]


class LogRender(DefaultLogRender):
    @property
    def last_time(self):
        return self._last_time

    @last_time.setter
    def last_time(self, last_time):
        self._last_time = last_time

    def __call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: Optional[datetime] = None,
        time_format: Optional[Union[str, FormatTimeCallable]] = None,
        level: TextType = "",
        path: Optional[str] = None,
        line_no: Optional[int] = None,
        link_path: Optional[str] = None,
    ) -> Table:
        from rich.containers import Renderables

        output = Table.grid(padding=(0, 1))
        output.expand = True
        output.add_column(style="log.time")
        output.add_column(style="log.level", width=self.level_width)
        output.add_column(ratio=1, style="log.message", overflow="fold")
        if path:
            output.add_column(style="log.path")
        if line_no:
            output.add_column(style="log.line_no", width=4)
        row: List["RenderableType"] = []
        if self.show_time:
            log_time = log_time or console.get_datetime()
            time_format = time_format or self.time_format
            if callable(time_format):
                log_time_display = time_format(log_time)
            else:
                log_time_display = Text(log_time.strftime(time_format))
            if log_time_display == self.last_time and self.omit_repeated_times:
                row.append(Text(" " * len(log_time_display)))
            else:
                row.append(log_time_display)
                self.last_time = log_time_display
        if self.show_level:
            row.append(level)

        row.append(Renderables(renderables))
        if path:
            path_text = Text()
            path_text.append(
                path, style=f"link file://{link_path}" if link_path else ""
            )
            row.append(path_text)

        line_no_text = Text()
        line_no_text.append(
            str(line_no),
            style=f"link file://{link_path}#{line_no}" if link_path else "",
        )
        row.append(line_no_text)

        output.add_row(*row)
        return output
