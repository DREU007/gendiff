install:
	poetry install

gendiff:
	poetry run gendiff

build:
	poetry build
	
publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-remove:
	python3 -m pip uninstall hexlet-code

lint:
	poetry run flake8 gendiff tests

test:
	poetry run pytest