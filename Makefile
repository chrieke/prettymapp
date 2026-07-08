test:
	uv run black .
	uv run pytest prettymapp/tests --pylint --pylint-rcfile=pylintrc --mypy --mypy-ignore-missing-imports --durations=3

test[live]:
	uv run black .
	uv run pytest prettymapp/tests --pylint --pylint-rcfile=pylintrc --mypy --mypy-ignore-missing-imports --runlive --durations=5

setup:
	uv sync --extra streamlit

app:
	uv run streamlit run streamlit-prettymapp/app.py

package:
	rm -rf dist
	uv build
	uvx twine check dist/*

upload:
	uvx twine upload --skip-existing dist/*

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -exec rm -f {} +
