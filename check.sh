#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
[ -f ./venv/bin/python ] && python_exec='./venv/bin/python' || python_exec='python'
$python_exec -m ruff format wikidict tests scripts
$python_exec -m ruff check --fix --unsafe-fixes wikidict tests scripts
$python_exec -m mypy wikidict scripts tests
