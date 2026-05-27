#!/usr/bin/env python3
"""
PMO Governance Operations Log sample processor.

Transparent, rules-based classification over synthetic PMO worklog data.
It does not make autonomous portfolio decisions.
"""

from pathlib import Path
import csv
import html
import json
from datetime import datetime, date

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "sample-data" / "synthetic_operations_log.csv"
OUTDIR = ROOT / "examples" / "sample-outputs" / "generated"

def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def classify(row):
    findings = []
    note_type = (row.get("note_type") or "").lower()
    status = (row.get("status") or "").lower()
    decision = (row.get("decision_needed") or "").lower()
    escalation = (row.get("escalation_needed") or "").lower()
    owner = (row.get("owner") or "").strip()
    due = parse_date(row.get("due_date") or "")
    note = (row.get("note") or "").lower()

    if not owner:
        findings.append("missing_owner")
    if note_type in {"action", "follow_up"} and not due:
        findings.append("missing_due_date")
    if decision in {"yes", "possible"}:
        findings.append("decision_needed")
    if escalation in {"yes", "possible"}:
        findings.append("escalation_candidate")
    if note_type in {"risk", "issue", "dependency"}:
        findings.append(note_type)
    if "green" in status and "no milestone evidence" in note:
        findings.append("weak_green_status")
    if due and due < date(2026, 5, 22) and status not in {"closed", "complete"}:
        findings.append("overdue_or_due_now")
    if "blocked" in status:
        findings.append("blocked")
    return findings

def group_by_finding(rows):
    grouped = {}
    for row in rows:
        row["_findings"] = classify(row)
        for finding in row["_findings"]:
            grouped.setdefault(finding, []).append(row)
    return grouped

def html_table(rows, columns):
    if not rows:
        return "<p>None identified.</p>"
    parts = ["<table><thead><tr>"]
    for col in columns:
        parts.append(f"<th>{html.escape(col.replace('_',' ').title())}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for col in columns:
            parts.append(f"<td>{html.escape(row.get(col,'') or '')}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)

def page(title, body):
    style = "<style>body{font-family:Arial,sans-serif;max-width:1100px;margin:40px auto;line-height:1.55;color:#111827}h1,h2{color:#1f2937}table{border-collapse:collapse;width:100%;margin:16px 0}th,td{border:1px solid #d1d5db;padding:8px;text-align:left;vertical-align:top}th{background:#f3f4f6}.note{background:#f9fafb;border-left:4px solid #6b7280;padding:12px}</style>"
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title>{style}</head><body><h1>{html.escape(title)}</h1>{body}</body></html>"

def write_outputs(rows, grouped):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    columns = ["date","initiative","note_type","note","owner","due_date","status","impact","next_step"]

    weekly_body = """
    <div class='note'><p><strong>Executive summary:</strong> The synthetic portfolio has one active cross-initiative blocker, one weak green status signal, one regulatory timing risk, one finance approval dependency, and several follow-up items that need owner/date discipline before the next governance review.</p></div>
    <h2>Decisions Needed</h2>
    """ + html_table(grouped.get("decision_needed", []), columns) + """
    <h2>Escalation Candidates</h2>
    """ + html_table(grouped.get("escalation_candidate", []), columns) + """
    <h2>Blocked or Due-Now Items</h2>
    """ + html_table(grouped.get("blocked", []) + grouped.get("overdue_or_due_now", []), columns) + """
    <h2>Weak Signal Findings</h2>
    """ + html_table(grouped.get("weak_green_status", []), columns)

    (OUTDIR / "weekly-governance-summary.html").write_text(page("Weekly Governance Summary", weekly_body), encoding="utf-8")

    agenda_body = """
    <h2>Proposed 60-Minute Agenda</h2>
    <ol>
    <li>Confirm decision needs and blockers - 10 min</li>
    <li>Customer Portal / Data Platform dependency - 20 min</li>
    <li>Regulatory Reporting validation date - 10 min</li>
    <li>Finance phase 2 budget impact - 10 min</li>
    <li>Action review and carry-forward items - 10 min</li>
    </ol>
    <h2>Facilitator Prompts</h2>
    <ul>
    <li>What decision is needed today?</li>
    <li>Who owns the next action?</li>
    <li>What happens if no decision is made this week?</li>
    <li>Which items should be carried forward?</li>
    </ul>
    """
    (OUTDIR / "meeting-prep-package.html").write_text(page("Meeting Prep Package", agenda_body), encoding="utf-8")

    esc_body = "<h2>Escalation Candidates</h2>" + html_table(grouped.get("escalation_candidate", []), columns)
    esc_body += "<p>These are advisory escalation candidates. A human PMO lead or sponsor must decide whether and how to escalate.</p>"
    (OUTDIR / "executive-air-support-brief.html").write_text(page("Executive Air-Support Brief", esc_body), encoding="utf-8")

    with (OUTDIR / "classification-findings.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps({
                "date": row.get("date"),
                "initiative": row.get("initiative"),
                "note_type": row.get("note_type"),
                "findings": row.get("_findings", []),
                "human_review_required": True
            }) + "\\n")

    md = ["# Weekly Governance Summary", "", "This generated Markdown file is a machine-readable working output. Human-facing samples are provided in HTML.", "", "## Findings by Initiative"]
    for row in rows:
        findings = ", ".join(row.get("_findings", [])) or "no findings"
        md.append(f"- **{row.get('initiative')}**: {findings}")
    (OUTDIR / "weekly-governance-summary-working.md").write_text("\\n".join(md), encoding="utf-8")

def main():
    rows = load_rows(INPUT)
    grouped = group_by_finding(rows)
    write_outputs(rows, grouped)
    print(f"Processed {len(rows)} synthetic worklog rows.")
    print(f"Wrote outputs to {OUTDIR}")

if __name__ == "__main__":
    main()
