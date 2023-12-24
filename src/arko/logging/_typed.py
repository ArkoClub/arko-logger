from types import TracebackType
from typing import TypeAlias

SysExcInfoType: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None]
    | tuple[None, None, None]
)
ExcInfoType: TypeAlias = None | bool | SysExcInfoType | BaseException
