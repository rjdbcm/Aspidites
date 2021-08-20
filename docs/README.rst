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

Syntax
======

Lexicon
~~~~~~~

+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| Working?   | Symbol    | Verbage             | Example                                                                                                           |
+============+===========+=====================+===================================================================================================================+
| ✅         | ``->``    | respects            | ``identifier`` ``->`` ``constraining clauses``                                                                    |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``<-``    | imposes             | ``identifier`` ``<-`` ``imposed clauses``                                                                         |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ❌         | ``<@>``   | loops               | ``identifier`` ``<@>`` ``iterable container``\ \ ``indent`` ``...``                                               |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``<*>``   | return              | ``<*>`` ``statement``                                                                                             |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``#``     | pragma              | ``#`` ``compiler directive``                                                                                      |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``))``    | return respects     | ``))`` ``return constraints``                                                                                     |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``(G(``   | define G as function| ``(`` ``FuncName`` ``(`` ``identifier`` ``->`` ``constraining clauses`` ``))`` ``return constraints``             |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+

Examples
~~~~~~~~

First Class Functions
^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    #cython.binding(True)
    (Add(x = 3 -> int; y = 3 -> int)) int
        <*>x+y

Generators, Procedures, and Coroutines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `generators`
    (Yield123()) coroutine
        <^>Add(0, 1)
        <^>Add(0, 2)
        <^>Add(0, 3)

    `procedures`
    (Hello()) procedure
        print("Hello, World!")

    `coroutines`
    (Hello2()) coroutine
        <^>Hello()

Persistent Evolvable Iterables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `persistent vectors`
    D = [2, 4, 6, 8, 10]

    `persistent sets`
    G = {'a', 'b', 'c'}

    `persistent mappings`
    C = {'a': (3+5),
         'b': 8,
         'c': True,
           4: None,
         'd': 6**2*5+3}

Refinement Types use Contract Clauses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `new contracts can impose more complex contractual clauses`
    colors <- list[3](int, <256, >=0)

Closures and Lambdas
^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `any woma function can be closed in place to become an instance that complies with the`
    `type specification or Undefined for instances that breach the type specification contract`
    x = Add(3, 3)...

    `seamless exception handling allows tracing of undefined code branches`
    y = Add(4, 3.5)...

    `mixed usage of closure and regular function calls`
    z = Add(x(), 3)

    `Scala-style closure functions`
    scala = (_ * 2)
    val = scala(_ + _)
    val = val(scala)...

Undefined() as the Nullity Element
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `modulus and division by 0 handled by returning Undefined()`
    denom = 0
    div_by_zero = 1 / denom
    mod_zero = 1 % denom
    div_by_zero2 = 1 / 0
    mod_zero2 = 1 % 0

Optional Structured Entrypoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `main: structure for executable actions when run as a binary`
    (Hello()) procedure
        print("Hello, World!")

    main:
    Hello()
    print("I'm a binary.")


Logo/Mascot
===========

| Wheelie the Woma™ and Woma Programming Language™ are unregistered trademarks of Ross J. Duff.
| The logos/mascots (stored in docs/_static as .png files)
| are copyright © Ross J. Duff but may be transferred to an
| appropriate trust at a later date.
| This is to prevent confusing/malicious use.

Contributing
============

| If you'd like to help with the Aspidites project as a developer check
out the Issues page or fork and make a pull request.
| Now, for early woma adopters that do not wish to write any Python,
reporting issues is always appreciated.
| If you'd like to help out financially, Aspidites' maintainer accepts
`Liberapay <https://liberapay.com/rjdbcm/>`__.

Information for Developers
==========================

|libraries.io|

Core Dependencies
~~~~~~~~~~~~~~~~~

Aspidites has 10 core dependencies, all licensed under a compatible OSI
approved license. In general, dependencies are vendored unless they
contain Python Extensions.

-  cython
-  pyrsistent
-  pyparsing
-  mypy
-  pytest
-  pytest-xdist
-  pytest-mock
-  numpy
-  future
-  hypothesis

Copying
~~~~~~~

|GitHub|

Additional License Info
^^^^^^^^^^^^^^^^^^^^^^^

| The following 3rd-party software packages may be used by or
| distributed with Aspidites.
| This document was automatically generated by FOSSA on 08/18/21; any
| information relevant to third-party vendors listed below are collected
| using common, reasonable means.
| Revision ID: e6c2f5efb1d22eab44f820031f59bb27ef2f873f

cython
^^^^^^

--------------

| Apache-2.0
| 
| Attribution Notice:
|  Apache License
|  Version 2.0, January 2004
|  http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

#. Definitions.

   | "License" shall mean the terms and conditions for use,
   | reproduction,
   |  and distribution as defined by Sections 1 through 9 of this
   | document.

   | "Licensor" shall mean the copyright owner or entity authorized by
   |  the copyright owner that is granting the License.

   | "Legal Entity" shall mean the union of the acting entity and all
   |  other entities that control, are controlled by, or are under
   | common
   |  control with that entity. For the purposes of this definition,
   |  "control" means (i) the power, direct or indirect, to cause the
   |  direction or management of such entity, whether by contract or
   |  otherwise, or (ii) ownership of fifty percent (50%) or more of the
   |  outstanding shares, or (iii) beneficial ownership of such entity.

   | "You" (or "Your") shall mean an individual or Legal Entity
   |  exercising permissions granted by this License.

   | "Source" form shall mean the preferred form for making
   | modifications,
   |  including but not limited to software source code, documentation
   |  source, and configuration files.

   | "Object" form shall mean any form resulting from mechanical
   |  transformation or translation of a Source form, including but
   |  not limited to compiled object code, generated documentation,
   |  and conversions to other media types.

   | "Work" shall mean the work of authorship, whether in Source or
   |  Object form, made available under the License, as indicated by a
   |  copyright notice that is included in or attached to the work
   |  (an example is provided in the Appendix below).

   | "Derivative Works" shall mean any work, whether in Source or Object
   |  form, that is based on (or derived from) the Work and for which
   the
   |  editorial revisions, annotations, elaborations, or other
   modifications
   |  represent, as a whole, an original work of authorship. For the
   purposes
   |  of this License, Derivative Works shall not include works that
   remain
   |  separable from, or merely link (or bind by name) to the interfaces
   of,
   |  the Work and Derivative Works thereof.

   | "Contribution" shall mean any work of authorship, including
   |  the original version of the Work and any modifications or
   additions
   |  to that Work or Derivative Works thereof, that is intentionally
   |  submitted to Licensor for inclusion in the Work by the copyright
   owner
   |  or by an individual or Legal Entity authorized to submit on behalf
   of
   |  the copyright owner. For the purposes of this definition,
   "submitted"
   |  means any form of electronic, verbal, or written communication
   sent
   |  to the Licensor or its representatives, including but not limited
   to
   |  communication on electronic mailing lists, source code control
   systems,
   |  and issue tracking systems that are managed by, or on behalf of,
   the
   |  Licensor for the purpose of discussing and improving the Work, but
   |  excluding communication that is conspicuously marked or otherwise
   |  designated in writing by the copyright owner as "Not a
   Contribution."

   | "Contributor" shall mean Licensor and any individual or Legal
   Entity
   |  on behalf of whom a Contribution has been received by Licensor and
   |  subsequently incorporated within the Work.

#. | Grant of Copyright License. Subject to the terms and conditions of
   |  this License, each Contributor hereby grants to You a perpetual,
   |  worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   |  copyright license to reproduce, prepare Derivative Works of,
   |  publicly display, publicly perform, sublicense, and distribute the
   |  Work and such Derivative Works in Source or Object form.

#. | Grant of Patent License. Subject to the terms and conditions of
   |  this License, each Contributor hereby grants to You a perpetual,
   |  worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   |  (except as stated in this section) patent license to make, have
   made,
   |  use, offer to sell, sell, import, and otherwise transfer the Work,
   |  where such license applies only to those patent claims licensable
   |  by such Contributor that are necessarily infringed by their
   |  Contribution(s) alone or by combination of their Contribution(s)
   |  with the Work to which such Contribution(s) was submitted. If You
   |  institute patent litigation against any entity (including a
   |  cross-claim or counterclaim in a lawsuit) alleging that the Work
   |  or a Contribution incorporated within the Work constitutes direct
   |  or contributory patent infringement, then any patent licenses
   |  granted to You under this License for that Work shall terminate
   |  as of the date such litigation is filed.

#. | Redistribution. You may reproduce and distribute copies of the
   |  Work or Derivative Works thereof in any medium, with or without
   |  modifications, and in Source or Object form, provided that You
   |  meet the following conditions:

   | (a) You must give any other recipients of the Work or
   |  Derivative Works a copy of this License; and

   | (b) You must cause any modified files to carry prominent notices
   |  stating that You changed the files; and

   | (c) You must retain, in the Source form of any Derivative Works
   |  that You distribute, all copyright, patent, trademark, and
   |  attribution notices from the Source form of the Work,
   |  excluding those notices that do not pertain to any part of
   |  the Derivative Works; and

   | (d) If the Work includes a "NOTICE" text file as part of its
   |  distribution, then any Derivative Works that You distribute must
   |  include a readable copy of the attribution notices contained
   |  within such NOTICE file, excluding those notices that do not
   |  pertain to any part of the Derivative Works, in at least one
   |  of the following places: within a NOTICE text file distributed
   |  as part of the Derivative Works; within the Source form or
   |  documentation, if provided along with the Derivative Works; or,
   |  within a display generated by the Derivative Works, if and
   |  wherever such third-party notices normally appear. The contents
   |  of the NOTICE file are for informational purposes only and
   |  do not modify the License. You may add Your own attribution
   |  notices within Derivative Works that You distribute, alongside
   |  or as an addendum to the NOTICE text from the Work, provided
   |  that such additional attribution notices cannot be construed
   |  as modifying the License.

   | You may add Your own copyright statement to Your modifications and
   |  may provide additional or different license terms and conditions
   |  for use, reproduction, or distribution of Your modifications, or
   |  for any such Derivative Works as a whole, provided Your use,
   |  reproduction, and distribution of the Work otherwise complies with
   |  the conditions stated in this License.

#. | Submission of Contributions. Unless You explicitly state otherwise,
   |  any Contribution intentionally submitted for inclusion in the Work
   |  by You to the Licensor shall be under the terms and conditions of
   |  this License, without any additional terms or conditions.
   |  Notwithstanding the above, nothing herein shall supersede or
   modify
   |  the terms of any separate license agreement you may have executed
   |  with Licensor regarding such Contributions.

#. | Trademarks. This License does not grant permission to use the trade
   |  names, trademarks, service marks, or product names of the
   Licensor,
   |  except as required for reasonable and customary use in describing
   the
   |  origin of the Work and reproducing the content of the NOTICE file.

#. | Disclaimer of Warranty. Unless required by applicable law or
   |  agreed to in writing, Licensor provides the Work (and each
   |  Contributor provides its Contributions) on an "AS IS" BASIS,
   |  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
   |  implied, including, without limitation, any warranties or
   conditions
   |  of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
   |  PARTICULAR PURPOSE. You are solely responsible for determining the
   |  appropriateness of using or redistributing the Work and assume any
   |  risks associated with Your exercise of permissions under this
   License.

