# noinspection PyUnresolvedReferences,PyProtectedMember
from contextlib import _GeneratorContextManager
from typing import Any, Callable, TypeVar

DEF: Any
POS: Any
EMPTY: Any

class FunctionMaker:
    args: Any
    varargs: Any
    varkw: Any
    defaults: Any
    kwonlyargs: Any
    kwonlydefaults: Any
    shortsignature: Any
    name: Any
    doc: Any
    module: Any
    annotations: Any
    signature: Any
    dict: Any
    def __init__(self, func: Any | None = ..., name: Any | None = ..., signature: Any | None = ..., defaults: Any | None = ..., doc: Any | None = ..., module: Any | None = ..., funcdict: Any | None = ...) -> None: ...
    def update(self, func, **kw) -> None: ...
    def make(self, src_templ, evaldict: Any | None = ..., addsource: bool = ..., **attrs): ...
    @classmethod
    def create(cls, obj, body, evaldict, defaults: Any | None = ..., doc: Any | None = ..., module: Any | None = ..., addsource: bool = ..., **attrs): ...

def fix(args, kwargs, sig): ...
F = TypeVar('F', bound=Callable[..., Any])

def decorate(func: F, caller, extras=..., kwsyntax: bool = ...) -> F: ...
def decorator(caller: F, _func: F = ..., kwsyntax: bool = ...) -> F: ...

class ContextManager(_GeneratorContextManager):
    def __init__(self, g, *a, **k): ...
    def __call__(self, func): ...

def contextmanager(func): ...
def append(a, vancestors) -> None: ...
def dispatch_on(*dispatch_args): ...
