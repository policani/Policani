# Operations Log Schema

Use these fields when structuring rough notes.

Required when known:
- date
- initiative
- note
- note_type
- owner
- due_date
- status
- impact
- next_step
- decision_needed
- escalation_needed
- source

Allowed note_type values:
- status_update
- action
- decision
- risk
- issue
- dependency
- escalation
- meeting_logistics
- project_plan_update
- follow_up
- open_question

If a field is missing, do not invent it. Flag it as missing and add a clarification question.
