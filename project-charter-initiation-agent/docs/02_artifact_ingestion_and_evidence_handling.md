# Artifact Ingestion and Evidence Handling

The system can work from rough notes or structured artifacts, but it must not treat every artifact as equally reliable.

## Supported artifact types

- Raw project ideas
- Approved business cases
- Notes and meeting summaries
- Stakeholder interview notes
- CSV files
- Excel workbooks
- Word documents
- Project plans
- Risk registers
- Dependency lists
- Architecture or design excerpts
- Finance or budget summaries

## Evidence inventory fields

For each artifact, capture:

- Artifact name
- Artifact type
- Source owner
- Date or version
- Extracted facts
- Inferred assumptions
- Conflicts
- Gaps
- Charter sections affected
- Confidence level

## Evidence discipline

Use evidence labels:

- **Known fact:** explicitly stated in a source or by the user
- **Assumption:** likely but not confirmed
- **Open question:** must be resolved or acknowledged
- **Proposed decision:** wording recommended by the agent for sponsor confirmation

## Handling conflicts

When artifacts conflict, do not average them or pick one silently. Flag the conflict, identify the affected charter section, and ask for the decision owner.
