from rich.console import Console
from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction
from logging import LogRecord

__all__ = ("Message", "Sink", "StreamSink")

from typing.io import IO


class Message(str):
    record: LogRecord


class Sink(ABC):
    @abstractmethod
    def write(self, message: Message) -> None:
        """写入"""

    @abstractmethod
    def stop(self) -> None:
        """关闭"""

    @abstractmethod
    async def complete(self) -> None:
        """完成"""


class StreamSink(Sink):
    def __init__(self, stream: IO[str]):
        self._console = Console(file=stream)
        self._stream = stream
        self._flushable = callable(getattr(stream, "flush", None))
        self._stoppable = callable(getattr(stream, "stop", None))
        self._completable = iscoroutinefunction(getattr(stream, "complete", None))

    def write(self, message: Message) -> None:
        self._stream.write(message)
        if self._flushable:
            self._stream.flush()

    def stop(self) -> None:
        if self._stoppable:
            self._stream.stop()

    async def complete(self) -> None:
        if self._completable:
            await self._stream.complete()
