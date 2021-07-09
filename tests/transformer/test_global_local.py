from Aspidites.libraries.RestrictedPython import compile_restricted_exec
from Aspidites.libraries.RestrictedPython._compat import IS_PY3
from tests.helper import restricted_exec

import pytest


GLOBAL_EXAMPLE = """
def x():
    global a
    a = 11
x()
"""


def test_Global():
    glb = {'a': None}
    restricted_exec(GLOBAL_EXAMPLE, glb)
    assert glb['a'] == 11


# Example from:
# https://www.smallsurething.com/a-quick-guide-to-nonlocal-in-python-3/
NONLOCAL_EXAMPLE = """
def outside():
    msg = "Outside!"
    def inside():
        nonlocal msg
        msg = "Inside!"
        print(msg)
    inside()
    print(msg)
outside()
"""


@pytest.mark.skipif(
    not IS_PY3,
    reason="The `nonlocal` statement was introduced in Python 3.0.")
def test_Nonlocal():
    result = compile_restricted_exec(NONLOCAL_EXAMPLE)
    assert result.errors == ('Line 5: Nonlocal statements are not allowed.',)
    assert result.code is None
