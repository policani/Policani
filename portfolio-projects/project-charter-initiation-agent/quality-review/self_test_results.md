# Self-Test Results

## Scenario tested

Customer Onboarding Control Tower Modernization.

## Inputs used

- Raw project idea prompt
- Artifact ingestion test prompt
- Sample intake responses
- Approved business case summary
- Stakeholder roles CSV
- Budget summary CSV
- Risk/dependency/open-decision CSV
- Delivery plan excerpt
- Structured intake JSON
- Stakeholder interview notes DOCX
- Budget and milestone workbook XLSX

## Generated outputs

- `examples/fictional-customer-onboarding-control-tower/generated_markdown/project_charter.md`
- `examples/fictional-customer-onboarding-control-tower/generated_html/project_charter.html`
- `examples/fictional-customer-onboarding-control-tower/generated_docx/project_charter.docx`
- `examples/fictional-customer-onboarding-control-tower/quality_review/charter_quality_review.md`

## Self-test command

```bash
make self-test
```

## Validator result

All required content signals passed:

- Why the project exists
- Business outcome
- Sponsor and owner
- Scope
- Deliverables
- Success measures
- Assumptions and constraints
- Risks, dependencies, and open decisions
- Governance and change control
- Milestone path

## DOCX render check

The generated DOCX was rendered to page images during package QA. The rendered document produced 4 clean pages with no observed clipping, overlap, missing text, or broken tables.

## Readiness conclusion

The sample charter is conditionally initiation-ready. It is appropriate for sponsor review and planning authorization, with normal planning-entry gaps called out explicitly.
