# Business Case Intake Method

## Purpose

The intake method turns an early idea into a usable case brief without over-questioning the user. It should behave like a senior practitioner: extract what is already known, identify the gaps that matter, challenge unsupported root-cause claims, and confirm the situation before drafting.

## Pre-parsing protocol

Before asking questions, map the user's statement against five dimensions:

1. **Problem clarity** — observable symptom, root-cause hypothesis, quantified impact, scope, urgency.
2. **Organizational context** — accountable owner, decision-maker, stakeholders, strategic priorities, leadership urgency.
3. **Financial parameters** — budget ceiling, ROI horizon, cost categories, hard benefits, soft benefits, activity baseline.
4. **Constraints and prior art** — prior attempts, hard constraints, dependencies, deadlines.
5. **Audience and purpose** — primary reader, decision to drive, format/length, likely objection.

Credit what the user already supplied. Ask only what remains unresolved.

## Root-cause challenge

A business case built on the wrong diagnosis usually recommends the wrong solution. Challenge the root cause when the user's input contains a diagnosis stated as fact.

Common false diagnoses:

| Stated diagnosis | What may actually be true |
|---|---|
| We are at capacity | Work-in-progress is distorted, priorities are unmanaged, or capacity is hidden by intake noise |
| The tool does not work | The tool may be exposing a process, data, governance, or discipline problem |
| Teams are not aligned | Decision rights may be unclear, incentives may conflict, or ownership may be fragmented |
| We need more resources | Existing resources may be spread across too many commitments |
| We need automation | The process may not be stable enough to automate responsibly |

Use one targeted root-cause probe before proceeding:

> What observable evidence tells us this is the root cause rather than a symptom?

## Question cap

Ask no more than eight questions in one batch. Group by dimension. Do not ask one question at a time unless the user explicitly requests a live interview.

## Gap severity

| Gap | Severity | Why it matters |
|---|---|---|
| Quantified cost of inaction | Critical | Problem statement is undefendable without stakes |
| Decision-maker identity | Critical | Call to action cannot be specific |
| False diagnosis accepted | Critical | Options analysis may solve the wrong problem |
| Budget ceiling | High | Options may be structurally unrealistic |
| ROI horizon | High | Return model may be framed over the wrong period |
| Scope definition | High | Solution may solve the wrong thing |
| Time-to-dollar translation | High | Cycle-time or labor claims may not survive financial review |
| Compliance baseline | High | Risk case may remain qualitative |
| Strategic alignment | Medium | Case may lack organizational mandate |
| Urgency driver | Medium | No reason to decide now |

## Situation brief

Before drafting, confirm the situation in this format:

```markdown
## Situation Brief — Pre-Draft Confirmation

**Problem:** [Business problem in one sentence.]

**Stakes:** [Cost or consequence of inaction.]

**Scope:** [What is in and out.]

**Audience & Decision:** [Who reads this and what decision it drives.]

**Key Constraints:** [Budget, timing, dependencies, off-limits options.]

**Assumptions carried forward:** [Unvalidated but necessary assumptions.]
```
