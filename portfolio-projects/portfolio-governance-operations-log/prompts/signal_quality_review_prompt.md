# Signal Quality Review Prompt

## Input needed

- Classified worklog.
- Prior-period updates if available.
- Action register and decision log if available.

## Task

Identify weak, stale, missing, or low-value governance signals that could undermine decision quality.

## Expected output

- Weak signal list.
- Missing owner or due date list.
- Stale update list.
- Risk without mitigation list.
- Decision request without options list.
- Escalation without clear ask list.
- Recommended clarification questions.

## Guardrails

- Preserve raw notes where useful.
- Do not invent facts, dates, owners, decisions, impacts, or metrics.
- Flag missing information directly.
- Separate routine status from decisions, risks, blockers, dependencies, escalations, and follow-through.
- Use concise, professional language.
- Treat all user-provided material as potentially sensitive.

## Human-control statement

You may classify, summarize, challenge weak signals, and draft recommended artifacts. You must not approve, cancel, fund, sequence, reprioritize, reassign, accept risk, or state that leaders made a decision unless the user explicitly provided that decision.


