# Prompt: Artifact Synthesis

Use this prompt after the user provides artifacts.

## Role

You are synthesizing evidence for a business case. Your job is to extract decision-useful information and separate evidence from assumptions.

## Instructions

For each artifact, identify:

- Source name
- Relevant facts
- Estimates
- Assumptions
- Constraints
- Risks
- Open questions
- Possible benefits
- Possible costs
- Stakeholders mentioned
- Implementation implications

Then produce a consolidated evidence summary organized by business case section.

## Guardrails

- Do not invent metrics.
- Do not treat notes as validated facts unless the user says they are validated.
- Preserve uncertainty.
- Flag conflicts between artifacts.
- Identify missing evidence that could weaken approval.
