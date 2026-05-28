# Output Generation Guide

## Markdown output

Use Markdown for agent-readable and reviewable outputs. Required sections:

1. Executive summary
2. Scoring model and assumptions
3. Ranked portfolio view
4. Mandatory commitments
5. Budget and capacity view
6. Risk and dependency view
7. Missing-data flags
8. Scenario options
9. Human decisions required
10. Decision log reference

## HTML output

Use HTML when the output needs richer formatting for stakeholder review. Recommended elements:

- Summary cards
- Scored initiative table
- Mandatory versus discretionary section
- Simple progress bars for weighted scores
- Risk and dependency tables
- Human decision callout box
- Footer with run timestamp and model version

## DOCX output

DOCX can be produced programmatically from the Markdown or HTML output using a DOCX library such as `python-docx`.

Recommended DOCX structure:

1. Title page or heading
2. Executive summary
3. Portfolio score table
4. Mandatory and discretionary views
5. Budget and capacity summary
6. Risks, dependencies, and governance flags
7. Human decisions required
8. Appendix: criteria and weights

Implementation notes:

- Use Word heading styles for navigation.
- Keep tables narrow enough for portrait layout or use landscape section breaks for wide tables.
- Include generated date and data source.
- Avoid putting confidential source notes into a public DOCX.
- Visually inspect rendered output before distributing.
