#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=True, initializedcheck=False
# #########################     LICENSE     ############################ #

# Copyright (c) 2005-2021, Michele Simionato
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#   Redistributions in bytecode form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

"""
Decorator module, see
https://github.com/micheles/decorator/blob/master/docs/documentation.md
for the documentation.
"""
import inspect
import itertools
import operator
import re
import sys
from inspect import getfullargspec, iscoroutinefunction
from typing import Any, Callable, TypeVar


DEF = re.compile(r"\s*def\s*([_\w][_\w\d]*)\s*\(")
POS = inspect.Parameter.POSITIONAL_OR_KEYWORD
EMPTY = inspect.Parameter.empty


# this is not used anymore in the core, but kept for backward compatibility
class FunctionMaker(object):
    """
    An object with the ability to create functions with a given signature.
    It has attributes name, doc, module, signature, defaults, dict and
    methods update and make.
    """

    # Atomic get-and-increment provided by the GIL
    _compile_count = itertools.count()

    # make pylint happy
    args: str
    varargs: str
    varkw: str
    defaults: str
    kwonlyargs: str
    kwonlydefaults: str
    __version__ = '5.0.9'

    def __init__(self, func=None, name=None, signature=None,
                 defaults=None, doc=None, module=None, funcdict=None):
        self.shortsignature = signature
        if func:
            # func can be a class or a callable, but not an instance method
            self.name = func.__name__
            if self.name == '<lambda>':  # small hack for lambda functions
                self.name = '_lambda_'
            self.doc = func.__doc__
            self.module = func.__module__
            if inspect.isfunction(func):
                argspec = getfullargspec(func)
                self.annotations = getattr(func, '__annotations__', {})
                for a in ('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs',
                          'kwonlydefaults'):
                    setattr(self, a, getattr(argspec, a))
                for i, arg in enumerate(self.args):
                    setattr(self, 'arg%d' % i, arg)
                allargs = list(self.args)
                allshortargs = list(self.args)
                if self.varargs:
                    allargs.append('*' + self.varargs)
                    allshortargs.append('*' + self.varargs)
                elif self.kwonlyargs:
                    allargs.append('*')  # single star syntax
                for a in self.kwonlyargs:
                    allargs.append('%s=None' % a)
                    allshortargs.append('%s=%s' % (a, a))
                if self.varkw:
                    allargs.append('**' + self.varkw)
                    allshortargs.append('**' + self.varkw)
                self.signature = ', '.join(allargs)
                self.shortsignature = ', '.join(allshortargs)
                self.dict = func.__dict__.copy()
        # func=None happens when decorating a caller
        if name:
            self.name = name
        if signature is not None:
            self.signature = signature
        if defaults:
            self.defaults = defaults
        if doc:
            self.doc = doc
        if module:
            self.module = module
        if funcdict:
            self.dict = funcdict
        # check existence required attributes
        assert hasattr(self, 'name')
        if not hasattr(self, 'signature'):
            raise TypeError('You are decorating a non function: %s' % func)

    def update(self, func, **kw):
        """
        Update the signature of func with the data in self
        """
        func.__name__ = self.name
        func.__doc__ = getattr(self, 'doc', None)
        func.__dict__ = getattr(self, 'dict', {})
        func.__defaults__ = self.defaults
        func.__kwdefaults__ = self.kwonlydefaults or None
        func.__annotations__ = getattr(self, 'annotations', None)
        try:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            frame = sys._getframe(3)
        except AttributeError:  # for IronPython and similar implementations
            callermodule = '?'
        else:
            callermodule = frame.f_globals.get('__name__', '?')
        func.__module__ = getattr(self, 'module', callermodule)
        func.__dict__.update(kw)

    def make(self, src_templ, evaldict=None, addsource=False, **attrs):
        """
        Make a new function from a given template and update the signature
        """
        src = src_templ % vars(self)  # expand name and signature
        evaldict = evaldict or {}
        mo = DEF.search(src)
        if mo is None:
            raise SyntaxError('not a valid function template\n%s' % src)
        name = mo.group(1)  # extract the function name
        names = set([name] + [arg.strip(' *') for arg in
                              self.shortsignature.split(',')])
        for n in names:
            if n in ('_func_', '_call_'):
                raise NameError('%s is overridden in\n%s' % (n, src))

        if not src.endswith('\n'):  # add a newline for old Pythons
            src += '\n'

        # Ensure each generated function has a unique filename for profilers
        # (such as cProfile) that depend on the tuple of (<filename>,
        # <definition line>, <function name>) being unique.
        filename = '<decorator-gen-%d>' % next(self._compile_count)
        try:
            code = compile(src, filename, 'single')
            exec(code, evaldict)
        except Exception:
            print('Error in generated code:', sys.stderr)
            print(src, sys.stderr)
            raise
        func = evaldict[name]
        if addsource:
            attrs['__source__'] = src
        self.update(func, **attrs)
        return func

    @classmethod
    def create(cls, obj, body, evaldict, defaults=None,
               doc=None, module=None, addsource=True, **attrs):
        """
        Create a function from the strings name, signature and body.
        evaldict is the evaluation dictionary. If addsource is true an
        attribute __source__ is added to the result. The attributes attrs
        are added, if any.
        """
        if isinstance(obj, str):  # "name(signature)"
            name, rest = obj.strip().split('(', 1)
            signature = rest[:-1]  # strip a right parens
            func = None
        else:  # a function
            name = None
            signature = None
            func = obj
        self = cls(func, name, signature, defaults, doc, module)
        ibody = '\n'.join('    ' + line for line in body.splitlines())
        caller = evaldict.get('_call_')  # when called from `decorate`
        if caller and iscoroutinefunction(caller):
            body = ('async def %(name)s(%(signature)s):\n' + ibody).replace(
                'return', 'return await')
        else:
            body = 'def %(name)s(%(signature)s):\n' + ibody
        return self.make(body, evaldict, addsource, **attrs)


