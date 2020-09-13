
coverage :
	pipenv run coverage run --source=pyairnow -m pytest tests

coverage-html :
	pipenv run coverage html -d .htmlcov && open .htmlcov/index.html

coverage-report :
	pipenv run coverage report -m

lint :
	pipenv run flake8

test :
	pipenv run python -m pytest tests

test-x :
	pipenv run python -m pytest tests -x

test-wip :
	pipenv run python -m pytest tests -m wip

#all: serve

.PHONY: coverage coverage-html coverage-report \
	lint test test-wip test-x
