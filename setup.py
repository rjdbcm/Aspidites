#!/usr/bin/python3
import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from Aspidites import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class InstallWrapper(install):
    """Provides a install wrapper for native woma
    extensions. These don't really belong in the
    Python package."""

    def run(self):
        # Run this first so the install stops in case
        # these fail otherwise the Python package is
        # successfully installed
        self.preinstall()
        # Run the standard PyPi copy
        install.run(self)
        self.postinstall()

    def preinstall(self):
        """preinstall hook"""
        ...

    def postinstall(self):
        """postinstall hook"""
        ...


setup(
    name="Aspidites",
    version=__version__,
    author="Ross J. Duff",
    author_email="",
    description="Aspidites is the reference implementation of the Woma Language",
    license="GPL",
    keywords="language",
    url="https://github.com/rjdbcm/Aspidites",
    packages=find_packages(),
    entry_points={'console_scripts': ['aspidites = Aspidites.__main__:main']},
    package_data={'': ["*.wom"]},  # add any native *.wom files
    long_description=read('README.md'),
    cmdclass={'install': InstallWrapper},
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
)