#. | Limitation of Liability. In no event and under no legal theory,
   |  whether in tort (including negligence), contract, or otherwise,
   |  unless required by applicable law (such as deliberate and grossly
   |  negligent acts) or agreed to in writing, shall any Contributor be
   |  liable to You for damages, including any direct, indirect,
   special,
   |  incidental, or consequential damages of any character arising as a
   |  result of this License or out of the use or inability to use the
   |  Work (including but not limited to damages for loss of goodwill,
   |  work stoppage, computer failure or malfunction, or any and all
   |  other commercial damages or losses), even if such Contributor
   |  has been advised of the possibility of such damages.

#. | Accepting Warranty or Additional Liability. While redistributing
   |  the Work or Derivative Works thereof, You may choose to offer,
   |  and charge a fee for, acceptance of support, warranty, indemnity,
   |  or other liability obligations and/or rights consistent with this
   |  License. However, in accepting such obligations, You may act only
   |  on Your own behalf and on Your sole responsibility, not on behalf
   |  of any other Contributor, and only if You agree to indemnify,
   |  defend, and hold each Contributor harmless for any liability
   |  incurred by, or claims asserted against, such Contributor by
   reason
   |  of your accepting any such warranty or additional liability.

| END OF TERMS AND CONDITIONS
| 
| 

| Multi-license:
| GPL-2.0-only OR LGPL-2.0-or-later OR BSD-3-Clause

| 
| Attribution:
| Copyright (c) 2010-2011, IPython Development Team . All rights
reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
met:

#. | Redistributions of source code must retain the above copyright
   notice,
   |  this list of conditions and the following disclaimer.

#. | Redistributions in binary form must reproduce the above copyright
   notice,
   |  this list of conditions and the following disclaimer in the
   documentation
   |  and/or other materials provided with the distribution.

#. | Neither the name of the copyright holder nor the names of its
   |  contributors may be used to endorse or promote products derived
   from
   |  this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS"
| AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE
| IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE
| DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE
| FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL
| DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR
| SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER
| CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY,
| OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
| 

MIT

| 
| Attribution:
| Copyright (c) \_\_
| Permission is hereby granted, free of charge, to any person obtaining
a copy
| of this software and associated documentation files (the "Software"),
to deal
| in the Software without restriction, including without limitation the
rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
| copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE
| SOFTWARE.
| 

public-domain

future
^^^^^^

--------------

MIT

| 
| Attribution Notice:
| Copyright (c) 2013-2019 Python Charmers Pty Ltd, Australia

| Permission is hereby granted, free of charge, to any person obtaining
a copy
| of this software and associated documentation files (the "Software"),
to deal
| in the Software without restriction, including without limitation the
rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in
| all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN
| THE SOFTWARE.
| 
| 

Python-2.0

| Attribution:
| 1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

#. Subject to the terms and conditions of this License Agreement, PSF
   hereby grants Licensee a nonexclusive, royalty-free, world-wide
   license to reproduce, analyze, test, perform and/or display publicly,
   prepare derivative works, distribute, and otherwise use Python alone
   or in any derivative version, provided, however, that PSF's License
   Agreement and PSF's notice of copyright, i.e., "Copyright (c) 2001,
   2002, 2003, 2004, 2005, 2006 Python Software Foundation; All Rights
   Reserved" are retained in Python alone or in any derivative version
   prepared by Licensee.
#. In the event Licensee prepares a derivative work that is based on or
   incorporates Python or any part thereof, and wants to make the
   derivative work available to others as provided herein, then Licensee
   hereby agrees to include in any such work a brief summary of the
   changes made to Python.
#. PSF is making Python available to Licensee on an "AS IS" basis. PSF
   MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF
   EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND DISCLAIMS ANY
   REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY
   PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT INFRINGE ANY
   THIRD PARTY RIGHTS.
#. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON FOR
   ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT
   OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON, OR ANY
   DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
#. This License Agreement will automatically terminate upon a material
   breach of its terms and conditions.
#. Nothing in this License Agreement shall be deemed to create any
   relationship of agency, partnership, or joint venture between PSF and
   Licensee. This License Agreement does not grant permission to use PSF
   trademarks or trade name in a trademark sense to endorse or promote
   products or services of Licensee, or any third party.
#. By copying, installing or otherwise using Python, Licensee agrees to
   be bound by the terms and conditions of this License
   Agreement.<<beginOptional>> BEOPEN.COM LICENSE AGREEMENT FOR PYTHON
   2.0
   BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1<<endOptional>>
#. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
   office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
   Individual or Organization ("Licensee") accessing and otherwise using
   this software in source or binary form and its associated
   documentation ("the Software").
#. Subject to the terms and conditions of this BeOpen Python License
   Agreement, BeOpen hereby grants Licensee a non-exclusive,
   royalty-free, world-wide license to reproduce, analyze, test, perform
   and/or display publicly, prepare derivative works, distribute, and
   otherwise use the Software alone or in any derivative version,
   provided, however, that the BeOpen Python License is retained in the
   Software, alone or in any derivative version prepared by Licensee.
#. BeOpen is making the Software available to Licensee on an "AS IS"
   basis. BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
   DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE
   WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
#. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
   SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
   LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR
   ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
#. This License Agreement will automatically terminate upon a material
   breach of its terms and conditions.
#. This License Agreement shall be governed by and interpreted in all
   respects by the law of the State of California, excluding conflict of
   law provisions. Nothing in this License Agreement shall be deemed to
   create any relationship of agency, partnership, or joint venture
   between BeOpen and Licensee. This License Agreement does not grant
   permission to use BeOpen trademarks or trade names in a trademark
   sense to endorse or promote products or services of Licensee, or any
   third party. As an exception, the "BeOpen Python" logos available at
   http://www.pythonlabs.com/logos.html may be used according to the
   permissions granted on that web page.
#. By copying, installing or otherwise using the software, Licensee
   agrees to be bound by the terms and conditions of this License
   Agreement.<<beginOptional>> IMPORTANT: PLEASE READ THE FOLLOWING
   AGREEMENT CAREFULLY.
   BY CLICKING ON "ACCEPT" WHERE INDICATED BELOW, OR BY COPYING,
   INSTALLING OR OTHERWISE USING PYTHON 1.6, beta 1 SOFTWARE, YOU ARE
   DEEMED TO HAVE AGREED TO THE TERMS AND CONDITIONS OF THIS LICENSE
   AGREEMENT.<<endOptional>>
#. This LICENSE AGREEMENT is between the Corporation for National
   Research Initiatives, having an office at 1895 Preston White Drive,
   Reston, VA 20191 ("CNRI"), and the Individual or Organization
   ("Licensee") accessing and otherwise using Python 1.6, beta 1
   software in source or binary form and its associated documentation,
   as released at the www.python.org Internet site on August 4, 2000
   ("Python 1.6b1").
#. Subject to the terms and conditions of this License Agreement, CNRI
   hereby grants Licensee a non-exclusive, royalty-free, world-wide
   license to reproduce, analyze, test, perform and/or display publicly,
   prepare derivative works, distribute, and otherwise use Python 1.6b1
   alone or in any derivative version, provided, however, that CNRIs
   License Agreement is retained in Python 1.6b1, alone or in any
   derivative version prepared by Licensee.
    Alternately, in lieu of CNRIs License Agreement, Licensee may
   substitute the following text (omitting the quotes): "Python 1.6,
   beta 1, is made available subject to the terms and conditions in
   CNRIs License Agreement. This Agreement may be located on the
   Internet using the following unique, persistent identifier (known as
   a handle): 1895.22/1011. This Agreement may also be obtained from a
   proxy server on the Internet using the
   URL:\ `http://hdl.handle.net/1895.22/1011" <http://hdl.handle.net/1895.22/1011">`__.
#. In the event Licensee prepares a derivative work that is based on or
   incorporates Python 1.6b1 or any part thereof, and wants to make the
   derivative work available to the public as provided herein, then
   Licensee hereby agrees to indicate in any such work the nature of the
   modifications made to Python 1.6b1.
#. CNRI is making Python 1.6b1 available to Licensee on an "AS IS"
   basis. CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
   DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6b1
   WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
#. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
   SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
   LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING PYTHON 1.6b1, OR
   ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
#. This License Agreement will automatically terminate upon a material
   breach of its terms and conditions.
#. This License Agreement shall be governed by and interpreted in all
   respects by the law of the State of Virginia, excluding conflict of
   law provisions. Nothing in this License Agreement shall be deemed to
   create any relationship of agency, partnership, or joint venture
   between CNRI and Licensee. This License Agreement does not grant
   permission to use CNRI trademarks or trade name in a trademark sense
   to endorse or promote products or services of Licensee, or any third
   party.
#. By clicking on the "ACCEPT" button where indicated, or by copying,
   installing or otherwise using Python 1.6b1, Licensee agrees to be
   bound by the terms and conditions of this License Agreement.
   Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
   The Netherlands. All rights reserved.
   Permission to use, copy, modify, and distribute this software and its
   documentation for any purpose and without fee is hereby granted,
   provided that the above copyright notice appear in all copies and
   that both that copyright notice and this permission notice appear in
   supporting documentation, and that the name of Stichting Mathematisch
   Centrum or CWI not be used in advertising or publicity pertaining to
   distribution of the software without specific, written prior
   permission.
   STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD
   TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
   AND FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE
   LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
   DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
   WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
   ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
   OF THIS SOFTWARE.

BSD-3-Clause

| 
| Attribution:
| Copyright (c) 2000 by Timothy O . All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
met:

#. | Redistributions of source code must retain the above copyright
   notice,
   |  this list of conditions and the following disclaimer.

#. | Redistributions in binary form must reproduce the above copyright
   notice,
   |  this list of conditions and the following disclaimer in the
   documentation
   |  and/or other materials provided with the distribution.

#. | Neither the name of the copyright holder nor the names of its
   |  contributors may be used to endorse or promote products derived
   from
   |  this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS"
| AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE
| IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE
| DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE
| FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL
| DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR
| SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER
| CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY,
| OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
| 

GPL-2.0-only

| 
| Attribution:
| Copyright (C) 2000 Bastian Kleineidam
| This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the
Free Software Foundation; version 2.
| This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.
| You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
| 

hypothesis
^^^^^^^^^^

--------------

MPL-2.0

