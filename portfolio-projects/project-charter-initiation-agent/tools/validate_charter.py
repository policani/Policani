#!/usr/bin/env python3
"""Lightweight charter validator for required content signals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_SIGNALS = {
    'why_project_exists': ['Purpose and Business Outcome', 'Why now'],
    'business_outcome': ['Supported business outcome'],
    'sponsor_and_owner': ['Executive Sponsor', 'Business Owner', 'Project Manager', 'Approval Body'],
    'scope': ['In Scope', 'Out of Scope'],
    'deliverables': ['Authorized Deliverables'],
    'success_measures': ['Success Measures'],
    'assumptions_constraints': ['Assumptions', 'Constraints'],
    'risks_dependencies_open_decisions': ['Initial Risks', 'Critical Dependencies', 'Open Decisions'],
    'governance': ['Steering cadence', 'Escalation path', 'Change-control model'],
    'milestone_path': ['Milestone Path']
}


def validate(text):
    results = []
    for name, signals in REQUIRED_SIGNALS.items():
        missing = [s for s in signals if s not in text]
        results.append({'criterion': name, 'status': 'pass' if not missing else 'fail', 'missing': missing})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--charter', required=True)
    parser.add_argument('--rubric', required=False)
    args = parser.parse_args()
    text = Path(args.charter).read_text(encoding='utf-8')
    results = validate(text)
    print(json.dumps(results, indent=2))
    if any(r['status'] == 'fail' for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
