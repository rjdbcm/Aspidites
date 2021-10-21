.. Aspidites documentation master file, created by
   sphinx-quickstart on Sun Aug 15 16:48:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Woma Programming Language!
=========================================

The reference implementation of the `Woma programming
language <https://www.github.com/rjdbcm/woma>`__ compiler. There is also
a genus of Python called *Aspidites*, latin for shield-bearer, that is
this project's namesake.

Installing
~~~~~~~~~~


.. tabs::

    .. group-tab:: PyPI

        |PyPI|\ |PyPI - Wheel|

        .. code:: shell

            $ pip install Aspidites

    .. group-tab:: Docker

        |Docker Image Version (latest by date)|\ |Docker Image Size (latest semver)|

        .. code:: shell

            $ docker pull ghcr.io/rjdbcm/aspidites:latest

    .. group-tab:: Github

        |GitHub commits since tagged version (branch)|

        .. code:: shell

            $ gh repo clone rjdbcm/Aspidites && pip install ./Aspidites

Running
~~~~~~~

Pretty straightforward just use:

.. tabs::

    .. group-tab:: PyPI

        .. code:: shell

            $ aspidites -h

    .. group-tab:: Docker

        .. code:: shell

            $ docker run -v $PWD:/workdir rjdbcm/aspidites:latest -h

    .. group-tab:: Github

        .. code:: shell

            $ aspidites -h


Paradigms
~~~~~~~~~

.. tabs::

    .. tab:: Refinement Type System

        This means Woma uses a simple predicate logic to create well-constrained types. This is currently implemented using `AndreaCensi/contracts <https://github.com/AndreaCensi/contracts>`_. More info on refinement type systems:

            "Refinement types enrich a language's type system with logical predicates that circumscribe the set of values
            described by the type, thereby providing software developers a tunable knob with which to inform the type
            system about what invariants and correctness properties should be checked on their code. In this article,
            we distill the ideas developed in the substantial literature on refinement types into a unified tutorial
            that explains the key ingredients of modern refinement type systems. In particular, we show how to implement
            a refinement type checker via a progression of languages that incrementally add features to the language or
            type system."

         Reference: Jhala, R. and Vazou, N., 2020. Refinement Types: A Tutorial. arXiv preprint arXiv:2010.07763. `Read More <https://arxiv.org/pdf/2010.07763.pdf>`__

    .. tab:: Pragmatic

        Compiler and testing directives as pragmas that are used inline in woma, this is similar to how pragmas are used in Ada.
        `Read More <https://www.adaic.org/resources/add_content/standards/05rm/html/RM-2-8.html>`__

    .. tab:: Functional

        Functions are first class citizens in woma. More info on functional programming:

            "In 1989 when functional programming was still considered a niche topic, Hughes wrote a visionary paper
            arguing convincingly ‘why functional programming matters’. More than two decades have passed.
            Has functional programming really mattered? Our answer is a resounding ‘Yes!’. Functional programming is now
            at the forefront of a new generation of programming technologies, and enjoying increasing popularity and
            influence. In this paper, we review the impact of functional programming, focusing on how it has changed
            the way we may construct programs, the way we may verify programs, and fundamentally the way we may think
            about programs."

        Reference:
        Zhenjiang Hu, John Hughes, Meng Wang, How functional programming mattered, National Science Review, Volume 2, Issue 3, September 2015, Pages 349–370,
        `Read More <https://doi.org/10.1093/nsr/nwv042>`__

    .. tab:: Constrained Logic

        Constraint satisfaction is core to woma, should constraints not be satisfied for a given function nullity is returned rather than raising an exception.
        More about constraint programming:

            "A discrete optimization problem can be given a declarative or procedural formulation, and
            both have their advantages. A declarative formulation simply states the constraints and
            objective function. It allows one to describe what sort of solution one seeks without the
            distraction of algorithmic details. A procedural formulation specifies how to search for a
            solution, and it therefore allows one to take advantage of insight into the problem in order
            to direct the search. The ideal, of course, would be to have the best of both worlds, and
            this is the goal of constraint programming."

        Reference:
        Alexander Bockmayr, John N. Hooker, Constraint programming, May 2003,
        `Read More <https://public.tepper.cmu.edu/jnh/cp-hb.pdf>`__

Inspirations
~~~~~~~~~~~~

-  `Ada <https://www.adacore.com/get-started>`__
-  `Scala <https://www.scala-lang.org/>`__
-  `Prolog <https://www.swi-prolog.org/features.html>`__
-  `Curry <https://curry.pages.ps.informatik.uni-kiel.de/curry-lang.org/>`__
-  `Cobra <http://cobra-language.com/>`__
-  `ELI <https://fastarray.appspot.com/index.html>`__

Motivation
~~~~~~~~~~

-  Words should be for the programmer and the data model not built-in language features.
-  A programmers focus should be on the logic of the program not trying to remember methods and namespaces.
-  The off-sides rule is sufficient to delineate scope, but should be limited in it's ability to nest.

Goals
~~~~~

-  Ultra-smooth runtime exception handling with useful warnings.
-  Demonic non-determinism, favors non-termination and type-negotiation
   (constraint satisfaction).
-  Terseness that uses symbolic operations in order to
   make code both concise ***and*** readable.
-  Great for writing high-integrity code that works natively with
   CPython.
-  Usable for general purpose ***or*** scientific computing.

.. |GitHub release (latest SemVer)| image:: https://img.shields.io/github/v/release/rjdbcm/Aspidites?color=grey&label=%20&logo=github&style=for-the-badge
.. |GitHub commits since tagged version (branch)| image:: https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main?style=for-the-badge
.. |PyPI| image:: https://img.shields.io/pypi/v/aspidites?color=grey&label=%20&style=for-the-badge&logo=python
.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/Aspidites?logo=python&logoColor=lightblue&style=for-the-badge
.. |Docker Image Version (latest by date)| image:: https://img.shields.io/docker/v/rjdbcm/aspidites?color=grey&label=%20&logo=docker&style=for-the-badge
.. |Docker Image Size (latest semver)| image:: https://img.shields.io/docker/image-size/rjdbcm/aspidites?style=for-the-badge
.. |Continuous Integration| image:: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml/badge.svg
   :target: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/8d03ef8667df59d55380/maintainability
   :target: https://codeclimate.com/github/rjdbcm/Aspidites/maintainability
.. |codecov| image:: https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0
   :target: https://codecov.io/gh/rjdbcm/Aspidites
.. |logo| image:: https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_wheelie.png

Table of Contents
~~~~~~~~~~~~~~~~~

.. toctree::
   :numbered:
   :maxdepth: 4

   syntax
   usage
   indepth
   builtins
   api
   devinfo

