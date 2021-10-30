import builtins
import io
import pickle
from .._vendor.RestrictedPython import safe_builtins, compile_restricted


def _print(text):
    print(text)


compile = compile_restricted
print = _print
globals().update(dict(__builtins__=safe_builtins))


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(safe_builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()
