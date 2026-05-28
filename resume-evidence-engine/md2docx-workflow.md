# MD-to-DOCX Workflow

Use this file when a final resume or cover letter exists as Markdown and the user wants a Word document.

## Purpose

Conversion is a rendering step. Do not rewrite, tailor, score, or improve the career content during conversion. The source Markdown owns content and structure. The renderer owns Word layout, spacing, typography, bullets, hyperlinks, and validation.

## User setup rule

Do not ask first-time users to install Python, Git, LibreOffice, PDF tools, or local packages. The included renderer files are for Codex or another capable agent to inspect and run when its managed environment supports execution.

Run the renderer from the project root, or pass an explicit output path. The renderer resolves its default config and Word template beside `md2docx_resume_flat.py`, but relative output paths are still created from the current working directory.

If rendering is unavailable, provide the final Markdown and say DOCX rendering cannot be completed in the current environment. Do not claim a DOCX was created.

PDF export is out of scope for this project.

## Required files

- `md2docx_resume_flat.py` - renderer CLI for agent-managed execution.
- `renderer-config.json` - renderer defaults and validation settings.
- `reference.docx` - Word style template.
- a completed resume or cover-letter `.md` source file.

Optional safe fixtures:

- `sample_resume.md`
- `sample_cover_letter.md`

## Trigger rules

Run DOCX conversion when any of these is true:

- the user asks for DOCX, Word, render, convert, final document, final resume, final cover letter, or download;
- `Default output workflow` is `Markdown first, then DOCX` and final resume or cover-letter Markdown exists;
- `Final resume DOCX handoff` is `Yes` and a final resume Markdown file has been generated;
- `Final cover letter DOCX handoff` is `Yes` and a final cover-letter Markdown/text file has been generated.

Do not render during scoring, early drafting, or analysis unless the user asks.

## Resume Markdown contract

- First `#` heading is the candidate name.
- Later `#` headings are resume sections.
- `##` headings under sections are roles, projects, or subsections.
- `-` or `*` list items become Word-native bullets.
- `[label](url)` becomes a clickable Word hyperlink displaying only `label`.
- Do not use tables, text boxes, columns, images, or decorative layout for resumes.

## Cover-letter Markdown contract

- May begin directly with `Hiring team,`.
- Do not add sender/contact/date blocks unless they are already in the source.
- Paragraphs render as business-letter body text.
- Bullets render only when explicitly present.

## Employer-facing filenames

Use human-readable output names:

- `Candidate Name - Resume - Company, Abbrev Role.docx`
- `Candidate Name - Cover Letter - Company, Abbrev Role.docx`

## Validation gates

Reject or revise output if:

- literal Markdown bullets such as `-` remain visible;
- Markdown link syntax remains visible;
- raw URLs appear instead of labeled hyperlinks, except intentionally visible URLs;
- hyperlinks are missing or broken;
- resume output contains tables, columns, text boxes, images, or drawing objects;
- sections collapse together or reading order becomes unclear;
- the DOCX artifact is missing, empty, or not a valid package.

## Page-count policy

Do not use PDF export or page-image rendering in the default workflow. If a platform cannot inspect page count directly, keep the Markdown clean and let the final DOCX be the deliverable.
