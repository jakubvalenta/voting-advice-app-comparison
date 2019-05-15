dist_dir = dist
data_dir = data
links_file = $(data_dir)/links.csv
apps_files = $(sort $(wildcard $(data_dir)/apps/*.csv))
python_pkg = voting_advice_app_comparison
python_src = $(wildcard $(python_pkg)/*)
template_src = $(wildcard $(python_pkg)/templates/*)
dist_svg = $(dist_dir)/graph.svg
dist_png = $(dist_dir)/graph.png
dist_gv = $(dist_dir)/graph.gv

.PHONY: setup setup-dev lint reformat help

graph: $(dist_png)  ## Render the graph as SVG and PNG

$(dist_dir):
	mkdir -p $(dist_dir)

$(dist_gv): $(python_src) $(template_src) $(links_file) $(apps_files) | $(dist_dir)
	pipenv run python3 -m "$(python_pkg)" $(links_file) $(apps_files)  > "$@"

$(dist_svg): $(dist_gv)
	dot -Tsvg "$^" -o "$@"

$(dist_png): $(dist_svg)
	rsvg-convert -d 72 "$^" | convert -trim +repage - "$@"
	optipng -preserve "$@"

clean:  ## Remove rendered graph SVG and temporary Graphviz file
	-rm $(dist_gv)
	-rm $(dist_svg)
	-rm $(dist_png)

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
