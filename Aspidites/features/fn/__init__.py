from .func import F, curried
from .stream import Stream
from .underscore import shortcut as _
from .iters import (
    take,
    drop,
    takelast,
    droplast,
    consume,
    nth,
    first_true,
    iterate,
    padnone,
    ncycles,
    repeatfunc,
    grouper,
    group_by,
    roundrobin,
    partition,
    splitat,
    splitby,
    powerset,
    pairwise,
    iter_suppress,
    flatten,
    accumulate
)
from .op import (
    call,
    apply,
    flip,
    curry,
    zipwith,
    foldl,
    foldr,
    unfold
)

from .recur import (
    tco,
    stackless
)

from .uniform import (
    reduce,
    filterfalse,
    zip_longest
)

__version__ = "0.5.2"

__all__ = [
    "F",            # BEGIN func.py
    "curried",      # END func.py
    "take",         # BEGIN iters.py
    "drop",
    "takelast",
    "droplast",
    "consume",
    "nth",
    "first_true",
    "iterate",
    "padnone",
    "ncycles",
    "repeatfunc",
    "grouper",
    "group_by",
    "roundrobin",
    "partition",
    "splitat",
    "splitby",
    "powerset",
    "pairwise",
    "iter_suppress",
    "flatten",
    "accumulate",       # END iters.py
    "call",             # BEGIN op.py
    "apply",
    "flip",
    "curry",
    "zipwith",
    "foldl",
    "foldr",
    "unfold",           # END op.py
    "tco",
    "stackless",
    "Stream",
    "_",
    "reduce",
    "filterfalse",
    "zip_longest"
    ]
