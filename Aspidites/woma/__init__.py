"""This is the standard library bootstrapped with the compiler on a per-version basis.
This should allow for some semblance of backwards compatibility.
"""
# Aspidites - Woma Programming Language Standard Library
# Copyright (C) 2021 Ross J. Duff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from .gcutils import get_all
from .fileutils import mkdir_p, atomic_save, iter_find_files, copytree
from .pickleutils import pickle_loads
from .guiutils import *
from .mathutils import clamp, ceil, floor
from contextlib import contextmanager
from functools import lru_cache

__version__ = '1.13.1'


def woma_version():
    return __version__
