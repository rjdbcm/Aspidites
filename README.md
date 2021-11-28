<a href="https://mobile.twitter.com/WheelieTheWoma"><img align="left" width="80" height="80" src="https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_wheelie.png" alt="Wheel the Woma"></a>

![stability](https://img.shields.io/badge/stability-stable-green) 
![GitHub Integration Status](https://img.shields.io/github/workflow/status/rjdbcm/Aspidites/Continuous%20Integration?label=Continous%20Integration&logo=github) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rjdbcm/Aspidites/Continuous%20Deployment?label=Continous%20Deployment&logo=github) [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/rjdbcm/Aspidites)](https://codeclimate.com/github/rjdbcm/Aspidites/maintainability) ![Lines of code](https://img.shields.io/badge/total%20lines-2.3k-green) [![codecov](https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0)](https://codecov.io/gh/rjdbcm/Aspidites) [![wakatime](https://wakatime.com/badge/user/7e591977-4df7-4d68-8463-9d6e7501a346/project/94018e6c-3d61-4301-a40e-7eb270b74563.svg)](https://wakatime.com/badge/user/7e591977-4df7-4d68-8463-9d6e7501a346/project/94018e6c-3d61-4301-a40e-7eb270b74563)
![GitHub top language](https://img.shields.io/github/languages/top/rjdbcm/Aspidites)
![platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
[![Twitter Follow](https://img.shields.io/twitter/follow/WheelieTheWoma?style=social)](https://mobile.twitter.com/WheelieTheWoma)

* * *

| English | [中文](http://aspidites.org/README_Zh_CN.html) |

* * *

- Who is the [Woma programming language](http://aspidites.org/woma) for?  

    - First and foremost it is for people wanting to write CPython extensions fast, like *really* fast. Traditionally these are written in C. Woma has the advantage of being shorthand for well constrained and type-checked Python Extensions.

- Isn't this just Cython with extra steps? 

    - Technically yes, but with totally different goals. Cython intends to be a syntactic superset of python where Woma syntax has taken inspiration from a variety of sources. You can think of Aspidites as a wrapper for Cython that parses Woma code into Cython's python superset with added support for contracts and nil-tracking. Cython does much of the "heavy lifting". The specifics of the Woma Programming Language are being standardized as a series of WEEPs ([Woma Extension and Evaluation Proposals](http://aspidites.org/woma/QQ.html)).
    
 - Why use the name _Aspidites_? What's a Woma?
 
    - There is also a genus of Python called _Aspidites_, latin for shield-bearer, that is this project's namesake. They are endemic to mainland Australia and are also known as the Woma Python.
  
- How do I get Aspidites?
    
    - We maintain several packages for Aspidites, however, we *recommend* using the PyPI install for the latest stable version. Docker is the place to go for the bleeding edge development versions of Aspidites.

- How do I actually learn the Woma Programming Language?
    
    - Use the docs found at [docs.aspidites.org](http://docs.aspidites.org/)

### Installing
---------
[![PyPI](https://img.shields.io/pypi/v/aspidites?label=PyPI&logo=pypi)](https://pypi.org/project/Aspidites/)[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Aspidites)](https://pypi.org/project/Aspidites/#files)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Aspidites?label=CPython)![PyPI - Downloads](https://img.shields.io/pypi/dm/Aspidites)
```
$ pip install Aspidites
```
-----------
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/rjdbcm/aspidites?label=Docker&logo=docker)[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/rjdbcm/aspidites)](https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated)![Docker Pulls](https://img.shields.io/docker/pulls/rjdbcm/aspidites)
```
$ docker pull ghcr.io/rjdbcm/aspidites:latest
```
-----------
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/rjdbcm/Aspidites?label=Github&logo=github&logoColor=black)![GitHub commits since tagged version (branch)](https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main)
```
$ gh repo clone rjdbcm/Aspidites
```

### Running
Pretty straightforward just use:
```shell
$ aspidites -h
```

Or with docker:
```shell
$ docker run -v $PWD:/workdir rjdbcm/aspidites:latest -h
```

## Paradigms

- [`refinement-type system`](https://arxiv.org/pdf/2010.07763.pdf)
- [`pragmatic`](https://www.adaic.org/resources/add_content/standards/05rm/html/RM-2-8.html)
- [`functional`](https://towardsdatascience.com/why-developers-are-falling-in-love-with-functional-programming-13514df4048e?gi=3361de79dc98)

## Philosophy

-  Words should be for the programmer and the data model not built-in language features.
-  A programmers focus should be on the logic of the program not trying to remember methods and namespaces.
-  The off-sides rule is sufficient to delineate scope, but should be limited in it's ability to nest.

## Goals

- Ultra-smooth runtime exception handling with useful warnings.
- Demonic non-determinism, favors non-termination and type-negotiation (constraint satisfaction).
- Terseness, symbolic operations are used to make code both concise ___and___ readable.
- Great for writing high-integrity code that works natively with CPython.
- Usable for general purpose ___or___ scientific computing.

## Examples

```
(Greeter(name -> str)) procedure    
    <*>print('Greetings,', name)
```

```
`Scala-style anonymous functions`
scala = (_ * 2)
val = scala(_ + _)
val(2, 3)
>>> 10
```

# Logo/Mascot
Wheelie the Woma™ and Woma Programming Language™ are unregistered trademarks of Ross J. Duff. 
The logos are copyright © Ross J. Duff but may be transferred to an appropriate trust at a later date.
This is to prevent confusing/malicious use.


# Contributing

If you'd like to help with the Aspidites project as a developer check out the Issues page or fork and make a pull request.
Now, for early woma adopters that do not wish to write any Python, reporting issues is always appreciated.
If you'd like to help out financially, Aspidites' maintainer accepts donations.

<a href="https://liberapay.com/rjdbcm/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a> <a href="https://www.buymeacoffee.com/woma"><img height=29 src=https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/bmc.png></a>

# Information for Developers
[![libraries.io](https://img.shields.io/badge/Libraries.io--inactive)](https://libraries.io/github/rjdbcm/Aspidites)

## Core Dependencies
Aspidites has just 3 core dependencies, two required and one optional, one all licensed under a compatible OSI approved license. In general, dependencies are vendored unless they are commonly-used libraries. 

Required:
- cython
- future

Optional:
- numpy

In addition to the core dependencies are the 4 optional dependencies, all licensed under a compatible OSI approved license, needed to run the canned test-suite.
- pytest
- pytest-xdist
- pytest-mock
- hypothesis

## Copying
![GitHub](https://img.shields.io/github/license/rjdbcm/Aspidites)

## Additional License Info
The following 3rd-party software packages may be distributed with <b>Aspidites</b>:  

### awesome-pattern-matching
Pattern Matching for Python 3.7+ in a simple, yet powerful, extensible manner. 

- Author: Julian Fleischer [(scravy)](https://github.com/scravy)
- License: MIT

### contracts
PyContracts is a Python package that allows to declare constraints on function parameters and return values. Contracts can be specified using Python3 annotations, or inside a docstring. PyContracts supports a basic type system, variables binding, arithmetic constraints, and has several specialized contracts and an extension API. 

- Author: Andrea Censi [(AndreaCensi)](https://github.com/AndreaCensi)
- License: LGPL

### fn
Functional programming in Python: implementation of missing features to enjoy FP 

- Author: Oleksii Kachaiev [(kachayev)](https://github.com/kachayev)
- License: Apache 2.0

### pyparsing
Python library for creating PEG parsers.

- Author: Paul McGuire [(ptmcg)](https://github.com/ptmcg)
- License: MIT

### pyrsistent
Persistent/Immutable/Functional data structures for Python.

- Author: Tobias Gustafsson [(tobgu)](https://github.com/tobgu)
- License: MIT

### python-semanticversion
Semantic version comparison for Python (see http://semver.org/)

- Author: Raphaël Barrois [(rbarrois)](https://github.com/rbarrois)
- License: BSD 2 Clause

### RestrictedPython
 A restricted execution environment for Python to run untrusted code.
 
- Author: Zope Foundation [(zopefoundation)](https://github.com/zopefoundation)
- License: Zope Public License

