.PHONY: all setup sync run

# use "make run" after initial setup to skip pipenv setup

all: setup sync run

setup:
	@if ! which pip >/dev/null; then echo "You do not have pip! You are weak!"; exit 1; fi
	@for pkg in pipenv; do which $$pkg >/dev/null || sudo pip install $$pkg; done

sync: setup
	@pipenv sync

run:
	@pipenv run ./run.py
