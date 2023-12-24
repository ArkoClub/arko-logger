from multiprocessing import RLock as Lock
from typing import ClassVar, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.synchronize import RLock

__all__ = ("Orgu",)


class OrguCore(object):
    _instance: ClassVar[Optional["Orgu"]] = None
    _lock: ClassVar["RLock"] = Lock()

    def __new__(cls, *args, **kwargs) -> "Orgu":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(*args, **kwargs)
        return cls._instance


class Orgu(object):
    def __init__(self):
        ...
