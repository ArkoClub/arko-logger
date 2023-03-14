from enum import IntEnum
from typing import Literal

from rich.console import Console as DefaultConsole


class ColorSystem(IntEnum):
    STANDARD = 1
    EIGHT_BIT = 2
    TRUECOLOR = 3
    WINDOWS = 4
    PYCHARM = 5

    def __repr__(self) -> str:
        return f"ColorSystem.{self.name}"

    def __str__(self) -> str:
        return repr(self)


COLOR_SYSTEMS = {
    "standard": ColorSystem.STANDARD,
    "256": ColorSystem.EIGHT_BIT,
    "truecolor": ColorSystem.TRUECOLOR,
    "windows": ColorSystem.WINDOWS,
    "pycharm": ColorSystem.PYCHARM,
}


class Console(DefaultConsole):
    def __init__(
        self,
        *,
        color_system: Literal[
            "auto", "standard", "256", "truecolor", "windows", "pycharm"
        ]
        | None = "auto",
        **kwargs,
    ):
        super().__init__(**kwargs)

        if color_system is None:
            self._color_system = None
        elif color_system == "auto":
            self._color_system = self._detect_color_system()
        else:
            self._color_system = COLOR_SYSTEMS[color_system]

    def _detect_color_system(self) -> ColorSystem | None:
        ...
