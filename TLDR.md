# Aspidites 
[![Continuous Integration](https://github.com/rjdbcm/Aspidites/actions/workflows/ci.yml/badge.svg)](https://github.com/rjdbcm/Aspidites/actions/workflows/ci.yml) [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/rjdbcm/Aspidites)](https://codeclimate.com/github/rjdbcm/Aspidites/maintainability) [![codecov](https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0)](https://codecov.io/gh/rjdbcm/Aspidites)
![GitHub top language](https://img.shields.io/github/languages/top/rjdbcm/Aspidites)
![platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
----------------
The reference implementation of the [Woma programming language](https://www.github.com/rjdbcm/woma) compiler. There is also a genus of Python called _Aspidites_, latin for shield-bearer, that is this project's namesake. We maintain several packages for Aspidites, however, we *recommend* using the PyPI install for the latest stable version. Docker is the place to go for the bleeding edge development versions of Aspidites.
### Installing
---------
[![PyPI](https://img.shields.io/pypi/v/aspidites?label=PyPI&logo=pypi)](https://pypi.org/project/Aspidites/)[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Aspidites)](https://pypi.org/project/Aspidites/#files)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Aspidites?label=CPython)![PyPI - Downloads](https://img.shields.io/pypi/dd/Aspidites)
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
- [`constrained logic`](https://www.cse.unsw.edu.au/~tw/brwhkr08.pdf)

## Inspirations

- [`coconut`](http://coconut-lang.org/)
- [`Ada`](https://www.adacore.com/get-started)
- [`Scala`](https://www.scala-lang.org/)
- [`Prolog`](https://www.swi-prolog.org/features.html)
- [`Curry`](https://curry.pages.ps.informatik.uni-kiel.de/curry-lang.org/)
- [`Cobra`](http://cobra-language.com/)
- [`J`](https://www.jsoftware.com/#/README)
- [`ELI`](https://fastarray.appspot.com/index.html)

## Goals

- Ultra-smooth runtime exception handling with useful warnings.
- Demonic non-determinism, favors non-termination and type-negotiation (constraint satisfaction).
- Terseness that mixes keywords and symbolic operations in order to make code both concise ___and___ readable.
- Great for writing high-integrity code that works natively with CPython.
- Usable for general purpose ___or___ scientific computing.

# Syntax

## Lexicon

| Working?      | Symbol        | Verbage             |  Example                                                       |
|:--------------|:--------------|:--------------------|:---------------------------------------------------------------|
| ✅            | `->`          |respects             | `identifier` `->` `constraining clauses`                       |
| ✅            | `<-`          |imposes              | `identifier` `<-` `imposed clauses`                            |
| ✅            | `<*>`         |return               | `<*>` `statement `                                             |
| ✅            |  `#`          |pragma               | `#` `compiler directive`                                       |
| ✅            | ``))``        |return respects      | ``))`` ``return constraints``                                  |                                           
| ✅            | ``(G(``       |define G as function | ``(`` ``FuncName`` ``(`` ``identifier`` ``->`` ``constraining clauses`` ``;`` ``...`` ``))`` ``return constraints`` |


## Examples

```
(Greeter(name -> str)) procedure
    <*>print('Greetings,', name)

main:
Greeter("Aspidites user")

```
# Logo/Mascot
Wheelie the Woma™ and Woma Programming Language™ are unregistered trademarks of Ross J. Duff. 
The logos are copyright © Ross J. Duff but may be transferred to an appropriate trust at a later date.
This is to prevent confusing/malicious use.<p align="center">[![logo](https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_wheelie_96_96.png)](https://mobile.twitter.com/WheelieTheWoma)</p><p align="center">[![Twitter Follow](https://img.shields.io/twitter/follow/WheelieTheWoma?style=social)](https://mobile.twitter.com/WheelieTheWoma )</p>


# Contributing

If you'd like to help with the Aspidites project as a developer check out the Issues page or fork and make a pull request.
Now, for early woma adopters that do not wish to write any Python, reporting issues is always appreciated.
If you'd like to help out financially, Aspidites' maintainer accepts [Liberapay](https://liberapay.com/rjdbcm/).

# Information for Developers
[![libraries.io](https://img.shields.io/badge/Libraries.io--inactive)](https://libraries.io/github/rjdbcm/Aspidites)

## Core Dependencies
Aspidites has 10 core dependencies, all licensed under a compatible OSI approved license. In general, dependencies are vendored unless they contain Python Extensions.
- cython
- pyrsistent
- pyparsing
- mypy
- pytest
- pytest-xdist
- pytest-mock
- numpy
- future
- hypothesis

## Copying
![GitHub](https://img.shields.io/github/license/rjdbcm/Aspidites)
