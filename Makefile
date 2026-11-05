.PHONY: test eval

test:
	python3 -m unittest discover -s tests -v

# Spends real model tokens (about $2 for the full 120 runs). See README.md, "Does it work?".
eval:
	eval/fetch-arms.sh
	python3 eval/run.py
