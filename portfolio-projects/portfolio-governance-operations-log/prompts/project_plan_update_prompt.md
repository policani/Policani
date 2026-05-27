# Project Plan Update Recommendations Prompt

## Input needed

- Classified worklog.
- Project snapshot.
- Current milestone list if available.
- Action register, RAID log, and decision log if available.

## Task

Identify project-plan, RAID, decision-log, and action-register updates implied by the worklog.

## Expected output

- Suggested task updates.
- Milestone changes.
- Date changes.
- Dependency updates.
- Owner changes needing confirmation.
- RAID updates.
- Human confirmation questions.

## Guardrails

- Preserve raw notes where useful.
- Do not invent facts, dates, owners, decisions, impacts, or metrics.
- Flag missing information directly.
- Separate routine status from decisions, risks, blockers, dependencies, escalations, and follow-through.
- Use concise, professional language.
- Treat all user-provided material as potentially sensitive.
- Produce recommendations only. Do not directly modify a real plan.

## Human-control statement

You may classify, summarize, challenge weak signals, and draft recommended artifacts. You must not approve, cancel, fund, sequence, reprioritize, reassign, accept risk, or state that leaders made a decision unless the user explicitly provided that decision.


