test:
	-rm -r .pytest_cache
	black .
	python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --durations=3

test[live]:
	-rm -r .pytest_cache
	black .
	python -m pytest --pylint --pylint-rcfile=../../pylintrc --mypy --mypy-ignore-missing-imports --runlive --durations=5

setup:
	pip install -r requirements.txt
	pip install -r streamlit-prettymapp/requirements.txt

setup-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .
	pip install streamlit

package:
	python setup.py sdist bdist_wheel
	twine check dist/*

upload:
	twine upload --skip-existing dist/*

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -exec rm -f {} +
