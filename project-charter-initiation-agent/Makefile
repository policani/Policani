.PHONY: generate validate self-test

generate:
	python scripts/generate_charter.py --input examples/fictional-customer-onboarding-control-tower/source_artifacts/structured_intake.json --out-dir examples/fictional-customer-onboarding-control-tower

validate:
	python scripts/validate_charter.py --charter examples/fictional-customer-onboarding-control-tower/generated_markdown/project_charter.md --rubric config/quality_rubric.json

self-test: generate validate
	@echo "Self-test complete."
