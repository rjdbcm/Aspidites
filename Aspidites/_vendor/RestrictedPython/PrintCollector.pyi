from typing import Any

class PrintCollector:
    txt: Any
    def __init__(self, _getattr_: Any | None = ...) -> None: ...
    def write(self, text) -> None: ...
    def __call__(self): ...