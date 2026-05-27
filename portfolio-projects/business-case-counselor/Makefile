.PHONY: sample review clean

sample:
	PYTHONPATH=src python -m business_case_counselor.cli build \
		--answers examples/sample_business_case_input.json \
		--evidence examples/sample_evidence_inbox \
		--out examples/sample_outputs \
		--docx

review:
	PYTHONPATH=src python -m business_case_counselor.cli review \
		--answers examples/sample_business_case_input.json

clean:
	rm -rf work outputs .pytest_cache __pycache__
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
