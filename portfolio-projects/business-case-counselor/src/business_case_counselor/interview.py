from __future__ import annotations

import json
from pathlib import Path

QUESTIONS = [
    ("title", "Business case title"),
    ("problem_statement", "What observable business problem or opportunity triggered this?"),
    ("root_cause_hypothesis", "What is your working root-cause hypothesis?"),
    ("root_cause_challenge", "What evidence suggests this is the root cause rather than a symptom?"),
    ("status_quo_impact", "What is the quantified or directional cost of inaction?"),
    ("decision_owner", "Who has authority to approve, fund, or prioritize this?"),
    ("requested_action", "What specific approval or decision are you requesting?"),
    ("decision_timing", "When is the decision needed and why?"),
    ("consequence_of_delay", "What happens if the decision is delayed?"),
    ("audience_profile", "Who is the primary audience: CFO, CEO, operational leader, technology leader, interview panel, or multi-audience?"),
]

LIST_QUESTIONS = [
    ("observable_symptoms", "List observable symptoms, comma-separated"),
    ("stakeholders", "List key stakeholders, comma-separated"),
    ("scope_in", "List what is in scope, comma-separated"),
    ("scope_out", "List what is out of scope, comma-separated"),
    ("dependencies", "List key dependencies, comma-separated"),
    ("next_steps", "List immediate next steps if approved, comma-separated"),
    ("open_questions", "List remaining open questions, comma-separated"),
]


def run_interview(out_path: Path) -> None:
    data: dict = {"version": "Draft", "classification": "Internal"}
    print("Business Case Counselor Interview")
    print("Press Enter to skip unknown answers. Unknowns can be matured later.\n")
    for key, question in QUESTIONS:
        data[key] = input(f"{question}\n> ").strip()
    for key, question in LIST_QUESTIONS:
        raw = input(f"{question}\n> ").strip()
        data[key] = [x.strip() for x in raw.split(",") if x.strip()]

    data.setdefault("strategic_alignment", [])
    data.setdefault("baseline_metrics", [])
    data.setdefault("evaluation_criteria", [])
    data.setdefault("options", [{"name":"Option 0: Do Nothing", "description":"Maintain current state."}])
    data.setdefault("benefits", [])
    data.setdefault("costs", [])
    data.setdefault("financial_summary", {})
    data.setdefault("risks", [])
    data.setdefault("assumptions", [])
    data.setdefault("constraints", [])
    data.setdefault("implementation_milestones", [])
    data.setdefault("success_measures", [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")
