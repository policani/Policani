# Scoring Reference

Use this file with `project-config.md` and `evidence-map.md`.

## Pre-screen

Before scoring, screen for configured hard stops:
- Work model
- Travel
- Relocation
- Clearance/security/suitability
- Compensation
- Degree/license requirements
- Physical requirements and schedule constraints
- Required tools, equipment, certifications, or licenses
- Domain or role type exclusions

If a hard stop is explicit, return the capped score and one short reason. Do not route variants or cases.

## Base scoring model

Use the ordered `scoring_priority_rules` in `project-config.md`. Convert the user's ordered list into weighting. Higher-ranked rules get more influence.

Recommended default components if the user has not supplied a different model:
- Authority and ownership
- Evidence strength
- Work problem fit
- Scope and scale
- Domain/industry transferability
- Work model and sustainability
- Compensation and level fit
- Seniority/title fit
- Credential, license, or tool match
- Physical requirement and schedule fit

Score as mutual fit, not raw capability.

## Score interpretation

Use thresholds from `project-config.md`. If the config omits thresholds, use:

- Strong: 85-100
- Good fit: 75-84
- Proceed with caution: 65-74
- Stop: 0-64
- Proceed threshold: 65

- Strong: clear apply; resume customization likely sharpens signal.
- Good fit: proceed; name risks.
- Proceed with caution: possible; gaps must be explicit and mitigable.
- Stop: weak fit, structural gap, or outside constraints.

## Required single-role output

First visible line:
`[whole-number]% [Company], [Abbrev Role]`

For scores at or above proceed threshold:
- Resume fit: Insert selected variant filename
- Proof narratives: Insert strongest 1-3 proof narratives, work examples, or missing proof prompts
- Why this resume: 1-2 lines
- Key match strengths: up to 3 bullets
- Primary risks / gaps: up to 2 bullets
- Verdict: Strong | Good fit | Proceed with caution

For caution-band roles add:

| Gap | Evidence Available | Mitigable? |
|---|---|---|
| Insert gap | Insert source evidence or missing evidence | Yes / Partial / No |

## Batch output

Preserve input order. Show only roles at or above proceed threshold.

| Score | Custom lift | Company | Role | Strongest baseline | Apply |
|---|---:|---|---|---|---|

Then show Ignore list for below-threshold, hard-stop, or insufficient-data roles.

## Custom lift

Estimate how much targeted resume work could improve presentation of supported fit.

- +0: baseline already fits or gap is structural
- +1-3: light wording/routing lift
- +4-6: targeted evidence surfacing likely helps
- +7-10: strong evidence exists but baseline undersells a decisive concern
- +11 or more: rare; use only when baseline is badly misrouted but evidence is strong

Never use customization lift to bypass hard stops.
