# Business Case Counselor

Business Case Counselor is a GitHub-ready starter package for interviewing, building, maturing, and critically reviewing business case documents.

It is designed for business owners, knowledge workers, entry-to-senior managers, software developers, engineers, PMO/portfolio teams, and delivery leaders who need a disciplined decision document before project initiation.

A business case answers one executive question:

> Should we fund, start, change, defer, or reject this initiative based on the problem, options, costs, benefits, risks, and recommended path?

## What this package does

- Interviews the user through a structured business-case intake.
- Solicits artifacts: ideas, notes, `.md`, `.txt`, `.csv`, `.json`, `.docx`, `.xlsx`, exported project plans, and related evidence.
- Builds an evidence-grounded business case in Markdown.
- Generates a richly formatted Word document when `python-docx` is installed.
- Scores maturity across decision-quality criteria.
- Provides critical professional counsel from multiple review lenses: sponsor, finance, operations, technology, delivery, risk, and user/customer impact.
- Preserves the business case as the baseline for project charter, funding approval, portfolio prioritization, and later governance checks.

## Core mental model

```text
current state -> gap -> options -> recommendation -> value -> risk -> action
```

## Repository structure

```text
business-case-counselor/
├── AGENTS.md
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/business_case_counselor/
│   ├── cli.py
│   ├── evidence.py
│   ├── interview.py
│   ├── model.py
│   ├── render_docx.py
│   ├── render_md.py
│   └── review.py
├── templates/
│   ├── business_case_template.md
│   ├── business_case_intake.json
│   ├── decision_log_template.csv
│   ├── assumptions_risks_constraints.csv
│   └── benefits_costs_template.csv
├── prompts/
│   ├── 01_business_case_interview.md
│   ├── 02_artifact_synthesis.md
│   ├── 03_critical_review_council.md
│   └── 04_docx_formatting_guardrails.md
├── docs/
│   ├── artifact_intake_guide.md
│   ├── business_case_playbook.md
│   ├── maturity_model.md
│   └── review_council.md
└── examples/
    ├── sample_business_case_input.json
    ├── sample_evidence_inbox/
    └── sample_outputs/
```

## Install

```bash
git clone <your-repo-url>
cd business-case-counselor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The Markdown path works with the Python standard library. DOCX export requires `python-docx`. XLSX evidence extraction requires `openpyxl`.

## Fast start

Generate the sample business case:

```bash
python -m business_case_counselor.cli build \
  --answers examples/sample_business_case_input.json \
  --evidence examples/sample_evidence_inbox \
  --out examples/sample_outputs \
  --docx
```

Create a blank workspace for a new case:

```bash
python -m business_case_counselor.cli init --workspace work/my_case
```

Run the interview questions:

```bash
python -m business_case_counselor.cli interview --out work/my_case/business_case_answers.json
```

Build outputs:

```bash
python -m business_case_counselor.cli build \
  --answers work/my_case/business_case_answers.json \
  --evidence work/my_case/evidence_inbox \
  --out work/my_case/outputs \
  --docx
```

Review an existing answer file:

```bash
python -m business_case_counselor.cli review --answers work/my_case/business_case_answers.json
```

## Artifact intake

Place supporting materials in `evidence_inbox/`. Supported first-pass ingestion:

| Type | Use |
|---|---|
| `.md`, `.txt` | Notes, pasted discovery, meeting notes, strategy excerpts |
| `.csv` | Cost tables, benefit estimates, risk logs, stakeholder lists |
| `.json` | Structured inputs, exported forms |
| `.docx` | Existing drafts, business requirements, project summaries |
| `.xlsx` | Cost models, inventories, estimates, prioritization data |

For project plans, export summary data to `.csv` when possible. Proprietary binary project formats vary by tool and are intentionally not parsed by default.

## Quality gates

Before a business case is ready for leadership, it should pass these gates:

1. The problem is specific enough to approve or reject.
2. The current-state pain includes evidence or quantified impact where possible.
3. At least three options are compared, including “do nothing.”
4. The recommendation is clear and falsifiable.
5. Costs, benefits, assumptions, constraints, and risks are explicit.
6. The decision request is actionable: approve, reject, fund discovery, defer, or request more evidence.
7. The implementation path has owners, milestones, and governance hooks.
8. The case states what evidence would change the recommendation.

## Intended use

Use this package when an idea needs approval, funding, prioritization, or governance sign-off, especially where the work affects strategy, budget, people, technology, risk, or operating model change.

If approved, the business case typically feeds project initiation, the project charter, funding approval, portfolio prioritization, detailed planning, and requirements work.

## License

MIT. See `LICENSE`.
