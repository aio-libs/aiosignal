# Some simple testing tasks (sorry, UNIX only).

SRC = aiosignal tests setup.py

all: test

.install-deps:
	pip install -r requirements/dev.txt
	@touch .install-deps

lint:
# CI env-var is set by GitHub actions
ifndef CI
	pre-commit run --all-files
endif
	mypy aiosignal

.develop: .install-deps $(shell find aiosignal -type f)
	# pip install -e .
	@touch .develop

test: .develop
	@pytest -q

vtest: .develop
	@pytest -s -v

cov cover coverage:
	tox

cov-dev: .develop
	@pytest -c pytest.ci.ini --cov-report=html
	@echo "open file://`pwd`/htmlcov/index.html"

cov-ci-run: .develop
	@echo "Regular run"
	@pytest -c pytest.ci.ini --cov-report=html

cov-dev-full: cov-ci-run
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf cover
	@make -C docs clean
	@python setup.py clean
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake
	@rm -f .install-deps
	@rm -rf aiosignal.egg-info

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U 'pip'
	@pip install -Ur requirements/dev.txt
	@pre-commit install

install-dev: .develop

.PHONY: all build flake test vtest cov clean doc mypy