| 
| Attribution Notice:
| 1. Definitions
|  1.1. "Contributor" means each individual or legal entity that
creates, contributes to the creation of, or owns Covered Software.
|  1.2. "Contributor Version" means the combination of the Contributions
of others (if any) used by a Contributor and that particular
Contributor's Contribution.
|  1.3. "Contribution" means Covered Software of a particular
Contributor.
|  1.4. "Covered Software" means Source Code Form to which the initial
Contributor has attached the notice in Exhibit A, the Executable Form of
such Source Code Form, and Modifications of such Source Code Form, in
each case including portions thereof.
|  1.5. "Incompatible With Secondary Licenses" means
|  (a) that the initial Contributor has attached the notice described in
Exhibit B to the Covered Software; or
|  (b) that the Covered Software was made available under the terms of
version 1.1 or earlier of the License, but not also under the terms of a
Secondary License.
|  1.6. "Executable Form" means any form of the work other than Source
Code Form.
|  1.7. "Larger Work" means a work that combines Covered Software with
other material, in a separate file or files, that is not Covered
Software.
|  1.8. "License" means this document.
|  1.9. "Licensable" means having the right to grant, to the maximum
extent possible, whether at the time of the initial grant or
subsequently, any and all of the rights conveyed by this License.
|  1.10. "Modifications" means any of the following:
|  (a) any file in Source Code Form that results from an addition to,
deletion from, or modification of the contents of Covered Software; or
|  (b) any new file in Source Code Form that contains any Covered
Software.
|  1.11. "Patent Claims" of a Contributor means any patent claim(s),
including without limitation, method, process, and apparatus claims, in
any patent Licensable by such Contributor that would be infringed, but
for the grant of the License, by the making, using, selling, offering
for sale, having made, import, or transfer of either its Contributions
or its Contributor Version.
|  1.12. "Secondary License" means either the GNU General Public
License, Version 2.0, the GNU Lesser General Public License, Version
2.1, the GNU Affero General Public License, Version 3.0, or any later
versions of those licenses.
|  1.13. "Source Code Form" means the form of the work preferred for
making modifications.
|  1.14. "You" (or "Your") means an individual or a legal entity
exercising rights under this License. For legal entities, "You" includes
any entity that controls, is controlled by, or is under common control
with You. For purposes of this definition, "control" means (a) the
power, direct or indirect, to cause the direction or management of such
entity, whether by contract or otherwise, or (b) ownership of more than
fifty percent (50%) of the outstanding shares or beneficial ownership of
such entity.

#. License Grants and Conditions
    2.1. Grants
    Each Contributor hereby grants You a world-wide, royalty-free,
   non-exclusive license:
    (a) under intellectual property rights (other than patent or
   trademark) Licensable by such Contributor to use, reproduce, make
   available, modify, display, perform, distribute, and otherwise
   exploit its Contributions, either on an unmodified basis, with
   Modifications, or as part of a Larger Work; and
    (b) under Patent Claims of such Contributor to make, use, sell,
   offer for sale, have made, import, and otherwise transfer either its
   Contributions or its Contributor Version.
    2.2. Effective Date
    The licenses granted in Section 2.1 with respect to any Contribution
   become effective for each Contribution on the date the Contributor
   first distributes such Contribution.
    2.3. Limitations on Grant Scope
    The licenses granted in this Section 2 are the only rights granted
   under this License. No additional rights or licenses will be implied
   from the distribution or licensing of Covered Software under this
   License. Notwithstanding Section 2.1(b) above, no patent license is
   granted by a Contributor:
    (a) for any code that a Contributor has removed from Covered
   Software; or
    (b) for infringements caused by: (i) Your and any other third
   party's modifications of Covered Software, or (ii) the combination of
   its Contributions with other software (except as part of its
   Contributor Version); or
    (c) under Patent Claims infringed by Covered Software in the absence
   of its Contributions.
    This License does not grant any rights in the trademarks, service
   marks, or logos of any Contributor (except as may be necessary to
   comply with the notice requirements in Section 3.4).
    2.4. Subsequent Licenses
    No Contributor makes additional grants as a result of Your choice to
   distribute the Covered Software under a subsequent version of this
   License (see Section 10.2) or under the terms of a Secondary License
   (if permitted under the terms of Section 3.3).
    2.5. Representation
    Each Contributor represents that the Contributor believes its
   Contributions are its original creation(s) or it has sufficient
   rights to grant the rights to its Contributions conveyed by this
   License.
    2.6. Fair Use
    This License is not intended to limit any rights You have under
   applicable copyright doctrines of fair use, fair dealing, or other
   equivalents.
    2.7. Conditions
    Sections 3.1, 3.2, 3.3, and 3.4 are conditions of the licenses
   granted in Section 2.1.
#. Responsibilities
    3.1. Distribution of Source Form
    All distribution of Covered Software in Source Code Form, including
   any Modifications that You create or to which You contribute, must be
   under the terms of this License. You must inform recipients that the
   Source Code Form of the Covered Software is governed by the terms of
   this License, and how they can obtain a copy of this License. You may
   not attempt to alter or restrict the recipients' rights in the Source
   Code Form.
    3.2. Distribution of Executable Form
    If You distribute Covered Software in Executable Form then:
    (a) such Covered Software must also be made available in Source Code
   Form, as described in Section 3.1, and You must inform recipients of
   the Executable Form how they can obtain a copy of such Source Code
   Form by reasonable means in a timely manner, at a charge no more than
   the cost of distribution to the recipient; and
    (b) You may distribute such Executable Form under the terms of this
   License, or sublicense it under different terms, provided that the
   license for the Executable Form does not attempt to limit or alter
   the recipients' rights in the Source Code Form under this License.
    3.3. Distribution of a Larger Work
    You may create and distribute a Larger Work under terms of Your
   choice, provided that You also comply with the requirements of this
   License for the Covered Software. If the Larger Work is a combination
   of Covered Software with a work governed by one or more Secondary
   Licenses, and the Covered Software is not Incompatible With Secondary
   Licenses, this License permits You to additionally distribute such
   Covered Software under the terms of such Secondary License(s), so
   that the recipient of the Larger Work may, at their option, further
   distribute the Covered Software under the terms of either this
   License or such Secondary License(s).
    3.4. Notices
    You may not remove or alter the substance of any license notices
   (including copyright notices, patent notices, disclaimers of
   warranty, or limitations of liability) contained within the Source
   Code Form of the Covered Software, except that You may alter any
   license notices to the extent required to remedy known factual
   inaccuracies.
    3.5. Application of Additional Terms
    You may choose to offer, and to charge a fee for, warranty, support,
   indemnity or liability obligations to one or more recipients of
   Covered Software. However, You may do so only on Your own behalf, and
   not on behalf of any Contributor. You must make it absolutely clear
   that any such warranty, support, indemnity, or liability obligation
   is offered by You alone, and You hereby agree to indemnify every
   Contributor for any liability incurred by such Contributor as a
   result of warranty, support, indemnity or liability terms You offer.
   You may include additional disclaimers of warranty and limitations of
   liability specific to any jurisdiction.
#. Inability to Comply Due to Statute or Regulation
    If it is impossible for You to comply with any of the terms of this
   License with respect to some or all of the Covered Software due to
   statute, judicial order, or regulation then You must: (a) comply with
   the terms of this License to the maximum extent possible; and (b)
   describe the limitations and the code they affect. Such description
   must be placed in a text file included with all distributions of the
   Covered Software under this License. Except to the extent prohibited
   by statute or regulation, such description must be sufficiently
   detailed for a recipient of ordinary skill to be able to understand
   it.
#. Termination
    5.1. The rights granted under this License will terminate
   automatically if You fail to comply with any of its terms. However,
   if You become compliant, then the rights granted under this License
   from a particular Contributor are reinstated (a) provisionally,
   unless and until such Contributor explicitly and finally terminates
   Your grants, and (b) on an ongoing basis, if such Contributor fails
   to notify You of the non-compliance by some reasonable means prior to
   60 days after You have come back into compliance. Moreover, Your
   grants from a particular Contributor are reinstated on an ongoing
   basis if such Contributor notifies You of the non-compliance by some
   reasonable means, this is the first time You have received notice of
   non-compliance with this License from such Contributor, and You
   become compliant prior to 30 days after Your receipt of the notice.
    5.2. If You initiate litigation against any entity by asserting a
   patent infringement claim (excluding declaratory judgment actions,
   counter-claims, and cross-claims) alleging that a Contributor Version
   directly or indirectly infringes any patent, then the rights granted
   to You by any and all Contributors for the Covered Software under
   Section 2.1 of this License shall terminate.
    5.3. In the event of termination under Sections 5.1 or 5.2 above,
   all end user license agreements (excluding distributors and
   resellers) which have been validly granted by You or Your
   distributors under this License prior to termination shall survive
   termination.
#. Disclaimer of Warranty
    Covered Software is provided under this License on an "as is" basis,
   without warranty of any kind, either expressed, implied, or
   statutory, including, without limitation, warranties that the Covered
   Software is free of defects, merchantable, fit for a particular
   purpose or non-infringing. The entire risk as to the quality and
   performance of the Covered Software is with You. Should any Covered
   Software prove defective in any respect, You (not any Contributor)
   assume the cost of any necessary servicing, repair, or correction.
   This disclaimer of warranty constitutes an essential part of this
   License. No use of any Covered Software is authorized under this
   License except under this disclaimer.
#. Limitation of Liability
    Under no circumstances and under no legal theory, whether tort
   (including negligence), contract, or otherwise, shall any
   Contributor, or anyone who distributes Covered Software as permitted
   above, be liable to You for any direct, indirect, special,
   incidental, or consequential damages of any character including,
   without limitation, damages for lost profits, loss of goodwill, work
   stoppage, computer failure or malfunction, or any and all other
   commercial damages or losses, even if such party shall have been
   informed of the possibility of such damages. This limitation of
   liability shall not apply to liability for death or personal injury
   resulting from such party's negligence to the extent applicable law
   prohibits such limitation. Some jurisdictions do not allow the
   exclusion or limitation of incidental or consequential damages, so
   this exclusion and limitation may not apply to You.
#. Litigation
    Any litigation relating to this License may be brought only in the
   courts of a jurisdiction where the defendant maintains its principal
   place of business and such litigation shall be governed by laws of
   that jurisdiction, without reference to its conflict-of-law
   provisions. Nothing in this Section shall prevent a party's ability
   to bring cross-claims or counter-claims.
#. Miscellaneous
    This License represents the complete agreement concerning the
   subject matter hereof. If any provision of this License is held to be
   unenforceable, such provision shall be reformed only to the extent
   necessary to make it enforceable. Any law or regulation which
   provides that the language of a contract shall be construed against
   the drafter shall not be used to construe this License against a
   Contributor.
#. Versions of the License
    10.1. New Versions
    Mozilla Foundation is the license steward. Except as provided in
   Section 10.3, no one other than the license steward has the right to
   modify or publish new versions of this License. Each version will be
   given a distinguishing version number.
    10.2. Effect of New Versions
    You may distribute the Covered Software under the terms of the
   version of the License under which You originally received the
   Covered Software, or under the terms of any subsequent version
   published by the license steward.
    10.3. Modified Versions
    If you create software not governed by this License, and you want to
   create a new license for such software, you may create and use a
   modified version of this License if you rename the license and remove
   any references to the name of the license steward (except to note
   that such modified license differs from this License).
    10.4. Distributing Source Code Form that is Incompatible With
   Secondary Licenses
    If You choose to distribute Source Code Form that is Incompatible
   With Secondary Licenses under the terms of this version of the
   License, the notice described in Exhibit B of this License must be
   attached.<<beginOptional>> Exhibit A - Source Code Form License
   Notice
   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.
   If it is not possible or desirable to put the notice in a particular
   file, then You may include the notice in a location (such as a
   LICENSE file in a relevant directory) where a recipient would be
   likely to look for such a notice.
   You may add additional accurate notices of copyright ownership.
   Exhibit B - "Incompatible With Secondary Licenses" Notice
   This Source Code Form is "Incompatible With Secondary Licenses", as
   defined by the Mozilla Public License, v. 2.0.<<endOptional>>

