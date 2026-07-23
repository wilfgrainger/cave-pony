.PHONY: validate test clean

validate:
	python3 tools/validate.py

test:
	test -f tests/test_profile_artwork.py
	python3 -m unittest discover -s tests -v

clean:
	rm -rf tools/__pycache__ tests/__pycache__
