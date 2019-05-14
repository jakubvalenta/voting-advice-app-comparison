graph: graph.ps

graph.gv: voting_advice_app_comparison/main.py cz.csv de.csv map.csv
	python -m voting_advice_app_comparison cz.csv de.csv map.csv > $@

graph.ps: graph.gv
	dot -Tps graph.gv -o graph1.ps
