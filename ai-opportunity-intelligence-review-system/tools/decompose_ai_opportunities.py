#!/usr/bin/env python3
"""Generate sample AI opportunity intelligence review outputs.

This is intentionally simple and transparent. It demonstrates the operating
model with synthetic data; it is not an autonomous investment decision engine.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
from datetime import date
from pathlib import Path


REQUIRED_COLUMNS = [
    "id",
    "name",
    "sponsor",
    "business_problem",
    "current_workflow",
    "proposed_ai_role",
    "affected_users",
    "volume",
    "frequency",
    "value_claim",
    "data_readiness",
    "risk_level",
    "workflow_clarity",
    "strategic_fit",
    "existing_tools",
    "deadline",
    "notes",
]


def norm(value: str) -> str:
    return (value or "").strip().lower()


def score_level(value: str, mapping: dict[str, int], default: int = 3) -> int:
    return mapping.get(norm(value), default)


def contains(row: dict[str, str], *needles: str) -> bool:
    text = " ".join(row.values()).lower()
    return any(needle.lower() in text for needle in needles)


def decompose_stack(row: dict[str, str]) -> dict[str, str]:
    workflow = row["current_workflow"]
    role = row["proposed_ai_role"]
    tools = row["existing_tools"]
    users = row["affected_users"]
    problem = row["business_problem"]

    if contains(row, "predict", "churn", "risk"):
        interpretation = "Detect patterns, estimate risk, and explain evidence behind the signal."
        decision = "Prepare prioritization recommendations and human-reviewed intervention options."
    elif contains(row, "summar", "synthes", "cluster", "theme"):
        interpretation = "Synthesize source material, cluster themes, and cite supporting examples."
        decision = "Prepare decision implications, action items, or follow-up questions for review."
    elif contains(row, "contract", "redline", "legal"):
        interpretation = "Compare text against approved clauses, risk patterns, and policy constraints."
        decision = "Prepare redline suggestions and risk notes for attorney review."
    elif contains(row, "schedule", "dispatch", "orchestrat"):
        interpretation = "Interpret capacity, location, priority, constraint, and conflict signals."
        decision = "Recommend schedule adjustments and exception paths for dispatcher approval."
    elif contains(row, "policy", "q&a", "question"):
        interpretation = "Match questions to approved policy sources and detect confidence or escalation needs."
        decision = "Draft cited answers or route uncertain questions to a human owner."
    else:
        interpretation = "Classify inputs, extract relevant facts, and identify decision-useful patterns."
        decision = "Prepare recommendations, options, or next-step classifications for human review."

    return {
        "purpose": f"Improve {workflow} by addressing: {problem}",
        "sensing": f"Observe approved inputs from {tools or 'defined source systems'} plus user-provided workflow context.",
        "interpretation": interpretation,
        "decision": decision,
        "orchestration": f"Coordinate outputs with {users}; do not execute irreversible actions without human approval.",
        "learning": "Compare outputs against human decisions, exception outcomes, quality review notes, and stop/scale criteria.",
        "govern_assure": "Use source citations, eval examples, searchable logs, permission boundaries, rollback or undo paths, and human review queues.",
        "proposed_ai_role": role,
    }


def classify_work_shape(row: dict[str, str]) -> str:
    if score_level(row["workflow_clarity"], {"low": 1, "medium": 3, "high": 5}) <= 1:
        return "Unclear or bundled work"
    if contains(row, "summar", "synthes", "cluster", "research", "feedback"):
        return "Research and synthesis"
    if contains(row, "exception", "triage", "route", "dispatch"):
        return "Exception handling and operational coordination"
    if contains(row, "policy", "q&a", "question", "support"):
        return "Employee or customer interaction with escalation"
    if contains(row, "predict", "risk", "prioritization"):
        return "Structured judgment support"
    if contains(row, "dashboard", "reporting", "visibility"):
        return "Portfolio reporting and governance design"
    return "Bounded workflow support"


def recommend_route(row: dict[str, str], scores: dict[str, int]) -> tuple[str, str, str]:
    risk = norm(row["risk_level"])
    data = norm(row["data_readiness"])
    workflow = norm(row["workflow_clarity"])
    fit = norm(row["strategic_fit"])

    if contains(row, "governance design more than ai", "problem is governance"):
        return (
            "Process-First",
            "The stated pain appears to be governance design rather than an AI capability gap.",
            "Define the operating rhythm, ownership, and data model before building AI support.",
        )
    if risk == "high" and data in {"weak", "unknown"}:
        return (
            "Wait",
            "High risk and weak data make a proof unreliable without control and evidence work first.",
            "Create data readiness and control requirements before authorizing a prototype.",
        )
    if contains(row, "field service", "scheduling", "dispatch") and fit == "high":
        return (
            "Build",
            "The workflow appears operationally differentiated and depends on orchestration logic tied to local constraints.",
            "Prototype the scheduling intelligence layer first, then decide whether custom build is justified.",
        )
    if contains(row, "vendor intake", "screener") and fit == "high":
        return (
            "Build",
            "The opportunity directly supports the organization's AI governance intelligence layer and may become reusable operating infrastructure.",
            "Build a constrained internal workflow package after testing with synthetic and historical intake records.",
        )
    if workflow == "low":
        return (
            "Decompose Further",
            "The workflow is not clear enough to route as one AI investment.",
            "Map the workflow and split bundled ideas into smaller opportunity records.",
        )
    if contains(row, "policy", "q&a", "question") and data == "available":
        return (
            "Buy",
            "The workflow is common enough that vendor or platform capability should be tested before custom build.",
            "Run a controlled comparison of approved knowledge-base or HR-service capabilities with citation and escalation requirements.",
        )
    if risk == "high":
        return (
            "Prototype",
            "The opportunity may be valuable, but it needs a constrained proof with strong human review.",
            "Run a limited offline test using approved examples, eval cases, logs, and expert review.",
        )
    if data == "available" and fit == "high":
        return (
            "Prototype",
            "The workflow, data, and strategic fit are strong enough for a cheap bounded proof.",
            "Run a timeboxed prototype against historical examples and compare against human baseline.",
        )
    if contains(row, "overlap", "existing transcript", "existing tools", "deck generator", "sales deck"):
        return (
            "Automate With Existing Tools",
            "Existing capabilities may solve enough of the need without a new AI project.",
            "Test current-tool configuration and adoption before building custom functionality.",
        )
    if data in {"unknown", "weak"}:
        return (
            "Process-First",
            "The opportunity lacks enough usable evidence or data readiness for credible AI evaluation.",
            "Establish baseline, source ownership, and sample records before AI proof work.",
        )
    return (
        "Prototype",
        "The opportunity has enough clarity for a bounded proof, but value still needs evidence.",
        "Design a small proof with baseline, success measure, stop condition, and human review.",
    )


def score_row(row: dict[str, str]) -> dict[str, int]:
    problem = 4 if len(row["business_problem"]) > 40 else 2
    workflow = score_level(row["workflow_clarity"], {"low": 1, "medium": 3, "high": 5})
    data = score_level(row["data_readiness"], {"unknown": 1, "weak": 1, "partial": 3, "available": 5})
    risk = score_level(row["risk_level"], {"low": 5, "moderate": 3, "high": 1})
    fit = score_level(row["strategic_fit"], {"low": 1, "medium": 3, "high": 5})
    proof = 5 if data >= 3 and workflow >= 3 else 2
    decomposition = 5 if row["proposed_ai_role"] and row["current_workflow"] else 2
    value = 4 if any(word in norm(row["value_claim"]) for word in ["reduce", "improve", "save", "increase"]) else 2
    return {
        "problem_clarity": problem,
        "intelligence_decomposition": decomposition,
        "workflow_readiness": workflow,
        "value_evidence": value,
        "data_readiness": data,
        "control_readiness": risk,
        "strategic_fit": fit,
        "proof_efficiency": proof,
    }


def render_markdown(rows: list[dict[str, str]], analyses: list[dict]) -> str:
    today = date.today().isoformat()
    route_counts: dict[str, int] = {}
    for item in analyses:
        route_counts[item["route"]] = route_counts.get(item["route"], 0) + 1

    lines = [
        "# AI Opportunity Intelligence Review Pack",
        "",
        f"Generated: {today}",
        "",
        "## Portfolio Summary",
        "",
        f"- Opportunities reviewed: {len(analyses)}",
        f"- Routes represented: {', '.join(f'{route} ({count})' for route, count in sorted(route_counts.items()))}",
        "- Human leaders retain authority for funding, staffing, vendor selection, risk acceptance, and sequencing.",
        "",
        "## Route Summary",
        "",
        "| ID | Opportunity | Work Shape | Route | Rationale | Next Step |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in analyses:
        lines.append(
            f"| {item['id']} | {item['name']} | {item['work_shape']} | {item['route']} | "
            f"{item['rationale']} | {item['next_step']} |"
        )

    lines.extend(["", "## Intelligence Stack Decomposition", ""])
    for item in analyses:
        stack = item["stack"]
        lines.extend(
            [
                f"### {item['id']} - {item['name']}",
                "",
                f"**Recommended route:** {item['route']}",
                "",
                "| Layer | Decomposition |",
                "| --- | --- |",
                f"| Purpose | {stack['purpose']} |",
                f"| Sensing | {stack['sensing']} |",
                f"| Interpretation | {stack['interpretation']} |",
                f"| Decision | {stack['decision']} |",
                f"| Orchestration | {stack['orchestration']} |",
                f"| Learning | {stack['learning']} |",
                f"| Govern and assure | {stack['govern_assure']} |",
                "",
                "#### Scores",
                "",
                "| Dimension | Score |",
                "| --- | ---: |",
            ]
        )
        for key, value in item["scores"].items():
            lines.append(f"| {key.replace('_', ' ').title()} | {value} |")
        lines.extend(
            [
                "",
                "#### Cheapest Credible Proof",
                "",
                item["next_step"],
                "",
                "#### Human Decision Needed",
                "",
                "Decide whether to authorize the recommended next learning step. Do not treat this review as funding, vendor, hiring, or risk approval.",
                "",
            ]
        )

    lines.extend(
        [
            "## Govern And Assure Themes",
            "",
            "- Use approved data sources and source citations.",
            "- Maintain searchable logs for agent outputs and human decisions.",
            "- Define human review queues before any external communication or irreversible action.",
            "- Use eval examples and stop conditions before scale decisions.",
            "- Require security, legal, architecture, procurement, or finance review when risk flags indicate.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    # Lightweight Markdown-ish renderer for the sample pack.
    body: list[str] = []
    in_table = False
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("|") and line.endswith("|"):
            cells = [html.escape(cell.strip()) for cell in line.strip("|").split("|")]
            if set(cells[0]) <= {"-", ":"}:
                continue
            if not in_table:
                body.append("<table>")
                in_table = True
            tag = "th" if all(c.lower() in {"id", "opportunity", "work shape", "route", "rationale", "next step", "layer", "decomposition", "dimension", "score"} for c in cells) else "td"
            body.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
            continue
        if in_table:
            body.append("</table>")
            in_table = False
        if line.startswith("# "):
            body.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            body.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("#### "):
            body.append(f"<h4>{html.escape(line[5:])}</h4>")
        elif line.startswith("- "):
            body.append(f"<p>&bull; {html.escape(line[2:])}</p>")
        elif line:
            body.append(f"<p>{html.escape(line)}</p>")
    if in_table:
        body.append("</table>")
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Opportunity Intelligence Review Pack</title>
<style>
body { font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; color: #1f2937; }
h1, h2, h3 { color: #111827; }
table { border-collapse: collapse; width: 100%; margin: 16px 0 24px; font-size: 14px; }
th, td { border: 1px solid #d1d5db; padding: 8px; vertical-align: top; }
th { background: #f3f4f6; text-align: left; }
p { max-width: 980px; }
</style>
</head>
<body>
""" + "\n".join(body) + "\n</body>\n</html>\n"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def analyze(rows: list[dict[str, str]]) -> list[dict]:
    output = []
    for row in rows:
        scores = score_row(row)
        route, rationale, next_step = recommend_route(row, scores)
        output.append(
            {
                "id": row["id"],
                "name": row["name"],
                "sponsor": row["sponsor"],
                "work_shape": classify_work_shape(row),
                "route": route,
                "rationale": rationale,
                "next_step": next_step,
                "scores": scores,
                "stack": decompose_stack(row),
                "risk_level": row["risk_level"],
                "data_readiness": row["data_readiness"],
            }
        )
    return output


def write_logs(analyses: list[dict], output_dir: Path) -> None:
    csv_path = output_dir / "findings_log.csv"
    jsonl_path = output_dir / "findings_log.jsonl"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["id", "name", "work_shape", "route", "rationale", "next_step", "risk_level", "data_readiness"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in analyses:
            writer.writerow({key: item[key] for key in fieldnames})
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for item in analyses:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Decompose and review synthetic AI opportunities.")
    parser.add_argument("--input", required=True, type=Path, help="Input CSV path")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory")
    args = parser.parse_args()

    rows = load_rows(args.input)
    analyses = analyze(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    markdown = render_markdown(rows, analyses)
    (args.output_dir / "ai_opportunity_intelligence_review_pack.md").write_text(markdown, encoding="utf-8")
    (args.output_dir / "ai_opportunity_intelligence_review_pack.html").write_text(render_html(markdown), encoding="utf-8")
    write_logs(analyses, args.output_dir)

    print(f"Reviewed {len(rows)} opportunities")
    print(f"Generated outputs in {args.output_dir}")


if __name__ == "__main__":
    main()
