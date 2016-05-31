SHELL := /bin/bash
MAKEFILE_RULES := $(shell cat Makefile | grep "^[A-Za-z]" | awk '{print $$1}' | sed "s/://g" | sort -u)
PYTHON_ENV := $${PYTHON_ENV_LOCATION-"./env"}
PYTHON_REQUIREMENTS := $${PYTHON_REQUIREMENTS_FILE-"./requirements.txt"}


DEFAULT: help

virtualenv:  ## Build the python virtual environment.
	@echo -e "Building/verifying virtualenv at $(PYTHON_ENV) based on $(PYTHON_REQUIREMENTS)\n"
	@command -v pip >/dev/null 2>&1 || { echo >&2 "I require pip but it's not installed.  Aborting."; exit 1; }
	@if [ ! -f "$(PYTHON_ENV)/bin/activate" ] ; then \
	     virtualenv $(PYTHON_ENV) ; \
	fi
	@source $(PYTHON_ENV)/bin/activate ; \
	pip install -q -r $(PYTHON_REQUIREMENTS)


.PHONY: run
run:  ## Run the flask app.
run: virtualenv
	source $(PYTHON_ENV)/bin/activate ; \
	foreman start


.PHONY: lint
lint:  ## Lint the Python app.
lint: virtualenv
	@source $(PYTHON_ENV)/bin/activate ; \
	flake8 *.py

.PHONY: help
help:  ## This help dialog.
	@echo -e  "You can run the following commands from this$(MAKEFILE_LIST):\n"
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`) ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "  %-27s %s\n" $$help_command $$help_info ; \
	done