def fix(args, kwargs, sig):
    """
    Fix args and kwargs to be consistent with the signature
    """
    ba = sig.bind(*args, **kwargs)
    ba.apply_defaults()  # needed for test_dan_schult
    return ba.args, ba.kwargs


F = TypeVar('F', bound=Callable[..., Any])


def append(a, vancestors):
    """
    Append ``a`` to the list of the virtual ancestors, unless it is already
    included.
    """
    add = True
    for j, va in enumerate(vancestors):
        if issubclass(va, a):
            add = False
            break
        if issubclass(a, va):
            vancestors[j] = a
            add = False
    if add:
        vancestors.append(a)


# inspired from simplegeneric by P.J. Eby and functools.singledispatch
def dispatch_on(*dispatch_args):
    """
    Factory of decorators turning a function into a generic function
    dispatching on the given arguments.
    """
    assert dispatch_args, 'No dispatch args passed'
    dispatch_str = '(%s,)' % ', '.join(dispatch_args)

    def check(arguments, wrong=operator.ne, msg=''):
        """Make sure one passes the expected number of arguments"""
        if wrong(len(arguments), len(dispatch_args)):
            raise TypeError('Expected %d arguments, got %d%s' %
                            (len(dispatch_args), len(arguments), msg))

    def gen_func_dec(func):
        """Decorator turning a function into a generic function"""

        # first check the dispatch arguments
        argset = set(getfullargspec(func).args)
        if not set(dispatch_args) <= argset:
            raise NameError('Unknown dispatch arguments %s' % dispatch_str)

        typemap = {}

        def vancestors(*types):
            """
            Get a list of sets of virtual ancestors for the given types
            """
            check(types)
            ras = [[] for _ in range(len(dispatch_args))]
            for types_ in typemap:
                for t, type_, ra in zip(types, types_, ras):
                    if issubclass(t, type_) and type_ not in t.mro():
                        append(type_, ra)
            return [set(ra) for ra in ras]

        def ancestors(*types):
            """
            Get a list of virtual MROs, one for each type
            """
            check(types)
            lists = []
            for t, vas in zip(types, vancestors(*types)):
                n_vas = len(vas)
                if n_vas > 1:
                    raise RuntimeError(
                        'Ambiguous dispatch for %s: %s' % (t, vas))
                elif n_vas == 1:
                    va, = vas
                    mro = type('t', (t, va), {}).mro()[1:]
                else:
                    mro = t.mro()
                lists.append(mro[:-1])  # discard t and object
            return lists

        def register(*types):
            """
            Decorator to register an implementation for the given types
            """
            check(types)

            def dec(f):
                check(getfullargspec(f).args, operator.lt, ' in ' + f.__name__)
                typemap[types] = f
                return f

            return dec

        def dispatch_info(*types):
            """
            An utility to introspect the dispatch algorithm
            """
            check(types)
            lst = []
            for anc in itertools.product(*ancestors(*types)):
                lst.append(tuple(a.__name__ for a in anc))
            return lst

        def _dispatch(dispatch_args, *args, **kw):
            types = tuple(type(arg) for arg in dispatch_args)
            try:  # fast path
                f = typemap[types]
            except KeyError:
                pass
            else:
                return f(*args, **kw)
            combinations = itertools.product(*ancestors(*types))
            next(combinations)  # the first one has been already tried
            for types_ in combinations:
                f = typemap.get(types_)
                if f is not None:
                    return f(*args, **kw)

            # else call the default implementation
            return func(*args, **kw)

        return FunctionMaker.create(
            func, 'return _f_(%s, %%(shortsignature)s)' % dispatch_str,
            dict(_f_=_dispatch), register=register, default=func,
            typemap=typemap, vancestors=vancestors, ancestors=ancestors,
            dispatch_info=dispatch_info, __wrapped__=func)

    gen_func_dec.__name__ = 'dispatch_on' + dispatch_str
    return gen_func_dec

