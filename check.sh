#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black scripts tests
python -m flake8 scripts tests
python -m mypy scripts
