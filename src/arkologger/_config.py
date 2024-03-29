from multiprocessing import RLock as Lock
from pathlib import Path
from typing import (
    List,
    Literal,
    Optional,
    Union,
)

from pydantic import BaseSettings

__all__ = ["LoggerConfig"]


class LoggerConfig(BaseSettings):
    _lock = Lock()
    _instance: Optional["LoggerConfig"] = None

    def __new__(cls, *args, **kwargs) -> "LoggerConfig":
        with cls._lock:
            if cls._instance is None:
                cls.update_forward_refs()
                result = super(LoggerConfig, cls).__new__(cls)
                result.__init__(*args, **kwargs)
                cls._instance = result
        return cls._instance

    name: str = "arko-logger"
    level: Optional[Union[str, int]] = None

    color_system: Literal["auto", "standard", "256", "truecolor", "windows"] = "auto"
    debug: bool = False
    width: int = 180
    keywords: List[str] = []
    time_format: str = "[%Y-%m-%d %X]"
    capture_warnings: bool = True

    log_path: Union[str, Path] = "./logs"
    project_root: Union[str, Path] = Path(".")
    max_log_file_size: Optional[int] = 1000000

    traceback_max_frames: int = 20
    traceback_locals_max_depth: Optional[int] = None
    traceback_locals_max_length: int = 10
    traceback_locals_max_string: int = 80

    class Config(BaseSettings.Config):
        env_prefix = "logger_"
