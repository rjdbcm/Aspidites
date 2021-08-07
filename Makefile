clean: clean-build clean-pyc clean-test clean-md5 ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-md5:
	find . -name '*.md5' -exec rm -f {} +

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
	cd examples && $(MAKE) uninstall

test-all:
	pytest tests --cov Aspidites --cov-report=html:.coverage_html --full-trace --capture=tee-sys

coverage:
	pytest tests --cov-report=xml --cov=Aspidites

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major