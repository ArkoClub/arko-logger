from datetime import datetime
from typing import Iterable, TYPE_CHECKING

from rich.containers import Renderables
from rich.logging import LogRender
from rich.table import Table
from rich.text import Text, TextType

if TYPE_CHECKING:
    from rich.console import Console, ConsoleRenderable, RenderableType

    # noinspection PyProtectedMember
    from rich._log_render import FormatTimeCallable

__all__ = ("Render",)


class Render(LogRender):
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
        log_time: datetime | None = None,
        time_format: str | None | "FormatTimeCallable" = None,
        level: "TextType" = "",
        path: str | None = None,
        line_no: int | None = None,
        link_path: str | None = None,
    ) -> Table:
        output = Table.grid(padding=(0, 1))
        output.expand = True
        output.add_column(style="log.time")
        output.add_column(style="log.level", width=self.level_width)
        output.add_column(ratio=1, style="log.record", overflow="fold")
        if path:
            output.add_column(style="log.path")
        if line_no:
            output.add_column(style="log.line_no", width=4)
        row: list["RenderableType"] = []
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
