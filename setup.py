#!/usr/bin/python3
import os
import sys

from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install
from Aspidites import __version__, __license__, __title__, __author__, compiler, parser
from Aspidites.__main__ import get_cy_kwargs

cy_kwargs = get_cy_kwargs()
cy_kwargs.update({'embed': True})
code = open('Aspidites/woma/library.wom', 'r').read()
cy_kwargs.update(
    code=parser.parse_module(code),
    force=True,
    fname='Aspidites/woma/library.pyx',
    bytecode=True,
    c=True,
    verbose=0,
    build_requires=''
)
compiler.compile_module(**cy_kwargs)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


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
        c = "Aspidites build/lib/Aspidites/woma/library.wom -c -o build/lib/Aspidites/woma/library.pyx --embed=True"
        os.popen(c)
        print(c)
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
    test_suite='Aspidites/tests',
    distclass=Distribution if sys.platform != 'darwin' else BinaryDistribution,
    entry_points={'console_scripts': ['aspidites = Aspidites.__main__:main']},
    package_data={'': ["*.wom", "*.pyx", "*.pyi"]},  # add any native *.wom files
    long_description=read('README.md'),
    cmdclass={'install': InstallWrapper},
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Other",
        "Programming Language :: Python :: 3.9",
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
