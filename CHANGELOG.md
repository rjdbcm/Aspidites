**unreleased**
**v0.11.6**

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
