.PHONY: test eval

test:
	python3 -m unittest discover -s tests -v

# Spends real model tokens: about $4.20 for all 216 runs on Sonnet.
eval:
	eval/fetch-arms.sh
	python3 eval/run.py
