#!/usr/bin/env python3
"""Score a portfolio intake CSV using a transparent weighted scoring model.

This script intentionally uses only the Python standard library so it can run in
basic environments without installing packages.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

REQUIRED_GOVERNANCE_FIELDS = ["sponsor", "owner", "decision_authority", "mandatory_status"]
REQUIRED_DECISION_FIELDS = ["estimated_cost_usd", "capacity_fte_months", "benefit_summary"]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_criteria(path: Path) -> List[Dict[str, str]]:
    criteria = read_csv(path)
    total_weight = sum(float(c["weight"]) for c in criteria)
    if abs(total_weight - 1.0) > 0.001:
        raise ValueError(f"Criteria weights must sum to 1.00. Current total: {total_weight:.4f}")
    return criteria


def safe_float(value: str, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        return float(value)
    except ValueError:
        return default


def score_value(value: str) -> int:
    try:
        score = int(float(value))
    except (TypeError, ValueError):
        return 0
    if score < 1 or score > 5:
        return 0
    return score


def governance_flags(row: Dict[str, str], criteria: List[Dict[str, str]]) -> List[str]:
    flags = []
    for field in REQUIRED_GOVERNANCE_FIELDS:
        if not row.get(field, "").strip() or row.get(field, "").strip().lower() == "unknown":
            flags.append(f"Missing or unclear {field.replace('_', ' ')}")
    for field in REQUIRED_DECISION_FIELDS:
        if not row.get(field, "").strip():
            flags.append(f"Missing {field.replace('_', ' ')}")
    for criterion in criteria:
        score_col = f"{criterion['criterion_id']}_score"
        if score_value(row.get(score_col, "")) == 0:
            flags.append(f"Invalid or missing score: {criterion['criterion_name']}")
    return flags


def score_initiative(row: Dict[str, str], criteria: List[Dict[str, str]]) -> Tuple[float, Dict[str, int]]:
    weighted_sum = 0.0
    scores = {}
    for criterion in criteria:
        criterion_id = criterion["criterion_id"]
        score_col = f"{criterion_id}_score"
        score = score_value(row.get(score_col, ""))
        scores[criterion_id] = score
        weighted_sum += score * float(criterion["weight"])
    return round((weighted_sum / 5.0) * 100.0, 1), scores


def confidence(row: Dict[str, str], flags: List[str]) -> str:
    if any("sponsor" in f.lower() or "decision authority" in f.lower() for f in flags):
        return "Low"
    if flags:
        return "Medium"
    notes = row.get("evidence_notes", "")
    if "directional" in notes.lower() or "assumption" in notes.lower() or "unclear" in notes.lower():
        return "Medium"
    return "High"


def recommendation(row: Dict[str, str], weighted_score: float, flags: List[str], conf: str) -> str:
    mandatory_status = row.get("mandatory_status", "").strip().lower()
    if any("sponsor" in f.lower() or "decision authority" in f.lower() for f in flags):
        return "Hold for governance clarity"
    if mandatory_status == "mandatory":
        return "Mandatory commitment - protect capacity and sequence through governance"
    if weighted_score >= 78 and conf != "Low":
        if safe_float(row.get("estimated_cost_usd", "")) >= 1500000 or safe_float(row.get("capacity_fte_months", "")) >= 45:
            return "Board trade-off - high value but material funding or capacity burden"
        return "Prioritize"
    if weighted_score >= 65:
        return "Prioritize if capacity exists or refine sequencing"
    if weighted_score >= 50:
        return "Refine business case before funding decision"
    return "Defer or decline unless strategic context changes"


def make_scored_rows(rows: List[Dict[str, str]], criteria: List[Dict[str, str]]) -> List[Dict[str, str]]:
    scored = []
    for row in rows:
        flags = governance_flags(row, criteria)
        weighted_score, _ = score_initiative(row, criteria)
        conf = confidence(row, flags)
        rec = recommendation(row, weighted_score, flags, conf)
        out = dict(row)
        out["weighted_score_100"] = f"{weighted_score:.1f}"
        out["confidence"] = conf
        out["recommendation"] = rec
        out["flags"] = "; ".join(flags) if flags else "None"
        scored.append(out)
    scored.sort(key=lambda r: float(r["weighted_score_100"]), reverse=True)
    return scored


def money(value: str) -> str:
    amount = safe_float(value)
    return f"${amount:,.0f}"


def portfolio_summary(scored: List[Dict[str, str]]) -> Dict[str, object]:
    total_cost = sum(safe_float(r.get("estimated_cost_usd", "")) for r in scored)
    total_capacity = sum(safe_float(r.get("capacity_fte_months", "")) for r in scored)
    mandatory_counts = Counter(r.get("mandatory_status", "Unknown") or "Unknown" for r in scored)
    risk_counts = Counter(r.get("risk_rating", "Unknown") or "Unknown" for r in scored)
    theme_spend = defaultdict(float)
    for r in scored:
        theme_spend[r.get("strategic_theme", "Unknown") or "Unknown"] += safe_float(r.get("estimated_cost_usd", ""))
    governance_holds = [r for r in scored if r.get("recommendation") == "Hold for governance clarity"]
    return {
        "total_initiatives": len(scored),
        "total_cost": total_cost,
        "total_capacity": total_capacity,
        "mandatory_counts": dict(mandatory_counts),
        "risk_counts": dict(risk_counts),
        "theme_spend": dict(theme_spend),
        "governance_holds": len(governance_holds),
    }


def criteria_table_md(criteria: List[Dict[str, str]]) -> str:
    lines = ["| Criterion | Weight |", "| --- | ---: |"]
    for c in criteria:
        lines.append(f"| {c['criterion_name']} | {float(c['weight']) * 100:.0f}% |")
    return "\n".join(lines)


def scored_table_md(scored: List[Dict[str, str]]) -> str:
    lines = [
        "| Rank | ID | Initiative | Category | Mandatory status | Score | Confidence | Recommendation | Flags |",
        "| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for idx, r in enumerate(scored, 1):
        lines.append(
            f"| {idx} | {r['initiative_id']} | {r['title']} | {r['category']} | {r['mandatory_status']} | "
            f"{r['weighted_score_100']} | {r['confidence']} | {r['recommendation']} | {r['flags']} |"
        )
    return "\n".join(lines)


def write_markdown(scored: List[Dict[str, str]], criteria: List[Dict[str, str]], outdir: Path, log_path: Path) -> None:
    summary = portfolio_summary(scored)
    mandatory = [r for r in scored if r.get("mandatory_status", "").lower() == "mandatory"]
    discretionary = [r for r in scored if r.get("mandatory_status", "").lower() == "discretionary"]
    holds = [r for r in scored if r.get("recommendation") == "Hold for governance clarity"]

    theme_lines = ["| Strategic theme | Estimated spend |", "| --- | ---: |"]
    for theme, spend in sorted(summary["theme_spend"].items(), key=lambda x: x[1], reverse=True):
        theme_lines.append(f"| {theme} | ${spend:,.0f} |")

    decisions = []
    for r in mandatory:
        decisions.append(f"| Protect mandatory delivery capacity for {r['initiative_id']} | Portfolio Board | Confirm deadline, capacity, and dependency plan | Compliance exposure remains unresolved. |")
    for r in holds:
        decisions.append(f"| Resolve governance ownership for {r['initiative_id']} | Portfolio Board / sponsoring executive | Named sponsor and decision authority | Item remains unsuitable for funding decision. |")
    material = [r for r in discretionary if "Board trade-off" in r.get("recommendation", "")]
    for r in material:
        decisions.append(f"| Decide near-term sequencing for {r['initiative_id']} | Portfolio Board | Funding/capacity trade-off and dependency readiness | High-value work may crowd out other priorities. |")
    if not decisions:
        decisions.append("| Confirm portfolio sequence | Portfolio Board | Final review of scored view | Delayed sequencing decision. |")

    md = f"""# Portfolio Decision-Support Brief

