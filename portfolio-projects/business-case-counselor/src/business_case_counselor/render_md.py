from __future__ import annotations

from .evidence import EvidenceItem, evidence_appendix
from .model import BusinessCase
from .review import ReviewResult, review_to_markdown


def val(item: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return str(item[key])
    return default


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- Not yet defined."


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    if not rows:
        rows = [["Not yet defined."] + [""] * (len(headers)-1)]
    for row in rows:
        escaped = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def render_business_case_md(case: BusinessCase, evidence: list[EvidenceItem], review: ReviewResult) -> str:
    strategic_rows = [[val(x,"priority"), val(x,"connection")] for x in case.strategic_alignment]
    baseline_rows = [[val(x,"metric"), val(x,"current"), val(x,"target"), val(x,"gap")] for x in case.baseline_metrics]
    criteria_rows = [[val(x,"criterion"), val(x,"weight"), val(x,"rationale")] for x in case.evaluation_criteria]
    option_rows = [[o.name, o.description, o.cost, o.timeline, "; ".join(o.benefits), "; ".join(o.tradeoffs), o.score or o.rationale] for o in case.options]
    cost_rows = [[val(c,"category","area","name"), val(c,"one_time","one_time_cost","estimate"), val(c,"recurring","annual_recurring_cost","type"), val(c,"assumption","notes")] for c in case.costs]
    hard_rows = [[val(b,"name"), val(b,"annual_value"), val(b,"basis","evidence","evidence_or_assumption")] for b in case.benefits if val(b,"type").lower() == "hard"]
    soft_rows = [[val(b,"name"), val(b,"annual_value", default="Not included in ROI"), val(b,"basis","evidence","evidence_or_assumption")] for b in case.benefits if val(b,"type").lower() != "hard"]
    financial_rows = [[k.replace("_", " ").title(), str(v)] for k,v in case.financial_summary.items()]
    assumption_rows = [[val(a,"assumption","item","name"), val(a,"validation","mitigation","response")] for a in case.assumptions]
    sensitivity_rows = [[val(s,"scenario"), val(s,"variable"), val(s,"impact")] for s in case.sensitivity_scenarios]
    risk_rows = [[val(r,"risk","item","name"), val(r,"likelihood"), val(r,"impact"), val(r,"severity"), val(r,"mitigation"), val(r,"residual_risk"), val(r,"owner")] for r in case.risks]
    constraint_rows = [[val(c,"constraint","item","name"), val(c,"impact","mitigation","response")] for c in case.constraints]
    milestone_rows = [[val(m,"phase"), val(m,"milestone","name"), val(m,"timing"), val(m,"owner"), val(m,"deliverables","notes")] for m in case.implementation_milestones]
    resource_rows = [[val(r,"phase"), val(r,"internal_fte"), val(r,"external"), val(r,"technology"), val(r,"dependencies")] for r in case.resource_requirements]
    authority_rows = [[val(d,"decision_type"), val(d,"accountable"), val(d,"responsible"), val(d,"consulted"), val(d,"informed")] for d in case.decision_authority]
    metric_rows = [[val(m,"metric","name","measure"), val(m,"baseline"), val(m,"target"), val(m,"frequency","cadence","review_cadence"), val(m,"owner")] for m in case.success_measures]
    gate_rows = [[val(g,"gate"), val(g,"timing"), val(g,"criteria"), val(g,"authority")] for g in case.review_gates]

    return "\n".join([
        f"# Business Case: {case.title}", "",
        table(["Field", "Detail"], [["Prepared for", case.prepared_for], ["Prepared by", case.prepared_by], ["Date", case.date], ["Version", case.version], ["Classification", case.classification], ["Audience profile", case.audience_profile]]), "",
        "## Executive Summary", "",
        f"**The Problem:** {case.problem_statement or 'TBD'}", "",
        f"**The Recommendation:** {case.recommended_solution or 'TBD'}", "",
        f"**The Financial Case:** {case.financial_summary.get('year_1_investment', 'TBD')} investment; {case.financial_summary.get('annual_hard_benefit', 'TBD')} annual hard benefit; {case.financial_summary.get('payback_period', 'TBD')} payback.", "",
        f"**The Primary Risk:** {val(case.risks[0], 'risk', default='TBD') if case.risks else 'TBD'}", "",
        f"**The Ask:** {case.requested_action or 'TBD'} Decision requested from {case.decision_owner or 'TBD'} by {case.decision_timing or 'TBD'}. {case.consequence_of_delay or ''}", "",
        "## Decision Request", "",
        table(["Field", "Detail"], [["Decision needed", case.decision_needed], ["Decision owner", case.decision_owner], ["Requested action", case.requested_action], ["Decision timing", case.decision_timing], ["Consequence of delay", case.consequence_of_delay], ["Maturity score", f"{review.total_score}/{review.max_score} - {review.readiness}"]]), "",
        "## 1. Problem Statement & Business Need", "",
        "### 1.1 Observable Symptoms", "", bullet_list(case.observable_symptoms), "",
        "### 1.2 Root Cause Analysis", "", case.root_cause_hypothesis or "TBD", "",
        "### 1.3 Root-Cause Challenge", "", case.root_cause_challenge or "TBD", "",
        "### 1.4 Quantified Impact of Status Quo", "", case.status_quo_impact or "TBD", "",
        "### 1.5 Scope Definition", "", "**In scope:**", bullet_list(case.scope_in), "", "**Out of scope:**", bullet_list(case.scope_out), "",
        "### 1.6 Urgency Drivers", "", case.urgency_driver or "TBD", "",
        "## 2. Strategic Alignment", "", table(["Organizational Priority", "Connection to Initiative"], strategic_rows), "",
        "## 3. Current State Assessment", "", case.current_state or "TBD", "",
        "### Baseline Performance Metrics", "", table(["Metric", "Current", "Target", "Gap"], baseline_rows), "",
        "### Identified Gaps", "", case.gap_analysis or "TBD", "",
        "### Evidence Sources & Limitations", "", case.evidence_limitations or "TBD", "",
        "## 4. Options Analysis", "", "### Evaluation Criteria", "", table(["Criterion", "Weight", "Rationale"], criteria_rows), "", "### Option Summaries", "", table(["Option", "Description", "Cost", "Timeline", "Benefits", "Tradeoffs", "Score / Rationale"], option_rows), "",
        "## 5. Recommended Solution", "", "### 5.1 Recommendation", "", case.recommended_solution or "TBD", "", "### 5.2 Rationale", "", case.rationale or "TBD", "", "### 5.3 People / Process / Technology", "", f"**People:** {case.solution_people or 'TBD'}", "", f"**Process:** {case.solution_process or 'TBD'}", "", f"**Technology:** {case.solution_technology or 'TBD'}", "", "### 5.4 Dependencies & Prerequisites", "", bullet_list(case.dependencies), "", "### 5.5 Organizational Impact", "", case.organizational_impact or "TBD", "",
        "## 6. Financial Analysis", "", "### 6.1 Investment Summary", "", table(["Category", "One-Time Cost", "Annual Recurring Cost", "Notes / Assumptions"], cost_rows), "", "### 6.2 Benefit Model", "", "**Hard Benefits (included in ROI calculation)**", "", table(["Benefit", "Annual Value", "Basis / Assumption"], hard_rows), "", "**Soft Benefits (not included in ROI headline)**", "", table(["Benefit", "Value", "Basis / Assumption"], soft_rows), "", "### 6.3 Return Analysis", "", table(["Metric", "Value"], financial_rows), "", "### 6.4 Key Assumptions", "", table(["Assumption", "Validation"], assumption_rows), "", "### 6.5 Sensitivity Analysis", "", table(["Scenario", "Variable", "Impact"], sensitivity_rows), "",
        "## 7. Risk Assessment", "", "### Top Risks", "", bullet_list([val(r,"risk","item") for r in case.risks[:3]]), "", "### Risk Register", "", table(["Risk", "Likelihood", "Impact", "Severity", "Mitigation", "Residual Risk", "Owner"], risk_rows), "", "### Constraints", "", table(["Constraint", "Impact"], constraint_rows), "",
        "## 8. Implementation Roadmap", "", "### Timeline Overview", "", table(["Phase", "Milestone", "Timing", "Owner", "Deliverables"], milestone_rows), "", "### Resource Requirements", "", table(["Phase", "Internal FTEs", "External / Vendor", "Technology", "Dependencies"], resource_rows), "", "### Critical Path Items", "", bullet_list(case.critical_path), "", "### 90-Day Quick Wins", "", bullet_list(case.quick_wins), "",
        "## 9. Governance & Decision Framework", "", case.governance or "TBD", "", "### Decision Authority", "", table(["Decision Type", "Accountable", "Responsible", "Consulted", "Informed"], authority_rows), "", "### Escalation Path", "", case.escalation_path or "TBD", "", "### Success Metrics & Measurement Cadence", "", table(["Metric", "Baseline", "Target", "Frequency", "Owner"], metric_rows), "", "### Review Gates", "", table(["Gate", "Timing", "Decision Criteria", "Authority"], gate_rows), "",
        "## 10. Recommendation & Call to Action", "", "### Recommendation", "", case.recommended_solution or "TBD", "", "### Decision Requested", "", f"We request approval from {case.decision_owner or 'TBD'} to {case.requested_action or 'TBD'} by {case.decision_timing or 'TBD'}.", "", "### Consequence of Delay", "", case.consequence_of_delay or "TBD", "", "### Next Steps", "", bullet_list(case.next_steps), "", "### Open Questions", "", bullet_list(case.open_questions), "",
        "## Critical Professional Counsel", "", review_to_markdown(review).replace("# Business Case Maturity Review\n\n", ""), "",
        "## Appendix: Evidence Summary", "", evidence_appendix(evidence) if evidence else "No evidence artifacts were provided.", "",
        "---", "", "*Sample data, where present, is fictional and for demonstration only.*", ""
    ])
