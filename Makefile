test:
	bash test.sh

test[live]:
	bash test.sh --live

e2e:
	rm -rf project_20abe*/
	python $(SRC)/tests/test_e2e_30sec.py
	python $(SRC)/tests/test_e2e_catalog.py
	rm -rf project_20abe*/

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
