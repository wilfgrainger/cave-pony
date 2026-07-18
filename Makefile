.PHONY: validate test clean

validate:
	python3 tools/validate.py

test:
	python3 -m unittest discover -s tests -v

clean:
	rm -rf tools/__pycache__ tests/__pycache__
