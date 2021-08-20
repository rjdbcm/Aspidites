**unreleased**
**v0.9.31**

**v0.9.30**

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
fe655c7 fixed that pesky bumpversion_hook.py

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

- bbbaf12 Merge remote-tracking branch 'Aspidites/main' into main

- a65eac7 fix docker deployment to only push for tags or dev* branches

- 38b6e8c Update README.md

- f8338f8 fix docker deployment

- 1428ee6 Merge remote-tracking branch 'Aspidites/main' into main

- 739a775 add docker deployment

- 1ec41fc Update README.md

- c2c3f4b Bump version: 0.9.24 → 0.9.25

- c4b9e27 fix deploy.yml only runs on tagged builds

- d5202b8 Bump version: 0.9.23 → 0.9.24

- 4ff2fd9 fix deploy.yml only runs on tagged builds

- 51b970e Bump version: 0.9.22 → 0.9.23

- 2f8bf4d fix deploy.yml k

- 77663f5 Bump version: 0.9.21 → 0.9.22

- 6ac3857 fix deploy.yml k

- ac9fadb Bump version: 0.9.20 → 0.9.21

- 28e3cd0 fix deploy.yml k

- ba94102 Bump version: 0.9.19 → 0.9.20

- ded36b4 fix deploy.yml

- 39f132f Bump version: 0.9.18 → 0.9.19

- a2dd917 fix deploy.yml

- cce571d Bump version: 0.9.17 → 0.9.18

- 5a29d9e test install into pipenv

- bc9ea79 Bump version: 0.9.16 → 0.9.17

- 744af92 test install into pipenv

- 305ccd3 Bump version: 0.9.15 → 0.9.16

- 265013b make sure deploy.yml grabs the correct python version

- e01d7b8 Bump version: 0.9.14 → 0.9.15

- 7926062 make sure deploy.yml grabs the correct python version

- a490290 Bump version: 0.9.13 → 0.9.14

- 505ec99 make sure deploy.yml grabs the correct python version

- 12c592a Merge remote-tracking branch 'Aspidites/main' into main

- d4425fc Bump version: 0.9.12 → 0.9.13

- 178a273 add dist to .gitignore

- 61030a9 Update deploy.yml

- 03a2e51 Bump version: 0.9.11 → 0.9.12

- 12655c7 Fix setup.py to work for PEP 513.

- c949981 Bump version: 0.9.10 → 0.9.11

- a8008d0 remove ZPL classifier because PyPI

- 6f6d105 Bump version: 0.9.9 → 0.9.10

- 4de7e1d commas are handy

- 3fa24dd Update deploy.yml

- 22d8e4c Create deploy.yml

- 1a889e3 Update python-app.yml

- 9993c55 Update python-app.yml

- f327f42 Update python-app.yml

- 50a6f83 Bump version: 0.9.8 → 0.9.9

- 742368f added xfail for some systems not reliably catching/raising SystemExit.

- 7acaa64 minor refactor to remove debug from Maybe.__call__ signature

- 6e413cb Bump version: 0.9.7 → 0.9.8

- 00ecc2a fix tests for __main__.py entrypoint

- fbcfb8a Bump version: 0.9.6 → 0.9.7

- fd48405 fix tests for __main__.py entrypoint

- 4658529 fix tests for __main__.py entrypoint

- a58edb5 Bump version: 0.9.5 → 0.9.6

- 4bc93eb fix tests for __main__.py entrypoint

- 58ecf98 fix tests for __main__.py entrypoint

- b31a93b Merge remote-tracking branch 'Aspidites/main' into main

- 69e0b3a Bump version: 0.9.4 → 0.9.5

- 7ae74b5 add tests for __main__.py entrypoint

- c80d145 add tests for __main__.py entrypoint

- e5c34f1 Update feature-request.md

- c7066cd Update feature-request.md

- cd30052 Update feature-request.md

- a700f44 Update issue templates

- 9ed5676 Update README.md

- 50126d0 Update README.md

- 0a4f44f Bump version: 0.9.3 → 0.9.4

- a31f2c0 added dependency license attributions to readme added trove strings to setup.py

- 4251f56 added dependency license attributions to readme

- e6c2f5e added all license trove strings

- 5aa706a changes logged

- 262531b Bump version: 0.9.2 → 0.9.3

- 4994482 fixed all SafeMath fns

- bf65a5a changes logged

- a57135e changes logged

- 85727d1 Bump version: 0.9.1 → 0.9.2

- dbd5b8d fix tests

- 265730e changes logged

- d743357 Bump version: 0.9.0 → 0.9.1

- e810fa1 Add todo

- 4a6be7b fix inf**inf to become Undefined()

- dbc8806 changes logged

- a011dcb Bump version: 0.8.6 → 0.9.0

- 0e5c6f2 add monad tests fixed missing coverage big numbers in SafeExp just go to infinite

- 39a60e7 more test cleanup, coverage up to 90%

- 0ccbe50 clean up tests and get the semantic_contract_fuzzer working (renamed from friendliness_statistics.py).

- 953e2a8 Add license scan badge

- 84a7302 Merge remote-tracking branch 'Aspidites/main' into main

- af7bf3f changelog

- 8cd2de9 changelog

- abfed16 Added todo for docker setup_runner

- 5f0b5b3 proper build directory selection in compiler.py setup_runner.

- 33d5352 Bump version: 0.8.5 → 0.8.6

- 8439c22 revert removal of context managers from compiler.py

- cb1abf5 Bump version: 0.8.4 → 0.8.5

- 0344f73 removed context managers from compiler.py as docker builds don't like them.

- 8b8d543 Bump version: 0.8.3 → 0.8.4

- d537102 added workdir symlink to Dockerfile

- 23d3d82 Pipfile.lock added to .dockerignore

- e70c9a3 Bump version: 0.8.2 → 0.8.3

- 85c2394 tests now run from Aspidites -pt/--pytest Or they can be discovered from the project directory.

- 6f599ef test suite works on docker build test suite simplified

- 0e0f991 Bump version: 0.8.1 → 0.8.2

- 66620a3 test suite works on docker build test suite simplified

- 9d22bf0 Bump version: 0.8.0 → 0.8.1

- 807690a Added welcome message to help. Fixed test_aspidites.py paths

- 55e8807 make uninstall template no longer deletes __init__.py

- a0b2e63 Pipfile.lock added to .dockerignore

- ae548c3 Bump version: 0.8.2 → 0.8.3

- 026d8b7 tests now run from Aspidites -pt/--pytest Or they can be discovered from the project directory.

- ae59c62 test suite works on docker build test suite simplified

- e10b98e Bump version: 0.8.1 → 0.8.2

- cef9881 test suite works on docker build test suite simplified

- 8a943f7 Bump version: 0.8.0 → 0.8.1

- c70ab30 Added welcome message to help. Fixed test_aspidites.py paths

- c3a2539 make uninstall template no longer deletes __init__.py

- ecaa1f4 update dockerfile WORKDIR












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