Generated from synthetic data. This is an advisory output, not a funding decision.

## Executive summary

The synthetic portfolio contains **{summary['total_initiatives']} initiatives** with estimated spend of **${summary['total_cost']:,.0f}** and delivery demand of **{summary['total_capacity']:.0f} FTE-months**. One mandatory compliance initiative should be protected and sequenced through governance. The highest scoring discretionary items are strong but require explicit funding and capacity trade-offs. One platform initiative is on governance hold because sponsor and decision authority are missing.

## Scoring model and weights

{criteria_table_md(criteria)}

## Ranked portfolio view

{scored_table_md(scored)}

## Mandatory commitments

{scored_table_md(mandatory) if mandatory else 'No mandatory initiatives identified.'}

## Discretionary prioritization view

{scored_table_md(discretionary) if discretionary else 'No discretionary initiatives identified.'}

## Budget and capacity view

| Metric | Value |
| --- | ---: |
| Total estimated spend | ${summary['total_cost']:,.0f} |
| Total estimated capacity | {summary['total_capacity']:.0f} FTE-months |
| Governance holds | {summary['governance_holds']} |

## Spend by strategic theme

{chr(10).join(theme_lines)}

## Risk distribution

| Risk rating | Count |
| --- | ---: |
"""
    for risk, count in sorted(summary["risk_counts"].items()):
        md += f"| {risk} | {count} |\n"

    md += f"""
