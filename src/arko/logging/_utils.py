import os
from functools import lru_cache
from pathlib import Path

__all__ = ("resolve_log_path",)


@lru_cache(maxsize=64)
def resolve_log_path(path: str | Path, root: Path = Path(os.curdir).resolve()) -> str:
    if path != "<input>":
        try:
            path = str(Path(path).relative_to(root))
            path = path.split(".")[0].replace(os.sep, ".")
        except ValueError:
            import site

            path = None
            for s in site.getsitepackages():
                try:
                    path = str(Path(path).relative_to(Path(s)))
                    break
                except ValueError:
                    continue
            if path is None:
                path = "<SITE>"
            else:
                path = path.split(".")[0].replace(os.sep, ".")
    else:
        path = "<INPUT>"
    return path.replace("lib.site-packages.", "")
