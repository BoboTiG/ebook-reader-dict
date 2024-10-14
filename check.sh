#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m ruff format wikidict tests scripts
python -m ruff check --fix --unsafe-fixes wikidict tests scripts
python -m mypy wikidict scripts tests
