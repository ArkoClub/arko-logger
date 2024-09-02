from types import TracebackType
from typing import Mapping, TypeAlias

__all__ = ("ArgsType", "SysExcInfoType", "ExcInfoType")


ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]
SysExcInfoType: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None]
    | tuple[None, None, None]
)
ExcInfoType: TypeAlias = None | bool | SysExcInfoType | BaseException
