# Project Charter Initiation Agent

**A PMBOK® Guide-aligned, agent-assisted project initiation system for developing sponsor-ready project charters from business cases, notes, spreadsheets, project plans, CSVs, Word documents, stakeholder inputs, and source artifacts.**

Project Charter Initiation Agent helps business owners, project managers, program leaders, software teams, engineers, and knowledge workers move from an early idea or approved business case to an initiation-ready project charter. It behaves like a senior project initiation and governance advisor: it interviews the user, challenges vague scope, separates objectives from deliverables, identifies missing sponsors and decision rights, clarifies assumptions and constraints, defines success measures, and produces polished outputs in Markdown, HTML, and DOCX.

The charter does **not** reargue the business case. It establishes authorization, scope, ownership, execution guardrails, governance rhythm, escalation paths, change-control discipline, and the milestone path from initiation into planning and execution.

> This project uses PMBOK® Guide-aligned terminology and project initiation practices. It is not affiliated with, sponsored by, or endorsed by PMI.

## Search terms

Project charter template, project initiation, PMBOK Guide aligned, PMP, project governance, project management, stakeholder register, business case, scope definition, assumptions log, risk register, dependency log, RACI, change control, sponsor approval, project manager authority, project planning, AI agent, agentic workflow, Markdown, HTML, DOCX.

## Suggested GitHub topics

```text
project-management
project-charter
project-initiation
pmbok
pmp
project-governance
stakeholder-management
risk-management
change-control
raci
business-case
ai-agent
agentic-workflow
markdown
docx
html
```

## What this system produces

The final charter must answer:

- Why the project exists
- What business outcome it supports
- Who sponsors and owns it
- What is in scope and out of scope
- What deliverables are authorized
- What success measures will be used
- What assumptions and constraints govern the work
- What risks, dependencies, and open decisions must be managed
- What governance rhythm, escalation path, and change-control model will be used
- What milestone path moves the project from initiation into planning and execution

## Who this is for

This repository is designed for:

- Business owners and operational leaders who need to frame a project before committing teams and money
- Knowledge workers and managers who need a plain-language structure for project initiation
- Project managers, program managers, PMOs, and portfolio leaders who need governance-ready charter discipline
- Software developers, engineers, product leaders, and technology teams who need clear scope, decision rights, assumptions, dependencies, and delivery guardrails
- Sponsors and steering committees that need a concise authorization artifact before detailed planning begins

The language is intentionally accessible for non-specialists, structured enough for governance review, and rigorous enough to survive sponsor, delivery, finance, technology, legal, compliance, and operational scrutiny.

## What “PMBOK® Guide-aligned” means here

This package follows recognizable project initiation terminology and practices commonly associated with PMI/PMBOK-style project management:

- Project charter
- Project sponsor
- Business case linkage
- Project manager authority
- Stakeholder identification
- High-level scope definition
- Assumptions and constraints
- High-level risks and dependencies
- Success criteria
- Governance, escalation, and change control
- Transition from initiation into planning and execution

It is not a certification product, exam-prep product, or official PMI artifact. The phrase “PMBOK® Guide-aligned” is used descriptively to help practitioners recognize the project management model this package supports.

## Repository structure

```text
.
├── AGENTS.md                              # Agent-readable operating instructions
├── README.md                              # Human-facing overview, quick start, and GitHub discoverability language
├── config/                                # Machine-readable schemas, rubrics, defaults, and question banks
├── docs/                                  # Method guides and operating model
├── prompts/                               # Reusable prompt pack for agent-assisted project initiation
├── templates/                             # Charter, review, intake, stakeholder, risk, dependency, and success-measure templates
├── scripts/                               # Local generator and validator
├── examples/fictional-customer-onboarding-control-tower/
│   ├── sample_prompts/                    # Prompts used for the test scenario
│   ├── intake_responses/                  # Fictional user answers
│   ├── source_artifacts/                  # Dummy notes, CSVs, XLSX, DOCX, and plan excerpts
│   ├── generated_markdown/                # Generated charter in Markdown
│   ├── generated_html/                    # Generated charter in HTML
│   ├── generated_docx/                    # Generated charter in DOCX
│   └── quality_review/                    # Charter quality review and gap analysis
└── tests/self_test/                       # Self-test procedure and results
```

