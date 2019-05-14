curr_dir = $(shell pwd)
dist_dir = $(curr_dir)/dist
data_dir = $(curr_dir)/data
links_file = $(data_dir)/links.csv
apps_files = $(wildcard $(data_dir)/apps/*.csv)
python_pkg = voting_advice_app_comparison
python_src = $(wildcard $(python_pkg)/*.py)
dist_pdf = $(dist_dir)/graph.pdf
dist_gv = $(dist_dir)/graph.gv

.PHONY: setup setup-dev lint reformat help

graph: $(dist_pdf)  ## Render the graph as PDF

$(dist_dir):
	mkdir -p $(dist_dir)

$(dist_gv): $(dist_dir) $(python_src) $(links_file) $(apps_files)
	pipenv run python3 -m "$(python_pkg)" $(links_file) $(apps_files)  > "$@"

$(dist_pdf): $(dist_gv)
	dot -Tpdf "$^" -o "$@"

clean:  ## Remove rendered graph PDF and temporary Graphviz file
	-rm $(dist_gv)
	-rm $(dist_pdf)

setup:  ## Create Pipenv virtual environment and install dependencies.
	pipenv --three --site-packages
	pipenv install

setup-dev:  ## Install development dependencies
	pipenv install --dev

lint:  ## Run linting
	pipenv run flake8 $(python_pkg)
	pipenv run mypy $(python_pkg) --ignore-missing-imports
	pipenv run isort -c -rc $(python_pkg)

reformat:  ## Reformat Python code using Black
	black -l 79 --skip-string-normalization $(python_pkg)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'
