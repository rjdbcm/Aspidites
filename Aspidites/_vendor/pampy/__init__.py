import sys

from .pampy import (ANY, HEAD, REST, TAIL, MatchError, match,  # no _
                    match_dict, match_iterable, match_value)

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