## Dependency and overload observations

- P-001 depends on legal interpretation and archive platform upgrade.
- P-002 depends on identity roadmap and billing API readiness.
- P-003 depends on mobile workforce data cleanup.
- P-004 depends on cloud landing zone, security architecture review, and downstream migration planning.
- Current total demand exceeds a common small-portfolio constraint scenario of $3.0M and 80 FTE-months, so sequencing is required.

## Scenario option - $3.0M and 80 FTE-months

Recommended advisory posture:

1. Protect P-001 as mandatory compliance work, subject to deadline and dependency validation.
2. Sequence P-003 next if the portfolio board wants near-term operational value with lower cost and capacity burden.
3. Treat P-002 as a high-value board trade-off because it has strong growth value but material funding and dependency load.
4. Hold P-004 until sponsor, decision authority, and mandatory status are clarified.

## Human decisions required

| Decision | Recommended owner | Evidence needed | Consequence of delay |
| --- | --- | --- | --- |
{chr(10).join(decisions)}

## Decision log reference

See `{log_path.as_posix()}` for the generated scoring log.
"""
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "portfolio_decision_support_brief.md").write_text(md, encoding="utf-8")


def html_bar(score: str) -> str:
    pct = max(0, min(100, safe_float(score)))
    return f'<div class="bar"><span style="width:{pct:.1f}%"></span></div><span class="score">{pct:.1f}</span>'


def write_html(scored: List[Dict[str, str]], criteria: List[Dict[str, str]], outdir: Path) -> None:
    summary = portfolio_summary(scored)
    rows = []
    for idx, r in enumerate(scored, 1):
        rows.append(f"""
        <tr>
          <td>{idx}</td>
          <td>{html.escape(r['initiative_id'])}</td>
          <td>{html.escape(r['title'])}</td>
          <td>{html.escape(r['category'])}</td>
          <td>{html.escape(r['mandatory_status'])}</td>
          <td>{html_bar(r['weighted_score_100'])}</td>
          <td>{html.escape(r['confidence'])}</td>
          <td>{html.escape(r['recommendation'])}</td>
          <td>{html.escape(r['flags'])}</td>
        </tr>
        """)

    criteria_rows = []
    for c in criteria:
        criteria_rows.append(f"<tr><td>{html.escape(c['criterion_name'])}</td><td>{float(c['weight']) * 100:.0f}%</td><td>{html.escape(c['description'])}</td></tr>")

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Portfolio Summary</title>
<style>
:root {{ --border:#d7d7d7; --text:#1f2937; --muted:#6b7280; --bg:#f8fafc; --card:#ffffff; }}
body {{ font-family: Arial, Helvetica, sans-serif; margin: 32px; color: var(--text); background: var(--bg); }}
h1, h2 {{ margin-bottom: 8px; }}
.card-grid {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 16px; margin: 20px 0; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
.card .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
.card .value {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
table {{ width: 100%; border-collapse: collapse; background: var(--card); margin: 16px 0 28px; }}
th, td {{ border: 1px solid var(--border); padding: 9px 10px; vertical-align: top; font-size: 14px; }}
th {{ background: #eef2f7; text-align: left; }}
.bar {{ display: inline-block; width: 120px; height: 10px; border: 1px solid var(--border); background: #f3f4f6; margin-right: 8px; vertical-align: middle; }}
.bar span {{ display: block; height: 100%; background: #4b5563; }}
.score {{ font-weight: 700; }}
.callout {{ border-left: 5px solid #4b5563; background: #fff; padding: 14px 16px; margin: 18px 0; }}
.footer {{ color: var(--muted); font-size: 12px; margin-top: 28px; }}
</style>
</head>
<body>
<h1>Portfolio Summary</h1>
<p>Generated from synthetic data. Advisory decision support only; final funding and sequencing decisions remain with accountable human leaders.</p>
<div class="card-grid">
  <div class="card"><div class="label">Initiatives</div><div class="value">{summary['total_initiatives']}</div></div>
  <div class="card"><div class="label">Estimated spend</div><div class="value">${summary['total_cost']:,.0f}</div></div>
  <div class="card"><div class="label">Capacity demand</div><div class="value">{summary['total_capacity']:.0f}</div></div>
  <div class="card"><div class="label">Governance holds</div><div class="value">{summary['governance_holds']}</div></div>
</div>
<h2>Scored Portfolio View</h2>
<table>
<thead><tr><th>Rank</th><th>ID</th><th>Initiative</th><th>Category</th><th>Status</th><th>Score</th><th>Confidence</th><th>Recommendation</th><th>Flags</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
<h2>Scoring Criteria</h2>
<table>
<thead><tr><th>Criterion</th><th>Weight</th><th>Description</th></tr></thead>
<tbody>{''.join(criteria_rows)}</tbody>
</table>
<div class="callout">
<strong>Human decisions required:</strong> protect mandatory compliance capacity, decide whether to sequence the high-value discretionary work under current budget and capacity constraints, and resolve sponsor/decision-authority gaps before considering P-004 for funding.
</div>
<div class="footer">Model version: default-v1 | Generated: {datetime.now(timezone.utc).isoformat()}</div>
</body>
</html>
"""
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "portfolio_summary.html").write_text(html_doc, encoding="utf-8")


