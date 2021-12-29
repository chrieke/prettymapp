#!/bin/bash

rm -r .pytest_cache
black .
if [[ $* == *--live* ]]
then
  python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --cov=prettybasicmaps/ --runlive --durations=5  --ignore=./prettybasicmaps/old.py
  RET_VALUE=$?
else
  python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --cov=prettybasicmaps/ --durations=3  --ignore=./prettybasicmaps/old.py
  RET_VALUE=$?
  coverage-badge -f -o coverage.svg
fi
exit $RET_VALUE
