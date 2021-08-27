from Aspidites._vendor.RestrictedPython.transformer import RestrictingNodeTransformer as RestrictingNodeTransformer
from Aspidites._vendor._compat import IS_CPYTHON as IS_CPYTHON, IS_PY2 as IS_PY2
from typing import Any, NamedTuple

class CompileResult(NamedTuple):
    code: Any
    errors: Any
    warnings: Any
    used_names: Any
syntax_error_template: str
NOT_CPYTHON_WARNING: str

def compile_restricted_exec(source, filename: str = ..., flags: int = ..., dont_inherit: bool = ..., policy=...): ...
def compile_restricted_eval(source, filename: str = ..., flags: int = ..., dont_inherit: bool = ..., policy=...): ...
def compile_restricted_single(source, filename: str = ..., flags: int = ..., dont_inherit: bool = ..., policy=...): ...
def compile_restricted_function(p, body, name, filename: str = ..., globalize: Any | None = ..., flags: int = ..., dont_inherit: bool = ..., policy=...): ...
def compile_restricted(source, filename: str = ..., mode: str = ..., flags: int = ..., dont_inherit: bool = ..., policy=...): ...
