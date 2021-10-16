import builtins
import collections
import datetime
import functools
import importlib
import Aspidites._vendor.contracts.inspection as inspect
import io
import linecache
import os
from os.path import normcase
import _pickle
import pickle
import shutil
import sys
import types
import textwrap
import unicodedata
import unittest
import unittest.mock
import warnings

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    ThreadPoolExecutor = None

from Aspidites.tests.support import cpython_only
from Aspidites.tests.support import MISSING_C_DOCSTRINGS, ALWAYS_EQ
# from Aspidites.tests.support.os_helper import TESTFN
from Aspidites.tests.support.script_helper import assert_python_ok, assert_python_failure
from Aspidites.tests import inspect_fodder as mod
# from Aspidites.tests import inspect_fodder2 as mod2
# from Aspidites.tests import support
# from Aspidites.tests import inspect_stock_annotations
# from Aspidites.tests import inspect_stringized_annotations
# from Aspidites.tests import inspect_stringized_annotations_2

# from Aspidites.tests.test_import import _ready_to_import

modfile = mod.__file__
if modfile.endswith(('c', 'o')):
    modfile = modfile[:-1]

modfile = normcase(modfile)


def revise(filename, *args):
    return (normcase(filename),) + args


git = mod.StupidGit()


def signatures_with_lexicographic_keyword_only_parameters():
    """
    Yields a whole bunch of functions with only keyword-only parameters,
    where those parameters are always in lexicographically sorted order.
    """
    parameters = ['a', 'bar', 'c', 'delta', 'ephraim', 'magical', 'yoyo', 'z']
    for i in range(1, 2 ** len(parameters)):
        p = []
        bit = 1
        for j in range(len(parameters)):
            if i & (bit << j):
                p.append(parameters[j])
        fn_text = "def foo(*, " + ", ".join(p) + "): pass"
        symbols = {}
        exec(fn_text, symbols, symbols)
        yield symbols['foo']


def unsorted_keyword_only_parameters_fn(*, throw, out, the, baby, with_,
                                        the_, bathwater):
    pass


unsorted_keyword_only_parameters = 'throw out the baby with_ the_ bathwater'.split()


class IsTestBase(unittest.TestCase):
    predicates = {inspect.isclass, inspect.iscode, inspect.isframe, inspect.isfunction, inspect.ismethod,
                  inspect.ismodule, inspect.istraceback}

    def istest(self, predicate, exp):
        obj = eval(exp)
        self.assertTrue(predicate(obj), '%s(%s)' % (predicate.__name__, exp))

        for other in self.predicates - set([predicate]):
            if other == inspect.isfunction:
                continue
            self.assertFalse(other(obj), 'not %s(%s)' % (other.__name__, exp))


def generator_function_example(self):
    for i in range(2):
        yield i


async def async_generator_function_example(self):
    async for i in range(2):
        yield i


async def coroutine_function_example(self):
    return 'spam'


@types.coroutine
def gen_coroutine_function_example(self):
    yield
    return 'spam'


class TestPredicates(IsTestBase):

    def test_excluding_predicates(self):
        global tb

        self.istest(inspect.iscode, 'mod.spam.__code__')
        try:
            1 / 0
        except:
            tb = sys.exc_info()[2]
            self.istest(inspect.isframe, 'tb.tb_frame')
            self.istest(inspect.istraceback, 'tb')





        finally:

            tb = None
        self.istest(inspect.isfunction, 'mod.spam')
        self.istest(inspect.isfunction, 'mod.StupidGit.abuse')
        self.istest(inspect.ismethod, 'git.argue')
        self.istest(inspect.ismethod, 'mod.custom_method')
        self.istest(inspect.ismodule, 'mod')

    def test_isclass(self):
        self.istest(inspect.isclass, 'mod.StupidGit')
        self.assertTrue(inspect.isclass(list))

        class CustomGetattr(object):
            def __getattr__(self, attr):
                return None

        self.assertFalse(inspect.isclass(CustomGetattr()))

    def test_get_slot_members(self):
        class C(object):
            __slots__ = ("a", "b")

        x = C()
        x.a = 42

    def test_isabstract(self):
        from abc import ABCMeta, abstractmethod

        class AbstractClassExample(metaclass=ABCMeta):

            @abstractmethod
            def foo(self):
                pass

        class ClassExample(AbstractClassExample):
            def foo(self):
                pass

        a = ClassExample()


class SlotUser:
    'Docstrings for __slots__'
    __slots__ = {'power': 'measured in kilowatts',
                 'distance': 'measured in kilometers'}


class _BrokenDataDescriptor(object):
    """
    A broken data descriptor. See bug 
    """

    def __get__(*args):
        raise AttributeError("broken data descriptor")

    def __set__(*args):
        raise RuntimeError

    def __getattr__(*args):
        raise AttributeError("broken data descriptor")


class _BrokenMethodDescriptor(object):
    """
    A broken method descriptor. See bug 
    """

    def __get__(*args):
        raise AttributeError("broken method descriptor")

    def __getattr__(*args):
        raise AttributeError("broken method descriptor")


def attrs_wo_objs(cls):
    return [t[:3] for t in inspect.classify_class_attrs(cls)]


_global_ref = object()


class MyParameter(inspect.Parameter):
    pass


