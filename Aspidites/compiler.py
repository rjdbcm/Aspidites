#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
# Aspidites
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

import os
import py_compile
import sys
from glob import glob
import typing as t
from .templates import woma_template, makefile_template, pyproject_template, setup_template, default_template
from pyrsistent import pmap, v
from hashlib import sha256
from pathlib import Path
from ._vendor.semantic_version import Version
from Aspidites._vendor.pyparsing import ParseResults
import cython


class CheckedFileStack:

    """A convenience class for reading file data streams to stdout or to checksum"""

    __slots__ = v('all_files', 'pre_size')

    def __init__(self, initial=None, pre_size=128):
        pre_size: cython.int
        if initial is None:
            initial = {}
        self.all_files = pmap(initial, pre_size)
        self.all_files = self.all_files.evolver()
        self.pre_size = pre_size

    def __repr__(self):
        return self.__class__.__name__

    def _read(self, data, hash_func=None):
        chunk: t.Union[bytes, str] = data.read(self.pre_size)
        if hash_func is None:
            curr_hash = hash_func
        else:
            curr_hash = hash_func()
        while chunk:
            curr_hash and curr_hash.update(chunk)  # Short-circuits to nop if called without hash_func
            chunk = data.read(self.pre_size)
        return curr_hash

    def _write_checksum(self, fname) -> tuple:
        fname = Path(fname)
        base, name = fname.parent, fname.name
        base = Path(base)
        fname_sha256 = base / ("." + name + ".sha256")
        with open(fname, "rb") as data:
            curr_hash = self._read(data, hash_func=sha256)
            with open(fname_sha256, "wb") as digest:
                digest.write(curr_hash.digest())
            return pmap({curr_hash.digest(): fname}).items()[0]  # immutable

    def _read_checksum(self, fname):
        fname = Path(fname)
        base, name = fname.parent, fname.name
        base = Path(base)
        fname_sha256 = base / ("." + name + ".sha256")
        old = open(fname_sha256, "rb").read()
        with open(fname, "rb") as data:
            curr_hash = self._read(data, hash_func=sha256)
            new = curr_hash.digest()
            if new == old:
                print(
                    "sha256 digest check successful: %s %s"
                    % (name, new.hex())
                )
                return new
            else:
                print(
                    "sha256 digest failure: %s %s"
                    % (name, new.hex())
                )
                return ""

    def _commit(self):
        """Commits all registered files making the all_files attribute immutable.
        Short-circuits if no files are in the stack."""
        return not not len(self.all_files) and self.all_files.persistent()

    def register(self, fname):
        """Registers a filename to a checksum of its contents."""
        self.all_files.set(*self._write_checksum(fname))

    def create_file(self, fname, mode, root='', text=default_template) -> None:
        """API for creating and registering checked files"""
        if len(str(root)) > 0:
            root = Path(root)
            file = root/fname
        else:
            file = fname
        try:
            open(file, mode).write(text)
        except FileExistsError:
            self.register(file)

    def finalize(self) -> None:
        """Read and check all files against their stored digests."""
        all_file_checksums = self._commit()
        if not all_file_checksums:
            self.all_files.persistent()
            return None
        print("running checksums")
        for k, v in all_file_checksums.items():
            digest = self._read_checksum(v)
            try:
                all_file_checksums.get(digest)
            except AttributeError:
                raise RuntimeError("\nfor file %s\n%s\n  did not match cached digest\n%s")


class CompilerArgs:
    def __init__(self, **kwargs):
        self.code: ParseResults = kwargs['code']
        self.fname: Path = kwargs['fname']
        self.force: bool = kwargs['force']
        self.bytecode: bool = kwargs['bytecode']
        self.c: bool = kwargs['c']
        self.build_requires: t.Union[t.List, str] = kwargs['build_requires']
        self.verbose: int = kwargs['verbose']
        self.embed: t.Union[str, None] = kwargs['embed']
        self.__setattr__ = lambda x, y: None

    def __repr__(self) -> str:
        return self.__class__.__name__


class Compiler:
    def __init__(self, **kwargs):
        self.args = CompilerArgs(**kwargs)
        self.file_stack = CheckedFileStack()
        self.fname = Path(self.args.fname)
        self.app_name = self.fname.parent / self.fname.stem
        self.project = self.app_name.stem
        self.module_name = str(self.app_name).replace("/", ".")
        self.file_c = str(self.app_name) + ".c"
        self.root = self.fname.parent
        self.mode = "x" if self.args.force else "w"
        files = {
            self.fname: (
                self.mode,
                dict(root='', text=woma_template.substitute(code="\n".join(self.args.code)))
            ),
            '__init__.py': (
                self.mode,
                dict(root=self.root, text=f'__metadata__ = "{self.__dict__}"')
            ),
            'py.typed': (
                self.mode,
                dict(root=self.root)
            ),
            'pyproject.toml': (
                self.mode,
                dict(root=self.root, text=pyproject_template.substitute(build_requires=self.args.build_requires))
            ),
            'Makefile': (
                self.mode,
                dict(root=self.root, text=makefile_template.substitute(project=self.project))
            ),
        }

        for k, v in files.items():
            args_, kwargs_ = v
            self.file_stack.create_file(k, args_, **kwargs_)

        if self.args.bytecode:
            self.bytecode_compile()

        if self.args.c:
            # self.compile_c()
            if self.args.embed and 'main' in self.args.embed:
                pass  # maybe write a wrapper or something idk?
            self.setup(**kwargs)

        self.file_stack.finalize()

    def bytecode_compile(self) -> None:
        fname_pyc = str(self.app_name) + ".pyc"
        quiet = tuple(reversed(range(3))).index(self.args.verbose if self.args.verbose < 2 else 2)
        major, minor, patch, *_ = sys.version_info
        if Version(major=major, minor=minor, patch=patch) < Version('3.8.0'):
            py_compile.compile(str(self.fname), fname_pyc)
        else:
            py_compile.compile(str(self.fname), fname_pyc, quiet=quiet)
        self.file_stack.register(fname_pyc)

    def setup(self, **kwargs) -> None:
        module_name = str(self.app_name).replace("/", ".")
        text = setup_template.substitute(
           app_name=module_name,
           src_file=kwargs['fname'],
           inc_dirs=[],
           libs=[],
           exe_name=self.app_name,
           lib_dirs=[],
           **kwargs
        )
        self.file_stack.create_file('setup.py', self.mode, root=str(self.root), text=text)
        self.compile_object()

    def compile_object(self) -> None:
        glob_so = str(self.app_name) + ".*.so"
        setup_runner = "%s %s build_ext -b ." % (sys.executable, str(Path(self.root) / 'setup.py'))
        print("running", setup_runner)
        with os.popen(setup_runner) as p:
            chunk = p.read(64)
            while chunk:
                print(chunk, sep='', end='')
                chunk = p.read(64)
        self.file_stack.register(self.file_c)
        for i in glob(glob_so):
            self.file_stack.register(i)
