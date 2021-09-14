#!/usr/bin/python3
import sys
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install
# ~#~ # Build static libs # ~#~ #
from Cython.Build import cythonize
ext_modules = cythonize([str(Path('Aspidites/monads.py')), str(Path('Aspidites/math.py'))])
from Aspidites import __version__, __license__, __title__, __author__, compiler, parser
from Aspidites.__main__ import get_cy_kwargs
cy_kwargs = get_cy_kwargs()
cy_kwargs.update(embed="'main'")
code = open(Path('Aspidites/woma/library.wom'), 'r').read()
cy_kwargs.update(
    code=parser.parse_module(code),
    force=True,
    fname='Aspidites/woma/library.pyx',
    bytecode=True,
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
    ext_modules=ext_modules,
    test_suite='Aspidites/tests',
    distclass=Distribution if sys.platform != 'darwin' else BinaryDistribution,
    entry_points={'console_scripts': ['aspidites = Aspidites.__main__:main']},
    package_data={'': ["*.wom", "*.pyx", "*.pyi", "*.so", "*.c"]},  # add any native *.wom files
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