def write_log(scored: List[Dict[str, str]], criteria: List[Dict[str, str]], logdir: Path, input_path: Path, criteria_path: Path) -> Path:
    logdir.mkdir(parents=True, exist_ok=True)
    log_path = logdir / "scoring_run_log.jsonl"
    run_id = datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ")
    events = [
        {"event":"run_started","run_id":run_id,"timestamp":datetime.now(timezone.utc).isoformat(),"input":str(input_path),"criteria":str(criteria_path)},
        {"event":"criteria_loaded","run_id":run_id,"criteria_count":len(criteria),"weights_total":sum(float(c['weight']) for c in criteria)},
    ]
    for r in scored:
        events.append({
            "event":"initiative_scored",
            "run_id":run_id,
            "initiative_id":r.get("initiative_id"),
            "title":r.get("title"),
            "weighted_score_100":r.get("weighted_score_100"),
            "confidence":r.get("confidence"),
            "recommendation":r.get("recommendation"),
            "flags":r.get("flags"),
        })
    events.append({"event":"run_completed","run_id":run_id,"timestamp":datetime.now(timezone.utc).isoformat(),"initiative_count":len(scored)})
    with log_path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return log_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a portfolio intake CSV using weighted criteria.")
    parser.add_argument("--input", required=True, type=Path, help="Portfolio intake CSV.")
    parser.add_argument("--criteria", required=True, type=Path, help="Scoring criteria CSV.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for scored CSV and Markdown output.")
    parser.add_argument("--html-dir", required=True, type=Path, help="Directory for HTML output.")
    parser.add_argument("--log-dir", required=True, type=Path, help="Directory for JSONL log output.")
    args = parser.parse_args()

    criteria = load_criteria(args.criteria)
    rows = read_csv(args.input)
    scored = make_scored_rows(rows, criteria)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "scored_portfolio.csv", scored)
    log_path = write_log(scored, criteria, args.log_dir, args.input, args.criteria)
    write_markdown(scored, criteria, args.output_dir, log_path)
    write_html(scored, criteria, args.html_dir)

    print(f"Scored {len(scored)} initiatives.")
    print(f"Markdown and CSV: {args.output_dir}")
    print(f"HTML: {args.html_dir}")
    print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
