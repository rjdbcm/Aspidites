.PHONY:
	docker
	docs
	clean-md5
	clean-build
	clean-pyc
	clean-woma
	clean-test
	clean
	test-all
	xtest
	coverage
	patch
	minor
	major
	build
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build
VERSION       = $(shell python -c "import sys;from Aspidites import __version__;sys.stdout.write(__version__)");
clean: clean-build clean-pyc clean-test clean-sha clean-woma## remove all build, test, coverage and Python artifacts
	rm -fr CHANGELOG.bak

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr prof/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr __main__.pyi
	rm -fr main.spec
	rm -fr Aspidites/_vendor/contracts/metaclass.c
	rm -fr Aspidites/_vendor/contracts/interface.c
	rm -fr Aspidites/_vendor/contracts/syntax.c
	rm -fr Aspidites/_vendor/contracts/inspection.c
	rm -fr Aspidites/_vendor/contracts/docstring_parsing.c
	rm -fr Aspidites/_vendor/contracts/main_actual.c
	rm -fr Aspidites/_vendor/contracts/useful_contracts/numpy_specific.c
	rm -fr Aspidites/_vendor/contracts/useful_contracts/numbers.c
	rm -fr Aspidites/_vendor/contracts/library/*.c
	rm -fr Aspidites/_vendor/contracts/parser.c
	rm -fr Aspidites/_vendor/apm/_util.c
	rm -fr Aspidites/_vendor/apm/error.c
	rm -fr Aspidites/_vendor/apm/generic.c
	rm -fr Aspidites/_vendor/apm/match.c
	rm -fr Aspidites/_vendor/apm/no_value.c
	rm -fr Aspidites/_vendor/apm/overload.c
	rm -fr Aspidites/_vendor/apm/patterns.c
	rm -fr Aspidites/_vendor/apm/try_match.c
	rm -fr Aspidites/_vendor/fn/*.c
	rm -fr Aspidites/_vendor/RestrictedPython/Limits.c
	rm -fr Aspidites/api/convert.c
	rm -fr Aspidites/api/parser.c
	rm -fr Aspidites/api/reserved.c
	rm -fr Aspidites/_vendor/decorator_extension.c
	rm -fr Aspidites/_vendor/pyparsing_extension.c
	rm -fr Aspidites/api/templates.c
	rm -fr Aspidites/api/monads.c
	rm -fr Aspidites/api/math.c
	rm -fr Aspidites/api/api.c
	rm -fr Aspidites/__main__.c
	rm -fr Aspidites/api/compiler.c
	rm -fr Aspidites/api/compiler.*.so
	rm -fr Aspidites/api/__main__.*.so
	rm -fr Aspidites/api/api.*.so
	rm -fr Aspidites/api/math.*.so
	rm -fr Aspidites/api/monads.*.so
	rm -fr Aspidites/api/templates.*.so
	rm -fr Aspidites/_vendor/apm/_util.*.so
	rm -fr Aspidites/_vendor/apm/error.*.so
	rm -fr Aspidites/_vendor/apm/generic.*.so
	rm -fr Aspidites/_vendor/apm/match.*.so
	rm -fr Aspidites/_vendor/apm/no_value.*.so
	rm -fr Aspidites/_vendor/apm/overload.*.so
	rm -fr Aspidites/_vendor/apm/patterns.*.so
	rm -fr Aspidites/_vendor/apm/try_match.*.so
	rm -fr Aspidites/_vendor/decorator_extension.*.so
	rm -fr Aspidites/_vendor/pyparsing_extension.*.so
	rm -fr Aspidites/_vendor/fn/*.*.so
	rm -fr Aspidites/_vendor/contracts/metaclass.*.so
	rm -fr Aspidites/_vendor/contracts/interface.*.so
	rm -fr Aspidites/_vendor/contracts/parser.*.so
	rm -fr Aspidites/_vendor/contracts/syntax.*.so
	rm -fr Aspidites/_vendor/contracts/inspection.*.so
	rm -fr Aspidites/_vendor/contracts/docstring_parsing.*.so
	rm -fr Aspidites/_vendor/contracts/main_actual.*.so
	rm -fr Aspidites/_vendor/contracts/library/*.*.so
	rm -fr Aspidites/_vendor/contracts/useful_contracts/numpy_specific.*.so
	rm -fr Aspidites/_vendor/contracts/useful_contracts/numbers.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_helpers.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_checked_types.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_immutable.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pbag.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pclass.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pdeque.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_plist.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pmap.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_precord.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pset.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_pvector.*.so
	rm -fr Aspidites/_vendor/pyrsistent/_toolz.*.so
	rm -fr Aspidites/_vendor/pyrsistent/pvectorc.*.so
	rm -fr Aspidites/_vendor/pyrsistent/typing.*.so
	rm -fr Aspidites/_vendor/RestrictedPython/Limits.*.so
	rm -fr Aspidites/api/convert.*.so
	rm -fr Aspidites/api/parser.*.so
	rm -fr Aspidites/api/reserved.*.so
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.DS_Store' -exec rm -f {} +


clean-sha:
	find . -name '*.sha256' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .hypothesis/
	rm -fr .coverage_html/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	-cd Aspidites/tests/examples && $(MAKE) uninstall

clean-woma: ## remove compiled woma files
	-cd Aspidites/woma && $(MAKE) uninstall

docker:
	docker -v build . --no-cache -t rjdbcm/aspidites:$(VERSION)

test-all:
	python -m pytest Aspidites/tests --cov Aspidites --cov-report=html:.coverage_html --full-trace --capture=tee-sys

build-ext: clean
	python setup.py build_ext --inplace

quickbuild: clean-woma
	-cd Aspidites/tests/examples && $(MAKE) uninstall
	python setup.py build_ext --inplace

proftest: build-ext
	python -m pytest Aspidites/tests -x --profile --profile-svg

xtest: build-ext
	python -m pytest Aspidites/tests -x

quicktest: quickbuild
	python -m pytest Aspidites/tests -x

coverage:
	python -m pytest Aspidites/tests --cov-report=xml --cov=Aspidites

release:
	git add CHANGELOG.md
	bump2version --config-file ./dev/.bumpversion.cfg release

prerel:
	git add CHANGELOG.md
	bump2version --config-file ./dev/.bumpversion.cfg prerel

patch:
	python -m dev.scripts.bumpversion_hook patch
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version --config-file ./dev/.bumpversion.cfg patch

minor:
	python -m dev.scripts.bumpversion_hook minor
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version --config-file ./dev/.bumpversion.cfg minor

major:
	python -m dev.scripts.bumpversion_hook major
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version major

build: clean test-all clean
	python setup.py sdist bdist_wheel

%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)