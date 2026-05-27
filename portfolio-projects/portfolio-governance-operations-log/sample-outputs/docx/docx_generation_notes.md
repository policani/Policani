# DOCX Generation Notes

DOCX generation is intentionally not implemented in this sample package.

The repository focuses on transparent PMO workflow logic, Markdown portability, browser-readable HTML outputs, and synthetic data. If DOCX output is needed, use either Pandoc or `python-docx` in a controlled local environment.

## Option 1: Pandoc

Example:

```bash
pandoc sample-outputs/markdown/weekly_governance_summary.md -o weekly_governance_summary.docx
pandoc sample-outputs/markdown/executive_air_support_brief.md -o executive_air_support_brief.docx
```

Recommended use:

- Fast conversion from Markdown to Word.
- Good enough for internal review drafts.
- Best when the organization already uses Pandoc.

## Option 2: python-docx

Use `python-docx` when you need controlled headers, tables, margins, styles, and page breaks.

Suggested implementation pattern:

1. Load the Markdown or structured findings data.
2. Create a Word document with approved styles.
3. Map headings, paragraphs, and tables into Word objects.
4. Save the output to a local `docx/` folder.
5. Keep the source Markdown or CSV as the auditable system of record.

## Boundary

DOCX generation should remain a formatting step. It should not change governance meaning, approve recommendations, alter owners, or convert recommendations into decisions.
