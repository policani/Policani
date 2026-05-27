from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [dict(x) for x in _list(value) if isinstance(x, dict)]


@dataclass
class Option:
    name: str
    description: str = ""
    cost: str = ""
    timeline: str = ""
    benefits: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    score: str = ""
    rationale: str = ""
    advantages: list[str] = field(default_factory=list)  # backwards compatibility
    disadvantages: list[str] = field(default_factory=list)  # backwards compatibility
    notes: str = ""  # backwards compatibility

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Option":
        tradeoffs = [str(x) for x in _list(data.get("tradeoffs") or data.get("disadvantages"))]
        benefits = [str(x) for x in _list(data.get("benefits") or data.get("advantages"))]
        return cls(
            name=str(data.get("name", "Option")),
            description=str(data.get("description", "")),
            cost=str(data.get("cost", data.get("estimated_cost", ""))),
            timeline=str(data.get("timeline", data.get("estimated_timeline", ""))),
            benefits=benefits,
            tradeoffs=tradeoffs,
            risks=[str(x) for x in _list(data.get("risks"))],
            score=str(data.get("score", "")),
            rationale=str(data.get("rationale", data.get("notes", ""))),
            advantages=[str(x) for x in _list(data.get("advantages"))],
            disadvantages=[str(x) for x in _list(data.get("disadvantages"))],
            notes=str(data.get("notes", "")),
        )


@dataclass
class BusinessCase:
    title: str = "Untitled Business Case"
    prepared_for: str = ""
    prepared_by: str = ""
    date: str = ""
    version: str = "Draft"
    classification: str = "Internal"
    audience_profile: str = "Multi-audience"
    decision_needed: str = ""
    decision_owner: str = ""
    requested_action: str = ""
    decision_timing: str = ""
    consequence_of_delay: str = ""
    problem_statement: str = ""
    observable_symptoms: list[str] = field(default_factory=list)
    root_cause_hypothesis: str = ""
    root_cause_challenge: str = ""
    status_quo_impact: str = ""
    urgency_driver: str = ""
    strategic_alignment: list[dict[str, Any]] = field(default_factory=list)
    current_state: str = ""
    baseline_metrics: list[dict[str, Any]] = field(default_factory=list)
    gap_analysis: str = ""
    evidence_limitations: str = ""
    desired_future_state: str = ""
    stakeholders: list[str] = field(default_factory=list)
    scope_in: list[str] = field(default_factory=list)
    scope_out: list[str] = field(default_factory=list)
    evaluation_criteria: list[dict[str, Any]] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)
    recommended_solution: str = ""
    rationale: str = ""
    solution_people: str = ""
    solution_process: str = ""
    solution_technology: str = ""
    dependencies: list[str] = field(default_factory=list)
    organizational_impact: str = ""
    benefits: list[dict[str, Any]] = field(default_factory=list)
    costs: list[dict[str, Any]] = field(default_factory=list)
    financial_summary: dict[str, Any] = field(default_factory=dict)
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    sensitivity_scenarios: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[dict[str, Any]] = field(default_factory=list)
    implementation_milestones: list[dict[str, Any]] = field(default_factory=list)
    resource_requirements: list[dict[str, Any]] = field(default_factory=list)
    critical_path: list[str] = field(default_factory=list)
    quick_wins: list[str] = field(default_factory=list)
    governance: str = ""
    decision_authority: list[dict[str, Any]] = field(default_factory=list)
    escalation_path: str = ""
    success_measures: list[dict[str, Any]] = field(default_factory=list)
    review_gates: list[dict[str, Any]] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BusinessCase":
        options = [Option.from_dict(x) for x in data.get("options", [])]
        if not any("do nothing" in o.name.lower().strip() for o in options):
            options.insert(0, Option(name="Option 0: Do Nothing", description="Maintain the current state."))
        strategic = data.get("strategic_alignment", [])
        if isinstance(strategic, str):
            strategic = [{"priority":"Strategic alignment", "connection": strategic}]
        return cls(
            title=str(data.get("title") or "Untitled Business Case"),
            prepared_for=str(data.get("prepared_for", "")),
            prepared_by=str(data.get("prepared_by", "")),
            date=str(data.get("date", "")),
            version=str(data.get("version", "Draft")),
            classification=str(data.get("classification", "Internal")),
            audience_profile=str(data.get("audience_profile", "Multi-audience")),
            decision_needed=str(data.get("decision_needed", "")),
            decision_owner=str(data.get("decision_owner", "")),
            requested_action=str(data.get("requested_action", "")),
            decision_timing=str(data.get("decision_timing", "")),
            consequence_of_delay=str(data.get("consequence_of_delay", "")),
            problem_statement=str(data.get("problem_statement", "")),
            observable_symptoms=[str(x) for x in _list(data.get("observable_symptoms"))],
            root_cause_hypothesis=str(data.get("root_cause_hypothesis", "")),
            root_cause_challenge=str(data.get("root_cause_challenge", "")),
            status_quo_impact=str(data.get("status_quo_impact", "")),
            urgency_driver=str(data.get("urgency_driver", "")),
            strategic_alignment=_dict_list(strategic),
            current_state=str(data.get("current_state", "")),
            baseline_metrics=_dict_list(data.get("baseline_metrics")),
            gap_analysis=str(data.get("gap_analysis", "")),
            evidence_limitations=str(data.get("evidence_limitations", "")),
            desired_future_state=str(data.get("desired_future_state", "")),
            stakeholders=[str(x) for x in _list(data.get("stakeholders"))],
            scope_in=[str(x) for x in _list(data.get("scope_in"))],
            scope_out=[str(x) for x in _list(data.get("scope_out"))],
            evaluation_criteria=_dict_list(data.get("evaluation_criteria")),
            options=options,
            recommended_solution=str(data.get("recommended_solution", "")),
            rationale=str(data.get("rationale", "")),
            solution_people=str(data.get("solution_people", "")),
            solution_process=str(data.get("solution_process", "")),
            solution_technology=str(data.get("solution_technology", "")),
            dependencies=[str(x) for x in _list(data.get("dependencies"))],
            organizational_impact=str(data.get("organizational_impact", "")),
            benefits=_dict_list(data.get("benefits")),
            costs=_dict_list(data.get("costs")),
            financial_summary=dict(data.get("financial_summary") or {}),
            assumptions=_dict_list(data.get("assumptions")),
            sensitivity_scenarios=_dict_list(data.get("sensitivity_scenarios")),
            risks=_dict_list(data.get("risks")),
            constraints=_dict_list(data.get("constraints")),
            implementation_milestones=_dict_list(data.get("implementation_milestones")),
            resource_requirements=_dict_list(data.get("resource_requirements")),
            critical_path=[str(x) for x in _list(data.get("critical_path"))],
            quick_wins=[str(x) for x in _list(data.get("quick_wins"))],
            governance=str(data.get("governance", "")),
            decision_authority=_dict_list(data.get("decision_authority")),
            escalation_path=str(data.get("escalation_path", "")),
            success_measures=_dict_list(data.get("success_measures")),
            review_gates=_dict_list(data.get("review_gates")),
            next_steps=[str(x) for x in _list(data.get("next_steps"))],
            open_questions=[str(x) for x in _list(data.get("open_questions"))],
        )
