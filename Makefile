.PHONY: map clean

map:
	python3 collect.py
	python3 svgmap.py

clean:
	rm -rf data/z14 output/*
