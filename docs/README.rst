README
======

The reference implementation of the `Woma programming
language <https://www.github.com/rjdbcm/woma>`__ compiler. There is also
a genus of Python called *Aspidites*, latin for shield-bearer, that is
this project's namesake.

Installing
~~~~~~~~~~

PyPI
^^^^

|PyPI|\ |PyPI - Wheel|

.. code:: shell

    $ pip install Aspidites

Docker
^^^^^^

|Docker Image Version (latest by date)|\ |Docker Image Size (latest
semver)|

.. code:: shell

    $ docker pull ghcr.io/rjdbcm/aspidites:latest

Github
^^^^^^

|GitHub release (latest SemVer)|\ |GitHub commits since tagged version
(branch)|

.. code:: shell

    $ gh repo clone rjdbcm/Aspidites

Running
~~~~~~~

Pretty straightforward just use:

.. code:: shell

    $ aspidites -h

Or with docker:

.. code:: shell

    $ docker run -v $PWD:/workdir rjdbcm/aspidites:latest -h

Paradigms
~~~~~~~~~

-  `refinement-type system <https://arxiv.org/pdf/2010.07763.pdf>`__
-  `pragmatic <https://www.adaic.org/resources/add_content/standards/05rm/html/RM-2-8.html>`__
-  declarative
-  `functional <https://towardsdatascience.com/why-developers-are-falling-in-love-with-functional-programming-13514df4048e?gi=3361de79dc98>`__
-  `constrained logic <https://www.cse.unsw.edu.au/~tw/brwhkr08.pdf>`__

Inspirations
~~~~~~~~~~~~

-  `coconut <http://coconut-lang.org/>`__
-  `Ada <https://www.adacore.com/get-started>`__
-  `Scala <https://www.scala-lang.org/>`__
-  `Prolog <https://www.swi-prolog.org/features.html>`__
-  `Curry <https://curry.pages.ps.informatik.uni-kiel.de/curry-lang.org/>`__
-  `Cobra <http://cobra-language.com/>`__
-  `J <https://www.jsoftware.com/#/README>`__
-  `ELI <https://fastarray.appspot.com/index.html>`__

Goals
~~~~~

-  Ultra-smooth runtime exception handling with useful warnings.
-  Demonic non-determinism, favors non-termination and type-negotiation
   (constraint satisfaction).
-  Terseness that mixes keywords and symbolic operations in order to
   make code both concise ***and*** readable.
-  Great for writing high-integrity code that works natively with
   CPython.
-  Usable for general purpose ***or*** scientific computing.

.. |GitHub release (latest SemVer)| image:: https://img.shields.io/github/v/release/rjdbcm/Aspidites?color=pink&label=&logo=github&logoColor=black
.. |GitHub commits since tagged version (branch)| image:: https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main
.. |PyPI| image:: https://img.shields.io/pypi/v/aspidites?color=pink&label=&logo=pypi
   :target: https://pypi.org/project/Aspidites/
.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/Aspidites
   :target: https://pypi.org/project/Aspidites/#files
.. |Docker Image Version (latest by date)| image:: https://img.shields.io/docker/v/rjdbcm/aspidites?color=pink&label=%20&logo=docker
.. |Docker Image Size (latest semver)| image:: https://img.shields.io/docker/image-size/rjdbcm/aspidites
    :target: https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated
.. |Continuous Integration| image:: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml/badge.svg
   :target: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/8d03ef8667df59d55380/maintainability
   :target: https://codeclimate.com/github/rjdbcm/Aspidites/maintainability
.. |codecov| image:: https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0
   :target: https://codecov.io/gh/rjdbcm/Aspidites
.. |logo| image:: https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_wheelie.png
