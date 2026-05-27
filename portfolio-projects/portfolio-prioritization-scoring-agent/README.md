# Portfolio Prioritization Scoring Agent

A human-governed, AI-assisted portfolio decision-support system for evaluating approved projects and programs through transparent weighted scoring, portfolio metadata, strategic themes, constraints, risks, dependencies, ownership, and executive review artifacts.

This is not a funding engine, autonomous prioritization system, or replacement for a portfolio board. It helps humans structure the conversation, inspect tradeoffs, and make better decisions.

## Operating problem

Organizations often have many approved or proposed initiatives but no consistent way to compare their strategic value, financial contribution, risk, effort, mandatory status, dependencies, and operational impact. The result is noisy prioritization, unclear ownership, overloaded teams, and decisions that are hard to defend later.

This project helps portfolio leaders convert initiative metadata into a visible scoring model and decision-support package.

## Who this is for

- PMO, EPMO, and portfolio leaders
- Program and project leaders
- Business owners and sponsors
- Finance, technology, operations, and product stakeholders
- Knowledge workers who need a structured prioritization model without pretending the AI owns the decision

## What it does

- Defines portfolio categories, criteria, weights, gates, and review cadence
- Normalizes initiative metadata from business cases, charters, spreadsheets, or notes
- Applies transparent weighted scoring
- Separates mandatory and discretionary work
- Surfaces missing owners, unclear decision rights, weak assumptions, risks, and dependencies
- Produces portfolio summaries, scoring matrices, decision briefs, logs, and quality reviews

## What it does not do

- It does not make final funding or sequencing decisions
- It does not replace sponsor, finance, technology, or executive governance review
- It does not create full business cases or project charters
- It does not perform opaque optimization or machine-learning ranking
- It does not require real company data; all examples are synthetic

## How to use this in ChatGPT

Upload only the files inside `chatgpt-project/` when creating a ChatGPT Project. Do not upload the full repository. The other folders provide examples, sample data, templates, generated outputs, workflow diagrams, quality review, and local tooling for GitHub or Codex use.

The runtime folder is flat, self-contained, and designed to stay under the ChatGPT Project file-count limit.

Recommended first prompt after upload:

“Use the runtime instructions and trigger map to help me set up a portfolio prioritization scoring model. Interview me for strategy, initiative categories, scoring criteria, weights, governance cadence, budget/capacity constraints, and decision-rights assumptions. Keep final decisions human-owned.”

## Workflow

```mermaid
flowchart TD
    A[Approved Initiative Metadata
Business case and charter summaries, costs, benefits, owners, risks] --> B[Runtime Intake
Normalize fields, classify initiative type, identify missing data]
    B --> C{Governance Basics Present?}
    C -->|No| D[Clarification Queue
Sponsor, owner, decision rights, assumptions, constraints]
    D --> B
    C -->|Yes| E[Scoring Model Setup
Criteria, weights, gates, mandatory vs discretionary treatment]
    E --> F[Weighted Scoring
Strategic alignment, value, risk, impact, effort, dependencies]
    F --> G[Portfolio Review
Rankings, tradeoffs, constraints, risk/dependency view, KPI summary]
    G --> H{Decision Support Needed?}
    H -->|Yes| I[Executive Decision Brief
Options, tradeoffs, risks, assumptions, open questions]
    H -->|No| J[Portfolio Summary View
Scored matrix, watch items, recommended follow-up]
    I --> K[Human Portfolio Forum
Leaders decide funding, sequencing, acceptance, or deferral]
    J --> K
    K --> L[Decision Log and Follow-up
Record rationale, owners, actions, next review]

```

## Repository structure

- `chatgpt-project/` — flat runtime folder for ChatGPT upload
- `examples/` — synthetic data, sample prompts, sample outputs, and source artifacts
- `templates/` — reusable templates for review outside the runtime folder
- `tools/` — local Python scoring utility
- `workflow/` — Mermaid workflow diagram
- `quality-review/` — senior portfolio manager self-critique

## Human-control model

The system may recommend scoring approaches, identify gaps, calculate weighted scores, summarize tradeoffs, and prepare decision briefs. It must not approve, cancel, fund, sequence, or accept risk on behalf of leaders.
