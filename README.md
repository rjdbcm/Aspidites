# Aspidites

Aspidites programming language.

## Implementation

Aspidites (shield-bearer) is written in python and targets Cython

### Core Dependencies

- Cython
- Pyrsistent
- PyParsing

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

- Terseness that mixes keywords and symbolic operations in order to make code both concise ___and___ readable.
- Great for writing high-integrity code that works natively with CPython.
- Usable for general purpose ___or___ scientific computing.

# Syntax

| Verbage  | Symbol | Example                                               |
|:---------|:-------|:------------------------------------------------------|
| respects | `->`     | `identifier` `->` `constraining clauses`                    |
| imposes  | `<-`     | `identifier` `<-` `imposed clauses`                         |
| loops    | `<@> `   | `identifier` `<@>` `iterable container`<br>`indent` `...` |
| maybe    | `<>`     | `<>` `callable reference`                                  |
| surely   | `[]`     | `[]` `callable reference`                                  |
| return   | `<*>`    | `<*>` `statement `                                        |
| pragma   |  `#`     | `#` `compiler directive`

