from __future__ import annotations

from .evidence import EvidenceItem, evidence_appendix
from .model import BusinessCase
from .review import ReviewResult, review_to_markdown


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- Not yet defined."
    return "\n".join(f"- {item}" for item in items)


def val(item: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return str(item[key])
    return default


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    if not rows:
        rows = [["Not yet defined."] + [""] * (len(headers) - 1)]
    for row in rows:
        escaped = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def render_business_case_md(case: BusinessCase, evidence: list[EvidenceItem], review: ReviewResult) -> str:
    benefit_rows = [[
        val(b, "name", "benefit", "item"),
        val(b, "type", default="TBD"),
        val(b, "evidence", "evidence_or_assumption", default="TBD"),
        val(b, "measurement", "measurement_approach", default="TBD"),
    ] for b in case.benefits]

    cost_rows = [[
        val(c, "area", "name", "item"),
        val(c, "estimate", default="TBD"),
        val(c, "type", default="TBD"),
        val(c, "notes", default=""),
    ] for c in case.costs]

    risk_rows = []
    for kind, items in [("Risk", case.risks), ("Assumption", case.assumptions), ("Constraint", case.constraints)]:
        for item in items:
            risk_rows.append([
                kind,
                val(item, "item", "name", "risk", "assumption", "constraint"),
                val(item, "impact", default="TBD"),
                val(item, "mitigation", "validation", "response", default="TBD"),
            ])

    milestone_rows = [[
        val(m, "name", "milestone"),
        val(m, "owner", default="TBD"),
        val(m, "timing", "target", default="TBD"),
        val(m, "notes", default=""),
    ] for m in case.implementation_milestones]

    measure_rows = [[
        val(m, "name", "measure"),
        val(m, "baseline", default="TBD"),
        val(m, "target", default="TBD"),
        val(m, "cadence", "review_cadence", default="TBD"),
    ] for m in case.success_measures]

    option_rows = [[
        o.name,
        o.description or "TBD",
        "; ".join(o.advantages) if o.advantages else "TBD",
        "; ".join(o.disadvantages) if o.disadvantages else "TBD",
        o.notes or "",
    ] for o in case.options]

    lines = [
        f"# Business Case: {case.title}",
        "",
        "## 1. Executive Summary",
        "",
        _executive_summary(case),
        "",
        "## 2. Decision Request",
        "",
        table(["Field", "Detail"], [
            ["Decision needed", case.decision_needed or "TBD"],
            ["Decision owner/body", case.decision_owner or "TBD"],
            ["Requested action", case.requested_action or "TBD"],
            ["Timing", case.decision_timing or "TBD"],
            ["Maturity score", f"{review.total_score}/{review.max_score} - {review.readiness}"],
        ]),
        "",
        "## 3. Problem or Opportunity Statement",
        "",
        case.problem_statement or "TBD",
        "",
        "## 4. Strategic Alignment",
        "",
        case.strategic_alignment or "TBD",
        "",
        "## 5. Current State and Gap Analysis",
        "",
        "### Current State",
        "",
        case.current_state or "TBD",
        "",
        "### Gap Analysis",
        "",
        case.gap_analysis or "TBD",
        "",
        "### Desired Future State",
        "",
        case.desired_future_state or "TBD",
        "",
        "## 6. Options Analysis",
        "",
        table(["Option", "Description", "Advantages", "Disadvantages", "Decision Notes"], option_rows),
        "",
        "## 7. Recommended Solution",
        "",
        case.recommended_solution or "TBD",
        "",
        "## 8. Benefits and Value Case",
        "",
        table(["Benefit", "Type", "Evidence / Assumption", "Measurement Approach"], benefit_rows),
        "",
        "## 9. Costs, Funding, and ROI Considerations",
        "",
        table(["Cost Area", "Estimate", "One-time / Ongoing", "Notes"], cost_rows),
        "",
        "## 10. Risks, Assumptions, and Constraints",
        "",
        table(["Type", "Item", "Impact", "Mitigation / Validation"], risk_rows),
        "",
        "## 11. Implementation Approach, Milestones, and Ownership",
        "",
        table(["Milestone", "Owner", "Target Timing", "Notes"], milestone_rows),
        "",
        "## 12. Governance and Success Measures",
        "",
        case.governance or "TBD",
        "",
        table(["Measure", "Baseline", "Target", "Review Cadence"], measure_rows),
        "",
        "## 13. Scope, Stakeholders, and Next Steps",
        "",
        "### Stakeholders",
        bullet_list(case.stakeholders),
        "",
        "### In Scope",
        bullet_list(case.scope_in),
        "",
        "### Out of Scope",
        bullet_list(case.scope_out),
        "",
        "### Next Steps",
        bullet_list(case.next_steps),
        "",
        "### Open Questions",
        bullet_list(case.open_questions),
        "",
        "## 14. Critical Professional Counsel",
        "",
        review_to_markdown(review).replace("# Business Case Maturity Review\n\n", ""),
        "",
        "## 15. Appendix: Evidence Summary",
        "",
        evidence_appendix(evidence) if evidence else "No evidence artifacts were provided.",
        "",
    ]
    return "\n".join(lines)


def _executive_summary(case: BusinessCase) -> str:
    parts = []
    if case.problem_statement:
        parts.append(case.problem_statement)
    if case.recommended_solution:
        parts.append(f"The recommended path is: {case.recommended_solution}")
    if case.requested_action:
        parts.append(f"The requested action is: {case.requested_action}.")
    if not parts:
        return "TBD"
    return "\n\n".join(parts)
