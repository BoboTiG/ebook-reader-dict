#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black wikidict scripts tests
python -m flake8 wikidict scripts tests
python -m mypy wikidict scripts