MPL-2.0-no-copyleft-exception

| Attribution Notice:
| Copyright (c) 2013, David R. MacIver

| All code in this repository except where explicitly noted otherwise is
released
| under the Mozilla Public License v 2.0. You can obtain a copy at
https://mozilla.org/MPL/2.0/.

| Some code in this repository comes from other projects. Where
applicable, the
| original copyright and license are noted and any modifications made
are released
| dual licensed with the original license.

| Mozilla Public License Version 2.0
| \\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=\\=

#. | Definitions
   | ------------------

#. 

   #. "Contributor"
       means each individual or legal entity that creates, contributes
      to
       the creation of, or owns Covered Software.

#. 

   #. "Contributor Version"
       means the combination of the Contributions of others (if any)
      used
       by a Contributor and that particular Contributor's Contribution.

#. 

   #. "Contribution"
       means Covered Software of a particular Contributor.

#. 

   #. "Covered Software"
       means Source Code Form to which the initial Contributor has
      attached
       the notice in Exhibit A, the Executable Form of such Source Code
       Form, and Modifications of such Source Code Form, in each case
       including portions thereof.

#. 

   #. "Incompatible With Secondary Licenses"
       means

   | (a) that the initial Contributor has attached the notice described
   |  in Exhibit B to the Covered Software; or

   | (b) that the Covered Software was made available under the terms of
   |  version 1.1 or earlier of the License, but not also under the
   |  terms of a Secondary License.

#. 

   #. "Executable Form"
       means any form of the work other than Source Code Form.

#. 

   #. "Larger Work"
       means a work that combines Covered Software with other material,
      in
       a separate file or files, that is not Covered Software.

#. 

   #. "License"
       means this document.

#. 

   #. "Licensable"
       means having the right to grant, to the maximum extent possible,
       whether at the time of the initial grant or subsequently, any and
       all of the rights conveyed by this License.

#. 

   #. "Modifications"
       means any of the following:

   | (a) any file in Source Code Form that results from an addition to,
   |  deletion from, or modification of the contents of Covered
   |  Software; or

   | (b) any new file in Source Code Form that contains any Covered
   |  Software.

#. 

   #. "Patent Claims" of a Contributor
       means any patent claim(s), including without limitation, method,
       process, and apparatus claims, in any patent Licensable by such
       Contributor that would be infringed, but for the grant of the
       License, by the making, using, selling, offering for sale, having
       made, import, or transfer of either its Contributions or its
       Contributor Version.

#. 

   #. "Secondary License"
       means either the GNU General Public License, Version 2.0, the GNU
       Lesser General Public License, Version 2.1, the GNU Affero
      General
       Public License, Version 3.0, or any later versions of those
       licenses.

#. 

   #. "Source Code Form"
       means the form of the work preferred for making modifications.

#. 

   #. "You" (or "Your")
       means an individual or a legal entity exercising rights under
      this
       License. For legal entities, "You" includes any entity that
       controls, is controlled by, or is under common control with You.
      For
       purposes of this definition, "control" means (a) the power,
      direct
       or indirect, to cause the direction or management of such entity,
       whether by contract or otherwise, or (b) ownership of more than
       fifty percent (50%) of the outstanding shares or beneficial
       ownership of such entity.

#. | License Grants and Conditions
   | -----------------------------

#. 

   #. Grants

| Each Contributor hereby grants You a world-wide, royalty-free,
| non-exclusive license:

| (a) under intellectual property rights (other than patent or
trademark)
|  Licensable by such Contributor to use, reproduce, make available,
|  modify, display, perform, distribute, and otherwise exploit its
|  Contributions, either on an unmodified basis, with Modifications, or
|  as part of a Larger Work; and

| (b) under Patent Claims of such Contributor to make, use, sell, offer
|  for sale, have made, import, and otherwise transfer either its
|  Contributions or its Contributor Version.

2.2. Effective Date

| The licenses granted in Section 2.1 with respect to any Contribution
| become effective for each Contribution on the date the Contributor
first
| distributes such Contribution.

2.3. Limitations on Grant Scope

| The licenses granted in this Section 2 are the only rights granted
under
| this License. No additional rights or licenses will be implied from
the
| distribution or licensing of Covered Software under this License.
| Notwithstanding Section 2.1(b) above, no patent license is granted by
a
| Contributor:

| (a) for any code that a Contributor has removed from Covered Software;
|  or

| (b) for infringements caused by: (i) Your and any other third party's
|  modifications of Covered Software, or (ii) the combination of its
|  Contributions with other software (except as part of its Contributor
|  Version); or

| (c) under Patent Claims infringed by Covered Software in the absence
of
|  its Contributions.

| This License does not grant any rights in the trademarks, service
marks,
| or logos of any Contributor (except as may be necessary to comply with
| the notice requirements in Section 3.4).

2.4. Subsequent Licenses

| No Contributor makes additional grants as a result of Your choice to
| distribute the Covered Software under a subsequent version of this
| License (see Section 10.2) or under the terms of a Secondary License
(if
| permitted under the terms of Section 3.3).

2.5. Representation

| Each Contributor represents that the Contributor believes its
| Contributions are its original creation(s) or it has sufficient rights
| to grant the rights to its Contributions conveyed by this License.

2.6. Fair Use

| This License is not intended to limit any rights You have under
| applicable copyright doctrines of fair use, fair dealing, or other
| equivalents.

2.7. Conditions

| Sections 3.1, 3.2, 3.3, and 3.4 are conditions of the licenses granted
| in Section 2.1.

#. | Responsibilities
   | -------------------------

#. 

   #. Distribution of Source Form

| All distribution of Covered Software in Source Code Form, including
any
| Modifications that You create or to which You contribute, must be
under
| the terms of this License. You must inform recipients that the Source
| Code Form of the Covered Software is governed by the terms of this
| License, and how they can obtain a copy of this License. You may not
| attempt to alter or restrict the recipients' rights in the Source Code
| Form.

3.2. Distribution of Executable Form

If You distribute Covered Software in Executable Form then:

| (a) such Covered Software must also be made available in Source Code
|  Form, as described in Section 3.1, and You must inform recipients of
|  the Executable Form how they can obtain a copy of such Source Code
|  Form by reasonable means in a timely manner, at a charge no more
|  than the cost of distribution to the recipient; and

| (b) You may distribute such Executable Form under the terms of this
|  License, or sublicense it under different terms, provided that the
|  license for the Executable Form does not attempt to limit or alter
|  the recipients' rights in the Source Code Form under this License.

3.3. Distribution of a Larger Work

| You may create and distribute a Larger Work under terms of Your
choice,
| provided that You also comply with the requirements of this License
for
| the Covered Software. If the Larger Work is a combination of Covered
| Software with a work governed by one or more Secondary Licenses, and
the
| Covered Software is not Incompatible With Secondary Licenses, this
| License permits You to additionally distribute such Covered Software
| under the terms of such Secondary License(s), so that the recipient of
| the Larger Work may, at their option, further distribute the Covered
| Software under the terms of either this License or such Secondary
| License(s).

3.4. Notices

| You may not remove or alter the substance of any license notices
| (including copyright notices, patent notices, disclaimers of warranty,
| or limitations of liability) contained within the Source Code Form of
| the Covered Software, except that You may alter any license notices to
| the extent required to remedy known factual inaccuracies.

3.5. Application of Additional Terms

| You may choose to offer, and to charge a fee for, warranty, support,
| indemnity or liability obligations to one or more recipients of
Covered
| Software. However, You may do so only on Your own behalf, and not on
| behalf of any Contributor. You must make it absolutely clear that any
| such warranty, support, indemnity, or liability obligation is offered
by
| You alone, and You hereby agree to indemnify every Contributor for any
| liability incurred by such Contributor as a result of warranty,
support,
| indemnity or liability terms You offer. You may include additional
| disclaimers of warranty and limitations of liability specific to any
| jurisdiction.

#. Inability to Comply Due to Statute or Regulation
   -------------------------

| If it is impossible for You to comply with any of the terms of this
| License with respect to some or all of the Covered Software due to
| statute, judicial order, or regulation then You must: (a) comply with
| the terms of this License to the maximum extent possible; and (b)
| describe the limitations and the code they affect. Such description
must
| be placed in a text file included with all distributions of the
Covered
| Software under this License. Except to the extent prohibited by
statute
| or regulation, such description must be sufficiently detailed for a
| recipient of ordinary skill to be able to understand it.

#. | Termination
   | -------------------------

#. 

   #. The rights granted under this License will terminate automatically
      if You fail to comply with any of its terms. However, if You
      become
      compliant, then the rights granted under this License from a
      particular
      Contributor are reinstated (a) provisionally, unless and until
      such
      Contributor explicitly and finally terminates Your grants, and (b)
      on an
      ongoing basis, if such Contributor fails to notify You of the
      non-compliance by some reasonable means prior to 60 days after You
      have
      come back into compliance. Moreover, Your grants from a particular
      Contributor are reinstated on an ongoing basis if such Contributor
      notifies You of the non-compliance by some reasonable means, this
      is the
      first time You have received notice of non-compliance with this
      License
      from such Contributor, and You become compliant prior to 30 days
      after
      Your receipt of the notice.

#. 

   #. If You initiate litigation against any entity by asserting a
      patent
      infringement claim (excluding declaratory judgment actions,
      counter-claims, and cross-claims) alleging that a Contributor
      Version
      directly or indirectly infringes any patent, then the rights
      granted to
      You by any and all Contributors for the Covered Software under
      Section
      2.1 of this License shall terminate.

#. 

   #. In the event of termination under Sections 5.1 or 5.2 above, all
      end user license agreements (excluding distributors and resellers)
      which
      have been validly granted by You or Your distributors under this
      License
      prior to termination shall survive termination.

--------------

-  

   -  

-  

   #. Disclaimer of Warranty \*

-  ------------------------- \*
-  

   -  

-  Covered Software is provided under this License on an "as is" \*
-  basis, without warranty of any kind, either expressed, implied, or \*
-  statutory, including, without limitation, warranties that the \*
-  Covered Software is free of defects, merchantable, fit for a \*
-  particular purpose or non-infringing. The entire risk as to the \*
-  quality and performance of the Covered Software is with You. \*
-  Should any Covered Software prove defective in any respect, You \*
-  (not any Contributor) assume the cost of any necessary servicing, \*
-  repair, or correction. This disclaimer of warranty constitutes an \*
-  essential part of this License. No use of any Covered Software is \*
-  authorized under this License except under this disclaimer. \*
-  

   -  

      --------------

--------------

-  

   -  

-  

   #. Limitation of Liability \*

-  -------------------------- \*
-  

   -  

