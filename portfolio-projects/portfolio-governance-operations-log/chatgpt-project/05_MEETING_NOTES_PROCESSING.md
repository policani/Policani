# Meeting Notes Processing

## Purpose

Convert rough meeting notes into structured governance records.

## Inputs

- Raw meeting notes
- Transcript excerpts
- Chat comments
- Agenda notes
- Facilitator notes

## Outputs

1. Clean meeting summary
2. Decisions made
3. Action items
4. Owners
5. Due dates
6. Risks and issues
7. Dependencies
8. Project-plan updates to confirm
9. Follow-up meetings to schedule
10. Open questions
11. Unresolved items
12. Carry-forward list

## Processing rules

- Do not state that a decision was made unless the notes clearly say it was decided.
- Mark ambiguous decisions as `Decision not confirmed`.
- Mark unclear owners as `Owner missing`.
- Mark missing dates as `Due date missing`.
- Convert vague “follow up” language into a confirmation request.
- Separate parking-lot topics from action items.

## Output format

Use sections for decisions, actions, risks/issues, dependencies, plan updates, unresolved items, and next-cycle carry-forward.
