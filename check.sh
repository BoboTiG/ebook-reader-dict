#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black wikidict tests scripts
python -m flake8 wikidict tests scripts
python -m mypy wikidict
