#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
from sys import version_info

if version_info[0] == 3:
    from functools import reduce

reduce = reduce

from itertools import filterfalse
from itertools import zip_longest

# Using or importing the ABCs from 'collections' instead of from
# 'collections.abc' is deprecated, and in 3.8 it will stop working.
if version_info[0] <= 3 and version_info[1] < 8:
    from collections import Iterable
else:
    from collections.abc import Iterable
