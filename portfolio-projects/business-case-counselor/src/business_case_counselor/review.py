from __future__ import annotations

from dataclasses import dataclass
from .model import BusinessCase


@dataclass
class CriterionResult:
    name: str
    score: int
    finding: str
    counsel: str
    evidence_needed: str


@dataclass
class ReviewResult:
    total_score: int
    max_score: int
    readiness: str
    criteria: list[CriterionResult]
    top_improvements: list[str]


def present(text: str) -> bool:
    return bool(text and str(text).strip())


def has_number(text: str) -> bool:
    return any(ch.isdigit() for ch in str(text or ""))


def score_presence(*values, strong_count: int = 3) -> int:
    count = sum(1 for v in values if v)
    if count == 0:
        return 1
    if count < strong_count:
        return 3
    return 4


def review_case(case: BusinessCase) -> ReviewResult:
    checks: list[CriterionResult] = []

    def add(name: str, score: int, finding: str, counsel: str, evidence_needed: str):
        checks.append(CriterionResult(name, max(1, min(5, score)), finding, counsel, evidence_needed))

    problem_score = 1
    problem_bits = [present(case.problem_statement), bool(case.observable_symptoms), present(case.root_cause_hypothesis), present(case.status_quo_impact), bool(case.scope_in), present(case.urgency_driver)]
    problem_score = min(5, 1 + sum(1 for b in problem_bits if b))
    if has_number(case.status_quo_impact):
        problem_score = min(5, problem_score + 1)
    add(
        "Problem clarity",
        problem_score,
        "Tests whether the problem is stated in business terms, separated from root cause, scoped, and quantified.",
        "Tighten the business problem, name observable symptoms, separate symptom from root cause, and quantify the cost of inaction.",
        "Observable symptoms, root-cause evidence, scope boundaries, urgency driver, and status quo impact."
    )

    evidence_score = 1
    evidence_bits = [case.baseline_metrics, case.benefits, case.costs, case.risks, case.assumptions, present(case.evidence_limitations)]
    evidence_score = min(5, 1 + sum(1 for b in evidence_bits if b))
    add(
        "Evidence grounding",
        evidence_score,
        "Tests whether claims are supported by data, source artifacts, or clearly stated assumptions.",
        "Label assumptions, name evidence limitations, and connect each major number to a basis or source.",
        "Baseline metrics, source inventory, assumption log, data limitations, and validation plan."
    )

    do_nothing = any("do nothing" in o.name.lower() for o in case.options)
    option_count = len([o for o in case.options if present(o.description)])
    criteria_count = len(case.evaluation_criteria)
    options_score = 1 + min(2, option_count // 2) + (1 if do_nothing else 0) + (1 if criteria_count >= 3 else 0)
    add(
        "Options integrity",
        options_score,
        "Tests whether the recommendation follows from real alternatives rather than a predetermined solution.",
        "Evaluate Do Nothing and credible alternatives against consistent criteria. Do not strawman options.",
        "Option costs, timelines, benefits, tradeoffs, scores, and scoring rationale."
    )

    hard_benefits = [b for b in case.benefits if str(b.get("type", "")).lower() == "hard"]
    soft_benefits = [b for b in case.benefits if str(b.get("type", "")).lower() == "soft"]
    financial_score = 1
    financial_score += 1 if case.costs else 0
    financial_score += 1 if hard_benefits else 0
    financial_score += 1 if soft_benefits else 0
    financial_score += 1 if case.financial_summary else 0
    financial_score += 1 if case.sensitivity_scenarios else 0
    add(
        "Financial rigor",
        financial_score,
        "Tests cost completeness, hard/soft benefit separation, return analysis, assumptions, and sensitivity.",
        "Separate hard benefits from soft benefits, show Year 1 cost, annual hard benefit, payback/ROI, and downside scenarios.",
        "Cost categories, benefit basis, ROI/payback method, assumptions, sensitivity scenarios."
    )

    named_risks = len([r for r in case.risks if r.get("risk") or r.get("item")])
    owned_risks = len([r for r in case.risks if r.get("owner")])
    residual_risks = len([r for r in case.risks if r.get("residual_risk")])
    risk_score = 1 + (1 if named_risks >= 3 else 0) + (1 if any(r.get("likelihood") and r.get("impact") for r in case.risks) else 0) + (1 if owned_risks >= 2 else 0) + (1 if residual_risks >= 2 else 0)
    add(
        "Risk honesty",
        risk_score,
        "Tests whether material risks are named, assessed, mitigated, and owned.",
        "Use named failure modes, likelihood, impact, severity, mitigation, residual risk, and owner.",
        "Risk register, mitigation plan, owner list, dependency map, compliance/security review if applicable."
    )

    exec_score = 1 + sum(1 for v in [case.problem_statement, case.recommended_solution, case.financial_summary, case.risks, case.requested_action] if v)
    add(
        "Executive readability",
        exec_score,
        "Tests whether a time-pressed executive can understand the problem, recommendation, cost, return, risk, and ask quickly.",
        "Put the decision request near the front, keep the executive summary self-contained, and use tables for financials, risks, and options.",
        "Standalone executive summary, decision table, concise recommendation, readable financial and risk tables."
    )

    decision_score = 1 + sum(1 for v in [case.decision_needed, case.decision_owner, case.requested_action, case.decision_timing, case.consequence_of_delay, case.next_steps] if v)
    add(
        "Decision clarity",
        decision_score,
        "Tests whether the document asks for a specific decision from a specific decision-maker by a specific date.",
        "State the named decision, owner, deadline, consequence of delay, and first actions if approved.",
        "Decision owner, approval action, date, consequence of delay, next-step owner list."
    )

    total = sum(c.score for c in checks)
    max_score = len(checks) * 5
    if total >= 32:
        readiness = "Executive-ready. Suitable for leadership review with normal validation."
    elif total >= 27:
        readiness = "Strong draft. One focused revision cycle likely improves it to executive-ready."
    elif total >= 21:
        readiness = "Working draft. Significant gaps remain before external use."
    else:
        readiness = "Structural gaps. Rebuild or deepen intake before use."
    top = [f"{c.name}: {c.counsel}" for c in sorted(checks, key=lambda x: x.score)[:3]]
    return ReviewResult(total, max_score, readiness, checks, top)


def review_to_markdown(result: ReviewResult) -> str:
    lines = [
        "# Business Case Maturity Review",
        "",
        f"**Score:** {result.total_score}/{result.max_score}",
        f"**Readiness:** {result.readiness}",
        "",
        "## Top Improvements",
        "",
    ]
    for item in result.top_improvements:
        lines.append(f"- {item}")
    lines.extend(["", "## Quality Rubric", "", "| Dimension | Score | Finding | Counsel | Evidence Needed |", "|---|---:|---|---|---|"])
    for c in result.criteria:
        lines.append(f"| {c.name} | {c.score}/5 | {c.finding} | {c.counsel} | {c.evidence_needed} |")
    return "\n".join(lines)
