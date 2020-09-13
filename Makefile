
build :
	poetry run python setup.py sdist bdist_wheel

clean :
	$(RM) -rf build dist *.egg-info

coverage :
	poetry run coverage run --source=pyairnow -m pytest tests

coverage-html :
	poetry run coverage html -d .htmlcov && open .htmlcov/index.html

coverage-report :
	poetry run coverage report -m

export :
	poetry export -f requirements.txt -o requirements-dev.txt --dev

lint :
	poetry run flake8

test :
	poetry run python -m pytest tests

test-x :
	poetry run python -m pytest tests -x

test-wip :
	poetry run python -m pytest tests -m wip

all: build

.PHONY: build \
	coverage coverage-html coverage-report \
	lint test test-wip test-x