# GitHub Upload Checklist

Use this checklist before publishing the beta project to GitHub.

## Before Uploading

- Confirm the repository contains only templates, instructions, builder files, renderer files, fictional samples, and public documentation.
- Do not upload real resumes, cover letters, proof narratives, credentials, references, job preferences, or generated application materials.
- Confirm `outputs/`, `__pycache__/`, `.pyc` files, QA reports, ZIP files, and generated DOCX files are absent. Exception: keep the fictional sample DOCX in `docs/sample-builder-outputs/`.
- Keep `reference.docx`; it is the renderer's Word style template.
- Keep `docs/workflow-flowchart.pdf`; it is the lightweight workflow diagram.

## Recommended First Repository Settings

- Repository visibility: public only if the package contains no private career material.
- Repository name: use a short lowercase name, such as `resume-evidence-engine`.
- Description: `Resume Evidence Engine: evidence-bound workflow for agent-assisted scoring, resume drafting, cover letters, and DOCX handoff.`
- Add topics such as `job-search`, `resume`, `cover-letter`, `markdown`, `docx`, `codex`, and `career-tools`.

## Simple Upload Path

1. Create a new repository on GitHub.
2. Upload the cleaned contents of this folder.
3. Confirm GitHub shows `README.md` on the repository home page.
4. Confirm `LICENSE` appears in the repository file list.
5. Open `docs/workflow-flowchart.pdf` from GitHub and verify it renders.
6. Open `docs/readme.html` from GitHub and verify the readable guide renders.
7. Ask one beta tester to follow the README from a fresh download.

## Before Each Beta Release

- Re-read `README.md` and make sure every included file is listed in the file map.
- Run one sample DOCX render in a managed agent runtime when available, and keep only the intentional fictional sample DOCX if publishing it as an example.
- Confirm `AGENTS.md` is current. If a beta tester uses a platform that expects `CLAUDE.md`, tell them to copy or rename `AGENTS.md` locally for that platform.
- Confirm no real user data was added to source templates or samples.
