build:

deploy:
	set -a && source .config/env.properties && set +a
	pipenv run python scripts/deploy.py

install:
ifeq ($(INCLUDE_DEV), true)
	@echo "including dev dependencies"
	pipenv install --deploy --dev
else
	pipenv install --deploy
endif

test: test.lint test.script

test.lint: test.lint.python test.lint.yaml

test.lint.python:
	pipenv run flake8 scripts

test.lint.yaml:
	pipenv run yamllint .

test.script:
	pipenv run python scripts/test.py
