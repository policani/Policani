#!/usr/bin/env python3
"""Build sample governance outputs for the Portfolio Governance Operations Log.

This tool is intentionally small, inspectable, and standard-library only.
It uses transparent rule-based classification against synthetic data.
"""

from __future__ import annotations

import csv
import html
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

RUN_DATE = date(2026, 5, 24)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "examples" / "sample-data"
OUT = ROOT / "examples" / "sample-outputs"
OUT_MD = OUT
OUT_HTML = OUT

REQUIRED_COLUMNS = {
    "synthetic_worklog_entries.csv": [
        "entry_id",
        "date",
        "source",
        "initiative",
        "raw_note",
        "reported_by",
        "owner",
        "due_date",
        "status",
        "prior_period_note",
    ],
    "synthetic_previous_action_register.csv": [
        "action_id",
        "initiative",
        "action",
        "owner",
        "due_date",
        "status",
        "source",
        "notes",
    ],
    "synthetic_previous_decision_log.csv": [
        "decision_id",
        "date",
        "initiative",
        "decision",
        "decision_owner",
        "status",
        "notes",
    ],
    "synthetic_project_snapshot.csv": [
        "initiative",
        "sponsor",
        "initiative_owner",
        "status",
        "next_milestone",
        "milestone_date",
        "key_dependency",
        "governance_note",
    ],
    "synthetic_stakeholder_roster.csv": [
        "name",
        "role",
        "primary_initiative",
        "follow_up_preference",
    ],
    "synthetic_governance_calendar.csv": [
        "event_id",
        "date",
        "time",
        "meeting",
        "audience",
        "status",
        "notes",
    ],
}


@dataclass
class ClassifiedEntry:
    entry: Dict[str, str]
    primary_category: str
    tags: List[str]
    urgency: str
    action_needed: str
    missing_fields: List[str]
    confidence: str


