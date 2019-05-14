curr_dir = $(shell pwd)
dist_dir = $(curr_dir)/dist
data_dir = $(curr_dir)/data
links_file = $(data_dir)/links.csv
apps_files = $(wildcard $(data_dir)/apps/*.csv)
python_pkg = voting_advice_app_comparison
python_src = $(wildcard $(python_pkg)/*.py)
dist_pdf = $(dist_dir)/graph.pdf
dist_gv = $(dist_dir)/graph.gv

graph: $(dist_pdf)

$(dist_dir):
	mkdir -p $(dist_dir)

$(dist_gv): $(dist_dir) $(python_src) $(links_file) $(apps_files)
	python -m "$(python_pkg)" $(links_file) $(apps_files)  > "$@"

$(dist_pdf): $(dist_gv)
	dot -Tpdf "$^" -o "$@"

clean:
	-rm $(dist_gv)
	-rm $(dist_pdf)
