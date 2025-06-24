
build :
	poetry build

clean :
	$(RM) -rf build dist *.egg-info

coverage :
	poetry run coverage run --source=pyairnow -m pytest tests

coverage-html :
	poetry run coverage html -d .htmlcov && open .htmlcov/index.html

coverage-report :
	poetry run coverage report -m

lint :
	poetry run flake8

publish :
	poetry publish

requirements :
	poetry export -f requirements.txt -o requirements-dev.txt --with dev

test :
	poetry run python -m pytest tests

test-x :
	poetry run python -m pytest tests -x

test-wip :
	poetry run python -m pytest tests -m wip

type-check :
	poetry run mypy pyairnow

all: test lint build publish

.PHONY: build \
	coverage coverage-html coverage-report \
	lint test test-wip test-x type-check