def read_csv(name: str) -> List[Dict[str, str]]:
    path = DATA / name
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_csv(name: str) -> None:
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
    missing = [c for c in REQUIRED_COLUMNS[name] if c not in columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {', '.join(missing)}")


def parse_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def contains(text: str, *terms: str) -> bool:
    text = text.lower()
    return any(term.lower() in text for term in terms)


def classify_entry(entry: Dict[str, str]) -> ClassifiedEntry:
    note = entry["raw_note"]
    note_l = note.lower()
    status = entry.get("status", "").lower()
    tags: List[str] = []
    missing: List[str] = []

    if not entry.get("owner", "").strip():
        missing.append("owner")
    if not entry.get("due_date", "").strip() and contains(note, "action", "risk", "decision", "follow-up", "follow up", "confirm"):
        missing.append("due_date")

    if contains(note, "decision"):
        tags.append("decision needed")
        if not contains(note, "option", "tradeoff", "trade-off"):
            tags.append("decision options unclear")
            missing.append("options/tradeoffs")
    if contains(note, "action:", "action "):
        tags.append("action item")
    if contains(note, "follow-up", "follow up", "follow-up meeting", "schedule", "missed", "did not confirm", "needs owner confirmation"):
        tags.append("follow-up required")
    if contains(note, "risk"):
        tags.append("risk")
        if not contains(note, "mitigation", "mitigate", "response plan"):
            tags.append("risk missing mitigation")
            missing.append("mitigation")
    if contains(note, "blocked", "blocker", "blocked by", "waiting on", "remains blocked"):
        tags.append("blocker")
    if contains(note, "dependency", "depends on", "readiness", "api readiness"):
        tags.append("dependency")
    if contains(note, "executive air support", "air support", "sponsor decision", "executive support", "priority conflict", "prioritization conflict"):
        tags.append("executive air-support request")
    if contains(note, "rescheduled", "moved to", "unavailable", "calendar", "session moved"):
        tags.append("scheduling / rescheduling need")
    if contains(note, "milestone", "date moved", "moves from", "move from", "plan update", "project plan", "date change"):
        tags.append("project-plan update")
    if contains(note, "no status", "missing", "no update", "not received"):
        tags.append("missing status")
    if contains(note, "carry-forward", "carry forward"):
        tags.append("carry-forward item")
    if status == "green" and contains(note, "no evidence", "same wording", "not attached", "cannot confirm", "no concerns"):
        tags.append("weak green status")
    if entry.get("prior_period_note", "").strip() and entry.get("prior_period_note", "").lower() in note_l:
        tags.append("stale update")
    due = parse_date(entry.get("due_date", ""))
    if due and due < RUN_DATE and contains(note, "missed", "overdue", "not received", "confirm", "provide", "action", "due"):
        tags.append("overdue or aging action")
    if contains(note, "no milestone evidence", "not attached", "cannot confirm", "unknown", "unclear", "not yet written down", "not stated", "not explicitly accepted"):
        tags.append("weak signal")
    if contains(note, "requested help", "two working sessions", "not aligned"):
        tags.append("escalation candidate")

    if not tags:
        tags.append("routine status")

    primary = choose_primary(tags)
    urgency = choose_urgency(tags, status, due)
    action_needed = build_action_needed(entry, primary, tags, missing)
    # De-duplicate while preserving order
    tags = list(dict.fromkeys(tags))
    missing = list(dict.fromkeys(missing))
    confidence = "High" if primary != "Routine status" and "weak signal" not in tags else "Medium"
    if "owner" in missing or "options/tradeoffs" in missing:
        confidence = "Medium"
    return ClassifiedEntry(entry, primary, tags, urgency, action_needed, missing, confidence)


def choose_primary(tags: List[str]) -> str:
    priority = [
        ("executive air-support request", "Executive air-support request"),
        ("blocker", "Blocker"),
        ("decision needed", "Decision needed"),
        ("risk", "Risk"),
        ("missing status", "Missing status"),
        ("stale update", "Stale update"),
        ("weak green status", "Weak signal"),
        ("project-plan update", "Project-plan update"),
        ("scheduling / rescheduling need", "Scheduling / rescheduling need"),
        ("follow-up required", "Follow-up required"),
        ("action item", "Action item"),
        ("carry-forward item", "Carry-forward item"),
        ("escalation candidate", "Escalation candidate"),
        ("dependency", "Dependency"),
        ("overdue or aging action", "Follow-up required"),
    ]
    tagset = set(tags)
    for raw, label in priority:
        if raw in tagset:
            return label
    return "Routine status"


def choose_urgency(tags: List[str], status: str, due: date | None) -> str:
    tagset = set(tags)
    if "executive air-support request" in tagset or "blocker" in tagset:
        return "High"
    if "overdue or aging action" in tagset or "missing status" in tagset:
        return "High"
    if status.lower() == "red":
        return "High"
    if due and due <= RUN_DATE:
        return "Medium"
    if "decision needed" in tagset or "risk" in tagset or "project-plan update" in tagset:
        return "Medium"
    return "Low"


def build_action_needed(entry: Dict[str, str], primary: str, tags: List[str], missing: List[str]) -> str:
    owner = entry.get("owner") or "accountable owner"
    if primary == "Executive air-support request":
        return "Prepare concise executive air-support brief; confirm requested executive action and decision owner."
    if primary == "Blocker":
        return "Confirm dependency owner, impact, mitigation path, and whether escalation is needed."
    if primary == "Decision needed":
        return "Document options, tradeoffs, decision owner, and needed-by date before governance review."
    if primary == "Risk":
        return "Add mitigation owner and response plan; confirm whether risk should enter RAID log."
    if primary == "Missing status":
        return "Request missing update and confirm owner, due date, and impact on upcoming decision."
    if primary == "Stale update":
        return "Challenge repeated status; request current milestone evidence."
    if primary == "Weak signal":
        return "Request evidence, milestone status, or clarification before using in executive summary."
    if primary == "Project-plan update":
        return "Confirm date or milestone change with owner before updating project plan."
    if primary == "Escalation candidate":
        return "Confirm whether peer-level resolution is blocked and define the executive ask if needed."
    if primary == "Dependency":
        return "Confirm accountable parties, dependency date, and downstream impact."
    if primary == "Scheduling / rescheduling need":
        return "Confirm attendee availability, pre-read timing, and revised calendar details."
    if primary == "Follow-up required":
        return f"Send targeted follow-up to {owner}; confirm next step and due date."
    if primary == "Action item":
        return f"Add or update action register entry for {owner}; confirm due date if missing."
    if primary == "Carry-forward item":
        return "Carry into next governance agenda unless resolved before meeting."
    if missing:
        return "Clarify missing fields before summarizing."
    return "Include as routine status by exception only."


def md_table(headers: List[str], rows: Iterable[Iterable[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(escape_md(str(c)) for c in row) + " |")
    return "\n".join(out)


def escape_md(value: str) -> str:
    value = value.replace("\n", " ").strip()
    return value.replace("|", "\\|")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def simple_markdown_to_html(title: str, markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    body: List[str] = []
    in_ul = False
    in_table = False
    table_rows: List[str] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            body.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table, table_rows
        if in_table:
            body.append("<table>")
            for i, row in enumerate(table_rows):
                cells = [c.strip() for c in row.strip("|").split("|")]
                if i == 1 and all(set(c) <= {"-", ":"} for c in cells):
                    continue
                tag = "th" if i == 0 else "td"
                body.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>")
            body.append("</table>")
            in_table = False
            table_rows = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            close_ul()
            in_table = True
            table_rows.append(stripped)
            continue
        else:
            close_table()

        if not stripped:
            close_ul()
            continue
        if stripped.startswith("# "):
            close_ul()
            body.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_ul()
            body.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_ul()
            body.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{html.escape(stripped[2:])}</li>")
        elif re.match(r"^\d+\.\s", stripped):
            close_ul()
            body.append(f"<p>{html.escape(stripped)}</p>")
        else:
            close_ul()
            body.append(f"<p>{html.escape(stripped)}</p>")
    close_table()
    close_ul()
    css = """
    <style>
    body { font-family: Arial, Helvetica, sans-serif; color: #1f2937; line-height: 1.55; margin: 0; }
    main { max-width: 1100px; margin: 0 auto; padding: 36px 28px 56px; }
    h1 { margin-top: 0; }
    h2 { border-top: 1px solid #d1d5db; padding-top: 1rem; margin-top: 1.8rem; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }
    th, td { border: 1px solid #d1d5db; padding: 0.55rem; vertical-align: top; text-align: left; }
    th { background: #f9fafb; }
    ul { padding-left: 1.4rem; }
    footer { margin-top: 2rem; color: #4b5563; font-size: 0.9rem; }
    </style>
    """
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{css}
</head>
<body>
<main>
{chr(10).join(body)}
<footer>Synthetic sample output. Recommendations require human review and confirmation.</footer>
</main>
</body>
</html>
"""


def grouped(entries: List[ClassifiedEntry], key_func) -> Dict[str, List[ClassifiedEntry]]:
    result: Dict[str, List[ClassifiedEntry]] = defaultdict(list)
    for item in entries:
        result[key_func(item)].append(item)
    return dict(result)


def generate_classified_worklog(classified: List[ClassifiedEntry]) -> str:
    rows = []
    for item in classified:
        e = item.entry
        rows.append([
            e["entry_id"],
            e["date"],
            e["initiative"],
            item.primary_category,
            ", ".join(item.tags),
            e.get("owner") or "MISSING",
            e.get("due_date") or "MISSING",
            item.urgency,
            item.action_needed,
            ", ".join(item.missing_fields) or "none",
            item.confidence,
        ])
    return "# Classified Worklog\n\n" + md_table(
        ["ID","Date","Initiative","Primary category","Tags","Owner","Due date","Urgency","Action needed","Missing fields","Confidence"],
        rows,
    )


def generate_weekly_summary(classified: List[ClassifiedEntry], actions: List[Dict[str, str]], decisions: List[Dict[str, str]]) -> str:
    high = [c for c in classified if c.urgency == "High"]
    decisions_needed = [c for c in classified if "decision needed" in c.tags]
    escalations = [c for c in classified if "executive air-support request" in c.tags or "escalation candidate" in c.tags]
    weak = [c for c in classified if any(t in c.tags for t in ["weak signal","weak green status","stale update","missing status"])]
    overdue = [c for c in classified if "overdue or aging action" in c.tags]
    carry = [c for c in classified if "carry-forward item" in c.tags]

    parts = ["# Weekly Governance Summary"]
    parts.append("## Executive summary")
    parts.append(
        "The week’s governance signals point to one material cross-initiative dependency: Customer Portal Modernization remains constrained by Data Platform API readiness and prioritization conflict. Regulatory Reporting Remediation needs a clearer decision path for possible scope deferral, while Field Operations Workflow Automation has overdue adoption-readiness input and Data Platform Stabilization has green status that is not yet well supported by evidence."
    )
    parts.append("## Top governance concerns")
    parts.append(md_table(["Concern","Initiative","Owner","Action needed"], [
        [c.primary_category, c.entry["initiative"], c.entry.get("owner") or "MISSING", c.action_needed] for c in high
    ]))
    parts.append("## Decisions needed")
    parts.append(md_table(["Entry","Initiative","Decision signal","Missing information"], [
        [c.entry["entry_id"], c.entry["initiative"], c.entry["raw_note"], ", ".join(c.missing_fields) or "none"] for c in decisions_needed
    ]))
    parts.append("## Escalations")
    parts.append(md_table(["Entry","Initiative","Escalation signal","Recommended preparation"], [
        [c.entry["entry_id"], c.entry["initiative"], c.entry["raw_note"], c.action_needed] for c in escalations
    ]))
    parts.append("## Overdue actions and missing updates")
    parts.append(md_table(["Entry","Initiative","Owner","Due date","Issue"], [
        [c.entry["entry_id"], c.entry["initiative"], c.entry.get("owner") or "MISSING", c.entry.get("due_date") or "MISSING", c.entry["raw_note"]] for c in overdue + [x for x in weak if "missing status" in x.tags]
    ]))
    parts.append("## Weak or stale signals")
    parts.append(md_table(["Entry","Initiative","Signal","Follow-up"], [
        [c.entry["entry_id"], c.entry["initiative"], ", ".join(c.tags), c.action_needed] for c in weak
    ]))
    parts.append("## Carry-forward items")
    if carry:
        parts.extend([f"- {c.entry['entry_id']} — {c.entry['initiative']}: {c.entry['raw_note']}" for c in carry])
    else:
        parts.append("- No carry-forward items detected.")
    return "\n\n".join(parts)


def generate_meeting_agenda(classified: List[ClassifiedEntry]) -> str:
    return """# Governance Meeting Agenda

**Duration:** 60 minutes  
**Purpose:** Move the fictional portfolio from scattered updates to decisions, accountable actions, confirmed escalations, and next-cycle follow-through.

| Time | Topic | Owner | Outcome needed |
|---:|---|---|---|
| 0-5 | Open and meeting objective | PMO Lead | Confirm exception-based governance focus |
| 5-10 | Portfolio signal review | PMO Lead | Confirm top concerns and changes since prior cycle |
| 10-22 | Customer Portal / Data Platform blocker | Alex Rivera / Priya Shah | Confirm dependency path, owner, and whether executive air support is required |
| 22-32 | Regulatory Reporting scope deferral decision path | Riley Chen / Morgan Lee | Confirm options, tradeoffs, and decision owner |
| 32-42 | Field Operations adoption readiness | Taylor Brooks / Jordan Kim | Confirm overdue update, change-management risk, and follow-up meeting |
| 42-50 | Data Platform green-status evidence | Priya Shah / Noah Grant | Confirm milestone evidence, defect status, and plan-date implications |
| 50-56 | Action register and stakeholder follow-ups | PMO Lead | Confirm owners and due dates |
| 56-60 | Closeout | PMO Lead | Restate decisions, actions, unresolved items, and carry-forward topics |
"""


def generate_facilitator_guide(classified: List[ClassifiedEntry]) -> str:
    return """# Facilitator Guide

## Opening script

“Today’s goal is not to read status. Routine green items will be handled by exception. We need to confirm decisions, blockers, ownership, escalation asks, and follow-through before the next cycle.”

## Facilitation moves

### Customer Portal / Data Platform blocker

- Ask Alex: “What Portal work can continue without API readiness?”
- Ask Priya: “What evidence supports the revised API readiness date?”
- Ask both owners: “What did the two working sessions resolve, and what remains unresolved?”
- Ask Morgan: “If priorities conflict, what executive alignment is needed by Tuesday?”

### Regulatory Reporting Remediation

- Ask Riley: “What are the specific scope deferral options?”
- Ask Morgan: “Who owns the deferral decision, and what information is required?”
- Ask Sam: “Who owns reconciliation for the exception file?”

### Field Operations Workflow Automation

- Ask Jordan: “What is the current readiness status by region?”
- Ask Taylor: “What risk response is needed if supervisor signoff remains missing?”
- Confirm whether a focused regional follow-up meeting is required.

### Data Platform Stabilization

- Ask Priya: “What milestone evidence supports green status?”
- Ask Noah: “Can stabilization work and Portal API readiness proceed in parallel?”
- Confirm whether the API readiness milestone change should be reflected as a plan-update recommendation.

## Parking lot

Use the parking lot for items that are important but not decision-relevant in this meeting:

- implementation detail;
- status narration without decision impact;
- future enhancement requests;
- items lacking a clear owner.

## Closeout script

“Before we close, I will read back the decisions explicitly made, actions with owners and due dates, follow-up meetings to schedule, unresolved items, and carry-forward topics. Please correct anything now before I publish the closeout summary.”
"""


def generate_stakeholder_follow_up(classified: List[ClassifiedEntry], roster: List[Dict[str, str]]) -> str:
    by_owner = grouped([c for c in classified if c.urgency in ("High", "Medium")], lambda c: c.entry.get("owner") or "Unassigned")
    rows = []
    for owner, items in sorted(by_owner.items()):
        for c in items:
            rows.append([
                owner,
                c.entry["initiative"],
                c.urgency,
                c.action_needed,
                draft_followup(owner, c),
            ])
    return "# Stakeholder Follow-Up Plan\n\n" + md_table(
        ["Stakeholder","Initiative","Priority","Follow-up needed","Draft message"],
        rows
    )


def draft_followup(owner: str, c: ClassifiedEntry) -> str:
    owner_name = owner if owner != "Unassigned" else "team"
    return (
        f"Hi {owner_name} — I am preparing the portfolio governance review. "
        f"For {c.entry['initiative']}, please confirm: {c.action_needed} "
        f"Source note: {c.entry['entry_id']}. If any owner, due date, or decision input is missing, please provide it before the meeting."
    )


def generate_air_support_brief(classified: List[ClassifiedEntry]) -> str:
    relevant = [c for c in classified if c.entry["initiative"] == "Customer Portal Modernization" and (c.urgency == "High" or "executive air-support request" in c.tags)]
    return """# Executive Air-Support Brief — Customer Portal / Data Platform Dependency

## Situation

Customer Portal Modernization remains blocked by Data Platform API readiness. The Data Platform team is also managing stabilization work, and the prioritization conflict has not been resolved after two working sessions.

## Affected initiatives

- Customer Portal Modernization
- Data Platform Stabilization

## Business or delivery impact

The immediate delivery impact is uncertainty around the Customer Portal beta integration path. Design QA can continue, but integration testing cannot start until API readiness is confirmed or an alternate beta path is approved.

## Prior resolution attempts

- Alex Rivera and Priya Shah completed two working sessions.
- The dependency path from the prior governance meeting remains open.
- Architecture support has been requested to determine whether stabilization and API readiness work can proceed in parallel.

## Options requiring human decision

| Option | Tradeoff | Confirmation needed |
|---|---|---|
| Hold beta date until API readiness is confirmed | Preserves integrated path but may create schedule pressure | Confirm revised API readiness date |
| Split beta scope and proceed with mock service path | May protect beta learning but could defer integration validation | Confirm scope, quality risk, and sponsor tolerance |
| Executive priority alignment between Portal and Platform work | Clarifies resource focus but may affect stabilization sequencing | Sponsor decision and owner confirmation |

## Requested executive action

Confirm the priority path between Customer Portal beta readiness and Data Platform stabilization, including whether to hold the beta date, split beta scope, or direct a specific dependency resolution path.

## Risk of no action

The teams may continue parallel work without a shared dependency decision, increasing the likelihood of missed integration timing, repeated working sessions, and unclear sponsor expectations.

## Owner and due date

- Recommended decision owner: Morgan Lee
- Needed by: 2026-05-26
- PMO support: Casey Morgan to prepare decision readout and capture explicit decision outcome
"""


def generate_project_plan_updates(classified: List[ClassifiedEntry]) -> str:
    candidates = [c for c in classified if any(t in c.tags for t in ["project-plan update","dependency","blocker","risk","missing status"])]
    rows = []
    for c in candidates:
        plan_area = "Dependency / RAID"
        if "project-plan update" in c.tags:
            plan_area = "Milestone / schedule"
        elif "risk" in c.tags:
            plan_area = "RAID risk"
        elif "missing status" in c.tags:
            plan_area = "Action register"
        rows.append([
            c.entry["initiative"],
            plan_area,
            c.action_needed,
            c.entry["raw_note"],
            ", ".join(c.missing_fields) or "Owner confirmation",
        ])
    return "# Project Plan Update Recommendations\n\n## Updates requiring human confirmation\n\n" + md_table(
        ["Initiative","Plan area","Recommended update","Evidence","Confirmation needed"],
        rows
    ) + "\n\n## Explicit boundary\n\nThese are recommended updates only. The tool does not modify a real project plan, change dates, reassign owners, approve scope, or accept risk."


def generate_post_meeting_closeout(classified: List[ClassifiedEntry]) -> str:
    actions = [c for c in classified if c.urgency in ("High", "Medium")]
    return """# Post-Meeting Closeout Summary

## Decisions explicitly made

No final decisions are recorded in the synthetic worklog. Decision candidates remain open until a human owner provides an explicit decision.

## Decision candidates to carry forward

| Initiative | Decision candidate | Owner to confirm | Needed by |
|---|---|---|---|
| Customer Portal Modernization | Hold beta date, split beta scope, or confirm dependency resolution path | Morgan Lee | 2026-05-26 |
| Regulatory Reporting Remediation | Decide whether low-volume report variants can be deferred | Morgan Lee | 2026-05-24 |

## Action register updates

| Action | Owner | Due date | Source |
|---|---|---|---|
| Provide evidence for Data Platform green status and API readiness milestone | Priya Shah | 2026-05-22 | WL-002 / WL-013 |
| Confirm Portal dependency path and escalation ask | Alex Rivera / Priya Shah | 2026-05-22 | WL-003 / WL-009 / WL-016 |
| Provide change champion roster and regional readiness status | Jordan Kim | Needs confirmation | WL-015 |
| Confirm exception-file reconciliation owner | Sam Patel / Riley Chen | 2026-05-23 | WL-018 |
| Schedule regional operations and change champion follow-up meeting | Casey Morgan | 2026-05-23 | WL-011 |

## Follow-up meetings to schedule

| Meeting | Required attendees | Purpose | Target |
|---|---|---|---|
| Portal / Data Platform dependency working session | Alex Rivera, Priya Shah, Noah Grant, Casey Morgan | Confirm API readiness path and whether stabilization can run in parallel | 2026-05-24 |
| Field Operations adoption readiness review | Taylor Brooks, Jordan Kim, regional operations leads | Confirm adoption blockers and supervisor signoff path | Before next governance cycle |

## Unresolved items

- Data validation lead status and reconciliation ownership remain incomplete.
- Data Platform green status needs milestone evidence.
- Field Operations change-management risk lacks a mitigation plan.
- Regulatory Reporting deferral decision lacks documented options and tradeoffs.

## Next-cycle worklog seed

- Carry forward Customer Portal beta dependency decision.
- Carry forward Regulatory Reporting scope deferral decision path.
- Track evidence requested for Data Platform readiness.
- Track Field Operations readiness owner response and follow-up meeting outcome.
"""


def generate_signal_quality_review(classified: List[ClassifiedEntry]) -> str:
    weak = [c for c in classified if any(t in c.tags for t in ["weak signal","weak green status","stale update","risk missing mitigation","decision options unclear","missing status"])]
    rows = []
    for c in weak:
        rows.append([
            c.entry["entry_id"],
            c.entry["initiative"],
            ", ".join(c.tags),
            c.entry["raw_note"],
            c.action_needed,
            ", ".join(c.missing_fields) or "none",
        ])
    return "# Signal Quality Review\n\n## Weak, stale, or incomplete signals\n\n" + md_table(
        ["Entry","Initiative","Signal issue","Raw note","Recommended clarification","Missing fields"],
        rows
    ) + "\n\n## Senior PMO observations\n\n- The Customer Portal dependency is a real governance issue because it crosses initiative boundaries and appears unresolved after peer-level working sessions.\n- Data Platform green status should not be accepted into the executive summary without evidence.\n- Regulatory Reporting has a decision request but not a decision package.\n- Field Operations has overdue adoption-readiness input and a risk without mitigation; both need ownership discipline before the next cycle."


def write_findings(classified: List[ClassifiedEntry]) -> None:
    csv_path = OUT / "findings_log.csv"
    jsonl_path = OUT / "findings_log.jsonl"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["entry_id","initiative","primary_category","tags","urgency","missing_fields","action_needed"])
        for c in classified:
            writer.writerow([
                c.entry["entry_id"],
                c.entry["initiative"],
                c.primary_category,
                "; ".join(c.tags),
                c.urgency,
                "; ".join(c.missing_fields),
                c.action_needed,
            ])
    with jsonl_path.open("w", encoding="utf-8") as f:
        for c in classified:
            f.write(json.dumps({
                "entry_id": c.entry["entry_id"],
                "initiative": c.entry["initiative"],
                "primary_category": c.primary_category,
                "tags": c.tags,
                "urgency": c.urgency,
                "missing_fields": c.missing_fields,
                "action_needed": c.action_needed,
            }, ensure_ascii=False) + "\n")


def main() -> int:
    for name in REQUIRED_COLUMNS:
        validate_csv(name)

    worklog = read_csv("synthetic_worklog_entries.csv")
    actions = read_csv("synthetic_previous_action_register.csv")
    decisions = read_csv("synthetic_previous_decision_log.csv")
    roster = read_csv("synthetic_stakeholder_roster.csv")
    classified = [classify_entry(row) for row in worklog]

    outputs = {
        "classified_worklog.md": generate_classified_worklog(classified),
        "weekly_governance_summary.md": generate_weekly_summary(classified, actions, decisions),
        "meeting_agenda.md": generate_meeting_agenda(classified),
        "facilitator_guide.md": generate_facilitator_guide(classified),
        "stakeholder_follow_up_plan.md": generate_stakeholder_follow_up(classified, roster),
        "executive_air_support_brief.md": generate_air_support_brief(classified),
        "project_plan_update_recommendations.md": generate_project_plan_updates(classified),
        "post_meeting_closeout_summary.md": generate_post_meeting_closeout(classified),
        "signal_quality_review.md": generate_signal_quality_review(classified),
    }

    pack_parts = [
        "# Portfolio Governance Operations Log — Consolidated Sample Output Pack",
        "",
        "This file is generated from synthetic sample data by `tools/build_governance_outputs.py`. It consolidates the generated outputs into one GitHub-friendly artifact to keep the repository lean.",
        "",
    ]
    for filename, content in outputs.items():
        title = filename.replace("_", " ").replace(".md", "").title()
        pack_parts.append(f"---\n\n# {title}")
        body = content.split("\n", 1)[1] if content.startswith("# ") and "\n" in content else content
        pack_parts.append(body.strip())
        pack_parts.append("")

    consolidated = "\n".join(pack_parts).rstrip() + "\n"
    write(OUT / "sample_output_pack.md", consolidated)
    write(OUT / "sample-output-pack.html", simple_markdown_to_html("Portfolio Governance Operations Log — Sample Output Pack", consolidated))

    write_findings(classified)
    print(f"Generated consolidated Markdown/HTML output pack with {len(outputs)} sections.")
    print(f"Findings logs written to {OUT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
