# Artifact Ingestion and Privacy

## Acceptable inputs

- Freeform PMO notes
- Meeting notes
- Stakeholder updates
- Project-plan excerpts
- RAID excerpts
- Decision logs
- Action registers
- CSV tables
- Agenda notes
- Transcript excerpts

## Public-safety rules

For public samples, use synthetic data only. Do not include real employer, client, personal, financial, legal, security, incident, credential, or proprietary data.

## Real-use handling

When users provide real notes:

- treat the content as sensitive;
- avoid repeating unnecessary sensitive details;
- redact names or specifics when asked;
- preserve operational meaning while reducing exposure;
- never expose credentials, secrets, private customer facts, or security incident details.

## Ingestion behavior

If artifacts conflict, state the conflict. Do not silently choose one source unless the user identifies the source of truth.
