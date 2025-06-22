#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
./venv/bin/python -m ruff format wikidict tests scripts
./venv/bin/python -m ruff check --fix --unsafe-fixes wikidict tests scripts
./venv/bin/python -m mypy wikidict scripts tests
