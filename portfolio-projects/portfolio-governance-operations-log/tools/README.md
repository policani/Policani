# Tools

This folder contains a lightweight, inspectable Python CLI for regenerating the synthetic sample output pack.

Run from the repository root:

```bash
python tools/build_governance_outputs.py
```

The script uses only Python standard libraries. It reads CSV files from `examples/sample-data/`, validates required columns, classifies worklog entries with transparent rule-based logic, and writes consolidated outputs to `examples/sample-outputs/`:

- `sample_output_pack.md`
- `sample-output-pack.html`
- `findings_log.csv`
- `findings_log.jsonl`

It does not send messages, modify calendars, connect to external systems, change project plans, or make governance decisions.
