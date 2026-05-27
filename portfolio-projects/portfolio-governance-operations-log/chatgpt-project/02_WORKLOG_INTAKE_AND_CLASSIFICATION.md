# Worklog Intake and Classification

## Purpose

Turn rough notes into a structured governance worklog.

## Inputs

Accept freeform notes, meeting fragments, stakeholder updates, chat text, action notes, dependency notes, risk notes, scheduling notes, and escalation notes.

## Classification fields

For each note, produce:

| Field | Meaning |
|---|---|
| Worklog ID | Sequential ID if none is provided |
| Date | Date from note or `Not provided` |
| Initiative | Project / program / portfolio item |
| Raw note | Preserve original note |
| Primary category | Main governance category |
| Supporting flags | Secondary categories |
| Owner | Named owner or `Missing` |
| Due date | Date or `Missing` |
| Urgency | Low / Medium / High / Critical |
| Action needed | Specific follow-up or confirmation needed |
| Missing fields | Owner, due date, decision options, mitigation, evidence, ask, accountable parties |
| Human confirmation | What a person must confirm before action |

## Classification rules

- If the note asks for approval, tradeoff, scope choice, or executive direction, classify as `Decision needed`.
- If the note says blocked, waiting, dependent, cannot proceed, or delayed by another team, classify as `Blocker` or `Dependency`.
- If the note mentions potential impact or uncertainty, classify as `Risk` unless the impact is already happening, then classify as `Issue`.
- If the note says green, on track, fine, or no concern without evidence, flag as `Weak signal`.
- If the same status is repeated from a prior period without new evidence, flag as `Stale update`.
- If an action has no owner, flag `Missing owner`.
- If an action has no date, flag `Missing due date`.
- If an escalation has no clear ask, flag `Escalation ask missing`.
- If a plan date, dependency, milestone, or scope item changes, flag `Project-plan update`.

## Output

Return a table plus a short `Immediate attention` section.

## Guardrail

Do not invent owners, dates, impacts, or decisions. Mark them missing.
