SHELL := /usr/bin/env bash

UV ?= uv
RUFF ?= ruff
PYTEST ?= pytest

.DEFAULT_GOAL := help

.PHONY: help setup format lint lint-fix test test-cov migrate check clean

help:
	@echo "Available targets:"
	@echo "  make setup      - Install/update dependencies with uv"
	@echo "  make format     - Format Python code with ruff"
	@echo "  make lint       - Lint Python code with ruff"
	@echo "  make lint-fix   - Auto-fix lint issues with ruff"
	@echo "  make test       - Run test suite"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make migrate    - Run database migrations"
	@echo "  make check      - Run format, lint, and tests"
	@echo "  make clean      - Remove Python cache artifacts"

setup:
	$(UV) sync --dev

format:
	$(UV) run $(RUFF) format .

lint:
	$(UV) run $(RUFF) check .

lint-fix:
	$(UV) run $(RUFF) check --fix .

test:
	$(UV) run $(PYTEST)

test-cov:
	$(UV) run $(PYTEST) --cov=app --cov-report=term

migrate:
	$(UV) run python scripts/migrate.py

check: format lint test

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete