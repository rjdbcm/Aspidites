**unreleased**
**v1.0.0**
**v0.26.2**

- 7cd68b1 update .bumpversion.cfg


**v0.26.1**

- 5d771ab Merge remote-tracking branch 'origin/main'
- 09581e5 Update README.md
- 396125d Update README.md
- 6cc6f15 Update README.md
- 049253d Update README.md


**v0.26.0**

- 1b14255 added a tab on coroutines
- 9a20430 added a note on coroutines
- 9a5e98e added Any to the return annotation of Maybe
- 3d11296 looping works
- 2b0cc42 Update readme
- 1e83f50 remove table as it is now redundant


**v0.25.13**

- 7ff8d2c remove non-applicable note
- d0e8bc4 added SafeFactorial implementation of math.factorial
- 034d36b add trigram table to docs
- ab51d32 loop trigram (<@>) now parses into for loop for single bindvar
- f7a4501 loop trigram (<@>) now parses into for loop
- ecd71ec added for (<@>), pass (<#>), continue (<$>), and break (<%>) trigrams.
- a164c33 add immutables and ellipsis sections.
- b68be98 Update README.md


**v0.25.12**

- c2bc363 add todo-to-issue


**v0.25.11**

- db0cbfd cleaned up todos for automated issue creation
- 41e57c4 Update deploy.yml
- 3654fac add TODO to issue


**v0.25.10**

- f0f8bbf Update deploy.yml


**v0.25.9**

- e6f0fa1 got rid of deadline for test_single_underscore_in_binops_can_accept_one_arg


**v0.25.8**

- 5327c20 more vendored pyparsing tests


**v0.25.7**

- cef1ac1 Merge remote-tracking branch 'origin/main'
- 5317362 Update deploy.yml
- cab30fa add create-release


**v0.25.6**

- 6a1bd60 add the rest of the pyparsing test cases


**v0.25.5**

- cebe91e optimization of try-excepts
- 6cb464c Merge remote-tracking branch 'origin/main'
- 78e64bb Update README.md
- 1e2abca Update README.md


**v0.25.4**

- 5491a8d readd test_final.py
- d8ff880 improve readability
- 076dece Update test.yaml


**v0.25.3**

- e169a77 Update deploy.yml


**v0.25.2**

- 84f86f1 fix workflows to be dependent


**v0.25.1**

- 49a0cd5 Added missing func slot to Undefined


**v0.25.0**

- 32484ba Undefined records elements absorbed without affecting arithmetic
- 8171598 add hasattr check in place of try-except in Maybe repr
- b9e559c Merge remote-tracking branch 'origin/main'
- fb2d059 attempt to fix flakey CI tests introduced in 0.25.0
- 36b482a make it so repr succeeds for builtins called via Maybe
- c4c581a remove caching to try and fix flakey tests
- 060575d add SLOC to badges
- f4c795d add operator table to indepth.rst
- d370e0c add tokei configuration
- 3ffd3f3 Merge remote-tracking branch 'origin/main'
- 8c1e01e Create codecov.yml


**v0.24.10**

- b54770b added proftest for profiling
- 7d39e0b fix typo: now using internal pyparsing module for tests
- 792e994 use vendored inspection module
- e5ffa5a add cython language_level directive
- 12b9e2b in depth documentation added.
- 98dbc86 Undefined now caches parameters and works as described in the docs
- 78e6a73 edit to make sysconfig work again.
- b892dd7 reduce inspection.py to just what we need.
- 1d4c561 changelog updated



- 


**v0.24.9**

- 364b2c8 fix .coveragerc as it overrides pytest-cov's defaults


**v0.24.8**

- 999ae10 fix .coveragerc as it overrides pytest-cov's defaults


**v0.24.7**

- 76ed483 rollback codeclimate-action is still broken


**v0.24.6**

- ce1befe re add codeclimate coverage reporter
- 8693ec9 changelog updated
- c77b99d added vendored test suite for pyparsing.



- c77b99d added vendored test suite for pyparsing.


**v0.24.5**

- 


**v0.24.4**

- a412ce6 added comment to convert explaining PackRat
- e04dcee removed reference to distutils as it is pending deprecation
- c26c0a0 fixed whoopsie


**v0.24.3**

- 5cb1948 fixed encoding whoopsie


**v0.24.2**

- e5aaf64 improve cyclomatic complexity
- 8432e35 improve cyclomatic complexity


**v0.24.1**

- f0ce955 move around code for maintainability
- 58f9c24 move around code for maintainability
- b1e3000 move around code for maintainability


**v0.24.0**

- fc39c2f remove conditional def of match case. not backwards compatible at the moment.


**v0.23.0**

- 5d0a859 fix order of condition def py3.10


**v0.22.1**

- cc4b3f0 changelog updated
- 721938b profile guided optimization brought down contract parsing and instantiation to an average of 1.2ms/call



- 721938b profile guided optimization brought down contract parsing and instantiation to an average of 1.2ms/call


**v0.22.0**

- 9b3a4de fix import typo


**v0.21.2**

- d532585 interred pyparsing to _vendor and added static compile 2.9milliseconds/call -> 80microseconds/call to parseImpl
- 3ccf750 changelog updated
- de09c5a interred pyparsing to _vendor and added static compile 2.9milliseconds/call -> 80microseconds/call to parseImpl
- 16e656d major optimizations to speed up refinement typing with contracts
- f1dfe6e everything is mostly typed so boundschecking and wraparound are mostly off
- e6929d0 fix tuple typo
- 5d098c2 added a rudimentary REPL interpreter
- cd1c7cb moved decorator methods into decorator_extension.py for static compile
- 1694903 got rid of final decorator for classes keeping the module for now
- fdd58f4 fix PY3.10 test compatibility



- de09c5a interred pyparsing to _vendor and added static compile 2.9milliseconds/call -> 80microseconds/call to parseImpl
- 16e656d major optimizations to speed up refinement typing with contracts
- f1dfe6e everything is mostly typed so boundschecking and wraparound are mostly off
- e6929d0 fix tuple typo
- 5d098c2 added a rudimentary REPL interpreter
- cd1c7cb moved decorator methods into decorator_extension.py for static compile
- 1694903 got rid of final decorator for classes keeping the module for now
- fdd58f4 fix PY3.10 test compatibility


**v0.21.1**

- 7475765 fix python-setup action to use v2 and added quotes around 3.10 because YAML


**v0.21.0**

- 16a2a6c add CPython 3.10 to actions


**v0.20.1**

- eeb97c1 reference internal inspect functions where possible
- 110de20 clean up unused code
- 92bf9c3 added C( for declaring c-style functions


**v0.20.0**

- c0bae3d fixed typo that included backported.py in build list


**v0.19.0**

- 7364650 inspection is now essentially a statically compiled version of inspect.py


**v0.18.16**

- 


**v0.18.15**

- b3f951d major speedup of the new_contract decorator 30.8ms/call -> 23.05ms/call


**v0.18.14**

- d07381e slight speedup of warnings generated using early binding
- 597627b slight speedup of warnings generated using f-strings and explicit encoding/decoding


**v0.18.13**

- 944bdba fully static compile for the main compiler infrastructure


**v0.18.12**

- dd278bf fix windows wheel
- b0d4141 Merge remote-tracking branch 'origin/main'
- b87d031 Update README.md


**v0.18.11**

- fac6eee contracts backend is now a statically compiled extension excluding decorators
- 20739ee changelog updated

**v0.18.10**

- 97bc989 added numpy to pyproject.toml


**v0.18.9**

- c60ef23 removed CI for windows build


**v0.18.8**

- 14164d1 fix typo in api list[str] becomes List[str]


**v0.18.7**

- 135beb7 contracts metaclass is now statically compiled
- 8d00d77 changelog updated
- ea16aa8 major typo fixed
- 18d3a1d minor cleanup



- ea16aa8 major typo fixed
- 18d3a1d minor cleanup


**v0.18.6**

- 1e5fb28 made the parser a statically compiled object
- adc8589 added type hints and py.typed to package_data
- b456d1b changed import collections to import collections.abc as collections


**v0.18.5**

- 3d522fa fix windows build 6th attempt


**v0.18.4**

- 7e417fc fix windows build 5th attempt


**v0.18.3**

- 6497d17 fix windows build 4th attempt


**v0.18.2**

- f393ac3 fix windows build 3rd attempt


**v0.18.1**

- 51382dc fix windows build 2nd attempt


**v0.18.0**

- e8a4e28 fix windows build


**v0.17.0**

- 3034c5c Multiple statements in function declaration and conditionals added.
- 468e08b Merge remote-tracking branch 'origin/main'
- 642a735 Update dependabot.yml
- fb3c120 dependabot


**v0.16.0**

- 53c8846 Refactor of compiler and simplification of API.


**v0.15.0**

- 475d0e7 Refactor to get standalone binaries to compile


**v0.14.31**

- fc1bf2a add workaround for embed not working


**v0.14.30**

- 87c4cc6 add windows wheels


**v0.14.29**

- 8d2fdc3 add windows wheels


**v0.14.28**

- 6689923 separate sdist and wheel builds


**v0.14.27**

- 082119f build cp37, cp38, & cp39 wheels for manylinux and macos-11 with no waiting for CI!


**v0.14.26**

- d82bf50 build cp37, cp38, & cp39 wheels for manylinux and macos-11 with no waiting for CI!


**v0.14.25**

- 7dff089 build cp37, cp38, & cp39 wheels for manylinux and macos-11 with no waiting for CI!
- 50ae520 Merge remote-tracking branch 'origin/main'
- 8d5ae17 Update README.md


**v0.14.24**

- 858a60a build cp37, cp38, & cp39 wheels for manylinux and macos-11


**v0.14.23**

- cba8125 got rid of wait for macos-11-deploy, just depends on linux build.


**v0.14.22**

- c1e0408 better ci workflow


**v0.14.21**

- ef43e51 better ci workflow


**v0.14.20**

- 11f1a86 better ci workflow
- fc7c2b9 Update deploy.yml
- 17c07fd Update deploy.yml


**v0.14.19**

- fa2e1f1 better ci workflow


**v0.14.18**

- 7d0dc50 fix publish wheel


**v0.14.17**

- e5b04d0 added macos-11 job to deploy.yml


**v0.14.16**

- ea87470 fix package deploy


**v0.14.15**

- 6ebcb42 fix package deploy


**v0.14.14**

- 0abd300 fix package deploy


**v0.14.13**

- ee6db7b fix package deploy


**v0.14.12**

- 9b17dc7 fix package deploy


**v0.14.11**

- 8a3f508 fix package deploy


**v0.14.10**

- 9d4c96a fix package deploy


**v0.14.9**

- 4154775 fix package deploy
- e9a0cbb changelog updated



- 


**v0.14.8**

- d3a3db1 Merge remote-tracking branch 'origin/main'
- 9990f53 fix package deploy
- f32bd62 Update deploy.yml


**v0.14.7**

- a23edb0 fix package deploy


**v0.14.6**

- ce36b8a fix setup.py


**v0.14.5**

- def0588 fix Dockerfile


**v0.14.4**

- 9740058 fix test complaints
- 206ada4 Merge remote-tracking branch 'origin/main'
- 3e4b5f9 Update README.md
- f6e9d87 Update README.md



**v0.14.3**

- a1f2ad1 trying out static compiled library
- a9a16e9 prep CHANGELOG.md



**v0.14.2**

- 1495432 prep CHANGELOG.md
- 8cb61ee prep CHANGELOG.md
- d1e065a add default_file template
- 5cfde28 add default_file template
- 70d9bb3 cython_math
- 2fd20c8 ci.yml: maybe paambaati/codeclimate-action@v2.7.5 had a token expire?
- cd29f99 revert
- a741f80 made deploy depend on CI success.

**v0.14.1**

- 3efe0f9 moved tests so there is more organization
- 0e8b448 adjust codeclimate coverage
- 20a7c0f adjust codeclimate coverage
- a120dbf adjust codeclimate coverage
- c642c5d adjust codeclimate coverage
- 6ec0411 adjust codeclimate coverage
- ff01ce7 adjust codeclimate coverage
- c724255 adjust codeclimate coverage
- 2667e93 adjust codeclimate coverage
- fd289d5 adjust coverage
- 466dbd6 adjust coverage for Sequences
- fc48ad3 adjust coverage for __main__.py
- 144a586 fix some Windows compatibility stuff for test suite

**v0.14.0**

- 594c95f added isnan check for SafeUnary Ops
- cf7b488 Adjust range of integers tested


**v0.13.5**

- 0ca5c25 .gitignore: added /Aspidites.egg-info/
- c2d467c added more safe math and tests
- 417903b templates.py: moved around imports
- 65871d8 setup.py: includes *.so files in package data
- 1359109 removed pampy from vendored packages It's not what I would like for pattern matching
- fd311d8 moved math to its own module
- 6961de9 added evolver syntax
- 5517ca7 Added tabs to code examples and expanded width
- 141694d Added tabs to code examples
- 73ac0ca Added tabs to code examples
- 17590d5 Added tabs to code examples
- bf0d098 Merge remote-tracking branch 'origin/main'
- 01f6f62 Added tabs to code examples
- 277e3c1 Update README.rst
- 3357e1a Update README.rst
- df0eab1 Update README.rst
- c39f6aa Update README.rst
- ba6949b Update README.rst
- 68a04b2 Update devinfo.rst
- 9be3920 Added non-paywalled article
- 6b332b7 Update README.rst
- bd9c804 Update README.rst
- a7b80e1 Update README.rst
- 571260e Create FUNDING.yml
- cc59269 added workflow to check urls
- 44542ab shelved github-deploy.yml and chocolatey-deploy.yml
- 9495a75 added github-deploy.yml


**v0.13.4**

- 9ceffcc added github-deploy.yml
- 3123dbd dockerhub-description.yml gone
- 45bc99e update TLDR version of readme for docker
- 1f321c3 update TLDR version of readme for docker
- a3e6e97 update TLDR version of readme for docker
- 06d85cd Merge remote-tracking branch 'origin/main'
- a7bbd41 update TLDR version of readme for docker
- dae5e76 Update dockerhub-description.yml
- e96c3fb Merge remote-tracking branch 'origin/main'
- bcdd266 add TLDR version of readme for docker
- b1c917a Update container-deploy.yml
- bfc9cc9 Create dockerhub-description.yml


**v0.13.3**

- 5123753 docker build fixed maybe


**v0.13.2**

- eb811f0 docker build fixed maybe


**v0.13.1**

- 0beffe6 docker build fixed


**v0.13.0**

- 6c588be docker build fixed



**v0.12.4**

- 0a69158 fix bumpversion
- e10859a changelog updated
- c0ba773 Changelog
- 1b0c469 fix bumpversion
- 0e265ed compiler.py: CheckedFileStack refactored and added docstrings
- 5845710 Makefile: xtest added for dev
- ccf89f4 fix typo from refactor
- 29cb68d fix ci
- e1e85ba Refactor CheckedFileStack
- d0deb59 Merge pull request #11 from rjdbcm/dev
- 06aa424 Merge pull request #10 from rjdbcm/main
- 76af14b container-deploy.yml: update README.md path
- be7da01 .dockerignore: added a bunch of config files and CI stuff
- a6373fb Merge remote-tracking branch 'origin/dev' into dev
- 7306d89 Docker deploy now updates readme on Dockerhub
- 1202f47 Update ci.yml
- f49e87c Update ci.yml
- cf16be8 Merge remote-tracking branch 'origin/dev' into dev
- 5665be1 Merge pull request #9 from rjdbcm/dev
- 0ec30fc Update README.md
- 6604b5c Update README.md
- aeb3ff2 Update deploy.yml
- a5418b9 Merge pull request #8 from rjdbcm/main
- f2fc9cc update pygments-woma-lexer
- 8f3e698 update pygments-woma-lexer
- f2e6d7c v0.12.3 released
- e5706e2 changelog updated
- 0c01045 update pygments-woma-lexer
- 4203609 v0.12.2 released
- 8ca64fa changelog updated
- f7d39de Pulled a Warn class from SafeMath, Maybe etc.
- 73cb135 v0.12.1 released
- 9e19425 changelog updated
- ceafa58 clean up imports
- 01f394f monads.py: stack is inspected during __init__
- 29a8699 final.py: clean imports and add docstrings
- 99dcd66 fix tab typo
- c30dae3 add gitignores
- a0719ab add smol logo
- 53a87f8 Makefile: added all phonies and changed clean-md5 to clean-sha
- cd3ccc7 Merge remote-tracking branch 'origin/main'
- db0056e move WomaLexer into a separate repo pygments-woma-lexer
- c66fc8e changelog updated
- 8c87881 v0.12.0 released
- 5082236 changelog updated
- 5dee3f1 reserved.py: made nullit Literal and operators use a regex
- b645d1a parser.py: fixed some imports, fixed list_item precedence
- 51955d6 conf.py rewrote lexer in preparation to move to its own package
- ecd259d examples.wom: comp op comment out
- 47f6bbd Update README.md
- 4a92f4f Update README.md
- 94f09dc Update README.md
- e39b931 examples.wom: commented out nullit
- 1d481ba test_aspidites.py: imports
- e4c955b Merge remote-tracking branch 'origin/main'
- 7112ad6 add nullit to examples.wom
- bf3770b add cache to ci.yml
- c8c6cb7 source tree cleanup
- 3b62aec Update README.md
- e04474a Update README.md
- f73454b Update README.md
- 504b659 source tree cleanup
- 2dbb868 v0.11.28 released
- e83a1c5 changelog updated
- 9612bad fix gh action
- b38f0a2 v0.11.27 released
- cbbab05 changelog updated
- 9f66792 fix gh action
- a11f8ef v0.11.26 released
- 62b412a changelog updated
- 6763d53 fix gh action
- 43dbb8c v0.11.25 released
- 9983421 changelog updated
- 467bb83 fix gh action
- 4939c2e v0.11.24 released
- bf09f12 changelog updated
- 34ae2f9 fix gh action: last try
- 3ae88f4 v0.11.23 released
- e9625fa changelog updated
- 74ec955 fix gh action: last try
- 914e444 v0.11.22 released
- eec05d4 changelog updated
- 08cc826 fix gh action
- 5220093 v0.11.21 released
- eb63ae3 changelog updated
- 6266ad8 fix gh action
- 93c9508 v0.11.20 released
- be4cfe6 changelog updated
- 3887e2b fix gh action
- 4016c8e v0.11.19 released
- 8aa6c1c changelog updated
- 312e224 fix gh action
- d5c3513 v0.11.18 released
- 4869195 changelog updated
- dd2739f fix gh action
- 54ecacc v0.11.17 released
- b708d6e changelog updated
- 87a4f53 fix gh action
- d94801e v0.11.16 released
- c0f2f32 changelog updated
- 08b2f9e fix gh action
- 75598b6 v0.11.15 released
- 15602e4 changelog updated
- fd61123 fix gh action
- b665728 changelog updated
- a62f227 fix gh action
- af66c7b v0.11.14 released
- 74e3841 changelog updated
- a1cb254 fix gh action
- fcb0f20 v0.11.13 released
- 384b7d1 changelog updated
- aea7577 fix gh action
- 2614b65 v0.11.12 released
- f98f0dd changelog updated
- 032c0dd fix gh action
- 0c54ef2 v0.11.11 released
- 82a617f changelog updated
- 0dae705 add chocolatey package
- 9be4417 changelog updated
- 94589bd add chocolatey package
- 02a3674 changelog updated
- a971a26 changelog updated
- 4531c37 add chocolatey package
- 23a5029 changelog updated
- 9e06bd4 changelog updated
- 304deb8 add chocolatey package
- 8c8f742 v0.11.10 released
- eee216c changelog updated
- 9eea2b9 setup.py: fix typo
- 0d56b93 v0.11.9 released
- 4ed67e8 changelog updated
- 06adba0 fix path
- fa4a2e2 v0.11.8 released
- 3babd1a changelog updated
- 9c83996 update supported OSes
- 2e5e9f4 Update ci.yml add macos
- 48dc267 Update README.md
- 68215f2 Merge pull request #7 from rjdbcm/rjdbcm-patch-1
- 40973bd fix for windows unicode support
- 681e9c6 Update ci.yml
- 9cdc310 Update and rename python-app.yml to ci.yml
- 547ed18 convert.py: pep8
- 28bdc61 templates.py lib template add compile(restricted) and other builtins
- 9c7522f Makefile: test-all depends on clean-test
- a637984 Use pathlib.Path for path representations
- a0888d2 refactor monads.py for readability
- d7f1423 Added stubs for RestrictedPython
- 8c6c8d4 Merge remote-tracking branch 'origin/main'
- 6cb6219 refactor of the parser to make it a bit less brittle when modified
- 650419c Update README.md
- 6f24118 Update README.md
- 11413e5 Update README.md
- a72e1fa Merge remote-tracking branch 'origin/main'
- bc8fb5a remove joker
- ebf4ea6 Update social.yml
- a3f1eb7 test joke api
- f67eded test joke api
- 3a0638c test joke api
- c5817fb Merge remote-tracking branch 'origin/main'
- fcf13ea test joke api
- d362649 Update social.yml
- 9b786a1 Update social.yml
- 7243005 Merge remote-tracking branch 'origin/main'
- 994bf03 test joke api
- fdf800a Update README.md
- b8d5079 v0.11.7 released
- bbef565 changelog updated
- c0bbfc2 changelog updated
- 5707afc fix social message on container-deploy.yml
- 945cc72 Update python-app.yml
- fc1f72f absolute import of test examples
- 11ec1d0 fix build action
- ffee7cb fix build action
- 852897a PyPy not supported. Maybe and F now inherit from symtable.Function. This is the plan for future classes used as the basis of the functional interface.
- 29e1d22 compiler.py compatible with Python 3.7
- f6cbdc0 compiler.py compatible with Python 3.7
- d708ff8 compiler.py compatible with Python 3.7
- 189fa3d drop Python 3.6 support
- fde2df4 fix test to be a quick source install
- cbf29d3 Update Package to show tested python versions/implementations
- 1b17ab6 Update python-app.yml
- 10a93f2 Update python-app.yml
- 61dcabd Update python-app.yml
- 3e775e0 Update python-app.yml
- f23d236 Update python-app.yml
- 7174b0e Update python-app.yml
- 4f24fc5 Update python-app.yml
- d5aeed5 Update python-app.yml
- 20cd069 Update python-app.yml
- 151ec1f Update python-app.yml
- a224da0 Update python-app.yml
- ad8fa09 Update python-app.yml
- 9e2a44b Update python-app.yml
- ca11af3 CI workflow for CPython v3.9.6 and v3.8.11
- 6731f2a Update README.md
- 0beaa2c Update README.md
- 7717cd7 Update README.md
- 20cbb78 Update README.md
- e10f67e v0.11.6 released
- 9893963 changelog updated
- 62d6a06 revert testconfig sort, it wasn't that my tests were running 2x
- 3be0154 update codeclimate and coverage exclude patterns
- 3357545 v0.11.5 released
- 30e6be4 changelog updated
- 6eb2d29 deployment changes so twitter works
- 26d6e69 Bump version: 0.11.3 → 0.11.4
- 9667530 changelog updated
- 0d899d2 BUGFIX: 0.11.3 still had a buggy import of final so it's gone for now
- a783f1c Bump version: 0.11.2 → 0.11.3
- aa9ba95 changelog updated
- dad6dd3 BUGFIX: 0.11.2 had a buggy final import
- d372870 Bump version: 0.11.1 → 0.11.2
- b55f9e9 changelog updated
- 1d62e60 BUGFIX: testsuite formerly ran every unittest 2x
- 2d9baa6 adjust cognitive complexity threshold to 6 for codeclimate
- 8df122c Merge remote-tracking branch 'Aspidites/main' into main
- a90b3a8 added final class decorator and adjusted a few import statements to be relative
- b3f5017 parametrized tests and pytest.mark.uses_stdout tests are moved to the end
- ca2af84 Update README.md
- f811bc7 Bump version: 0.11.0 → 0.11.1
- c63b8ef changelog updated
- 82b9ec9 buffer size for CheckedFileStack now defaults to a more reasonable 128 bytes
- 1085506 changelog updated
- 4200f78 changelog reformatted
- 31c0234 Bump version: 0.10.1 → 0.11.0
- 2f76359 changelog updated
- 63d0548 refactor CheckedFileStack class and compiler.py functions to used pathlib
- 19ff71b inset search border
- ddb57de add some transparency and gradients
- 01c8e23 Added tabbed interfaces to docs/homepage
- 54121d2 remove duplicated code
- f4c3ac2 Bump version: 0.10.0 → 0.10.1
- b3070c4 changelog updated
- 598f86a patch setup.py woma compile
- c39ac21 changelog updated
- 38b992b Bump version: 0.9.34 → 0.10.0
- f0430e0 changelog updated
- a11958b refactor compiler.py for better decoupling of various writes
- 839cc92 Enables sets tests
- e0e5af8 Merge remote-tracking branch 'Aspidites/main' into main
- 09ef124 Remove link to blank search page from docs index.rst
- 048f0a6 Added more temp folders to .gitignore
- dca63cd Added docs to .coveragerc and .dockerignore
- c1fdb8c removed no covers from contracts utils.py functions that are still in use
- 63aae94 add testcases for sets.
- 5c3e33f prune docs from Manifest.in
- ef611fc added sanity tests for contract function inspection
- 7c72b3f Update README.md
- 979c1cb fix GNU license in doc
- 542bb0c adjust sections and pages of docs
- 6bc98f1 add copybutton for shell commands to docs
- d913dd4 Adjusted doc stylesheets for a responsive experience
- fbc2fe6 very nice reactive but unobtrusive doc website
- 2d7e5ef docs now have a nice examples section
- c105f64 fix animation
- 122da38 mild README.rst reformatting
- 6feadb4 toctree now goes 3 deep.
- 7daeb79 fixed so docs talk about the language not the reference implementation.
- b3fa422 Full sized Wheelie in docs
- b98ec6a logo update
- 77aa6f4 Prep compiler.py for refactor
- 7f65eb7 Add __mimetype__
- 7a41b9f Add updated docs logo
- c868389 Nice looking docs.
- 79440ba update docs logo
- 7209649 fix Programmable Error in rtd build
- 6780de9 Add numpy to docs/requirements.txt
- 61ceba6 Add readthedocs config and requirements.txt
- 300b23d Merge remote-tracking branch 'Aspidites/main' into main
- 9a3786d Add path insert to docs conf.py
- a2adcaa typo fixed in change logger
- 0116645 Update CHANGELOG.md
- ee02a7d Bump version: 0.9.33 → 0.9.34
- 82f2c1e changelog updated
- 3912e63 fixed main() call in test_aspidites.py
- 1cb8ccc Bump version: 0.9.32 → 0.9.33
- 34a83b2 changelog updated
- fa9d60d CLI test to fix coverage missing for __main__.py
- af52c56 Make sure to raise a SystemExit when running our tests from a different thread.
- 39ec7ce Makefile doesn't complain about circular deps
- 3f7a8b6 fix minor bumpversion_hook formatting issue
- 6c23140 Bump version: 0.9.31 → 0.9.32
- 21fadaa changelog updated
- 7aa21f1 quick update to version changelogger and it is finally working
- 6bbc8c1 minor makefile cleanup
- 8263ce4 changelog updated
- 49ea6b1 finally got bumps to work!
- c3db2a1 maybe fixed version changelogging
- 509a146 Bump version: 0.9.30 → 0.9.31
- c2aa35d changelog updated
- fe655c7 fixed that pesky bumpversion_hook.py
- 7e45564 Bump version: 0.9.29 → 0.9.30
- 010647c changelog updated
- 3856180 bumpversion_hook should be in order.
- 4423a00 changelog building hook executes and commits before any version bump.
- 78b1ba1 Bump version: 0.9.28 → 0.9.29
- acb37e5 version bumps trigger a changelog building hook
- d2940d4 added version bump and changelog builder
- ff33ccf direct function calls within function definitions now work!
- aee85d7 Bump version: 0.9.27 → 0.9.28
- 5c6443b Literally a patch just for a logo?!
- 610db59 Bump version: 0.9.26 → 0.9.27
- 2429e86 New logo! IP info in README.md test of entrypoint works
- c0c8905 Merge remote-tracking branch 'Aspidites/main' into main
- 770f488 logo should work on PyPI
- fb70a61 Update README.md
- 7d5f824 Merge remote-tracking branch 'Aspidites/main' into main
- c54e12a Bump version: 0.9.25 → 0.9.26
- 2cf9b29 themed docs for light or dark preferences. sphinx_rtd_theme a dev requirement added twitter tweeter.
- 341bb43 Update README.md



**v0.12.3**

- c0ba773 Changelog
- 1b0c469 fix bumpversion
- 0e265ed compiler.py: CheckedFileStack refactored and added docstrings
- 5845710 Makefile: xtest added for dev
- ccf89f4 fix typo from refactor
- 29cb68d fix ci
- e1e85ba Refactor CheckedFileStack
- d0deb59 Merge pull request #11 from rjdbcm/dev
- 06aa424 Merge pull request #10 from rjdbcm/main
- 76af14b container-deploy.yml: update README.md path
- be7da01 .dockerignore: added a bunch of config files and CI stuff
- a6373fb Merge remote-tracking branch 'origin/dev' into dev
- 7306d89 Docker deploy now updates readme on Dockerhub
- 1202f47 Update ci.yml
- f49e87c Update ci.yml
- cf16be8 Merge remote-tracking branch 'origin/dev' into dev
- 5665be1 Merge pull request #9 from rjdbcm/dev
- 0ec30fc Update README.md
- 6604b5c Update README.md
- aeb3ff2 Update deploy.yml
- a5418b9 Merge pull request #8 from rjdbcm/main
- f2fc9cc update pygments-woma-lexer
- 8f3e698 update pygments-woma-lexer

**v0.12.2**

- 0c01045 update pygments-woma-lexer

**v0.12.1**

- f7d39de Pulled a Warn class from SafeMath, Maybe etc.

**v0.12.0**

- ceafa58 clean up imports
- 01f394f monads.py: stack is inspected during __init__
- 29a8699 final.py: clean imports and add docstrings
- 99dcd66 fix tab typo
- c30dae3 add gitignores
- a0719ab add smol logo
- 53a87f8 Makefile: added all phonies and changed clean-md5 to clean-sha
- cd3ccc7 Merge remote-tracking branch 'origin/main'
- db0056e move WomaLexer into a separate repo pygments-woma-lexer
- c66fc8e changelog updated
- 47f6bbd Update README.md
- 4a92f4f Update README.md
- 94f09dc Update README.md



- 


**v0.11.28**

- 5dee3f1 reserved.py: made nullit Literal and operators use a regex
- b645d1a parser.py: fixed some imports, fixed list_item precedence
- 51955d6 conf.py rewrote lexer in preparation to move to its own package
- ecd259d examples.wom: comp op comment out
- e39b931 examples.wom: commented out nullit
- 1d481ba test_aspidites.py: imports
- e4c955b Merge remote-tracking branch 'origin/main'
- 7112ad6 add nullit to examples.wom
- bf3770b add cache to ci.yml
- c8c6cb7 source tree cleanup
- 3b62aec Update README.md
- e04474a Update README.md
- f73454b Update README.md
- 504b659 source tree cleanup


**v0.11.27**

- 9612bad fix gh action


**v0.11.26**

- 9f66792 fix gh action


**v0.11.25**

- 6763d53 fix gh action


**v0.11.24**

- 467bb83 fix gh action


**v0.11.23**

- 34ae2f9 fix gh action: last try


**v0.11.22**

- 74ec955 fix gh action: last try


**v0.11.21**

- 08cc826 fix gh action


**v0.11.20**

- 6266ad8 fix gh action


**v0.11.19**

- 3887e2b fix gh action


**v0.11.18**

- 312e224 fix gh action


**v0.11.17**

- dd2739f fix gh action


**v0.11.16**

- 87a4f53 fix gh action


**v0.11.15**

- 08b2f9e fix gh action


**v0.11.14**

- fd61123 fix gh action
- b665728 changelog updated
- a62f227 fix gh action



- a62f227 fix gh action


**v0.11.13**

- a1cb254 fix gh action


**v0.11.12**

- aea7577 fix gh action


**v0.11.11**

- 032c0dd fix gh action


**v0.11.10**

- 0dae705 add chocolatey package
- 9be4417 changelog updated
- 94589bd add chocolatey package
- 02a3674 changelog updated
- a971a26 changelog updated
- 4531c37 add chocolatey package
- 23a5029 changelog updated
- 9e06bd4 changelog updated
- 304deb8 add chocolatey package



- 94589bd add chocolatey package
- 02a3674 changelog updated
- a971a26 changelog updated
- 4531c37 add chocolatey package
- 23a5029 changelog updated
- 9e06bd4 changelog updated
- 304deb8 add chocolatey package



- a971a26 changelog updated
- 4531c37 add chocolatey package
- 23a5029 changelog updated
- 9e06bd4 changelog updated
- 304deb8 add chocolatey package



- 4531c37 add chocolatey package
- 23a5029 changelog updated
- 9e06bd4 changelog updated
- 304deb8 add chocolatey package



- 9e06bd4 changelog updated
- 304deb8 add chocolatey package



- 304deb8 add chocolatey package


**v0.11.9**

- 9eea2b9 setup.py: fix typo


**v0.11.8**

- 06adba0 fix path


**v0.11.7**

- 9c83996 update supported OSes
- 2e5e9f4 Update ci.yml add macos
- 48dc267 Update README.md
- 68215f2 Merge pull request #7 from rjdbcm/rjdbcm-patch-1
- 40973bd fix for windows unicode support
- 681e9c6 Update ci.yml
- 9cdc310 Update and rename python-app.yml to ci.yml
- 547ed18 convert.py: pep8
- 28bdc61 templates.py lib template add compile(restricted) and other builtins
- 9c7522f Makefile: test-all depends on clean-test
- a637984 Use pathlib.Path for path representations
- a0888d2 refactor monads.py for readability
- d7f1423 Added stubs for RestrictedPython
- 8c6c8d4 Merge remote-tracking branch 'origin/main'
- 6cb6219 refactor of the parser to make it a bit less brittle when modified
- 650419c Update README.md
- 6f24118 Update README.md
- 11413e5 Update README.md
- a72e1fa Merge remote-tracking branch 'origin/main'
- bc8fb5a remove joker
- ebf4ea6 Update social.yml
- a3f1eb7 test joke api
- f67eded test joke api
- 3a0638c test joke api
- c5817fb Merge remote-tracking branch 'origin/main'
- fcf13ea test joke api
- d362649 Update social.yml
- 9b786a1 Update social.yml
- 7243005 Merge remote-tracking branch 'origin/main'
- 994bf03 test joke api
- fdf800a Update README.md


**v0.11.6**

- c0bbfc2 changelog updated
- 5707afc fix social message on container-deploy.yml
- 945cc72 Update python-app.yml
- fc1f72f absolute import of test examples
- 11ec1d0 fix build action
- ffee7cb fix build action
- 852897a PyPy not supported. Maybe and F now inherit from symtable.Function. This is the plan for future classes used as the basis of the functional interface.
- 29e1d22 compiler.py compatible with Python 3.7
- f6cbdc0 compiler.py compatible with Python 3.7
- d708ff8 compiler.py compatible with Python 3.7
- 189fa3d drop Python 3.6 support
- fde2df4 fix test to be a quick source install
- cbf29d3 Update Package to show tested python versions/implementations
- 1b17ab6 Update python-app.yml
- 10a93f2 Update python-app.yml
- 61dcabd Update python-app.yml
- 3e775e0 Update python-app.yml
- f23d236 Update python-app.yml
- 7174b0e Update python-app.yml
- 4f24fc5 Update python-app.yml
- d5aeed5 Update python-app.yml
- 20cd069 Update python-app.yml
- 151ec1f Update python-app.yml
- a224da0 Update python-app.yml
- ad8fa09 Update python-app.yml
- 9e2a44b Update python-app.yml
- ca11af3 CI workflow for CPython v3.9.6 and v3.8.11
- 6731f2a Update README.md
- 0beaa2c Update README.md
- 7717cd7 Update README.md
- 20cbb78 Update README.md



- 5707afc fix social message on container-deploy.yml
- 945cc72 Update python-app.yml
- fc1f72f absolute import of test examples
- 11ec1d0 fix build action
- ffee7cb fix build action
- 852897a PyPy not supported. Maybe and F now inherit from symtable.Function. This is the plan for future classes used as the basis of the functional interface.
- 29e1d22 compiler.py compatible with Python 3.7
- f6cbdc0 compiler.py compatible with Python 3.7
- d708ff8 compiler.py compatible with Python 3.7
- 189fa3d drop Python 3.6 support
- fde2df4 fix test to be a quick source install
- cbf29d3 Update Package to show tested python versions/implementations
- 1b17ab6 Update python-app.yml
- 10a93f2 Update python-app.yml
- 61dcabd Update python-app.yml
- 3e775e0 Update python-app.yml
- f23d236 Update python-app.yml
- 7174b0e Update python-app.yml
- 4f24fc5 Update python-app.yml
- d5aeed5 Update python-app.yml
- 20cd069 Update python-app.yml
- 151ec1f Update python-app.yml
- a224da0 Update python-app.yml
- ad8fa09 Update python-app.yml
- 9e2a44b Update python-app.yml
- ca11af3 CI workflow for CPython v3.9.6 and v3.8.11
- 6731f2a Update README.md
- 0beaa2c Update README.md
- 7717cd7 Update README.md
- 20cbb78 Update README.md


**v0.11.5**

- 62d6a06 revert testconfig sort, it wasn't that my tests were running 2x
- 3be0154 update codeclimate and coverage exclude patterns


**v0.11.4**

- 6eb2d29 deployment changes so twitter works


**v0.11.3**

- 0d899d2 BUGFIX: 0.11.3 still had a buggy import of final so it's gone for now


**v0.11.2**

- dad6dd3 BUGFIX: 0.11.2 had a buggy final import


**v0.11.1**

- 1d62e60 BUGFIX: testsuite formerly ran every unittest 2x
- 2d9baa6 adjust cognitive complexity threshold to 6 for codeclimate
- 8df122c Merge remote-tracking branch 'Aspidites/main' into main
- a90b3a8 added final class decorator and adjusted a few import statements to be relative
- b3f5017 parametrized tests and pytest.mark.uses_stdout tests are moved to the end
- ca2af84 Update README.md



**v0.11.0**

- 82b9ec9 buffer size for CheckedFileStack now defaults to a more reasonable 128 bytes
- 1085506 changelog updated
- 4200f78 changelog reformatted



- 4200f78 changelog reformatted



**v0.10.1**

- 63d0548 refactor CheckedFileStack class and compiler.py functions to used pathlib
- 19ff71b inset search border
- ddb57de add some transparency and gradients
- 01c8e23 Added tabbed interfaces to docs/homepage
- 54121d2 remove duplicated code

**v0.10.0**

- 598f86a patch setup.py woma compile
- c39ac21 changelog updated

**v0.9.34**

- a11958b refactor compiler.py for better decoupling of various writes
- 839cc92 Enables sets tests
- e0e5af8 Merge remote-tracking branch 'Aspidites/main' into main
- 09ef124 Remove link to blank search page from docs index.rst
- 048f0a6 Added more temp folders to .gitignore
- dca63cd Added docs to .coveragerc and .dockerignore
- c1fdb8c removed no covers from contracts utils.py functions that are still in use
- 63aae94 add testcases for sets.
- 5c3e33f prune docs from Manifest.in
- ef611fc added sanity tests for contract function inspection
- 7c72b3f Update README.md
- 979c1cb fix GNU license in doc
- 542bb0c adjust sections and pages of docs
- 6bc98f1 add copybutton for shell commands to docs
- d913dd4 Adjusted doc stylesheets for a responsive experience
- fbc2fe6 very nice reactive but unobtrusive doc website
- 2d7e5ef docs now have a nice examples section
- c105f64 fix animation
- 122da38 mild README.rst reformatting
- 6feadb4 toctree now goes 3 deep.
- 7daeb79 fixed so docs talk about the language not the reference implementation.
- b3fa422 Full sized Wheelie in docs
- b98ec6a logo update
- 77aa6f4 Prep compiler.py for refactor
- 7f65eb7 Add __mimetype__
- 7a41b9f Add updated docs logo
- c868389 Nice looking docs.
- 79440ba update docs logo
- 7209649 fix Programmable Error in rtd build
- 6780de9 Add numpy to docs/requirements.txt
- 61ceba6 Add readthedocs config and requirements.txt
- 300b23d Merge remote-tracking branch 'Aspidites/main' into main
- 9a3786d Add path insert to docs conf.py
- a2adcaa typo fixed in change logger
- 0116645 Update CHANGELOG.md


**v0.9.33**

- 3912e63 fixed main() call in test_aspidites.py


**v0.9.32**

- fa9d60d CLI test to fix coverage missing for __main__.py
- af52c56 Make sure to raise a SystemExit when running our tests from a different thread.
- 39ec7ce Makefile doesn't complain about circular deps
- 3f7a8b6 fix minor bumpversion_hook formatting issue



**v0.9.31**

- 7aa21f1 quick update to version changelogger and it is finally working
- 6bbc8c1 minor makefile cleanup
- 8263ce4 changelog updated
- 49ea6b1 finally got bumps to work!
- c3db2a1 maybe fixed version changelogging



**v0.9.30**
- 509a146 Bump version: 0.9.30 → 0.9.31
- c2aa35d changelog updated
- fe655c7 fixed that pesky bumpversion_hook.py
- 509a146 (HEAD -> main, tag: v0.9.31) Bump version: 0.9.30 → 0.9.31
- c2aa35d changelog updated
- fe655c7 fixed that pesky bumpversion_hook.py

**v0.9.29**
- 7e45564 (HEAD -> main, tag: v0.9.30) Bump version: 0.9.29 → 0.9.30
- 010647c changelog updated
- 3856180 bumpversion_hook should be in order.
- 4423a00 changelog building hook executes and commits before any version bump.

**v0.9.28**
- direct function calls within function definitions now work!

**v0.9.27**
- Literally a patch just for a logo?!

**v0.9.26**

**v0.9.25**
**v0.9.24**
**v0.9.23**
**v0.9.22**
**v0.9.21**
**v0.9.20**
**v0.9.19**
**v0.9.18**
**v0.9.17**
**v0.9.16**
**v0.9.15**
**v0.9.14**
**v0.9.13**
**v0.9.12**
**v0.9.11**
**v0.9.10**
**v0.9.9**
**v0.9.8**
**v0.9.7**
**v0.9.6**
**v0.9.5**
**v0.9.4**

**v0.9.3**
- All Safe math either end up at Undefined, a number, or inf

**v0.9.2**
- SafeExp+tests fully working. 

**v0.9.1**
- SafeExp now goes to Undefined in case of inf**inf
- fixed test-fail for inf**inf

**v0.9.0**
- Massive increase in test coverage (>90%)
- SafeExp now goes straight to inf in case of OverflowError

**v0.8.6**
- Added todo for docker setup_runner
- proper build directory selection in compiler.py setup_runner.

**v0.8.5**
- revert of v0.8.4

**v0.8.4**
- removed context managers from compiler.py

**v0.8.3**
- Pipfile.lock added to .dockerignore
- added workdir symlink to dockerfile

**v0.8.1** & **v0.8.2**
- test suite works on docker build
- test suite simplified


**v0.8.0**
- make uninstall template no longer deletes __init__.py

**v0.7.0**
- add coverage configuration file
- add dockerignore
- move tests into package
- print version info on CLI run

**v0.6.1**
- First release with a compiled woma standard library.

**v0.6.0**
- This release was pulled. This is a (slightly) fixed version of the wheel and source distribution pulled from PyPI.

**v0.5.2**

**v0.5.1**
- minor CLI fix for unused --embed-python just use --embed

**v0.5.0**
- PyPI Package installs dependencies

**v0.4.5**
- Code Cleanup

**v0.4.4**
- Initial PyPI Release

**v0.4.3**

**v0.4.2**

**v0.4.1**

**v0.4.0**

**v0.3.0**

**v0.2.8**

**v0.2.7**

**v0.2.6**

**v0.2.5**

**v0.2.4**

**v0.2.3**

**v0.2.2**

**v0.2.1**

**v0.2.0**

**v0.1.4**

**v0.1.3**

**v0.1.2**

**v0.1.1**

**v0.1.0**

**v0.0.5**

**v0.0.4**

**v0.0.3**

**v0.0.2**

**v0.0.1**
