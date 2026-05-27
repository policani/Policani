from __future__ import annotations

import json
from pathlib import Path

QUESTIONS = [
    ("title", "Business case title"),
    ("decision_needed", "What decision do you need leadership to make?"),
    ("decision_owner", "Who is the decision owner or approving body?"),
    ("requested_action", "What action are you requesting: approve funding, approve discovery, prioritize, change scope, defer, or reject?"),
    ("decision_timing", "When is the decision needed?"),
    ("problem_statement", "What problem or opportunity is being addressed?"),
    ("strategic_alignment", "What strategic objective does this support?"),
    ("current_state", "What is happening in the current state?"),
    ("gap_analysis", "What gap exists between current state and desired future state?"),
    ("desired_future_state", "What future state should exist if the case is approved?"),
    ("recommended_solution", "What path do you currently recommend, if any?"),
    ("governance", "How should progress and value be governed after approval?"),
]

LIST_QUESTIONS = [
    ("stakeholders", "List key stakeholders, comma-separated"),
    ("scope_in", "List what is in scope, comma-separated"),
    ("scope_out", "List what is out of scope, comma-separated"),
    ("next_steps", "List immediate next steps, comma-separated"),
    ("open_questions", "List open questions, comma-separated"),
]


def run_interview(out_path: Path) -> None:
    data: dict = {}
    print("Business Case Counselor Interview")
    print("Press Enter to skip unknown answers. Unknowns can be matured later.\n")
    for key, question in QUESTIONS:
        data[key] = input(f"{question}\n> ").strip()
    for key, question in LIST_QUESTIONS:
        raw = input(f"{question}\n> ").strip()
        data[key] = [x.strip() for x in raw.split(",") if x.strip()]

    data["options"] = [
        {"name": "Do nothing", "description": input("Describe the do-nothing option\n> ").strip(), "advantages": [], "disadvantages": [], "notes": ""},
        {"name": "Option A", "description": input("Describe Option A\n> ").strip(), "advantages": [], "disadvantages": [], "notes": ""},
        {"name": "Option B", "description": input("Describe Option B\n> ").strip(), "advantages": [], "disadvantages": [], "notes": ""},
    ]
    data.setdefault("benefits", [])
    data.setdefault("costs", [])
    data.setdefault("risks", [])
    data.setdefault("assumptions", [])
    data.setdefault("constraints", [])
    data.setdefault("implementation_milestones", [])
    data.setdefault("success_measures", [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")
