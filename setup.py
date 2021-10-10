#!/usr/bin/python3
import sys
from glob import glob
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install
import numpy
# ~#~ # Build static libs # ~#~ #
from Cython.Build import cythonize
ext_modules = cythonize([str(Path('Aspidites/_vendor/contracts/metaclass.py')),
                         str(Path('Aspidites/_vendor/contracts/interface.py')),
                         str(Path('Aspidites/_vendor/contracts/syntax.py')),
                         str(Path('Aspidites/_vendor/contracts/inspection.py')),
                         str(Path('Aspidites/_vendor/contracts/docstring_parsing.py')),
                         str(Path('Aspidites/_vendor/contracts/main_actual.py')),
                         str(Path('Aspidites/_vendor/contracts/library/arithmetic.py')),
                         str(Path('Aspidites/_vendor/contracts/library/files.py')),
                         str(Path('Aspidites/_vendor/contracts/library/array_ops.py')),
                         str(Path('Aspidites/_vendor/contracts/library/tuple.py')),
                         str(Path('Aspidites/_vendor/contracts/library/types_misc.py')),
                         str(Path('Aspidites/_vendor/contracts/library/lists.py')), 
                         str(Path('Aspidites/_vendor/contracts/library/miscellaneous_aliases.py')),
                         str(Path('Aspidites/_vendor/contracts/library/attributes.py')),
                         str(Path('Aspidites/_vendor/contracts/library/suggester.py')),
                         str(Path('Aspidites/_vendor/contracts/library/variables.py')),
                         str(Path('Aspidites/_vendor/contracts/library/separate_context.py')),
                         str(Path('Aspidites/_vendor/contracts/library/simple_values.py')),
                         str(Path('Aspidites/_vendor/contracts/library/map.py')),
                         str(Path('Aspidites/_vendor/contracts/library/comparison.py')),
                         str(Path('Aspidites/_vendor/contracts/library/extensions.py')),
                         str(Path('Aspidites/_vendor/contracts/library/collection.py')),
                         str(Path('Aspidites/_vendor/contracts/library/datetime_tz.py')),
                         str(Path('Aspidites/_vendor/contracts/library/scoped_variables.py')),
                         str(Path('Aspidites/_vendor/contracts/library/array.py')),
                         str(Path('Aspidites/_vendor/contracts/library/sets.py')),
                         str(Path('Aspidites/_vendor/contracts/library/dummy.py')),
                         str(Path('Aspidites/_vendor/contracts/library/dicts.py')),
                         str(Path('Aspidites/_vendor/contracts/library/compositions.py')),
                         str(Path('Aspidites/_vendor/contracts/library/strings.py')),
                         str(Path('Aspidites/_vendor/contracts/library/isinstance_imp.py')),
                         str(Path('Aspidites/_vendor/contracts/library/seq.py')),
                         str(Path('Aspidites/_vendor/contracts/useful_contracts/numbers.py')),
                         str(Path('Aspidites/_vendor/contracts/useful_contracts/numpy_specific.py')),
                         str(Path("Aspidites/_vendor/fn/func.py")),
                         str(Path("Aspidites/_vendor/fn/iters.py")),
                         str(Path("Aspidites/_vendor/fn/op.py")),
                         str(Path("Aspidites/_vendor/fn/recur.py")),
                         str(Path("Aspidites/_vendor/fn/stream.py")),
                         str(Path("Aspidites/_vendor/fn/underscore.py")),
                         str(Path("Aspidites/_vendor/fn/uniform.py")),
                         str(Path('Aspidites/_vendor/decorator_extension.py')),
                         str(Path('Aspidites/_vendor/pyparsing_extension.py')),
                         str(Path('Aspidites/parser/convert.py')),
                         str(Path('Aspidites/parser/reserved.py')),
                         str(Path('Aspidites/parser/parser.py')),
                         str(Path('Aspidites/templates.py')),
                         str(Path('Aspidites/monads.py')),
                         str(Path('Aspidites/math.py')),
                         str(Path('Aspidites/api.py')),
                         str(Path('Aspidites/__main__.py')),
                         str(Path('Aspidites/compiler.py'))
                         ])
from Aspidites import __version__, __license__, __title__, __author__, compiler, parser
from Aspidites.__main__ import get_cy_kwargs
cy_kwargs = get_cy_kwargs()
cy_kwargs.update(embed="'main'")
code = open(Path('Aspidites/woma/library.wom'), 'r').read()
cy_kwargs.update(
    code=parser.parse_module(code),
    force=True,
    fname='Aspidites/woma/library.pyx',
    bytecode=False,
    c=True,
    verbose=0,
    build_requires=''
)
compiler.Compiler(**cy_kwargs)


def read(fname):
    return open(Path(fname).absolute()).read()


# Tested with wheel v0.29.0, 0.36.2
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


class InstallWrapper(install):
    """Provides a install wrapper for native woma
    extensions. These don't really belong in the
    Python package."""

    def run(self):
        # Run this first so the install stops in case
        # these fail otherwise the Python package is
        # successfully installed
        print("running preinstall hooks")
        self.preinstall()
        install.run(self)  # pip install
        print("running postinstall hooks")
        self.postinstall()

    def preinstall(self):
        """preinstall hook"""
        # target = Path('build/lib/Aspidites/woma/library.wom')
        # output = Path('build/lib/Aspidites/woma/library.pyx')
        # c = "Aspidites %s -c -o %s --embed=True" % (target, output)
        # os.popen(c)
        # print(c)
        pass

    def postinstall(self):
        """postinstall hook"""
        pass


setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email="rjdbcm@mail.umkc.edu",
    description="Aspidites is the reference implementation of the Woma Language",
    license=__license__,
    keywords="language",
    url="https://github.com/rjdbcm/Aspidites",
    install_requires=[
        'pyrsistent',
        'numpy',
        'cython>0.28,<3',
        'pyparsing',
        'mypy',
        'pytest',
        'pytest-xdist',
        'pytest-mock',
        'hypothesis',
        'future'
        ],
    packages=find_packages(),
    include_dirs=[numpy.get_include()],
    ext_modules=ext_modules,
    test_suite='Aspidites/tests',
    distclass=Distribution if sys.platform != 'darwin' else BinaryDistribution,
    entry_points={'console_scripts': ['aspidites = Aspidites.__main__:main']},
    package_data={'': ["*.wom", "*.pyx", "*.pyi", "*.so", "*.c", "Aspidites/py.typed"]},  # add any native *.wom files
    long_description=read('README.md'),
    cmdclass={'install': InstallWrapper},
    long_description_content_type='text/markdown',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Other",
        # "Programming Language :: Python :: 3.6", EOL in December 2021 and don't want to vendor dataclasses
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: Implementation :: PyPy", looks like a no go
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Compilers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: BSD License",
        # "License :: OSI Approved :: Zope Public License (ZPL)", ??? Invalid
        "License :: OSI Approved :: Apache Software License",
    ],
)
