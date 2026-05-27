# Tools

`build_governance_outputs.py` is a lightweight standard-library Python CLI that regenerates the sample outputs from synthetic CSV files.

Run from the repository root:

```bash
python tools/build_governance_outputs.py
```

The tool:

- validates required columns;
- classifies worklog entries using transparent rule-based logic;
- detects missing owners, due dates, stale updates, weak green status, decision needs, escalation candidates, overdue actions, dependency blockers, and follow-up meeting needs;
- writes Markdown and HTML sample outputs;
- writes findings logs in CSV and JSONL.

It does not connect to external systems, send email, change calendars, update real project plans, or make decisions.
