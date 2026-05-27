# Business Case Counselor

Business Case Counselor is a GitHub-ready starter project for interviewing, building, maturing, and critically reviewing business case documents.

It combines two layers:

1. **A local document generator** that can ingest source artifacts and produce Markdown, DOCX, and HTML business case outputs.
2. **An agent-readable business case operating system** that guides intake, root-cause challenge, audience framing, financial discipline, options analysis, risk review, and executive-quality decision writing.

The project is designed for business owners, knowledge workers, entry-level through senior managers, software developers, engineers, project leaders, and operators who need to turn early ideas into decision-ready cases.

It is not meant to replace business judgment. It is meant to make judgment easier to apply by forcing weak ideas, missing evidence, vague benefits, unsupported financials, and soft risk language into the open before the document reaches a sponsor, CFO, or governance body.

## What it builds

A complete business case can include:

- Executive summary
- Problem statement and business need
- Root-cause challenge
- Strategic alignment
- Current-state assessment
- Options analysis, including Do Nothing
- Recommended solution
- Cost, benefit, ROI, payback, and sensitivity analysis
- Named risk register with likelihood, impact, mitigation, residual risk, and owner
- Implementation roadmap
- Governance and decision framework
- Recommendation and call to action
- Evidence appendix
- Critical professional counsel / maturity review

## Inputs supported

The evidence ingestion layer can read and summarize:

- Markdown: `.md`
- Plain text: `.txt`
- CSV: `.csv`
- JSON: `.json`
- Word: `.docx`
- Excel: `.xlsx`

Unsupported files are safely ignored. The tool does not claim evidence that is not present. Missing evidence is surfaced as assumptions, open questions, or maturity-review findings.

## Repository structure

```text
business-case-counselor/
  README.md
  AGENTS.md
  docs/
    artifact_intake_guide.md
    audience_framing.md
    business_case_framework.md
    business_case_playbook.md
    github_publish_checklist.md
    intake_method.md
    maturity_model.md
    quality_rubric.md
    review_council.md
  prompts/
    01_adaptive_intake_and_root_cause.md
    02_artifact_synthesis.md
    03_draft_business_case.md
    04_critical_review_council.md
    05_audience_reframe.md
    06_docx_html_export.md
  templates/
    business_case_intake.json
    business_case_template.md
    benefits_costs_template.csv
    assumptions_risks_constraints.csv
    decision_log_template.csv
  src/business_case_counselor/
    cli.py
    evidence.py
    interview.py
    model.py
    render_docx.py
    render_html.py
    render_md.py
    review.py
  examples/
    sample_business_case_input.json
    sample_evidence_inbox/
    sample_prompts/
    sample_outputs/
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Use the CLI

Create a workspace:

```bash
business-case-counselor init --workspace ./work/my_case
```

Edit the generated `business_case_answers.json`, then add supporting artifacts to `evidence_inbox/`.

Build Markdown, DOCX, and HTML outputs:

```bash
business-case-counselor build \
  --answers ./work/my_case/business_case_answers.json \
  --evidence ./work/my_case/evidence_inbox \
  --out ./work/my_case/outputs \
  --docx \
  --html
```

Run a maturity review only:

```bash
business-case-counselor review \
  --answers ./work/my_case/business_case_answers.json \
  --out ./work/my_case/outputs/maturity_review.md
```

## Use with an AI agent

The project also includes agent-readable instructions and prompt packs. Start with:

- `AGENTS.md`
- `docs/intake_method.md`
- `docs/business_case_framework.md`
- `docs/quality_rubric.md`
- `docs/audience_framing.md`
- `prompts/01_adaptive_intake_and_root_cause.md`

Recommended workflow:

1. Intake the idea and source artifacts.
2. Challenge the stated root cause before accepting it.
3. Confirm the situation brief.
4. Draft the business case in dependency order.
5. Review against the seven-dimension quality rubric.
6. Revise weak sections only.
7. Export Markdown, DOCX, or HTML.

## Sample outputs

See `examples/sample_outputs/` for a complete dummy-data business case generated in:

- Markdown
- DOCX
- HTML

See `examples/sample_prompts/` for a prompt pack in:

- Markdown
- DOCX
- HTML

All sample data is fictional and exists only to demonstrate the workflow.

## Design principles

- Start with the business problem, not the requested solution.
- Challenge symptoms before treating them as root causes.
- Separate hard financial benefits from soft directional benefits.
- Include a genuine Do Nothing option with cost of inaction.
- Treat risks as named failure modes, not categories.
- Make the decision request specific: who decides, what they approve, by when, and what happens if delayed.
- Keep the final document readable for executives and actionable for operators.

## License

MIT
