# Aspidites

Aspidites is the reference implementation of the Woma programming language compiler.

### Core Dependencies

- Cython
- Pyrsistent
- PyParsing
- MyPy
- Optional(NumPy)

## Paradigms

- `negotiably-typed`
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

| Verbage   | Symbol   | Example                                                       |
|:----------|:---------|:--------------------------------------------------------------|
| respects<br>✅| `->`     | `identifier` `->` `constraining clauses`                    |
| imposes<br>✅| `<-`     | `identifier` `<-` `imposed clauses`                         |
| loops<br>❌| `<@> `   | `identifier` `<@>` `iterable container`<br>`indent` `...`   |
| return  <br>✅| `<*>`    | `<*>` `statement `                                          |
| pragma  <br>❌|  `#`     | `#` `compiler directive`                                    |

