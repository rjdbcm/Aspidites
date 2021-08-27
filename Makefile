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

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr __main__.pyi
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

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

test-all: clean-test
	pytest Aspidites/tests --cov Aspidites --cov-report=html:.coverage_html --full-trace --capture=tee-sys

coverage:
	pytest Aspidites/tests --cov-report=xml --cov=Aspidites

patch:
	python -m Aspidites.scripts.bumpversion_hook patch
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version patch

minor:
	python -m Aspidites.scripts.bumpversion_hook minor
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version minor

major:
	python -m Aspidites.scripts.bumpversion_hook major
	git add CHANGELOG.md
	git commit -m 'changelog updated'
	bump2version major

build: clean test-all clean
	python setup.py sdist bdist_wheel

%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)