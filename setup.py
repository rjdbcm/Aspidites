#!/usr/bin/python3
import os
from setuptools import setup, find_packages
from Aspidites import __version__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Aspidites",
    version=__version__,
    author="Ross J. Duff",
    author_email="",
    description="Aspidites is the reference implementation of the Woma Language",
    license="LGPL",
    keywords="language",
    url="https://github.com/rjdbcm/Aspidites",
    packages=find_packages(),
    entry_points={'console_scripts': ['aspidites = Aspidites.__main__:main']},
    package_data={'': ["*.wom"]},  # add any native *.wom files
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
)