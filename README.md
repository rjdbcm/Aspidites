# Aspidites [![codecov](https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0)](https://codecov.io/gh/rjdbcm/Aspidites)

Aspidites is the reference implementation of the [Woma programming language](https://www.github.com/rjdbcm/woma) compiler.

### Core Dependencies

- Cython
- Pyrsistent
- PyParsing
- MyPy
- NumPy

## Paradigms

- `refinement-type system`
- `pragmatic`
- `declarative`
- `functional`
- `constrained logic`

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
- Demonic non-determinism, favors non-termination and type-negotiation.
- Terseness that mixes keywords and symbolic operations in order to make code both concise ___and___ readable.
- Great for writing high-integrity code that works natively with CPython.
- Usable for general purpose ___or___ scientific computing.

# Syntax

| Working?      | Symbol        | Verbage             |  Example                                                       |
|:--------------|:--------------|:--------------------|:---------------------------------------------------------------|
| ✅            | `->`          |respects             | `identifier` `->` `constraining clauses`                       |
| ✅            | `<-`          |imposes              | `identifier` `<-` `imposed clauses`                            |
| ❌            | `<@> `        |loops                | `identifier` `<@>` `iterable container`<br>`indent` `...`      |
| ✅            | `<*>`         |return               | `<*>` `statement `                                             |
| ✅            |  `#`          |pragma               | `#` `compiler directive`                                       |

# Examples

```
(Greeter(name -> str)) procedure
    <*>print('Greetings,', name)

```