## Quick start: agent workflow

1. Open `AGENTS.md` and use it as the system or project instruction file for your agent.
2. Drop source artifacts into an evidence folder or paste them into the chat.
3. Start with `prompts/00_master_operating_prompt.md`.
4. Use `prompts/01_artifact_ingestion_prompt.md` to summarize and tag evidence.
5. Run `prompts/02_adaptive_intake_prompt.md` to fill missing initiation facts.
6. Run the challenge prompts for scope, authority, success measures, risks, dependencies, assumptions, and governance.
7. Generate the charter with `prompts/07_charter_generation_prompt.md`.
8. Review it with `prompts/08_charter_quality_review_prompt.md`.
9. Package outputs with `prompts/09_output_generation_prompt.md`.

## Quick start: local sample generator

The local script can regenerate the fictional sample from the included JSON data:

```bash
pip install -r requirements.txt
python scripts/generate_charter.py \
  --input examples/fictional-customer-onboarding-control-tower/source_artifacts/structured_intake.json \
  --out-dir examples/fictional-customer-onboarding-control-tower

python scripts/validate_charter.py \
  --charter examples/fictional-customer-onboarding-control-tower/generated_markdown/project_charter.md \
  --rubric config/quality_rubric.json
```

Or run the included self-test:

```bash
make self-test
```

## Operating model

The system works in four layers:

1. **Artifact intake** — source materials are inventoried, summarized, tagged, and classified as facts, assumptions, conflicts, or gaps.
2. **Adaptive project initiation interview** — the agent asks only the highest-leverage questions needed to make the charter initiation-ready.
3. **Governance and scope challenge** — the agent tests sponsor authority, ownership, decision rights, scope boundaries, success measures, constraints, risks, dependencies, and change-control thresholds.
4. **Charter generation and quality review** — the agent produces Markdown, HTML, and DOCX outputs and reviews the charter against a readiness rubric.

## Design principles

- **Authorization over advocacy:** the charter references the approved business case; it does not sell the project again.
- **Initiation over planning detail:** the charter defines the why, what, who, boundaries, constraints, and governance model; the project plan defines detailed execution.
- **Plain language over process theater:** every section must make execution clearer.
- **Specificity over volume:** vague scope, unnamed decision rights, and generic success criteria are defects.
- **Evidence-bound outputs:** the agent must distinguish known facts, assumptions, open questions, and proposed decisions.
- **Critical guidance built in:** the agent should challenge weak framing instead of merely formatting user input.
- **Governance that can operate:** the charter must define rhythm, thresholds, escalation, and change control.

## What “initiation-ready” means

A charter is initiation-ready when:

- A sponsor can approve it
- A project owner or project manager can use it to enter detailed planning
- Finance can understand funding boundaries
- Technology and operations can see constraints and dependencies
- Governance bodies can tell how decisions will be made
- Scope, success measures, risks, dependencies, and open decisions are explicit enough to manage

## Included sample scenario

The repository includes a complete fictional test case: **Customer Onboarding Control Tower Modernization**.

The sample includes:

- Raw project idea prompt
- Artifact-ingestion prompt
- Sample intake responses
- Business case summary
- Stakeholder notes
- Budget CSV
- Stakeholder-role CSV
- Risk, dependency, and open-decision CSV
- Delivery-plan excerpt
- Structured JSON intake
- XLSX budget and milestone workbook
- Generated Markdown charter
- Generated HTML charter
- Generated DOCX charter
- Charter quality review

## Local validation

Use the validator to check whether the generated charter contains the required initiation signals:

```bash
python scripts/validate_charter.py \
  --charter examples/fictional-customer-onboarding-control-tower/generated_markdown/project_charter.md \
  --rubric config/quality_rubric.json
```

The validator is intentionally lightweight. It does not prove that a charter is sponsor-approved or execution-ready. It checks for required content signals and should be paired with the quality review prompt.

## License

MIT License.
