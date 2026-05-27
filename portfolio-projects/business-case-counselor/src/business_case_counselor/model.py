from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


@dataclass
class Option:
    name: str
    description: str = ""
    advantages: list[str] = field(default_factory=list)
    disadvantages: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Option":
        return cls(
            name=str(data.get("name", "Option")),
            description=str(data.get("description", "")),
            advantages=[str(x) for x in _list(data.get("advantages"))],
            disadvantages=[str(x) for x in _list(data.get("disadvantages"))],
            notes=str(data.get("notes", "")),
        )


@dataclass
class BusinessCase:
    title: str = "Untitled Business Case"
    decision_needed: str = ""
    decision_owner: str = ""
    requested_action: str = ""
    decision_timing: str = ""
    problem_statement: str = ""
    strategic_alignment: str = ""
    current_state: str = ""
    gap_analysis: str = ""
    desired_future_state: str = ""
    stakeholders: list[str] = field(default_factory=list)
    scope_in: list[str] = field(default_factory=list)
    scope_out: list[str] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)
    recommended_solution: str = ""
    benefits: list[dict[str, Any]] = field(default_factory=list)
    costs: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[dict[str, Any]] = field(default_factory=list)
    implementation_milestones: list[dict[str, Any]] = field(default_factory=list)
    governance: str = ""
    success_measures: list[dict[str, Any]] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BusinessCase":
        options = [Option.from_dict(x) for x in data.get("options", [])]
        if not any(o.name.lower().strip() == "do nothing" for o in options):
            options.insert(0, Option(name="Do nothing", description="Maintain the current state."))
        return cls(
            title=str(data.get("title") or "Untitled Business Case"),
            decision_needed=str(data.get("decision_needed", "")),
            decision_owner=str(data.get("decision_owner", "")),
            requested_action=str(data.get("requested_action", "")),
            decision_timing=str(data.get("decision_timing", "")),
            problem_statement=str(data.get("problem_statement", "")),
            strategic_alignment=str(data.get("strategic_alignment", "")),
            current_state=str(data.get("current_state", "")),
            gap_analysis=str(data.get("gap_analysis", "")),
            desired_future_state=str(data.get("desired_future_state", "")),
            stakeholders=[str(x) for x in _list(data.get("stakeholders"))],
            scope_in=[str(x) for x in _list(data.get("scope_in"))],
            scope_out=[str(x) for x in _list(data.get("scope_out"))],
            options=options,
            recommended_solution=str(data.get("recommended_solution", "")),
            benefits=[dict(x) for x in _list(data.get("benefits")) if isinstance(x, dict)],
            costs=[dict(x) for x in _list(data.get("costs")) if isinstance(x, dict)],
            risks=[dict(x) for x in _list(data.get("risks")) if isinstance(x, dict)],
            assumptions=[dict(x) for x in _list(data.get("assumptions")) if isinstance(x, dict)],
            constraints=[dict(x) for x in _list(data.get("constraints")) if isinstance(x, dict)],
            implementation_milestones=[dict(x) for x in _list(data.get("implementation_milestones")) if isinstance(x, dict)],
            governance=str(data.get("governance", "")),
            success_measures=[dict(x) for x in _list(data.get("success_measures")) if isinstance(x, dict)],
            next_steps=[str(x) for x in _list(data.get("next_steps"))],
            open_questions=[str(x) for x in _list(data.get("open_questions"))],
        )
