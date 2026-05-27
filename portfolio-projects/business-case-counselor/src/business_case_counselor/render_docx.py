from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .evidence import EvidenceItem, evidence_appendix
from .model import BusinessCase
from .review import ReviewResult


def _require_docx():
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.section import WD_SECTION
        from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
        from docx.shared import Inches, Pt
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
    except ImportError as exc:
        raise RuntimeError("DOCX export requires python-docx. Install with: pip install python-docx") from exc
    return Document, WD_ALIGN_PARAGRAPH, WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, Inches, Pt, OxmlElement, qn


def set_cell_shading(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def style_table(table, header_fill="D9EAF7"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(8.5)
            if i == 0:
                set_cell_shading(cell, header_fill)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.bold = True


def add_kv_table(doc, rows: list[tuple[str, str]]):
    table = doc.add_table(rows=1, cols=2)
    hdr = table.rows[0].cells
    hdr[0].text = "Field"
    hdr[1].text = "Detail"
    for field, detail in rows:
        cells = table.add_row().cells
        cells[0].text = field
        cells[1].text = detail or "TBD"
    style_table(table)
    return table


def add_table(doc, headers: list[str], rows: list[list[str]]):
    table = doc.add_table(rows=1, cols=len(headers))
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    if not rows:
        rows = [["Not yet defined."] + [""] * (len(headers) - 1)]
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row[:len(headers)]):
            cells[i].text = str(value or "")
    style_table(table)
    return table


def add_bullets(doc, items: Iterable[str]):
    real = [x for x in items if x]
    if not real:
        doc.add_paragraph("Not yet defined.", style="List Bullet")
        return
    for item in real:
        doc.add_paragraph(str(item), style="List Bullet")


def val(item: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return str(item[key])
    return default


def render_business_case_docx(case: BusinessCase, evidence: list[EvidenceItem], review: ReviewResult, out_path: Path) -> None:
    global OxmlElement, qn, WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, Pt
    Document, WD_ALIGN_PARAGRAPH, WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, Inches, Pt, OxmlElement, qn = _require_docx()

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

    styles = doc.styles
    styles["Normal"].font.name = "Calibri"
    styles["Normal"].font.size = Pt(10)
    for s in ["Heading 1", "Heading 2", "Heading 3"]:
        styles[s].font.name = "Calibri"

    title = doc.add_heading(f"Business Case: {case.title}", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = doc.add_paragraph("Decision document for approval, prioritization, funding, or governance review")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("1. Executive Summary", level=1)
    summary_parts = []
    if case.problem_statement:
        summary_parts.append(case.problem_statement)
    if case.recommended_solution:
        summary_parts.append(f"The recommended path is: {case.recommended_solution}")
    if case.requested_action:
        summary_parts.append(f"The requested action is: {case.requested_action}.")
    doc.add_paragraph("\n\n".join(summary_parts) if summary_parts else "TBD")

    doc.add_heading("2. Decision Request", level=1)
    add_kv_table(doc, [
        ("Decision needed", case.decision_needed),
        ("Decision owner/body", case.decision_owner),
        ("Requested action", case.requested_action),
        ("Timing", case.decision_timing),
        ("Maturity score", f"{review.total_score}/{review.max_score} - {review.readiness}"),
    ])

    doc.add_heading("3. Problem or Opportunity Statement", level=1)
    doc.add_paragraph(case.problem_statement or "TBD")

    doc.add_heading("4. Strategic Alignment", level=1)
    doc.add_paragraph(case.strategic_alignment or "TBD")

    doc.add_heading("5. Current State and Gap Analysis", level=1)
    doc.add_heading("Current State", level=2)
    doc.add_paragraph(case.current_state or "TBD")
    doc.add_heading("Gap Analysis", level=2)
    doc.add_paragraph(case.gap_analysis or "TBD")
    doc.add_heading("Desired Future State", level=2)
    doc.add_paragraph(case.desired_future_state or "TBD")

    doc.add_heading("6. Options Analysis", level=1)
    option_rows = [[
        o.name,
        o.description or "TBD",
        "; ".join(o.advantages) if o.advantages else "TBD",
        "; ".join(o.disadvantages) if o.disadvantages else "TBD",
        o.notes or "",
    ] for o in case.options]
    add_table(doc, ["Option", "Description", "Advantages", "Disadvantages", "Decision Notes"], option_rows)

    doc.add_heading("7. Recommended Solution", level=1)
    doc.add_paragraph(case.recommended_solution or "TBD")

    doc.add_heading("8. Benefits and Value Case", level=1)
    benefit_rows = [[
        val(b, "name", "benefit", "item"),
        val(b, "type", default="TBD"),
        val(b, "evidence", "evidence_or_assumption", default="TBD"),
        val(b, "measurement", "measurement_approach", default="TBD"),
    ] for b in case.benefits]
    add_table(doc, ["Benefit", "Type", "Evidence / Assumption", "Measurement Approach"], benefit_rows)

    doc.add_heading("9. Costs, Funding, and ROI Considerations", level=1)
    cost_rows = [[
        val(c, "area", "name", "item"),
        val(c, "estimate", default="TBD"),
        val(c, "type", default="TBD"),
        val(c, "notes", default=""),
    ] for c in case.costs]
    add_table(doc, ["Cost Area", "Estimate", "One-time / Ongoing", "Notes"], cost_rows)

    doc.add_heading("10. Risks, Assumptions, and Constraints", level=1)
    risk_rows = []
    for kind, items in [("Risk", case.risks), ("Assumption", case.assumptions), ("Constraint", case.constraints)]:
        for item in items:
            risk_rows.append([
                kind,
                val(item, "item", "name", "risk", "assumption", "constraint"),
                val(item, "impact", default="TBD"),
                val(item, "mitigation", "validation", "response", default="TBD"),
            ])
    add_table(doc, ["Type", "Item", "Impact", "Mitigation / Validation"], risk_rows)

    doc.add_heading("11. Implementation Approach, Milestones, and Ownership", level=1)
    milestone_rows = [[
        val(m, "name", "milestone"),
        val(m, "owner", default="TBD"),
        val(m, "timing", "target", default="TBD"),
        val(m, "notes", default=""),
    ] for m in case.implementation_milestones]
    add_table(doc, ["Milestone", "Owner", "Target Timing", "Notes"], milestone_rows)

    doc.add_heading("12. Governance and Success Measures", level=1)
    doc.add_paragraph(case.governance or "TBD")
    measure_rows = [[
        val(m, "name", "measure"),
        val(m, "baseline", default="TBD"),
        val(m, "target", default="TBD"),
        val(m, "cadence", "review_cadence", default="TBD"),
    ] for m in case.success_measures]
    add_table(doc, ["Measure", "Baseline", "Target", "Review Cadence"], measure_rows)

    doc.add_heading("13. Scope, Stakeholders, and Next Steps", level=1)
    doc.add_heading("Stakeholders", level=2)
    add_bullets(doc, case.stakeholders)
    doc.add_heading("In Scope", level=2)
    add_bullets(doc, case.scope_in)
    doc.add_heading("Out of Scope", level=2)
    add_bullets(doc, case.scope_out)
    doc.add_heading("Next Steps", level=2)
    add_bullets(doc, case.next_steps)
    doc.add_heading("Open Questions", level=2)
    add_bullets(doc, case.open_questions)

    doc.add_heading("14. Critical Professional Counsel", level=1)
    doc.add_paragraph(f"Score: {review.total_score}/{review.max_score}. Readiness: {review.readiness}")
    doc.add_heading("Top Improvements", level=2)
    add_bullets(doc, review.top_improvements)
    doc.add_heading("Criterion Detail", level=2)
    for c in review.criteria:
        doc.add_heading(f"{c.name}: {c.score}/5", level=3)
        doc.add_paragraph(f"Issue: {c.issue}")
        doc.add_paragraph(f"Counsel: {c.counsel}")
        doc.add_paragraph(f"Evidence needed: {c.evidence_needed}")

    doc.add_heading("15. Appendix: Evidence Summary", level=1)
    appendix = evidence_appendix(evidence) if evidence else "No evidence artifacts were provided."
    for line in appendix.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            doc.add_heading(stripped[4:], level=2)
        elif stripped.startswith("Type: "):
            p = doc.add_paragraph()
            run = p.add_run(stripped)
            run.bold = True
        else:
            p = doc.add_paragraph(stripped)
            for run in p.runs:
                run.font.size = Pt(8.5)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