-  Under no circumstances and under no legal theory, whether tort \*
-  (including negligence), contract, or otherwise, shall any \*
-  Contributor, or anyone who distributes Covered Software as \*
-  permitted above, be liable to You for any direct, indirect, \*
-  special, incidental, or consequential damages of any character \*
-  including, without limitation, damages for lost profits, loss of \*
-  goodwill, work stoppage, computer failure or malfunction, or any \*
-  and all other commercial damages or losses, even if such party \*
-  shall have been informed of the possibility of such damages. This \*
-  limitation of liability shall not apply to liability for death or \*
-  personal injury resulting from such party's negligence to the \*
-  extent applicable law prohibits such limitation. Some \*
-  jurisdictions do not allow the exclusion or limitation of \*
-  incidental or consequential damages, so this exclusion and \*
-  limitation may not apply to You. \*
-  

   -  

      --------------

#. Litigation
   -------------------------

| Any litigation relating to this License may be brought only in the
| courts of a jurisdiction where the defendant maintains its principal
| place of business and such litigation shall be governed by laws of
that
| jurisdiction, without reference to its conflict-of-law provisions.
| Nothing in this Section shall prevent a party's ability to bring
| cross-claims or counter-claims.

#. Miscellaneous
   -------------------------

| This License represents the complete agreement concerning the subject
| matter hereof. If any provision of this License is held to be
| unenforceable, such provision shall be reformed only to the extent
| necessary to make it enforceable. Any law or regulation which provides
| that the language of a contract shall be construed against the drafter
| shall not be used to construe this License against a Contributor.

#. | Versions of the License
   | -------------------------

#. 

   #. New Versions

| Mozilla Foundation is the license steward. Except as provided in
Section
| 10.3, no one other than the license steward has the right to modify or
| publish new versions of this License. Each version will be given a
| distinguishing version number.

10.2. Effect of New Versions

| You may distribute the Covered Software under the terms of the version
| of the License under which You originally received the Covered
Software,
| or under the terms of any subsequent version published by the license
| steward.

10.3. Modified Versions

| If you create software not governed by this License, and you want to
| create a new license for such software, you may create and use a
| modified version of this License if you rename the license and remove
| any references to the name of the license steward (except to note that
| such modified license differs from this License).

| 10.4. Distributing Source Code Form that is Incompatible With
Secondary
| Licenses

| If You choose to distribute Source Code Form that is Incompatible With
| Secondary Licenses under the terms of this version of the License, the
| notice described in Exhibit B of this License must be attached.

| Exhibit A - Source Code Form License Notice
| -------------------------

| This Source Code Form is subject to the terms of the Mozilla Public
|  License, v. 2.0. If a copy of the MPL was not distributed with this
|  file, You can obtain one at https://mozilla.org/MPL/2.0/.

| If it is not possible or desirable to put the notice in a particular
| file, then You may include the notice in a location (such as a LICENSE
| file in a relevant directory) where a recipient would be likely to
look
| for such a notice.

You may add additional accurate notices of copyright ownership.

| Exhibit B - "Incompatible With Secondary Licenses" Notice
| -------------------------

| This Source Code Form is "Incompatible With Secondary Licenses", as
|  defined by the Mozilla Public License, v. 2.0.
| 
| 

| Multi-license:
| MPL-2.0 OR public-domain

| 
| Attribution:
| 1. Definitions
|  1.1. "Contributor" means each individual or legal entity that
creates, contributes to the creation of, or owns Covered Software.
|  1.2. "Contributor Version" means the combination of the Contributions
of others (if any) used by a Contributor and that particular
Contributor's Contribution.
|  1.3. "Contribution" means Covered Software of a particular
Contributor.
|  1.4. "Covered Software" means Source Code Form to which the initial
Contributor has attached the notice in Exhibit A, the Executable Form of
such Source Code Form, and Modifications of such Source Code Form, in
each case including portions thereof.
|  1.5. "Incompatible With Secondary Licenses" means
|  (a) that the initial Contributor has attached the notice described in
Exhibit B to the Covered Software; or
|  (b) that the Covered Software was made available under the terms of
version 1.1 or earlier of the License, but not also under the terms of a
Secondary License.
|  1.6. "Executable Form" means any form of the work other than Source
Code Form.
|  1.7. "Larger Work" means a work that combines Covered Software with
other material, in a separate file or files, that is not Covered
Software.
|  1.8. "License" means this document.
|  1.9. "Licensable" means having the right to grant, to the maximum
extent possible, whether at the time of the initial grant or
subsequently, any and all of the rights conveyed by this License.
|  1.10. "Modifications" means any of the following:
|  (a) any file in Source Code Form that results from an addition to,
deletion from, or modification of the contents of Covered Software; or
|  (b) any new file in Source Code Form that contains any Covered
Software.
|  1.11. "Patent Claims" of a Contributor means any patent claim(s),
including without limitation, method, process, and apparatus claims, in
any patent Licensable by such Contributor that would be infringed, but
for the grant of the License, by the making, using, selling, offering
for sale, having made, import, or transfer of either its Contributions
or its Contributor Version.
|  1.12. "Secondary License" means either the GNU General Public
License, Version 2.0, the GNU Lesser General Public License, Version
2.1, the GNU Affero General Public License, Version 3.0, or any later
versions of those licenses.
|  1.13. "Source Code Form" means the form of the work preferred for
making modifications.
|  1.14. "You" (or "Your") means an individual or a legal entity
exercising rights under this License. For legal entities, "You" includes
any entity that controls, is controlled by, or is under common control
with You. For purposes of this definition, "control" means (a) the
power, direct or indirect, to cause the direction or management of such
entity, whether by contract or otherwise, or (b) ownership of more than
fifty percent (50%) of the outstanding shares or beneficial ownership of
such entity.

#. License Grants and Conditions
    2.1. Grants
    Each Contributor hereby grants You a world-wide, royalty-free,
   non-exclusive license:
    (a) under intellectual property rights (other than patent or
   trademark) Licensable by such Contributor to use, reproduce, make
   available, modify, display, perform, distribute, and otherwise
   exploit its Contributions, either on an unmodified basis, with
   Modifications, or as part of a Larger Work; and
    (b) under Patent Claims of such Contributor to make, use, sell,
   offer for sale, have made, import, and otherwise transfer either its
   Contributions or its Contributor Version.
    2.2. Effective Date
    The licenses granted in Section 2.1 with respect to any Contribution
   become effective for each Contribution on the date the Contributor
   first distributes such Contribution.
    2.3. Limitations on Grant Scope
    The licenses granted in this Section 2 are the only rights granted
   under this License. No additional rights or licenses will be implied
   from the distribution or licensing of Covered Software under this
   License. Notwithstanding Section 2.1(b) above, no patent license is
   granted by a Contributor:
    (a) for any code that a Contributor has removed from Covered
   Software; or
    (b) for infringements caused by: (i) Your and any other third
   party's modifications of Covered Software, or (ii) the combination of
   its Contributions with other software (except as part of its
   Contributor Version); or
    (c) under Patent Claims infringed by Covered Software in the absence
   of its Contributions.
    This License does not grant any rights in the trademarks, service
   marks, or logos of any Contributor (except as may be necessary to
   comply with the notice requirements in Section 3.4).
    2.4. Subsequent Licenses
    No Contributor makes additional grants as a result of Your choice to
   distribute the Covered Software under a subsequent version of this
   License (see Section 10.2) or under the terms of a Secondary License
   (if permitted under the terms of Section 3.3).
    2.5. Representation
    Each Contributor represents that the Contributor believes its
   Contributions are its original creation(s) or it has sufficient
   rights to grant the rights to its Contributions conveyed by this
   License.
    2.6. Fair Use
    This License is not intended to limit any rights You have under
   applicable copyright doctrines of fair use, fair dealing, or other
   equivalents.
    2.7. Conditions
    Sections 3.1, 3.2, 3.3, and 3.4 are conditions of the licenses
   granted in Section 2.1.
#. Responsibilities
    3.1. Distribution of Source Form
    All distribution of Covered Software in Source Code Form, including
   any Modifications that You create or to which You contribute, must be
   under the terms of this License. You must inform recipients that the
   Source Code Form of the Covered Software is governed by the terms of
   this License, and how they can obtain a copy of this License. You may
   not attempt to alter or restrict the recipients' rights in the Source
   Code Form.
    3.2. Distribution of Executable Form
    If You distribute Covered Software in Executable Form then:
    (a) such Covered Software must also be made available in Source Code
   Form, as described in Section 3.1, and You must inform recipients of
   the Executable Form how they can obtain a copy of such Source Code
   Form by reasonable means in a timely manner, at a charge no more than
   the cost of distribution to the recipient; and
    (b) You may distribute such Executable Form under the terms of this
   License, or sublicense it under different terms, provided that the
   license for the Executable Form does not attempt to limit or alter
   the recipients' rights in the Source Code Form under this License.
    3.3. Distribution of a Larger Work
    You may create and distribute a Larger Work under terms of Your
   choice, provided that You also comply with the requirements of this
   License for the Covered Software. If the Larger Work is a combination
   of Covered Software with a work governed by one or more Secondary
   Licenses, and the Covered Software is not Incompatible With Secondary
   Licenses, this License permits You to additionally distribute such
   Covered Software under the terms of such Secondary License(s), so
   that the recipient of the Larger Work may, at their option, further
   distribute the Covered Software under the terms of either this
   License or such Secondary License(s).
    3.4. Notices
    You may not remove or alter the substance of any license notices
   (including copyright notices, patent notices, disclaimers of
   warranty, or limitations of liability) contained within the Source
   Code Form of the Covered Software, except that You may alter any
   license notices to the extent required to remedy known factual
   inaccuracies.
    3.5. Application of Additional Terms
    You may choose to offer, and to charge a fee for, warranty, support,
   indemnity or liability obligations to one or more recipients of
   Covered Software. However, You may do so only on Your own behalf, and
   not on behalf of any Contributor. You must make it absolutely clear
   that any such warranty, support, indemnity, or liability obligation
   is offered by You alone, and You hereby agree to indemnify every
   Contributor for any liability incurred by such Contributor as a
   result of warranty, support, indemnity or liability terms You offer.
   You may include additional disclaimers of warranty and limitations of
   liability specific to any jurisdiction.
#. Inability to Comply Due to Statute or Regulation
    If it is impossible for You to comply with any of the terms of this
   License with respect to some or all of the Covered Software due to
   statute, judicial order, or regulation then You must: (a) comply with
   the terms of this License to the maximum extent possible; and (b)
   describe the limitations and the code they affect. Such description
   must be placed in a text file included with all distributions of the
   Covered Software under this License. Except to the extent prohibited
   by statute or regulation, such description must be sufficiently
   detailed for a recipient of ordinary skill to be able to understand
   it.
#. Termination
    5.1. The rights granted under this License will terminate
   automatically if You fail to comply with any of its terms. However,
   if You become compliant, then the rights granted under this License
   from a particular Contributor are reinstated (a) provisionally,
   unless and until such Contributor explicitly and finally terminates
   Your grants, and (b) on an ongoing basis, if such Contributor fails
   to notify You of the non-compliance by some reasonable means prior to
   60 days after You have come back into compliance. Moreover, Your
   grants from a particular Contributor are reinstated on an ongoing
   basis if such Contributor notifies You of the non-compliance by some
   reasonable means, this is the first time You have received notice of
   non-compliance with this License from such Contributor, and You
   become compliant prior to 30 days after Your receipt of the notice.
    5.2. If You initiate litigation against any entity by asserting a
   patent infringement claim (excluding declaratory judgment actions,
   counter-claims, and cross-claims) alleging that a Contributor Version
   directly or indirectly infringes any patent, then the rights granted
   to You by any and all Contributors for the Covered Software under
   Section 2.1 of this License shall terminate.
    5.3. In the event of termination under Sections 5.1 or 5.2 above,
   all end user license agreements (excluding distributors and
   resellers) which have been validly granted by You or Your
   distributors under this License prior to termination shall survive
   termination.
