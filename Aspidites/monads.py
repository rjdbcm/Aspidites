import shutil
import inspect
from pyrsistent import pvector, v
import traceback
from _warnings import warn
from Aspidites.templates import _warning

from Aspidites.features.contracts import ContractNotRespected

from Aspidites import final
from contextlib import suppress


class Maybe:
    """Sandboxes a Definitely call and handles ContractNotRespected by returning Undefined"""
    __metaclass__ = final
    __slots__ = v('_func', '_args', '_kwargs', '__instance__')

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.__instance__ = Undefined()

    def __invert__(self):
        return ~self.__instance__

    def __neg__(self):
        return -self.__instance__

    @property
    def func(self):
        return self._func

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def __call__(self, debug=False, warn_undefined=True):
        try:
            with suppress(ValueError):
                val = self.func(*self.args, **self.kwargs)
            with suppress(UnboundLocalError):
                self.__instance__ = Surely(val)
                return self.__instance__
            # self.__instance__ = Undefined()
        except ContractNotRespected as e:
            if warn_undefined:
                tb_scope = len(inspect.trace()) if debug else 1
                for i in range(tb_scope):
                    stack = inspect.stack()
                    locals = stack[1][0].f_locals
                    str_locals = str()
                    for k,v in locals.items():
                        str_locals += k + ": " + str(v) + "\n"
                    the_caller = stack[1][0].f_code
                    fname, lineno, func, atfault = inspect.trace()[i][1], inspect.trace()[i][2], \
                                                   inspect.trace()[i][3], inspect.trace()[i][4]
                    atfault = str(atfault[0]).strip("\n").lstrip(' ') + "\n" + str_locals
                    w = _warning.safe_substitute(file=fname, lineno=lineno, func=func + str(the_caller), atfault=atfault,
                                        tb=str(e))
                    warn(w, category=RuntimeWarning)
            self.__instance__ = Undefined()
            return self.__instance__


class Undefined:
    """A monad for a failed programmatic unit; like NoneType but hashable.
    Falsy singleton"""
    __metaclass__ = final
    __slots__ = v('__weakref__', '__instance__')
    __instance = None

    def __hash__(self):
        return hash(self.__instance__)

    def __eq__(self, other):
        return self.__hash__ == other.__hash__

    def __add__(self, other):
        return other

    def __sub__(self, other):
        return -other

    def __neg__(self):
        return self

    def __invert__(self):
        return self

    def __mul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __floordiv__(self, other):
        return self

    def __str__(self):
        return str()

    def __float__(self):
        return float()

    def __complex__(self):
        return complex()

    def __oct__(self):
        return oct(0)

    def __index__(self):
        return 0

    def __len__(self):
        # Undefined has 0 elements
        return 0

    def __repr__(self):
        return self.__class__.__name__

    def __nonzero__(self):
        return False

    def __call__(self, *args, **kwargs):
        return self.__new__(self.__class__)

    def __new__(mcs, *args, **kwargs):
        if mcs.__instance is None:
            mcs.__instance = super(Undefined, mcs).__new__(mcs)
            mcs.__instance__ = mcs.__instance
        return mcs.__instance__  # instance descriptor from __slots__ -> actual instance


class Surely:
    """A monad for a successful programmatic unit
      Truthy, defers to an instance of a successful computation"""
    __metaclass__ = final
    __slots__ = v('__weakref__',
                  '__instance__'
                  '__str__',
                  '__int__',
                  '__float__',
                  '__complex__')

    def __hash__(self):
        return hash(self.__instance__)

    def __eq__(self, other):
        return self.__hash__ == other.__hash__

    def __add__(self, other):
        return self.__instance___ + other

    def __sub__(self, other):
        return self.__instance__ - other

    def __neg__(self):
        return -self.__instance__

    def __invert__(self):
        try:
            return ~self.__instance__
        except TypeError:
            return Undefined()

    def __mul__(self, other):
        return self.__instance__ * other

    def __truediv__(self, other):
        return self.__instance__ / other

    def __floordiv__(self, other):
        return self.__instance__ // other

    def __oct__(self):
        try:
            return oct(self.__instance__)
        except TypeError:
            return Undefined()

    def __nonzero__(self):
        return bool(self.__instance__)

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.__instance__

    # basically deep magic
    def __new__(cls, instance__=Undefined(), *args, **kwargs):
        cls.__instance__ = instance__
        return cls.__instance__


