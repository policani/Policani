from __future__ import annotations

from pathlib import Path
import html

from .evidence import EvidenceItem
from .model import BusinessCase
from .review import ReviewResult
from .render_md import val


def esc(x) -> str:
    return html.escape(str(x or ""))


def p(text: str) -> str:
    return f"<p>{esc(text) if text else 'TBD'}</p>"


def ul(items: list[str]) -> str:
    if not items:
        return "<ul><li>Not yet defined.</li></ul>"
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        rows = [["Not yet defined."] + [""] * (len(headers)-1)]
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>"


def section(title: str, body: str) -> str:
    return f"<section><h2>{esc(title)}</h2>{body}</section>"


def render_business_case_html(case: BusinessCase, evidence: list[EvidenceItem], review: ReviewResult, out_path: Path | None = None) -> str:
    strategic_rows = [[val(x,"priority"), val(x,"connection")] for x in case.strategic_alignment]
    baseline_rows = [[val(x,"metric"), val(x,"current"), val(x,"target"), val(x,"gap")] for x in case.baseline_metrics]
    criteria_rows = [[val(x,"criterion"), val(x,"weight"), val(x,"rationale")] for x in case.evaluation_criteria]
    option_rows = [[o.name, o.description, o.cost, o.timeline, "; ".join(o.benefits), "; ".join(o.tradeoffs), o.score or o.rationale] for o in case.options]
    cost_rows = [[val(c,"category","area","name"), val(c,"one_time","one_time_cost","estimate"), val(c,"recurring","annual_recurring_cost","type"), val(c,"assumption","notes")] for c in case.costs]
    hard_rows = [[val(b,"name"), val(b,"annual_value"), val(b,"basis","evidence","evidence_or_assumption")] for b in case.benefits if val(b,"type").lower() == "hard"]
    soft_rows = [[val(b,"name"), val(b,"annual_value", default="Not included in ROI"), val(b,"basis","evidence","evidence_or_assumption")] for b in case.benefits if val(b,"type").lower() != "hard"]
    financial_rows = [[k.replace("_", " ").title(), str(v)] for k,v in case.financial_summary.items()]
    risk_rows = [[val(r,"risk","item","name"), val(r,"likelihood"), val(r,"impact"), val(r,"severity"), val(r,"mitigation"), val(r,"residual_risk"), val(r,"owner")] for r in case.risks]
    milestone_rows = [[val(m,"phase"), val(m,"milestone","name"), val(m,"timing"), val(m,"owner"), val(m,"deliverables","notes")] for m in case.implementation_milestones]
    authority_rows = [[val(d,"decision_type"), val(d,"accountable"), val(d,"responsible"), val(d,"consulted"), val(d,"informed")] for d in case.decision_authority]
    metric_rows = [[val(m,"metric","name","measure"), val(m,"baseline"), val(m,"target"), val(m,"frequency","cadence","review_cadence"), val(m,"owner")] for m in case.success_measures]
    gate_rows = [[val(g,"gate"), val(g,"timing"), val(g,"criteria"), val(g,"authority")] for g in case.review_gates]
    review_rows = [[c.name, f"{c.score}/5", c.finding, c.counsel, c.evidence_needed] for c in review.criteria]
    evidence_rows = [[e.path, e.kind, e.summary] for e in evidence]

    html_text = f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Business Case: {esc(case.title)}</title>
