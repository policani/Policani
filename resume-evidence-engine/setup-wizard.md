# Setup Wizard

Use this file when the user runs `/setup` or asks for first-time configuration help.

## Setup rule

Do not score roles or write employer-facing materials during setup. The goal is to build the user's evidence system first.

## Configuration interview rules

The preferred first step is to open `builders/config-builder.html` locally, answer the form questions, export `project-config.md`, and replace the starter config file before upload. The builder contains the detailed explanations, controlled choices, and binary settings so the uploaded config can stay small.

When helping inside the project, treat `project-config.md` as the generated value file:

- `Value:` is the user's answer.
- `Priority [number] value:` is the scoring tradeoff order.
- Any answer containing `Insert` is incomplete. Name the setting and line number.
- `Yes` / `No` fields are binary.
- `Required`, `Prefer`, and `Flexible` fields control how hard the engine treats the constraint.
- Values beginning `custom:` are user-written rules. Ask for clarification if they conflict with other settings.

If the user does not understand a setting, explain the practical effect and recommend a safe default. Do not silently choose for them unless they ask for defaults.


## Interview sequence

### 1. Identity and contact
Ask for:
- Name
- Preferred name
- City/state/country
- Phone
- Email
- LinkedIn URL
- Portfolio/case-study URL, if any
- Work authorization constraints
- Time zone

Update recommendation: `project-config.md` Candidate contact section.

### 2. Search and work constraints
Ask for:
- Target roles, as a comma-delimited list
- Target audiences, as a comma-delimited list
- Target role families
- Target titles
- Seniority level
- Desired employment types
- Work model requirements
- Travel limits
- Relocation limits
- Geography limits
- Compensation range
- Industries to include or exclude
- Role types to include or exclude
- Non-negotiable hard stops

Use broad examples so the system does not assume a technology or office-worker audience:
- Target roles: `maintenance technician, facilities maintenance, apartment maintenance, equipment repair`
- Target audiences: `property managers, facilities supervisors, plant managers, school districts, homeowners, hiring managers`
- Target role families: `skilled trades, facilities and maintenance, customer service, healthcare support, office administration, operations, technology`

When an answer could be either a preference or a hard stop, ask which it is. Example: `Remote preferred` is not the same as `Reject non-remote roles`.

Update recommendation: regenerate `project-config.md` with `builders/config-builder.html`, or edit the matching Job-search target and Constraints sections directly.

### 3. Scoring priorities
Ask the user to rank what matters most. Suggested categories:
- Authority and ownership
- Evidence strength
- Work problem fit
- Scope and scale
- Compensation
- Work model
- Travel burden
- Domain fit
- Seniority/title fit
- Growth potential
- Mission, product, service, or workplace interest
- Learning curve
- Credential match
- License or certification match
- Physical requirements fit
- Schedule fit
- Safety record or reliability
- People leadership

Convert the user's ranking into the `project-config.md` Scoring priority order.

### 4. Resume and output settings
Ask for:
- Page target and maximum page count
- Whether functional title clarification is allowed when truthful
- How many optional proof links may appear
- Credential inclusion policy
- Hyperlink policy
- Confirm that final resumes and cover letters are Markdown first, then DOCX
- DOCX renderer mode and density; safe defaults are `fast` and `auto`
- Cover letter default
- Cover letter length
- Salutation and signature block

Explain high-friction settings before the user answers:

**Hyperlink policy:** controls links in employer-facing materials. Safe default is `contact only`. Use `contact and portfolio` only when public proof is part of the strategy. Use `none` when plain ATS ingestion is the only priority.

**Allowed title adjustment policy:** controls whether generic official titles may be clarified into truthful functional titles. Safe default is `Functional titles allowed when truthful` only if the user can defend the title in an interview.

**Credential inclusion policy:** controls whether credentials appear by default. Safe default is `Include role-relevant credentials`.

**DOCX handoff policy:** completed final Markdown resumes and cover letters should be rendered to Word documents when the agent environment supports it. Rendering is a separate conversion step; it should not rewrite the content.

Update recommendation: regenerate `project-config.md` with `builders/config-builder.html`, or edit the Output behavior section directly.

### 5. Canonical resume build
Ask for complete factual work history:
- Employer
- Actual title
- Functional title, if different and truthful
- Location
- Dates
- Scope
- Teams led or influenced
- Budgets, revenue, portfolio size, risk, customer scale, or other stakes
- Tools and systems
- Outcomes
- Promotions or expanding responsibility
- Reason for leaving only if useful

Update recommendation: `core-canonical-resume.md`.

If the user wants form-based help, tell them to open `builders/resume-builder.html` and export a Markdown resume file. The builder can create a core canonical resume, a variant resume, or a final targeted resume without requiring installs or command-line work.

### 6. Evidence inventory
Ask the user to identify 6-12 strongest proof points:
- A repair, service, delivery, or quality story
- A transformation or turnaround
- A scale, volume, or growth story
- A financial outcome
- A risk, compliance, or governance story
- A customer or partner outcome
- A technical delivery or launch outcome
- A safety, inspection, maintenance, or reliability outcome
- A scheduling, response-time, or service-recovery outcome
- A people leadership example
- A strategic planning example
- An operating model, workflow, or process redesign

Update recommendation: `evidence-map.md` and proof narrative templates.

### 7. Variant selection
Help the user choose two primary resume lanes. Examples:
- Skilled trades / maintenance
- Facilities / property operations
- Manufacturing / warehouse / logistics
- Healthcare support / patient services
- Office administration / coordination
- Retail / hospitality / customer service
- Field service / route service
- Supervisory / team lead roles
- Technology / systems support
- Program / project / business operations

Update recommendation: rename and complete the two variant templates.

### 8. Credentials and education
Ask for:
- Degrees completed
- College coursework without degree, if relevant
- Certifications, active or expired
- Licenses
- Coursework
- Technical training
- Credential URLs or proof locations
- Any credentials that should not be used

Update recommendation: `ref-credentials.md`.

### 9. Positioning issues
Ask about known gaps:
- No degree
- Industry change
- Title inflation risk
- Contractor/vendor roles
- P&L adjacency versus direct ownership
- Recent people-management gap
- Domain depth concerns
- Compensation or level mismatch
- Employment gaps
- Relocation/travel/work model constraints

For each issue, ask what is true, what must not be claimed, and what evidence can be used to offset the concern.

Update recommendation: `ref-positioning.md`.

### 10. DOCX handoff check
Confirm whether the current agent environment can render DOCX files using the included renderer files. Do not ask the user to install Python, Git, LibreOffice, PDF tools, or local packages.

If rendering is available, the agent may create a DOCX from `sample_resume.md` or `sample_cover_letter.md` as an internal smoke test. If rendering is unavailable, tell the user the project can still score roles and draft final Markdown, but DOCX output depends on a supported agent runtime.

### 11. Final setup checklist
Before regular use, confirm:
- `project-config.md` has no placeholder values on configurable answer lines.
- All values are clear controlled choices or valid `custom:` rules.
- Canonical resume contains factual history only.
- Two variants are completed.
- Evidence map routes the user's top capabilities.
- At least two proof narratives are complete.
- Credentials are accurate and not overstated.
- Positioning file names real gaps and approved arguments.
- `md2docx_resume_flat.py`, `reference.docx`, and `md2docx-workflow.md` are available if DOCX handoff is enabled.

When every checklist item is true, update `project-config.md` so `Setup status` is `Complete`. Until then, leave it as `In Progress`; normal scoring and employer-facing drafting should remain blocked.