#. Disclaimer of Warranty
    Covered Software is provided under this License on an "as is" basis,
   without warranty of any kind, either expressed, implied, or
   statutory, including, without limitation, warranties that the Covered
   Software is free of defects, merchantable, fit for a particular
   purpose or non-infringing. The entire risk as to the quality and
   performance of the Covered Software is with You. Should any Covered
   Software prove defective in any respect, You (not any Contributor)
   assume the cost of any necessary servicing, repair, or correction.
   This disclaimer of warranty constitutes an essential part of this
   License. No use of any Covered Software is authorized under this
   License except under this disclaimer.
#. Limitation of Liability
    Under no circumstances and under no legal theory, whether tort
   (including negligence), contract, or otherwise, shall any
   Contributor, or anyone who distributes Covered Software as permitted
   above, be liable to You for any direct, indirect, special,
   incidental, or consequential damages of any character including,
   without limitation, damages for lost profits, loss of goodwill, work
   stoppage, computer failure or malfunction, or any and all other
   commercial damages or losses, even if such party shall have been
   informed of the possibility of such damages. This limitation of
   liability shall not apply to liability for death or personal injury
   resulting from such party's negligence to the extent applicable law
   prohibits such limitation. Some jurisdictions do not allow the
   exclusion or limitation of incidental or consequential damages, so
   this exclusion and limitation may not apply to You.
#. Litigation
    Any litigation relating to this License may be brought only in the
   courts of a jurisdiction where the defendant maintains its principal
   place of business and such litigation shall be governed by laws of
   that jurisdiction, without reference to its conflict-of-law
   provisions. Nothing in this Section shall prevent a party's ability
   to bring cross-claims or counter-claims.
#. Miscellaneous
    This License represents the complete agreement concerning the
   subject matter hereof. If any provision of this License is held to be
   unenforceable, such provision shall be reformed only to the extent
   necessary to make it enforceable. Any law or regulation which
   provides that the language of a contract shall be construed against
   the drafter shall not be used to construe this License against a
   Contributor.
#. Versions of the License
    10.1. New Versions
    Mozilla Foundation is the license steward. Except as provided in
   Section 10.3, no one other than the license steward has the right to
   modify or publish new versions of this License. Each version will be
   given a distinguishing version number.
    10.2. Effect of New Versions
    You may distribute the Covered Software under the terms of the
   version of the License under which You originally received the
   Covered Software, or under the terms of any subsequent version
   published by the license steward.
    10.3. Modified Versions
    If you create software not governed by this License, and you want to
   create a new license for such software, you may create and use a
   modified version of this License if you rename the license and remove
   any references to the name of the license steward (except to note
   that such modified license differs from this License).
    10.4. Distributing Source Code Form that is Incompatible With
   Secondary Licenses
    If You choose to distribute Source Code Form that is Incompatible
   With Secondary Licenses under the terms of this version of the
   License, the notice described in Exhibit B of this License must be
   attached.<<beginOptional>> Exhibit A - Source Code Form License
   Notice
   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.
   If it is not possible or desirable to put the notice in a particular
   file, then You may include the notice in a location (such as a
   LICENSE file in a relevant directory) where a recipient would be
   likely to look for such a notice.
   You may add additional accurate notices of copyright ownership.
   Exhibit B - "Incompatible With Secondary Licenses" Notice
   This Source Code Form is "Incompatible With Secondary Licenses", as
   defined by the Mozilla Public License, v. 2.0.<<endOptional>>

mypy
^^^^

--------------

| Multi-license:
| GPL-3.0-only OR MIT OR Python-2.0

| 
| Attribution Notice:
| Mypy (and mypyc) are licensed under the terms of the MIT license,
reproduced below.

= = = = =

The MIT License

Copyright (c) 2015-2021 Jukka Lehtosalo and contributors

| Permission is hereby granted, free of charge, to any person obtaining
a
| copy of this software and associated documentation files (the
"Software"),
| to deal in the Software without restriction, including without
limitation
| the rights to use, copy, modify, merge, publish, distribute,
sublicense,
| and/or sell copies of the Software, and to permit persons to whom the
| Software is furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in
| all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING
| FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
| DEALINGS IN THE SOFTWARE.

= = = = =

| Portions of mypy and mypyc are licensed under different licenses. The
| files under stdlib-samples as well as the files
| mypyc/lib-rt/pythonsupport.h, mypyc/lib-rt/getargs.c and
| mypyc/lib-rt/getargsfast.c are licensed under the PSF 2 License,
reproduced
| below.

= = = = =

| PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
| -------------------------

#. | This LICENSE AGREEMENT is between the Python Software Foundation
   | ("PSF"), and the Individual or Organization ("Licensee") accessing
   and
   | otherwise using this software ("Python") in source or binary form
   and
   | its associated documentation.

#. | Subject to the terms and conditions of this License Agreement, PSF
   hereby
   | grants Licensee a nonexclusive, royalty-free, world-wide license to
   reproduce,
   | analyze, test, perform and/or display publicly, prepare derivative
   works,
   | distribute, and otherwise use Python alone or in any derivative
   version,
   | provided, however, that PSF's License Agreement and PSF's notice of
   copyright,
   | i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007,
   2008, 2009, 2010,
   | 2011, 2012 Python Software Foundation; All Rights Reserved" are
   retained in Python
   | alone or in any derivative version prepared by Licensee.

#. | In the event Licensee prepares a derivative work that is based on
   | or incorporates Python or any part thereof, and wants to make
   | the derivative work available to others as provided herein, then
   | Licensee hereby agrees to include in any such work a brief summary
   of
   | the changes made to Python.

#. | PSF is making Python available to Licensee on an "AS IS"
   | basis. PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
   | FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
   | A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
   | OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
   THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | Nothing in this License Agreement shall be deemed to create any
   | relationship of agency, partnership, or joint venture between PSF
   and
   | Licensee. This License Agreement does not grant permission to use
   PSF
   | trademarks or trade name in a trademark sense to endorse or promote
   | products or services of Licensee, or any third party.

#. | By copying, installing or otherwise using Python, Licensee
   | agrees to be bound by the terms and conditions of this License
   | Agreement.

| BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
| -------------------------

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

#. | This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
   | office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
   | Individual or Organization ("Licensee") accessing and otherwise
   using
   | this software in source or binary form and its associated
   | documentation ("the Software").

#. | Subject to the terms and conditions of this BeOpen Python License
   | Agreement, BeOpen hereby grants Licensee a non-exclusive,
   | royalty-free, world-wide license to reproduce, analyze, test,
   perform
   | and/or display publicly, prepare derivative works, distribute, and
   | otherwise use the Software alone or in any derivative version,
   | provided, however, that the BeOpen Python License is retained in
   the
   | Software, alone or in any derivative version prepared by Licensee.

#. | BeOpen is making the Software available to Licensee on an "AS IS"
   | basis. BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
   | SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
   LOSS
   | AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR
   ANY
   | DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | This License Agreement shall be governed by and interpreted in all
   | respects by the law of the State of California, excluding conflict
   of
   | law provisions. Nothing in this License Agreement shall be deemed
   to
   | create any relationship of agency, partnership, or joint venture
   | between BeOpen and Licensee. This License Agreement does not grant
   | permission to use BeOpen trademarks or trade names in a trademark
   | sense to endorse or promote products or services of Licensee, or
   any
   | third party. As an exception, the "BeOpen Python" logos available
   at
   | http://www.pythonlabs.com/logos.html may be used according to the
   | permissions granted on that web page.

#. | By copying, installing or otherwise using the software, Licensee
   | agrees to be bound by the terms and conditions of this License
   | Agreement.

| CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1
| -------------------------

#. | This LICENSE AGREEMENT is between the Corporation for National
   | Research Initiatives, having an office at 1895 Preston White Drive,
   | Reston, VA 20191 ("CNRI"), and the Individual or Organization
   | ("Licensee") accessing and otherwise using Python 1.6.1 software in
   | source or binary form and its associated documentation.

#. | Subject to the terms and conditions of this License Agreement, CNRI
   | hereby grants Licensee a nonexclusive, royalty-free, world-wide
   | license to reproduce, analyze, test, perform and/or display
   publicly,
   | prepare derivative works, distribute, and otherwise use Python
   1.6.1
   | alone or in any derivative version, provided, however, that CNRI's
   | License Agreement and CNRI's notice of copyright, i.e., "Copyright
   (c)
   | 1995-2001 Corporation for National Research Initiatives; All Rights
   | Reserved" are retained in Python 1.6.1 alone or in any derivative
   | version prepared by Licensee. Alternately, in lieu of CNRI's
   License
   | Agreement, Licensee may substitute the following text (omitting the
   | quotes): "Python 1.6.1 is made available subject to the terms and
   | conditions in CNRI's License Agreement. This Agreement together
   with
   | Python 1.6.1 may be located on the Internet using the following
   | unique, persistent identifier (known as a handle): 1895.22/1013.
   This
   | Agreement may also be obtained from a proxy server on the Internet
   | using the following URL: http://hdl.handle.net/1895.22/1013".

#. | In the event Licensee prepares a derivative work that is based on
   | or incorporates Python 1.6.1 or any part thereof, and wants to make
   | the derivative work available to others as provided herein, then
   | Licensee hereby agrees to include in any such work a brief summary
   of
   | the changes made to Python 1.6.1.

#. | CNRI is making Python 1.6.1 available to Licensee on an "AS IS"
   | basis. CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6.1 WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
   | 1.6.1 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
   AS
   | A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON
   1.6.1,
   | OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
   THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | This License Agreement shall be governed by the federal
   | intellectual property law of the United States, including without
   | limitation the federal copyright law, and, to the extent such
   | U.S. federal law does not apply, by the law of the Commonwealth of
   | Virginia, excluding Virginia's conflict of law provisions.
   | Notwithstanding the foregoing, with regard to derivative works
   based
   | on Python 1.6.1 that incorporate non-separable material that was
   | previously distributed under the GNU General Public License (GPL),
   the
   | law of the Commonwealth of Virginia shall govern this License
   | Agreement only as to issues arising under or with respect to
   | Paragraphs 4, 5, and 7 of this License Agreement. Nothing in this
   | License Agreement shall be deemed to create any relationship of
   | agency, partnership, or joint venture between CNRI and Licensee.
   This
   | License Agreement does not grant permission to use CNRI trademarks
   or
   | trade name in a trademark sense to endorse or promote products or
   | services of Licensee, or any third party.

#. | By clicking on the "ACCEPT" button where indicated, or by copying,
   | installing or otherwise using Python 1.6.1, Licensee agrees to be
   | bound by the terms and conditions of this License Agreement.

   ::

       ACCEPT

| CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
| -------------------------

| Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
| The Netherlands. All rights reserved.

| Permission to use, copy, modify, and distribute this software and its
| documentation for any purpose and without fee is hereby granted,
| provided that the above copyright notice appear in all copies and that
| both that copyright notice and this permission notice appear in
| supporting documentation, and that the name of Stichting Mathematisch
| Centrum or CWI not be used in advertising or publicity pertaining to
| distribution of the software without specific, written prior
| permission.

| STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
| THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
| FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
| FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
| WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
| ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
| OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
| 
| 

MIT

| 
| Custom Text:
| Mypy (and mypyc) are licensed under the terms of the MIT license,
reproduced below.

= = = = =

The MIT License

Copyright (c) 2015-2021 Jukka Lehtosalo and contributors

| Permission is hereby granted, free of charge, to any person obtaining
a
| copy of this software and associated documentation files (the
"Software"),
| to deal in the Software without restriction, including without
limitation
| the rights to use, copy, modify, merge, publish, distribute,
sublicense,
| and/or sell copies of the Software, and to permit persons to whom the
| Software is furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in
| all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING
| FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
| DEALINGS IN THE SOFTWARE.

= = = = =

| Portions of mypy and mypyc are licensed under different licenses. The
| files under stdlib-samples as well as the files
| mypyc/lib-rt/pythonsupport.h, mypyc/lib-rt/getargs.c and
| mypyc/lib-rt/getargsfast.c are licensed under the PSF 2 License,
reproduced
| below.

= = = = =

| PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
| -------------------------

#. | This LICENSE AGREEMENT is between the Python Software Foundation
   | ("PSF"), and the Individual or Organization ("Licensee") accessing
   and
   | otherwise using this software ("Python") in source or binary form
   and
   | its associated documentation.

#. | Subject to the terms and conditions of this License Agreement, PSF
   hereby
   | grants Licensee a nonexclusive, royalty-free, world-wide license to
   reproduce,
   | analyze, test, perform and/or display publicly, prepare derivative
   works,
   | distribute, and otherwise use Python alone or in any derivative
   version,
   | provided, however, that PSF's License Agreement and PSF's notice of
   copyright,
   | i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007,
   2008, 2009, 2010,
   | 2011, 2012 Python Software Foundation; All Rights Reserved" are
   retained in Python
   | alone or in any derivative version prepared by Licensee.

#. | In the event Licensee prepares a derivative work that is based on
   | or incorporates Python or any part thereof, and wants to make
   | the derivative work available to others as provided herein, then
   | Licensee hereby agrees to include in any such work a brief summary
   of
   | the changes made to Python.

#. | PSF is making Python available to Licensee on an "AS IS"
   | basis. PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
   | FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
   | A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
   | OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
   THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | Nothing in this License Agreement shall be deemed to create any
   | relationship of agency, partnership, or joint venture between PSF
   and
   | Licensee. This License Agreement does not grant permission to use
   PSF
   | trademarks or trade name in a trademark sense to endorse or promote
   | products or services of Licensee, or any third party.

#. | By copying, installing or otherwise using Python, Licensee
   | agrees to be bound by the terms and conditions of this License
   | Agreement.

| BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
| -------------------------

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

#. | This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
   | office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
   | Individual or Organization ("Licensee") accessing and otherwise
   using
   | this software in source or binary form and its associated
   | documentation ("the Software").

#. | Subject to the terms and conditions of this BeOpen Python License
   | Agreement, BeOpen hereby grants Licensee a non-exclusive,
   | royalty-free, world-wide license to reproduce, analyze, test,
   perform
   | and/or display publicly, prepare derivative works, distribute, and
   | otherwise use the Software alone or in any derivative version,
   | provided, however, that the BeOpen Python License is retained in
   the
   | Software, alone or in any derivative version prepared by Licensee.

#. | BeOpen is making the Software available to Licensee on an "AS IS"
   | basis. BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
   | SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
   LOSS
   | AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR
   ANY
   | DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | This License Agreement shall be governed by and interpreted in all
   | respects by the law of the State of California, excluding conflict
   of
   | law provisions. Nothing in this License Agreement shall be deemed
   to
   | create any relationship of agency, partnership, or joint venture
   | between BeOpen and Licensee. This License Agreement does not grant
   | permission to use BeOpen trademarks or trade names in a trademark
   | sense to endorse or promote products or services of Licensee, or
   any
   | third party. As an exception, the "BeOpen Python" logos available
   at
   | http://www.pythonlabs.com/logos.html may be used according to the
   | permissions granted on that web page.

#. | By copying, installing or otherwise using the software, Licensee
   | agrees to be bound by the terms and conditions of this License
   | Agreement.

| CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1
| -------------------------
| -------------------------

#. | This LICENSE AGREEMENT is between the Corporation for National
   | Research Initiatives, having an office at 1895 Preston White Drive,
   | Reston, VA 20191 ("CNRI"), and the Individual or Organization
   | ("Licensee") accessing and otherwise using Python 1.6.1 software in
   | source or binary form and its associated documentation.

#. | Subject to the terms and conditions of this License Agreement, CNRI
   | hereby grants Licensee a nonexclusive, royalty-free, world-wide
   | license to reproduce, analyze, test, perform and/or display
   publicly,
   | prepare derivative works, distribute, and otherwise use Python
   1.6.1
   | alone or in any derivative version, provided, however, that CNRI's
   | License Agreement and CNRI's notice of copyright, i.e., "Copyright
   (c)
   | 1995-2001 Corporation for National Research Initiatives; All Rights
   | Reserved" are retained in Python 1.6.1 alone or in any derivative
   | version prepared by Licensee. Alternately, in lieu of CNRI's
   License
   | Agreement, Licensee may substitute the following text (omitting the
   | quotes): "Python 1.6.1 is made available subject to the terms and
   | conditions in CNRI's License Agreement. This Agreement together
   with
   | Python 1.6.1 may be located on the Internet using the following
   | unique, persistent identifier (known as a handle): 1895.22/1013.
   This
   | Agreement may also be obtained from a proxy server on the Internet
   | using the following URL:
   `http://hdl.handle.net/1895.22/1013" <http://hdl.handle.net/1895.22/1013">`__.

#. | In the event Licensee prepares a derivative work that is based on
   | or incorporates Python 1.6.1 or any part thereof, and wants to make
   | the derivative work available to others as provided herein, then
   | Licensee hereby agrees to include in any such work a brief summary
   of
   | the changes made to Python 1.6.1.

#. | CNRI is making Python 1.6.1 available to Licensee on an "AS IS"
   | basis. CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
   | IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
   | DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
   FITNESS
   | FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6.1 WILL NOT
   | INFRINGE ANY THIRD PARTY RIGHTS.

#. | CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
   | 1.6.1 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
   AS
   | A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON
   1.6.1,
   | OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
   THEREOF.

#. | This License Agreement will automatically terminate upon a material
   | breach of its terms and conditions.

#. | This License Agreement shall be governed by the federal
   | intellectual property law of the United States, including without
   | limitation the federal copyright law, and, to the extent such
   | U.S. federal law does not apply, by the law of the Commonwealth of
   | Virginia, excluding Virginia's conflict of law provisions.
   | Notwithstanding the foregoing, with regard to derivative works
   based
   | on Python 1.6.1 that incorporate non-separable material that was
   | previously distributed under the GNU General Public License (GPL),
   the
   | law of the Commonwealth of Virginia shall govern this License
   | Agreement only as to issues arising under or with respect to
   | Paragraphs 4, 5, and 7 of this License Agreement. Nothing in this
   | License Agreement shall be deemed to create any relationship of
   | agency, partnership, or joint venture between CNRI and Licensee.
   This
   | License Agreement does not grant permission to use CNRI trademarks
   or
   | trade name in a trademark sense to endorse or promote products or
   | services of Licensee, or any third party.

#. | By clicking on the "ACCEPT" button where indicated, or by copying,
   | installing or otherwise using Python 1.6.1, Licensee agrees to be
   | bound by the terms and conditions of this License Agreement.

   ::

       ACCEPT

| CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
| -------------------------

| Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
| The Netherlands. All rights reserved.

| Permission to use, copy, modify, and distribute this software and its
| documentation for any purpose and without fee is hereby granted,
| provided that the above copyright notice appear in all copies and that
| both that copyright notice and this permission notice appear in
| supporting documentation, and that the name of Stichting Mathematisch
| Centrum or CWI not be used in advertising or publicity pertaining to
| distribution of the software without specific, written prior
| permission.

| STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
| THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
| FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
| FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
| WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
| ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
| OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
| 
| 

| Multi-license:
| Apache-2.0 OR MIT

| 
| Attribution:
| Copyright 2015 Jukka Lehtosalo and contributors

| Licensed under the Apache License, Version 2.0 (the "License");
| you may not use this file except in compliance with the License.
| You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

| Unless required by applicable law or agreed to in writing, software
| distributed under the License is distributed on an "AS IS" BASIS,
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.

| See the License for the specific language governing permissions and
limitations under the License.
| 

numpy
^^^^^

--------------

| Multi-license:
| Apache-2.0 OR MIT

| 
| Attribution:
| Copyright 2014 Melissa O

| Licensed under the Apache License, Version 2.0 (the "License");
| you may not use this file except in compliance with the License.
| You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

| Unless required by applicable law or agreed to in writing, software
| distributed under the License is distributed on an "AS IS" BASIS,
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permissions and
limitations under the License.

.. raw:: html

   </pre>

Apache-2.0

| 
| Attribution:
| Copyright 2014 Melissa O

| Licensed under the Apache License, Version 2.0 (the "License");
| you may not use this file except in compliance with the License.
| You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

| Unless required by applicable law or agreed to in writing, software
| distributed under the License is distributed on an "AS IS" BASIS,
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permissions and
limitations under the License.

.. raw:: html

   </pre>

public-domain

| Multi-license:
| OPL-1.0 OR public-domain

| Multi-license:
| MIT OR Zlib

| 
| Attribution:
| Copyright (c) 2014 Ryan Juckett
| Permission is hereby granted, free of charge, to any person obtaining
a copy
| of this software and associated documentation files (the "Software"),
to deal
| in the Software without restriction, including without limitation the
rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
| copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE
| SOFTWARE.
| 

MIT

| Attribution:
| Copyright (c) 2014 Ryan Juckett
| Permission is hereby granted, free of charge, to any person obtaining
a copy
| of this software and associated documentation files (the "Software"),
to deal
| in the Software without restriction, including without limitation the
rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
| copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE
| SOFTWARE.
| 

| Multi-license:
| BSD-3-Clause OR MIT

| Custom Text:
| Copyright (c) 2005-2021, NumPy Developers.
| All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
| met:

