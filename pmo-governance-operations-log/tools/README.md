# Tools

This folder contains lightweight sample tooling for the PMO Governance Operations Log.

Run from the repository root:

```bash
python tools/process_operations_log.py
```

The script reads synthetic data from `examples/sample-data/synthetic_operations_log.csv` and writes generated outputs to `examples/sample-outputs/generated/`.

The script uses transparent, rules-based classification. It does not make decisions, approve work, or replace PMO judgment.
