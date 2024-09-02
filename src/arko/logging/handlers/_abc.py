import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import AnyStr, IO, Self

__all__ = (
    "AbstractHandler",
    "AbstractAsyncHandler",
    "AbstractFileHandler",
)


class AbstractHandler(ABC, logging.Handler):
    @abstractmethod
    def start(self) -> None:
        """start handle"""

    @abstractmethod
    def stop(self) -> None:
        """stop handle"""

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        self.stop()

    def __del__(self) -> None:
        self.stop()


class AbstractAsyncHandler(ABC, logging.Handler):
    @abstractmethod
    async def start(self) -> None:
        """start handle"""

    @abstractmethod
    async def stop(self) -> None:
        """stop handle"""

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        await self.stop()


class AbstractFileHandler(ABC, AbstractHandler):
    """"""
