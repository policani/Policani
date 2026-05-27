# Artifact Intake Guide

The tool is designed to accept rough input. Do not wait until the materials are polished.

## Useful artifacts

| Artifact | Why it helps |
|---|---|
| High-level ideas | Establishes intent and decision context |
| Notes | Captures pain points, stakeholder concerns, and open questions |
| Excel spreadsheets | Supports cost, benefit, volume, risk, inventory, or prioritization analysis |
| CSV files | Easy structured input for costs, benefits, risks, assumptions, and stakeholders |
| Word documents | Existing drafts, requirements, governance notes, planning summaries |
| Project plans | Milestones, dependencies, roles, and timing assumptions |
| Architecture notes | Feasibility, dependencies, constraints, and implementation risk |
| Meeting notes | Stakeholder alignment, objections, and decision history |

## Intake discipline

Put source artifacts into `evidence_inbox/`. Keep file names descriptive.

Recommended file naming:

```text
2026-05-initiative-notes.md
cost-benefit-draft.xlsx
stakeholder-feedback.docx
risk-log.csv
current-state-process-notes.txt
```

## Evidence handling rules

1. Preserve source files.
2. Summarize evidence without overstating it.
3. Keep estimates separate from validated facts.
4. Record unknowns as open questions.
5. Do not convert weak assumptions into confident benefits.
6. For spreadsheets, note which values are formulas, estimates, or source data when possible.

## Project plans

Project plan formats vary. For consistent ingestion, export key fields to CSV:

- Task or milestone name
- Owner
- Start date
- Finish date
- Dependency
- Status
- Notes

The business case does not need a full delivery plan. It needs enough implementation shape for leadership to judge feasibility, timing, ownership, and risk.
