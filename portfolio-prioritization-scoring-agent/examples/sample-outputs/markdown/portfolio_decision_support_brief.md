# Portfolio Decision-Support Brief

Generated from synthetic data. This is an advisory output, not a funding decision.

## Executive summary

The synthetic portfolio contains **4 initiatives** with estimated spend of **$6,100,000** and delivery demand of **189 FTE-months**. One mandatory compliance initiative should be protected and sequenced through governance. The highest scoring discretionary items are strong but require explicit funding and capacity trade-offs. One platform initiative is on governance hold because sponsor and decision authority are missing.

## Scoring model and weights

| Criterion | Weight |
| --- | ---: |
| Strategic alignment | 25% |
| Financial or mission value | 15% |
| Customer or operational impact | 15% |
| Risk reduction or compliance criticality | 15% |
| Dependency enablement | 10% |
| Readiness and confidence | 10% |
| Effort or cost feasibility | 10% |

## Ranked portfolio view

| Rank | ID | Initiative | Category | Mandatory status | Score | Confidence | Recommendation | Flags |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | P-003 | Field Service Scheduling Automation | Operational Efficiency | Discretionary | 80.0 | High | Prioritize | None |
| 2 | P-002 | Self-Service Revenue Portal Expansion | Growth / Revenue | Discretionary | 79.0 | High | Board trade-off - high value but material funding or capacity burden | None |
| 3 | P-001 | Data Retention Compliance Remediation | Regulatory / Mandatory | Mandatory | 71.0 | Medium | Mandatory commitment - protect capacity and sequence through governance | None |
| 4 | P-004 | Data Lake Migration Foundation | Technology Foundation | Unknown | 57.0 | Low | Hold for governance clarity | Missing or unclear sponsor; Missing or unclear decision authority; Missing or unclear mandatory status |

## Mandatory commitments

| Rank | ID | Initiative | Category | Mandatory status | Score | Confidence | Recommendation | Flags |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | P-001 | Data Retention Compliance Remediation | Regulatory / Mandatory | Mandatory | 71.0 | Medium | Mandatory commitment - protect capacity and sequence through governance | None |

## Discretionary prioritization view

| Rank | ID | Initiative | Category | Mandatory status | Score | Confidence | Recommendation | Flags |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | P-003 | Field Service Scheduling Automation | Operational Efficiency | Discretionary | 80.0 | High | Prioritize | None |
| 2 | P-002 | Self-Service Revenue Portal Expansion | Growth / Revenue | Discretionary | 79.0 | High | Board trade-off - high value but material funding or capacity burden | None |

## Budget and capacity view

| Metric | Value |
| --- | ---: |
| Total estimated spend | $6,100,000 |
| Total estimated capacity | 189 FTE-months |
| Governance holds | 1 |

## Spend by strategic theme

| Strategic theme | Estimated spend |
| --- | ---: |
| Data Quality and Scale | $2,100,000 |
| Customer Growth | $1,850,000 |
| Trust and Resilience | $1,200,000 |
| Operational Leverage | $950,000 |

## Risk distribution

| Risk rating | Count |
| --- | ---: |
| High | 2 |
| Medium | 2 |

## Dependency and overload observations

- P-001 depends on legal interpretation and archive platform upgrade.
- P-002 depends on identity roadmap and billing API readiness.
- P-003 depends on mobile workforce data cleanup.
- P-004 depends on cloud landing zone, security architecture review, and downstream migration planning.
- Current total demand exceeds a common small-portfolio constraint scenario of $3.0M and 80 FTE-months, so sequencing is required.

## Scenario option - $3.0M and 80 FTE-months

Recommended advisory posture:

1. Protect P-001 as mandatory compliance work, subject to deadline and dependency validation.
2. Sequence P-003 next if the portfolio board wants near-term operational value with lower cost and capacity burden.
3. Treat P-002 as a high-value board trade-off because it has strong growth value but material funding and dependency load.
4. Hold P-004 until sponsor, decision authority, and mandatory status are clarified.

## Human decisions required

| Decision | Recommended owner | Evidence needed | Consequence of delay |
| --- | --- | --- | --- |
| Protect mandatory delivery capacity for P-001 | Portfolio Board | Confirm deadline, capacity, and dependency plan | Compliance exposure remains unresolved. |
| Resolve governance ownership for P-004 | Portfolio Board / sponsoring executive | Named sponsor and decision authority | Item remains unsuitable for funding decision. |
| Decide near-term sequencing for P-002 | Portfolio Board | Funding/capacity trade-off and dependency readiness | High-value work may crowd out other priorities. |

## Decision log reference

See `/mnt/data/portfolio-prioritization-scoring-agent/samples/generated_logs/scoring_run_log.jsonl` for the generated scoring log.
