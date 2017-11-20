.PHONY: all install-dev test coverage cov test-all tox release-minor release-patch upload-minor upload-patch clean-pyc

all: test

install-dev:
	pip install -q -e .[dev]

test: clean-pyc install-dev
	pytest tests/

coverage: clean-pyc install-dev
	pytest --cov-report term-missing --cov-report html --cov=deprecated tests/

cov: coverage

test-all: install-dev
	tox

tox: test-all

release-minor:
	bumpversion minor
	python setup.py release

release-patch:
	bumpversion patch
	python setup.py release

upload-minor: release-minor
	python setup.py upload
	git push origin --tags

upload-patch: release-patch
	python setup.py upload
	git push origin --tags

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
