import sys
from .pampy import match, ANY, HEAD, TAIL, REST, MatchError  # no _
from .pampy import match_value, match_iterable, match_dict
__version__ = '0.3.0'


__all__ = [
    "match",
    "ANY",
    "HEAD",
    "TAIL",
    "REST",
    "MatchError",
    "match_value",
    "match_iterable",
    "match_dict"
]
