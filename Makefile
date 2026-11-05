.PHONY: test eval

test:
	python3 -m unittest discover -s tests -v

# Spends real model tokens (~$0.02 per run). See eval/README.md.
eval:
	eval/fetch-arms.sh
	python3 eval/run.py