class TestParameterObject(unittest.TestCase):
    def test_signature_parameter_kinds(self):
        P = inspect.Parameter
        self.assertTrue(P.POSITIONAL_ONLY < P.POSITIONAL_OR_KEYWORD < \
                        P.VAR_POSITIONAL < P.KEYWORD_ONLY < P.VAR_KEYWORD)

        self.assertEqual(str(P.POSITIONAL_ONLY), 'POSITIONAL_ONLY')
        self.assertTrue('POSITIONAL_ONLY' in repr(P.POSITIONAL_ONLY))

    def test_signature_parameter_object(self):
        p = inspect.Parameter('foo', default=10,
                              kind=inspect.Parameter.POSITIONAL_ONLY)
        self.assertEqual(p.name, 'foo')
        self.assertEqual(p.default, 10)
        self.assertIs(p.annotation, p.empty)
        self.assertEqual(p.kind, inspect.Parameter.POSITIONAL_ONLY)

        with self.assertRaisesRegex(ValueError, "value '123' is "
                                                "not a valid Parameter.kind"):
            inspect.Parameter('foo', default=10, kind='123')

        with self.assertRaisesRegex(ValueError, 'not a valid parameter name'):
            inspect.Parameter('1', kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(TypeError, 'name must be a str'):
            inspect.Parameter(None, kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError,
                                    'is not a valid parameter name'):
            inspect.Parameter('$', kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError,
                                    'is not a valid parameter name'):
            inspect.Parameter('.a', kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.VAR_POSITIONAL)

        p = inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            p.replace(kind=inspect.Parameter.VAR_POSITIONAL)

        self.assertTrue(repr(p).startswith('<Parameter'))
        self.assertTrue('"a=42"' in repr(p))

    def test_signature_parameter_hashable(self):
        P = inspect.Parameter
        foo = P('foo', kind=P.POSITIONAL_ONLY)
        self.assertEqual(hash(foo), hash(P('foo', kind=P.POSITIONAL_ONLY)))
        self.assertNotEqual(hash(foo), hash(P('foo', kind=P.POSITIONAL_ONLY,
                                              default=42)))
        self.assertNotEqual(hash(foo),
                            hash(foo.replace(kind=P.VAR_POSITIONAL)))

    def test_signature_parameter_equality(self):
        P = inspect.Parameter
        p = P('foo', default=42, kind=inspect.Parameter.KEYWORD_ONLY)

        self.assertTrue(p == p)
        self.assertFalse(p != p)
        self.assertFalse(p == 42)
        self.assertTrue(p != 42)
        self.assertTrue(p == ALWAYS_EQ)
        self.assertFalse(p != ALWAYS_EQ)

        self.assertTrue(p == P('foo', default=42,
                               kind=inspect.Parameter.KEYWORD_ONLY))
        self.assertFalse(p != P('foo', default=42,
                                kind=inspect.Parameter.KEYWORD_ONLY))

    def test_signature_parameter_replace(self):
        p = inspect.Parameter('foo', default=42,
                              kind=inspect.Parameter.KEYWORD_ONLY)

        self.assertIsNot(p, p.replace())
        self.assertEqual(p, p.replace())

        p2 = p.replace(annotation=1)
        self.assertEqual(p2.annotation, 1)
        p2 = p2.replace(annotation=p2.empty)
        self.assertEqual(p, p2)

        p2 = p2.replace(name='bar')
        self.assertEqual(p2.name, 'bar')
        self.assertNotEqual(p2, p)

        with self.assertRaisesRegex(ValueError,
                                    'name is a required attribute'):
            p2 = p2.replace(name=p2.empty)

        p2 = p2.replace(name='foo', default=None)
        self.assertIs(p2.default, None)
        self.assertNotEqual(p2, p)

        p2 = p2.replace(name='foo', default=p2.empty)
        self.assertIs(p2.default, p2.empty)

        p2 = p2.replace(default=42, kind=p2.POSITIONAL_OR_KEYWORD)
        self.assertEqual(p2.kind, p2.POSITIONAL_OR_KEYWORD)
        self.assertNotEqual(p2, p)

        with self.assertRaisesRegex(ValueError,
                                    "value <class 'Aspidites._vendor.contracts.inspection._empty'> "
                                    "is not a valid Parameter.kind"):
            p2 = p2.replace(kind=p2.empty)

        p2 = p2.replace(kind=p2.KEYWORD_ONLY)
        self.assertEqual(p2, p)

    def test_signature_parameter_positional_only(self):
        with self.assertRaisesRegex(TypeError, 'name must be a str'):
            inspect.Parameter(None, kind=inspect.Parameter.POSITIONAL_ONLY)

    @cpython_only
    def test_signature_parameter_implicit(self):
        with self.assertRaisesRegex(ValueError,
                                    'implicit arguments must be passed as '
                                    'positional or keyword arguments, '
                                    'not positional-only'):
            inspect.Parameter('.0', kind=inspect.Parameter.POSITIONAL_ONLY)

        param = inspect.Parameter(
            '.0', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(param.kind, inspect.Parameter.POSITIONAL_ONLY)
        self.assertEqual(param.name, 'implicit0')

    def test_signature_parameter_immutability(self):
        p = inspect.Parameter('spam', kind=inspect.Parameter.KEYWORD_ONLY)

        with self.assertRaises(AttributeError):
            p.foo = 'bar'

        with self.assertRaises(AttributeError):
            p.kind = 123


if __name__ == "__main__":
    unittest.main()