::

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
| "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
| LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
| A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
| OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
| SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
| LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
| DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
| THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
| (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

| The NumPy repository and source distributions bundle several libraries
that are
| compatibly licensed. We list these here.

| Name: lapack-lite
| Files: numpy/linalg/lapack\_lite/\*
| License: BSD-3-Clause
|  For details, see numpy/linalg/lapack\_lite/LICENSE.txt

| Name: tempita
| Files: tools/npy\_tempita/\*
| License: MIT
|  For details, see tools/npy\_tempita/license.txt

| Name: dragon4
| Files: numpy/core/src/multiarray/dragon4.c
| License: MIT
|  For license text, see numpy/core/src/multiarray/dragon4.c

| Name: libdivide
| Files: numpy/core/include/numpy/libdivide/\*
| License: Zlib
|  For license text, see numpy/core/include/numpy/libdivide/LICENSE.txt
| 
| 

| Multi-license:
| BSD-3-Clause OR Zlib

| Custom Text:
| Copyright (c) 2005-2021, NumPy Developers.
| All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
| met:

::

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
| "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
| LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
| A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
| OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
| SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
| LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
| DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
| THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
| (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

| The NumPy repository and source distributions bundle several libraries
that are
| compatibly licensed. We list these here.

| Name: lapack-lite
| Files: numpy/linalg/lapack\_lite/\*
| License: BSD-3-Clause
|  For details, see numpy/linalg/lapack\_lite/LICENSE.txt

| Name: tempita
| Files: tools/npy\_tempita/\*
| License: MIT
|  For details, see tools/npy\_tempita/license.txt

| Name: dragon4
| Files: numpy/core/src/multiarray/dragon4.c
| License: MIT
|  For license text, see numpy/core/src/multiarray/dragon4.c

| Name: libdivide
| Files: numpy/core/include/numpy/libdivide/\*
| License: Zlib
|  For license text, see numpy/core/include/numpy/libdivide/LICENSE.txt
| 
| 

BSD-3-Clause

| 
| Custom Text:
| Copyright (c) 2005-2021, NumPy Developers.
| All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
| met:

::

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
| "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
| LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
| A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
| OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
| SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
| LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
| DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
| THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
| (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

| The NumPy repository and source distributions bundle several libraries
that are
| compatibly licensed. We list these here.

| Name: lapack-lite
| Files: numpy/linalg/lapack\_lite/\*
| License: BSD-3-Clause
|  For details, see numpy/linalg/lapack\_lite/LICENSE.txt

| Name: tempita
| Files: tools/npy\_tempita/\*
| License: MIT
|  For details, see tools/npy\_tempita/license.txt

| Name: dragon4
| Files: numpy/core/src/multiarray/dragon4.c
| License: MIT
|  For license text, see numpy/core/src/multiarray/dragon4.c

| Name: libdivide
| Files: numpy/core/include/numpy/libdivide/\*
| License: Zlib
|  For license text, see numpy/core/include/numpy/libdivide/LICENSE.txt
| 
| 

| Multi-license:
| BSD-3-Clause OR NCSA

| Custom Text:
| Copyright (c) 2005-2021, NumPy Developers.
| All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
| met:

::

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
| "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
| LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
| A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
| OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
| SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
| LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
| DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
| THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
| (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

| The NumPy repository and source distributions bundle several libraries
that are
| compatibly licensed. We list these here.

| Name: lapack-lite
| Files: numpy/linalg/lapack\_lite/\*
| License: BSD-3-Clause
|  For details, see numpy/linalg/lapack\_lite/LICENSE.txt

| Name: tempita
| Files: tools/npy\_tempita/\*
| License: MIT
|  For details, see tools/npy\_tempita/license.txt

| Name: dragon4
| Files: numpy/core/src/multiarray/dragon4.c
| License: MIT
|  For license text, see numpy/core/src/multiarray/dragon4.c

| Name: libdivide
| Files: numpy/core/include/numpy/libdivide/\*
| License: Zlib
|  For license text, see numpy/core/include/numpy/libdivide/LICENSE.txt
| 
| 

Multi-license:

BSD-3-Clause OR Python-2.0

| Custom Text:
| Copyright (c) 2005-2021, NumPy Developers.
| All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
| met:

::

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
| "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
| LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
| A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
| OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
| SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
| LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
| DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
| THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
| (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

| The NumPy repository and source distributions bundle several libraries
that are
| compatibly licensed. We list these here.

| Name: lapack-lite
| Files: numpy/linalg/lapack\_lite/\*
| License: BSD-3-Clause
|  For details, see numpy/linalg/lapack\_lite/LICENSE.txt

| Name: tempita
| Files: tools/npy\_tempita/\*
| License: MIT
|  For details, see tools/npy\_tempita/license.txt

| Name: dragon4
| Files: numpy/core/src/multiarray/dragon4.c
| License: MIT
|  For license text, see numpy/core/src/multiarray/dragon4.c

| Name: libdivide
| Files: numpy/core/include/numpy/libdivide/\*
| License: Zlib
|  For license text, see numpy/core/include/numpy/libdivide/LICENSE.txt
| 
| 

| Zlib
| Attribution:
| This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.
| Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

#. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
#. Altered source versions must be plainly marked as such, and must not
   be misrepresented as being the original software.
#. This notice may not be removed or altered from any source
   distribution.

| SunPro
| Attribution:
| Copyright (C) 1993 by Sun Microsystems, Inc. All rights
reserved.\\nDeveloped at SunPro, a Sun Microsystems, Inc.
business.\\n\\nPermission to use, copy, modify, and distribute
this\\nsoftware is freely granted, provided that this notice\\nis
preserved.
| 

BSD-2-Clause

| 
| Attribution:
| Copyright (c) 2010 The Android Open Source Project<<beginOptional>>
| All rights reserved.<<endOptional>>

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
met:

#. | Redistributions of source code must retain the above copyright
   notice, this
   |  list of conditions and the following disclaimer.

#. | Redistributions in binary form must reproduce the above copyright
   notice,
   |  this list of conditions and the following disclaimer in the
   documentation

   and/or other materials provided with the distribution.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS"
| AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE
| IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE
| DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE
| FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL
| DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR
| SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER
| CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY,
| OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
| 

CC-BY-SA-3.0 AND CC-BY-4.0

| X11
| Attribution:
| Copyright (C) 1996 X Consortium
| Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:
| The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
| Except as contained in this notice, the name of the X Consortium shall
not be used in advertising or otherwise to promote the sale, use or
other dealings in this Software without prior written authorization from
the X Consortium.
| X Window System is a trademark of X Consortium, Inc.
| 

pyparsing
^^^^^^^^^

--------------

MIT

| Attribution Notice:
| Permission is hereby granted, free of charge, to any person obtaining
| a copy of this software and associated documentation files (the
| "Software"), to deal in the Software without restriction, including
| without limitation the rights to use, copy, modify, merge, publish,
| distribute, sublicense, and/or sell copies of the Software, and to
| permit persons to whom the Software is furnished to do so, subject to
| the following conditions:

| The above copyright notice and this permission notice shall be
| included in all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
| EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
| MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
| IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
| CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
| TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
| SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
| 
| 
| Multi-license:

-  GPL-3.0-only OR MIT

pyrsistent
^^^^^^^^^^

--------------

MIT

| Attribution Notice:
| Copyright (c) 2021 Tobias Gustafsson

| Permission is hereby granted, free of charge, to any person
| obtaining a copy of this software and associated documentation
| files (the "Software"), to deal in the Software without
| restriction, including without limitation the rights to use,
| copy, modify, merge, publish, distribute, sublicense, and/or sell
| copies of the Software, and to permit persons to whom the
| Software is furnished to do so, subject to the following
| conditions:

| The above copyright notice and this permission notice shall be
| included in all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
| EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
| OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
| NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
| HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
| WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
| FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
| OTHER DEALINGS IN THE SOFTWARE.
| 
| 

BSD-3-Clause

| Attribution:
| Copyright (c) 2013 Matthew Rocklin . All rights reserved.

| Redistribution and use in source and binary forms, with or without
| modification, are permitted provided that the following conditions are
met:

#. | Redistributions of source code must retain the above copyright
   notice,
   |  this list of conditions and the following disclaimer.

#. | Redistributions in binary form must reproduce the above copyright
   notice,
   |  this list of conditions and the following disclaimer in the
   documentation
   |  and/or other materials provided with the distribution.

#. | Neither the name of the copyright holder nor the names of its
   |  contributors may be used to endorse or promote products derived
   from
   |  this software without specific prior written permission.

| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS"
| AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE
| IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE
| DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE
| FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL
| DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR
| SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER
| CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY,
| OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE
| OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
| 
| 

pytest
^^^^^^

--------------

MIT

| Attribution Notice:
| The MIT License (MIT)

Copyright (c) 2004-2020 Holger Krekel and others

| Permission is hereby granted, free of charge, to any person obtaining
a copy of
| this software and associated documentation files (the "Software"), to
deal in
| the Software without restriction, including without limitation the
rights to
| use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies
| of the Software, and to permit persons to whom the Software is
furnished to do
| so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
| copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE
| SOFTWARE.
| 
| 

pytest-mock
^^^^^^^^^^^

--------------

MIT

| Attribution Notice:
| MIT License

Copyright (c) [2016] [Bruno Oliveira]

| Permission is hereby granted, free of charge, to any person obtaining
a copy
| of this software and associated documentation files (the "Software"),
to deal
| in the Software without restriction, including without limitation the
rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
| copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE
| SOFTWARE.
| 
| 

pytest-xdist
^^^^^^^^^^^^

--------------

MIT

| Attribution Notice:
| 
|  Permission is hereby granted, free of charge, to any person obtaining
a copy
|  of this software and associated documentation files (the "Software"),
to deal
|  in the Software without restriction, including without limitation the
rights
|  to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell
|  copies of the Software, and to permit persons to whom the Software is
|  furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be
included in all
|  copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR
|  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
|  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE
|  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER
|  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM,
|  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE
|  SOFTWARE.
| 
| 

.. |Continuous Integration| image:: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml/badge.svg
   :target: https://github.com/rjdbcm/Aspidites/actions/workflows/python-app.yml
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/8d03ef8667df59d55380/maintainability
   :target: https://codeclimate.com/github/rjdbcm/Aspidites/maintainability
.. |codecov| image:: https://codecov.io/gh/rjdbcm/Aspidites/branch/main/graph/badge.svg?token=78fHNV5al0
   :target: https://codecov.io/gh/rjdbcm/Aspidites
.. |logo| image:: https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_wheelie.png
.. |PyPI| image:: https://img.shields.io/pypi/v/aspidites?color=pink&label=&logo=pypi
   :target: https://pypi.org/project/Aspidites/
.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/Aspidites
   :target: https://pypi.org/project/Aspidites/#files
.. |Docker Image Version (latest by date)| image:: https://img.shields.io/docker/v/rjdbcm/aspidites?color=pink&label=%20&logo=docker
.. |Docker Image Size (latest semver)| image:: https://img.shields.io/docker/image-size/rjdbcm/aspidites
   :target: https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated
.. |GitHub release (latest SemVer)| image:: https://img.shields.io/github/v/release/rjdbcm/Aspidites?color=pink&label=&logo=github&logoColor=black
.. |GitHub commits since tagged version (branch)| image:: https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main
.. |libraries.io| image:: https://img.shields.io/badge/Libraries.io--inactive
   :target: https://libraries.io/github/rjdbcm/Aspidites
.. |GitHub| image:: https://img.shields.io/github/license/rjdbcm/Aspidites
