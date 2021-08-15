# Aspidites [![Continuous Integration](https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml/badge.svg)](https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0)](https://codecov.io/gh/rjdbcm/Aspidites)

The reference implementation of the [Woma programming language](https://www.github.com/rjdbcm/woma) compiler. There is also a genus of Python called _Aspidites_, latin for shield-bearer, that is this project's namesake.<p align="center">![logo](docs/_static/aspidites_logo.png)</p>

### Installing
#### PyPI
[![PyPI](https://img.shields.io/pypi/v/aspidites?color=pink&label=&logo=pypi)](https://pypi.org/project/Aspidites/)[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Aspidites)](https://pypi.org/project/Aspidites/#files)
```
$ pip install Aspidites
```

#### Docker
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/rjdbcm/aspidites?color=pink&label=&logo=docker)](https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated)[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/rjdbcm/aspidites)](https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated)
```
$ docker pull rjdbcm/aspidites
```

#### Github
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/rjdbcm/Aspidites?color=pink&label=%20&logo=github&logoColor=black)![GitHub commits since tagged version (branch)](https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main)
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
$ docker run -v $PWD:/usr/src/app rjdbcm/aspidites:v0.6.1 -h
```

## Paradigms

- [`refinement-type system`](https://arxiv.org/pdf/2010.07763.pdf)
- [`pragmatic`](https://www.adaic.org/resources/add_content/standards/05rm/html/RM-2-8.html)
- `declarative`
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
| ❌            | `<@> `        |loops                | `identifier` `<@>` `iterable container`<br>`indent` `...`      |
| ✅            | `<*>`         |return               | `<*>` `statement `                                             |
| ✅            |  `#`          |pragma               | `#` `compiler directive`                                       |



## Examples

```
(Greeter(name -> str)) procedure
    <*>print('Greetings,', name)

```

# Contributing

If you'd like to help with the Aspidites project as a developer check out the Issues page or fork and make a pull request.
Now, for early woma adopters that do not wish to write any Python, reporting issues is always appreciated.
If you'd like to help out financially, Aspidites' maintainer accepts [Liberapay](https://liberapay.com/rjdbcm/).

# Copying
![GitHub](https://img.shields.io/github/license/rjdbcm/Aspidites)

# Information for Developers
[![libraries.io](https://img.shields.io/badge/Libraries.io--inactive)](https://libraries.io/github/rjdbcm/Aspidites)

### Core Dependencies
Aspidites has 7 core dependencies. In general, dependencies are vendored unless they contain Python Extensions.
- Cython
- Pyrsistent
- PyParsing
- MyPy
- PyTest
- NumPy
- future

