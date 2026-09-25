# Development shortcuts: every target relies on uv (environment, dependencies)
# and Hatch (quality checks, test matrix). Run `make help` to list the targets.

UV ?= uv
HATCH ?= hatch
DOCS_BUILD_DIR ?= dist/docs
SPHINX_BUILD = $(UV) run --with-requirements docs/requirements.txt sphinx-build

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Create the virtual environment with the locked dependencies
	$(UV) sync --locked

.PHONY: lock
lock: ## Update the lockfile (uv.lock)
	$(UV) lock

.PHONY: test
test: install ## Run the test suite (current Python version)
	$(UV) run pytest

.PHONY: cov
cov: install ## Run the test suite with coverage (terminal and HTML reports)
	$(UV) run pytest --cov --cov-report=term-missing --cov-report=html

.PHONY: test-all
test-all: ## Run the test suite on all Python and wrapt versions
	$(HATCH) test --all

.PHONY: check
check: ## Run the quality checks (lint, format, types) and verify the lockfile
	$(UV) lock --check
	$(HATCH) check code
	$(HATCH) check fmt
	$(HATCH) check types

.PHONY: fix
fix: ## Fix the lint errors and reformat the code
	$(HATCH) check code --fix
	$(HATCH) check fmt --fix

.PHONY: docs
docs: ## Build the HTML documentation
	$(SPHINX_BUILD) -b html -d $(DOCS_BUILD_DIR)/doctrees docs/source/ $(DOCS_BUILD_DIR)/html

.PHONY: build
build: ## Build the source distribution and the wheel
	$(UV) build

.PHONY: version
version: ## Show the current version
	$(HATCH) version

.PHONY: bump-major bump-minor bump-patch
bump-major: ## Bump the major version (see docs/source/release.rst)
	$(HATCH) version major
bump-minor: ## Bump the minor version
	$(HATCH) version minor
bump-patch: ## Bump the patch version
	$(HATCH) version patch

.PHONY: clean
clean: ## Remove the build artifacts and the caches
	rm -rf dist/ build/ htmlcov/ .coverage .coverage.* .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -not -path "./.venv/*" -prune -exec rm -rf {} +
