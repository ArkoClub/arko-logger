import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import AnyStr, IO

from arko.logging.handlers._ctime_functions import get_ctime, set_ctime
from arko.logging.handlers._datetime import aware_now, Datetime
import datetime

__all__ = ("AbstractHandlerFile", "DefaultHandlerFile")


class FileDateFormatter:
    def __init__(self, _datetime: datetime.datetime | Datetime | None = None) -> None:
        self.datetime = _datetime or aware_now()

    def __format__(self, spec: str) -> str:
        if not spec:
            spec = "%Y-%m-%d_%H-%M-%S_%f"
        return self.datetime.__format__(spec)


def generate_rename_path(root: str, ext: str, creation_time: float) -> str:
    creation_datetime = Datetime.fromtimestamp(creation_time)
    date = FileDateFormatter(creation_datetime)

    renamed_path = "{}.{}{}".format(root, date, ext)
    counter = 1

    while os.path.exists(renamed_path):
        counter += 1
        renamed_path = "{}.{}.{}{}".format(root, date, counter, ext)

    return renamed_path


class Compression:
    @staticmethod
    def add_compress(path_in, path_out, opener, **kwargs):
        with opener(path_out, **kwargs) as f_comp:
            f_comp.add(path_in, os.path.basename(path_in))

    @staticmethod
    def write_compress(path_in, path_out, opener, **kwargs):
        with opener(path_out, **kwargs) as f_comp:
            f_comp.write(path_in, os.path.basename(path_in))

    @staticmethod
    def copy_compress(path_in, path_out, opener, **kwargs):
        with open(path_in, "rb") as f_in:
            with opener(path_out, **kwargs) as f_out:
                shutil.copyfileobj(f_in, f_out)

    @staticmethod
    def compression(path_in, ext, compress_function):
        path_out = "{}{}".format(path_in, ext)

        if os.path.exists(path_out):
            creation_time = get_ctime(path_out)
            root, ext_before = os.path.splitext(path_in)
            renamed_path = generate_rename_path(root, ext_before + ext, creation_time)
            os.rename(path_out, renamed_path)
        compress_function(path_in, path_out)
        os.remove(path_in)


class Retention:
    @staticmethod
    def retention_count(logs, number):
        def key_log(_log):
            return -os.stat(_log).st_mtime, _log

        for log in sorted(logs, key=key_log)[number:]:
            os.remove(log)

    @staticmethod
    def retention_age(logs, seconds):
        t = Datetime.now().timestamp()
        for log in logs:
            if os.stat(log).st_mtime <= t - seconds:
                os.remove(log)


class Rotation:
    @staticmethod
    def forward_day(t):
        return t + datetime.timedelta(days=1)

    @staticmethod
    def forward_weekday(t, weekday):
        while True:
            t += datetime.timedelta(days=1)
            if t.weekday() == weekday:
                return t

    @staticmethod
    def forward_interval(t, interval):
        return t + interval

    @staticmethod
    def rotation_size(message, file, size_limit):
        file.seek(0, 2)
        return file.tell() + len(message) > size_limit

    class RotationTime:
        def __init__(self, step_forward, time_init=None):
            self._step_forward = step_forward
            self._time_init = time_init
            self._limit = None

        def __call__(self, message, file):
            record_time = message.record["time"]

            if self._limit is None:
                filepath = os.path.realpath(file.name)
                creation_time = get_ctime(filepath)
                set_ctime(filepath, creation_time)
                start_time = Datetime.fromtimestamp(
                    creation_time, tz=datetime.timezone.utc
                )

                time_init = self._time_init

                if time_init is None:
                    limit = start_time.astimezone(record_time.tzinfo).replace(
                        tzinfo=None
                    )
                    limit = self._step_forward(limit)
                else:
                    timezone_info = (
                        record_time.tzinfo
                        if time_init.tzinfo is None
                        else time_init.tzinfo
                    )
                    limit = start_time.astimezone(timezone_info).replace(
                        hour=time_init.hour,
                        minute=time_init.minute,
                        second=time_init.second,
                        microsecond=time_init.microsecond,
                    )

                    if limit <= start_time:
                        limit = self._step_forward(limit)

                    if time_init.tzinfo is None:
                        limit = limit.replace(tzinfo=None)

                self._limit = limit

            if self._limit.tzinfo is None:
                record_time = record_time.replace(tzinfo=None)

            if record_time >= self._limit:
                while self._limit <= record_time:
                    self._limit = self._step_forward(self._limit)
                return True
            return False


class AbstractHandlerFile(ABC, IO[str]):
    @property
    @abstractmethod
    def encoding(self) -> str:
        """Return the encoding of the file."""

    @abstractmethod
    def fileno(self) -> int:
        """返回以整数表示的当前文件 文件描述符"""

    @abstractmethod
    def write(self, content: AnyStr) -> int:
        """Write the content to the file"""

    @abstractmethod
    def flush(self) -> None:
        """Flush the file"""


class DefaultHandlerFile(AbstractHandlerFile):
    def __init__(self, output_dir: str | Path | None = None):
        self._output_dir = (
            Path(output_dir).absolute()
            if output_dir is not None
            else Path(os.path.abspath(os.curdir)).joinpath("log")
        )

    def fileno(self) -> int:
        pass

    def write(self, content: AnyStr) -> int:
        pass

    def flush(self) -> None:
        pass
