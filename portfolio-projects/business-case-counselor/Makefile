.PHONY: test sample

test:
	python tools/smoke_test.py

sample:
	PYTHONPATH=src python -m business_case_counselor.cli build --answers examples/sample_business_case_input.json --evidence examples/sample_evidence_inbox --out examples/sample_outputs --docx --html
