
coverage :
	pipenv run coverage run --source=jadetree -m pytest tests

coverage-html :
	pipenv run coverage html -d .htmlcov && open .htmlcov/index.html

coverage-report :
	pipenv run coverage report -m

docs :
	$(MAKE) -C docs html

docs-clean :
	$(MAKE) -C docs clean

docs-serve :
	pipenv run sphinx-autobuild docs docs/_build/html --no-initial -B -s 1

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
	docs docs-clean docs-serve \
	lint test test-wip test-x
