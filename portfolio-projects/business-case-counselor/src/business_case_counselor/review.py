from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .model import BusinessCase


@dataclass
class CriterionResult:
    name: str
    score: int
    issue: str
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
    return bool(text and text.strip())


def score_text(text: str, strong_len: int = 220) -> int:
    if not present(text):
        return 0
    n = len(text.strip())
    if n < 40:
        return 1
    if n < 120:
        return 2
    if n < strong_len:
        return 3
    return 4


def score_list(items: list, min_count: int = 1, strong_count: int = 3) -> int:
    count = len([x for x in items if x])
    if count == 0:
        return 0
    if count < min_count:
        return 1
    if count < strong_count:
        return 3
    return 4


def cap_with_evidence(base: int, has_evidence: bool) -> int:
    if has_evidence:
        return min(5, base + 1)
    return base


def review_case(case: BusinessCase) -> ReviewResult:
    evidence_signals = bool(case.benefits or case.costs or case.risks or case.assumptions or case.success_measures)
    do_nothing = any(o.name.lower().strip() == "do nothing" for o in case.options)
    populated_options = [o for o in case.options if present(o.description) or o.advantages or o.disadvantages]

    checks: list[CriterionResult] = []

    def add(name: str, score: int, issue: str, counsel: str, evidence_needed: str):
        checks.append(CriterionResult(name, max(0, min(5, score)), issue, counsel, evidence_needed))

    add(
        "Decision clarity",
        score_text(case.decision_needed, 120) + (1 if present(case.requested_action) and present(case.decision_owner) else 0),
        "The case must make the requested leadership decision explicit.",
        "State the approval action, decision owner, timing, and what happens immediately after approval or rejection.",
        "Decision body, approval threshold, requested funding or authorization, and decision date.",
    )
    add(
        "Problem definition",
        score_text(case.problem_statement),
        "A vague problem statement makes every downstream option look arbitrary.",
        "Define the business problem in operational terms: who is affected, what pain exists, how often it occurs, and why it matters now.",
        "Current-state examples, incidents, lost time, cost, revenue leakage, risk exposure, or stakeholder feedback.",
    )
    add(
        "Strategic alignment",
        score_text(case.strategic_alignment),
        "The case needs to explain why this initiative belongs in the portfolio.",
        "Tie the initiative to named strategy, objectives, regulatory obligations, customer outcomes, cost discipline, or risk reduction.",
        "Strategic plan excerpts, OKRs, annual priorities, compliance drivers, customer commitments, or portfolio themes.",
    )
    add(
        "Current-state evidence",
        cap_with_evidence(score_text(case.current_state + " " + case.gap_analysis), evidence_signals),
        "Leadership will challenge the case if the pain is asserted but not evidenced.",
        "Quantify current-state pain where possible and label any estimates as assumptions.",
        "Baseline metrics, process data, financials, ticket volumes, cycle time, error rates, support load, risk events, or qualitative evidence.",
    )
    add(
        "Options analysis",
        min(5, score_list(populated_options, 2, 3) + (1 if do_nothing else 0)),
        "A single-solution case reads like advocacy rather than decision analysis.",
        "Compare at least three options, including do nothing, with clear tradeoffs.",
        "Option costs, benefits, feasibility, time-to-value, dependency, and risk notes.",
    )
    add(
        "Recommendation quality",
        score_text(case.recommended_solution),
        "The recommendation must follow from the option analysis.",
        "Explain why the recommended path is better than the alternatives under the stated constraints.",
        "Selection criteria, weighted tradeoffs, stakeholder input, feasibility assessment, and risk-adjusted value.",
    )
    add(
        "Value case",
        cap_with_evidence(score_list(case.benefits, 1, 3), bool(case.success_measures)),
        "Benefits must be credible enough to justify the investment or change.",
        "Separate hard financial benefits from qualitative, risk, compliance, productivity, and customer benefits.",
        "Benefit owner, baseline, target, measurement method, confidence level, and validation plan.",
    )
    add(
        "Cost and funding clarity",
        score_list(case.costs, 1, 3),
        "Missing or vague costs make approval fragile.",
        "Separate one-time implementation costs from recurring operating costs and identify funding source where possible.",
        "Labor, vendor, platform, training, support, change management, licensing, integration, and run-rate costs.",
    )
    add(
        "Risk and constraint discipline",
        min(5, score_list(case.risks, 1, 3) + score_list(case.assumptions, 1, 3)//2 + score_list(case.constraints, 1, 2)//2),
        "Risks, assumptions, and constraints should not be buried or softened.",
        "Make the risk register decision-useful: impact, likelihood, mitigation, owner, and validation trigger.",
        "Risk log, dependency map, compliance review, security review, vendor constraints, resource constraints, and assumption tests.",
    )
    add(
        "Implementation feasibility",
        min(5, score_list(case.implementation_milestones, 1, 4) + (1 if present(case.governance) else 0)),
        "The business case does not need a full project plan, but it needs a credible path.",
        "Show phases, milestones, owners, dependencies, and governance checkpoints.",
        "Milestone plan, owner list, dependency map, delivery estimate, governance cadence, and readiness criteria.",
    )
    add(
        "Evidence traceability",
        cap_with_evidence(score_list(case.open_questions, 0, 2), evidence_signals),
        "The case should distinguish what is known from what must still be validated.",
        "Add an evidence appendix, identify source artifacts, and list open questions that could change the recommendation.",
        "Named evidence artifacts, source notes, assumptions log, and unresolved decision questions.",
    )
    add(
        "Executive readability",
        min(5, (1 if present(case.title) else 0) + (1 if present(case.decision_needed) else 0) + (1 if present(case.problem_statement) else 0) + (1 if present(case.recommended_solution) else 0) + (1 if case.next_steps else 0)),
        "A business case must be usable by a busy decision-maker.",
        "Keep the summary short, put the decision request near the front, and use tables for tradeoffs, risks, costs, and next steps.",
        "Executive summary, decision table, option comparison, cost/benefit tables, and next-step owner list.",
    )

    total = sum(c.score for c in checks)
    max_score = len(checks) * 5
    if total <= 29:
        readiness = "Not ready. Use for discovery only."
    elif total <= 44:
        readiness = "Early draft. Major gaps remain."
    elif total <= 54:
        readiness = "Reviewable. Needs targeted strengthening."
    elif total <= 64:
        readiness = "Decision-ready with caveats."
    else:
        readiness = "Strong leadership-ready case."

    top = [f"{c.name}: {c.counsel}" for c in sorted(checks, key=lambda x: x.score)[:5]]
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
    lines.extend(["", "## Criterion Detail", ""])
    for c in result.criteria:
        lines.extend([
            f"### {c.name}: {c.score}/5",
            "",
            f"**Issue:** {c.issue}",
            "",
            f"**Counsel:** {c.counsel}",
            "",
            f"**Evidence needed:** {c.evidence_needed}",
            "",
        ])
    return "\n".join(lines)
