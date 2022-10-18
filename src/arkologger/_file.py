import os
from datetime import date
from pathlib import Path
from types import TracebackType
from typing import (
    AnyStr,
    IO,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
)

__all__ = ["FileIO"]


# noinspection SpellCheckingInspection
class FileIO(IO[str]):
    def __init__(self, path: Path, max_file_size: Optional[int] = 1000000):
        if path.suffix != "":
            path.parent.mkdir(exist_ok=True, parents=True)
        else:
            path.mkdir(exist_ok=True, parents=True)
            path = path.joinpath("log.log")
        self._path = path
        self._stream: Optional[IO[str]] = None
        self._max_file_size = max_file_size

    def _get_file_name(self, time: date) -> Path:
        num = 0

        def get_path(n) -> Path:
            return self.dir.joinpath(
                f"{time.strftime('%Y-%m-%d')}"
                f"{f'-{str(n).rjust(2, str(0))}' if n else ''}.log"
            )

        path = base = get_path(num)
        while path.exists():
            path = get_path(num := num + 1)
        if base.exists():
            base.rename(path)
            return get_path(num + 1)
        else:
            return get_path(num)

    @property
    def dir(self) -> Path:
        return self._path.parent

    @property
    def _file_stream(self) -> IO[str]:
        if self._stream:
            self._stream.close()
        today = date.today()
        if not self._path.exists():
            self._stream = self._path.open(mode="a+", encoding="utf-8")
            return self._stream
        file_size = os.path.getsize(self._path)
        modify_date = date.fromtimestamp(os.stat(self._path).st_mtime)
        if modify_date != today:
            file = self._get_file_name(modify_date)
            self._path.rename(file)
        elif self._max_file_size is not None and file_size >= self._max_file_size:
            file = self._get_file_name(today)
            self._path.rename(file)
        self._stream = self._path.open(mode="a+", encoding="utf-8")
        return self._stream

    def close(self) -> None:
        return self._file_stream.close()

    def fileno(self) -> int:
        return self._file_stream.fileno()

    def flush(self) -> None:
        return self._file_stream.flush()

    def isatty(self) -> bool:
        return self._file_stream.isatty()

    def read(self, __n: int = -1) -> AnyStr:
        return self._file_stream.read(__n)

    def readable(self) -> bool:
        return self._file_stream.readable()

    def readline(self, __limit: int = ...) -> AnyStr:
        return self._file_stream.readline()

    def readlines(self, __hint: int = ...) -> List[AnyStr]:
        return self._file_stream.readlines()

    def seek(self, __offset: int, __whence: int = 0) -> int:
        return self._file_stream.seek(__offset, __whence)

    def seekable(self) -> bool:
        return self._file_stream.seekable()

    def tell(self) -> int:
        return self._file_stream.tell()

    def truncate(self, __size: Optional[int] = None) -> int:
        return self._file_stream.truncate(__size)

    def writable(self) -> bool:
        return self._file_stream.writable()

    def write(self, __s: AnyStr) -> int:
        return self._file_stream.write(__s)

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        return self._file_stream.writelines(__lines)

    def __next__(self) -> AnyStr:
        return self._file_stream.__next__()

    def __iter__(self) -> Iterator[AnyStr]:
        return self._file_stream.__iter__()

    def __enter__(self) -> IO[AnyStr]:
        return self._file_stream.__enter__()

    def __exit__(
        self,
        __t: Optional[Type[BaseException]],
        __value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        return self._file_stream.__exit__(__t, __value, __traceback)
