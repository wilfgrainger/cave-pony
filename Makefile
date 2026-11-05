.PHONY: test eval

test:
	python3 -m unittest discover -s tests -v

# Spends real model tokens: about $2 for all 120 runs.
eval:
	eval/fetch-arms.sh
	python3 eval/run.py
