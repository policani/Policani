# Artifact Ingestion and Privacy Guide

## Purpose

The agent can ingest business cases, charters, spreadsheets, roadmaps, and stakeholder notes, but it should extract only the portfolio metadata needed for scoring and decision support.

## Supported artifact types

- Business case summaries
- Project charters
- Intake forms
- Portfolio spreadsheets
- Risk registers
- Dependency lists
- Executive notes
- Roadmap excerpts
- Approval logs

## Safe ingestion steps

1. Work from copies, not original confidential records.
2. Remove customer names, employee names, contract identifiers, security details, and sensitive financial details unless they are required for internal review.
3. Replace sensitive names with stable placeholders such as `Customer A`, `Vendor B`, or `System C`.
4. Convert large documents into concise summaries before scoring.
5. Extract only required fields into the intake schema.
6. Preserve source references internally, but do not expose confidential details in generated public samples.
7. Mark assumptions where source evidence is incomplete.
8. Keep a scoring log so changes are auditable.

## Spreadsheet handling

Recommended spreadsheet columns are listed in `data/portfolio_intake_schema.csv`. For safety:

- Remove hidden sheets before sharing.
- Remove comments, tracked changes, and personal metadata.
- Check formulas for external references.
- Convert to CSV for repeatable scoring when possible.
- Do not paste full financial models into an AI session unless approved for that environment.

## Anonymization checklist

- Names replaced with roles or placeholders
- Customer or vendor names removed unless approved
- Exact contract numbers removed
- Sensitive system names generalized
- Security architecture details removed
- Exact compensation or personal data removed
- Financials rounded where detailed values are not required
- Source document metadata scrubbed

## Sandbox recommendation

Use a local or approved sandbox when processing sensitive materials. Do not load proprietary source artifacts into public or unapproved tools. For published GitHub samples, use synthetic data only.
