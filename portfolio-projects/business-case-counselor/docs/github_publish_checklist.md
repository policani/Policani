# GitHub Publish Checklist

Use this checklist before publishing the repository.

## Repository readiness

- README explains the tool, audience, install path, and fast start.
- `AGENTS.md` explains how AI agents should interview, challenge, mature, and review the case.
- Templates are editable and do not contain private data.
- Example artifacts are generic.
- Sample outputs demonstrate both Markdown and DOCX output.
- The package can run with `PYTHONPATH=src python -m business_case_counselor.cli ...`.
- `requirements.txt` and `pyproject.toml` are aligned.
- License is present.

## Quality readiness

- Business case includes “do nothing.”
- The maturity model penalizes missing evidence.
- Critical review counsel is direct and actionable.
- Benefits and ROI claims are not invented by the tool.
- The decision request appears near the front.
- DOCX output uses headings and tables.

## Suggested first commit

```bash
git init
git add .
git commit -m "Initial business case counselor package"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
