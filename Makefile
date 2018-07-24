.PHONY: test run graph

test:
	find tests -iname "test_*.py" | xargs python3 -m unittest

run:
	python3 main.py one

graph:
	sfdp -Tps asdf.gv -o asdf.ps
