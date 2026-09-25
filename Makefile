.PHONY: all install-dev test coverage cov test-all check fmt release-minor release-patch build clean-pyc

all: test

install-dev:
	uv sync --locked

test: clean-pyc install-dev
	uv run pytest

coverage: clean-pyc install-dev
	uv run pytest --cov --cov-report term-missing --cov-report html

cov: coverage

test-all:
	hatch test --all

check:
	hatch check code
	hatch check fmt
	hatch check types

fmt:
	hatch check code --fix
	hatch check fmt --fix

release-minor:
	uvx bump2version minor

release-patch:
	uvx bump2version patch

build:
	uv build

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
