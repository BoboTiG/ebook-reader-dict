#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black wikidict tests
python -m flake8 wikidict tests
python -m mypy wikidict
