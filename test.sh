#!/bin/bash

rm -r .pytest_cache
black .
if [[ $* == *--live* ]]
then
  python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --cov=prettiermaps/ --runlive --durations=5  --ignore=./prettiermaps/old.py
  RET_VALUE=$?
else
  python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --cov=prettiermaps/ --durations=3  --ignore=./prettiermaps/old.py
  RET_VALUE=$?
  coverage-badge -f -o coverage.svg
fi
exit $RET_VALUE
