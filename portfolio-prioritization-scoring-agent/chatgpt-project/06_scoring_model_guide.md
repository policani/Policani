# Scoring Model Guide

## Design goals

The model is designed to be:

- Explainable: every score has a visible criterion, scale, and weight.
- Auditable: assumptions, missing data, and decision changes can be logged.
- Flexible: categories and weights can be calibrated by portfolio type.
- Conservative: mandatory work is flagged rather than hidden inside discretionary ranking.
- Practical: non-specialists can use it without advanced optimization tooling.

## Default formula

```
Normalized Score = (sum(score_i * weight_i) / 5) * 100
```

Where:

- Each criterion score is on a 1-5 scale.
- Each criterion weight is a decimal.
- Active weights must sum to 1.00.
- The final score is expressed on a 0-100 scale.

## Default criteria

| Criterion | Default weight | Plain-language meaning |
| --- | ---: | --- |
| Strategic alignment | 25% | How directly the initiative supports declared strategy. |
| Financial or mission value | 15% | Expected revenue, savings, cost avoidance, mission value, or measurable enterprise benefit. |
| Customer or operational impact | 15% | Degree of customer, employee, operating, service, or process impact. |
| Risk reduction or compliance criticality | 15% | Value of reducing legal, regulatory, security, operational, or business risk. |
| Dependency enablement | 10% | Degree to which the initiative unlocks or protects other important work. |
| Readiness and confidence | 10% | Confidence in scope, sponsorship, estimates, solution approach, and execution readiness. |
| Effort or cost feasibility | 10% | Affordability and execution burden, scored higher when effort is more feasible. |

## Scale anchors

Use a 1-5 scale.

| Score | Meaning |
| ---: | --- |
| 1 | Weak, low, unclear, poor fit, or unsupported. |
| 2 | Limited value or weak evidence. |
| 3 | Moderate value, acceptable evidence, or normal fit. |
| 4 | Strong value, clear evidence, or high fit. |
| 5 | Critical, exceptional, mandatory, or top-tier evidence. |

## Calibration rules

1. Avoid criteria overlap. If strategic alignment and financial value always move together, clarify the difference.
2. Keep the model to 5-8 criteria. More criteria usually creates false precision.
3. Make weights visible and approved by the portfolio board.
4. Use mandatory classification as a portfolio constraint, not just a scoring boost.
5. Use readiness and confidence to prevent weak business cases from ranking too high.
6. Keep cost or effort visible separately even when effort feasibility is scored.
7. Recalibrate quarterly or when strategy changes materially.

## Treatment of mandatory work

Mandatory work should be categorized before discretionary ranking:

- Legal or regulatory requirement
- Safety or security commitment
- Contractual obligation
- Audit finding or remediation commitment
- Executive-committed work already funded or externally promised

Mandatory work can still be scored to understand burden and sequencing, but the brief should separate mandatory commitments from discretionary trade-offs.

## Common anti-patterns

| Anti-pattern | Why it fails | Correction |
| --- | --- | --- |
| Ranking everything in one list | Mandatory and discretionary work get mixed together. | Separate commitments, discretionary choices, and governance holds. |
| Too many criteria | Creates false precision and slows adoption. | Use fewer criteria with clear scale anchors. |
| Unweighted votes | Treats every factor as equally important. | Confirm and document weights. |
| Hidden math | Stakeholders cannot challenge the output. | Show the formula, weights, and score drivers. |
| No confidence flag | Weak data looks as strong as validated data. | Add evidence and confidence ratings. |
| Missing decision rights | Scores exist but nobody owns the decision. | Identify sponsor, owner, and decision authority. |
