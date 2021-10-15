__version__ = '0.31.0'
__title__ = 'Aspidites'
__author__ = 'Ross J. Duff'
__license__ = "GPL"
__description__ = (
    f"""
    {__title__} v{__version__} is the reference Woma programming language compiler.
    Copyright (C) 2021  {__author__}
    This program comes with ABSOLUTELY NO WARRANTY; 
    This is free software, and you are welcome to redistribute it
    under the conditions of the {__license__}v3 found in the LICENSE file.
    """
)
__mimetype__ = 'text/woma'
__all__ = [
    'SafeMod',
    'SafeDiv',
    'SafeExp',
    'SafeFloorDiv',
    'SafeFactorial',
    'SafeUnarySub',
    'SafeUnaryAdd',
    'Undefined',
    'Maybe',
    'Surely',
    'Warn',
    'parse_module',
    'parse_statement',
    'bordered'
    ]

from Aspidites.api import *
from Aspidites.parser import *
from Aspidites.monads import *
from Aspidites.math import *

Maybe.__doc__ = Maybe.__doc__