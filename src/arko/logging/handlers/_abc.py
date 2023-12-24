from abc import ABC, abstractmethod
from rich.logging import RichHandler as _RichHandler

__all__ = ("AbstractHandler", "AbstractAsyncHandler", "AbstractFileHandler")


class AbstractHandler(ABC, _RichHandler):
    @abstractmethod
    def start(self) -> None:
        """start handle"""

    @abstractmethod
    def stop(self) -> None:
        """stop handle"""


class AbstractAsyncHandler(_RichHandler):
    async def start(self) -> None:
        """start handle"""

    async def stop(self) -> None:
        """stop handle"""


class AbstractFileHandler(AbstractHandler, ABC):
    """"""
