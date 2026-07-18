.PHONY: validate test build clean

validate:
	python3 tools/validate.py

test:
	python3 -m unittest discover -s tests -v

build:
	python3 tools/build.py

clean:
	rm -rf dist tools/__pycache__ tests/__pycache__
