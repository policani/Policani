# Portfolio Prioritization Scoring Agent

A lightweight, GitHub-ready operating system for portfolio scoring, prioritization, and executive decision support.

This package helps teams move from a pile of approved or proposed initiatives to an explainable portfolio view: what is in the portfolio, how initiatives compare, what is mandatory versus discretionary, where decision rights are unclear, and what trade-offs require human governance.

## What this is

- An agent-readable operating system for project portfolio prioritization.
- A plain-language weighted scoring model with transparent criteria, weights, assumptions, and flags.
- A reusable workflow for intake, scoring, what-if analysis, decision-support briefs, and quality review.
- A small Python CLI that scores synthetic or user-provided portfolio intake data and produces Markdown, HTML, CSV, and JSONL log outputs.

## What this is not

- Not an autonomous funding engine.
- Not a replacement for executive judgment, sponsor authority, finance review, architecture review, legal review, or portfolio board decisions.
- Not a full business case or charter builder. This system assumes upstream business cases, charters, or summaries already exist and works mainly from portfolio metadata and concise initiative summaries.

## Quick start

1. Review `AGENTS.md` to load the agent role, boundaries, and trust model.
2. Fill `config/portfolio_context_template.md` for your organization.
3. Use `prompts/01_initial_portfolio_operating_model_setup.md` to calibrate categories, criteria, weights, and governance cadence.
4. Load initiatives using `templates/portfolio_intake_form.md` or `data/portfolio_intake_schema.csv`.
5. Run the sample scoring flow:

```bash
python tools/score_portfolio.py \
  --input samples/sample_intake_responses/synthetic_portfolio_intake.csv \
  --criteria data/default_scoring_criteria.csv \
  --output-dir samples/generated_markdown \
  --html-dir samples/generated_html \
  --log-dir samples/generated_logs
```

6. Read `samples/generated_markdown/portfolio_decision_support_brief.md` and `samples/generated_html/portfolio_summary.html`.

## Repository layout

| Folder | Purpose |
| --- | --- |
| `config/` | Editable portfolio context and operating assumptions. |
| `docs/` | Operating model, scoring guide, trust model, KPI guide, ingestion guidance, and output guidance. |
| `prompts/` | Reusable agent prompt packs for setup, scoring, what-if analysis, executive briefs, and quality review. |
| `templates/` | Reusable intake, scoring, reporting, rubric, and decision-support templates. |
| `data/` | Default criteria, intake schema, and sample synthetic portfolio data. |
| `tools/` | Reproducible scoring CLI using Python standard library only. |
| `samples/` | Synthetic source artifacts, sample prompts, intake responses, generated outputs, logs, and self-critique. |

## Scoring model summary

The default model uses seven 1-5 scoring criteria:

1. Strategic alignment
2. Financial or mission value
3. Customer or operational impact
4. Risk reduction or compliance criticality
5. Dependency enablement
6. Readiness and confidence
7. Effort or cost feasibility

Each score is multiplied by an explicit weight. The weighted sum is normalized to a 100-point score. Mandatory or regulatory work is flagged separately so the model does not pretend every compliance commitment is purely discretionary.

## Human control principle

The agent may propose scores, expose assumptions, compare trade-offs, and draft decision-support briefs. Final portfolio funding, sequencing, termination, and commitment decisions stay with accountable human leaders.

## Industry alignment notes

The package uses common project portfolio management patterns: portfolio components, strategic alignment, weighted scoring, value-vs-effort thinking, governance cadence, risk and dependency visibility, and decision readiness. It is intentionally simpler than optimization-heavy portfolio tooling so the logic remains explainable and auditable.

Useful external references:

- PMI, The Standard for Portfolio Management: https://www.pmi.org/standards/for-portfolio-management
- PMI, Project Portfolio Management techniques: https://www.pmi.org/learning/library/project-portfolio-management-techniques-7624
- Smartsheet, Project Management Scoring Models: https://www.smartsheet.com/content/project-scoring

## License

No license has been selected. Add a license before publishing this repository publicly.
