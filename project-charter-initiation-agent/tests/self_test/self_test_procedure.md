# Self-Test Procedure

This package tests itself with a fictional project: Customer Onboarding Control Tower Modernization.

## Test steps

1. Use the raw project idea prompt in `sample_prompts/01_raw_project_idea_prompt.md`.
2. Ingest dummy source artifacts from `source_artifacts/`.
3. Use sample intake responses from `intake_responses/sample_intake_responses.md`.
4. Generate Markdown, HTML, and DOCX outputs from `source_artifacts/structured_intake.json`.
5. Validate the Markdown charter against required content signals.
6. Review the charter using `quality_review/charter_quality_review.md`.

## Expected result

The generated charter should be conditionally initiation-ready with no fatal defects.