<style>
:root {{ --ink:#17202a; --muted:#5d6d7e; --line:#d5d8dc; --shade:#f4f6f7; --accent:#1f4e79; }}
body {{ font-family: Arial, Helvetica, sans-serif; color: var(--ink); margin: 0; background: #fff; line-height: 1.45; }}
main {{ max-width: 1120px; margin: 0 auto; padding: 40px 28px; }}
header {{ border-bottom: 4px solid var(--accent); margin-bottom: 28px; padding-bottom: 16px; }}
h1 {{ margin: 0 0 8px; font-size: 30px; }}
h2 {{ color: var(--accent); border-bottom: 1px solid var(--line); padding-bottom: 6px; margin-top: 32px; }}
h3 {{ margin-top: 22px; }}
.meta, .callout {{ background: var(--shade); border: 1px solid var(--line); padding: 14px; border-radius: 8px; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0 18px; font-size: 13px; }}
th, td {{ border: 1px solid var(--line); padding: 8px; vertical-align: top; }}
th {{ background: #eaf2f8; text-align: left; }}
.badge {{ display: inline-block; background: #eaf2f8; color: var(--accent); padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: bold; }}
ul {{ margin-top: 8px; }}
footer {{ margin-top: 40px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--line); padding-top: 12px; }}
@media print {{ main {{ max-width: none; padding: 20px; }} table {{ font-size: 11px; }} }}
</style>
</head>
<body><main>
<header>
<h1>Business Case: {esc(case.title)}</h1>
<p class=\"badge\">{esc(case.classification)}</p>
<div class=\"meta\"><strong>Prepared for:</strong> {esc(case.prepared_for)}<br><strong>Prepared by:</strong> {esc(case.prepared_by)}<br><strong>Date:</strong> {esc(case.date)}<br><strong>Version:</strong> {esc(case.version)}<br><strong>Audience:</strong> {esc(case.audience_profile)}</div>
</header>
<section class=\"callout\"><h2>Executive Summary</h2>
<p><strong>The Problem:</strong> {esc(case.problem_statement or 'TBD')}</p>
<p><strong>The Recommendation:</strong> {esc(case.recommended_solution or 'TBD')}</p>
<p><strong>The Financial Case:</strong> {esc(case.financial_summary.get('year_1_investment','TBD'))} investment; {esc(case.financial_summary.get('annual_hard_benefit','TBD'))} annual hard benefit; {esc(case.financial_summary.get('payback_period','TBD'))} payback.</p>
<p><strong>The Primary Risk:</strong> {esc(val(case.risks[0], 'risk', default='TBD') if case.risks else 'TBD')}</p>
<p><strong>The Ask:</strong> {esc(case.requested_action or 'TBD')} Decision requested from {esc(case.decision_owner or 'TBD')} by {esc(case.decision_timing or 'TBD')}. {esc(case.consequence_of_delay)}</p>
</section>
{section('Decision Request', table(['Field','Detail'], [['Decision needed', case.decision_needed], ['Decision owner', case.decision_owner], ['Requested action', case.requested_action], ['Decision timing', case.decision_timing], ['Consequence of delay', case.consequence_of_delay], ['Maturity score', f'{review.total_score}/{review.max_score} - {review.readiness}']]))}
{section('1. Problem Statement & Business Need', '<h3>Observable Symptoms</h3>'+ul(case.observable_symptoms)+'<h3>Root Cause Analysis</h3>'+p(case.root_cause_hypothesis)+'<h3>Root-Cause Challenge</h3>'+p(case.root_cause_challenge)+'<h3>Quantified Impact of Status Quo</h3>'+p(case.status_quo_impact)+'<h3>Scope Definition</h3><strong>In scope</strong>'+ul(case.scope_in)+'<strong>Out of scope</strong>'+ul(case.scope_out)+'<h3>Urgency Drivers</h3>'+p(case.urgency_driver))}
{section('2. Strategic Alignment', table(['Organizational Priority','Connection to Initiative'], strategic_rows))}
{section('3. Current State Assessment', p(case.current_state)+'<h3>Baseline Performance Metrics</h3>'+table(['Metric','Current','Target','Gap'], baseline_rows)+'<h3>Identified Gaps</h3>'+p(case.gap_analysis)+'<h3>Evidence Sources & Limitations</h3>'+p(case.evidence_limitations))}
{section('4. Options Analysis', '<h3>Evaluation Criteria</h3>'+table(['Criterion','Weight','Rationale'], criteria_rows)+'<h3>Option Summaries</h3>'+table(['Option','Description','Cost','Timeline','Benefits','Tradeoffs','Score / Rationale'], option_rows))}
{section('5. Recommended Solution', '<h3>Recommendation</h3>'+p(case.recommended_solution)+'<h3>Rationale</h3>'+p(case.rationale)+'<h3>People / Process / Technology</h3>'+p('People: '+case.solution_people)+p('Process: '+case.solution_process)+p('Technology: '+case.solution_technology)+'<h3>Dependencies & Prerequisites</h3>'+ul(case.dependencies)+'<h3>Organizational Impact</h3>'+p(case.organizational_impact))}
{section('6. Financial Analysis', '<h3>Investment Summary</h3>'+table(['Category','One-Time Cost','Annual Recurring Cost','Notes / Assumptions'], cost_rows)+'<h3>Hard Benefits</h3>'+table(['Benefit','Annual Value','Basis / Assumption'], hard_rows)+'<h3>Soft Benefits</h3>'+table(['Benefit','Value','Basis / Assumption'], soft_rows)+'<h3>Return Analysis</h3>'+table(['Metric','Value'], financial_rows)+'<h3>Sensitivity Analysis</h3>'+table(['Scenario','Variable','Impact'], [[val(s,'scenario'), val(s,'variable'), val(s,'impact')] for s in case.sensitivity_scenarios]))}
{section('7. Risk Assessment', '<h3>Risk Register</h3>'+table(['Risk','Likelihood','Impact','Severity','Mitigation','Residual Risk','Owner'], risk_rows))}
{section('8. Implementation Roadmap', '<h3>Timeline Overview</h3>'+table(['Phase','Milestone','Timing','Owner','Deliverables'], milestone_rows)+'<h3>Critical Path</h3>'+ul(case.critical_path)+'<h3>90-Day Quick Wins</h3>'+ul(case.quick_wins))}
{section('9. Governance & Decision Framework', p(case.governance)+'<h3>Decision Authority</h3>'+table(['Decision Type','Accountable','Responsible','Consulted','Informed'], authority_rows)+'<h3>Success Metrics</h3>'+table(['Metric','Baseline','Target','Frequency','Owner'], metric_rows)+'<h3>Review Gates</h3>'+table(['Gate','Timing','Decision Criteria','Authority'], gate_rows))}
{section('10. Recommendation & Call to Action', '<h3>Decision Requested</h3>'+p(f'We request approval from {case.decision_owner or "TBD"} to {case.requested_action or "TBD"} by {case.decision_timing or "TBD"}.')+'<h3>Consequence of Delay</h3>'+p(case.consequence_of_delay)+'<h3>Next Steps</h3>'+ul(case.next_steps)+'<h3>Open Questions</h3>'+ul(case.open_questions))}
{section('Critical Professional Counsel', '<p><strong>Score:</strong> '+esc(f'{review.total_score}/{review.max_score}')+'</p><p><strong>Readiness:</strong> '+esc(review.readiness)+'</p>'+table(['Dimension','Score','Finding','Counsel','Evidence Needed'], review_rows))}
{section('Appendix: Evidence Summary', table(['Artifact','Type','Summary'], evidence_rows) if evidence_rows else p('No evidence artifacts were provided.'))}
<footer>Sample data, where present, is fictional and for demonstration only.</footer>
</main></body></html>"""
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_text, encoding="utf-8")
    return html_text
