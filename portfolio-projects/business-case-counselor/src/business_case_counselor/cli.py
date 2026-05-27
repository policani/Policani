from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .evidence import ingest_evidence
from .interview import run_interview
from .model import BusinessCase
from .render_md import render_business_case_md
from .render_docx import render_business_case_docx
from .review import review_case, review_to_markdown


def load_case(path: Path) -> BusinessCase:
    data = json.loads(path.read_text(encoding="utf-8"))
    return BusinessCase.from_dict(data)


def cmd_init(args) -> None:
    workspace = Path(args.workspace)
    (workspace / "evidence_inbox").mkdir(parents=True, exist_ok=True)
    (workspace / "outputs").mkdir(parents=True, exist_ok=True)
    template = Path(__file__).resolve().parents[2] / "templates" / "business_case_intake.json"
    out = workspace / "business_case_answers.json"
    if template.exists() and not out.exists():
        shutil.copyfile(template, out)
    print(f"Created workspace: {workspace}")
    print(f"Add artifacts to: {workspace / 'evidence_inbox'}")
    print(f"Edit intake file: {out}")


def cmd_interview(args) -> None:
    run_interview(Path(args.out))


def cmd_review(args) -> None:
    case = load_case(Path(args.answers))
    result = review_case(case)
    text = review_to_markdown(result)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)


def cmd_build(args) -> None:
    answers = Path(args.answers)
    evidence_folder = Path(args.evidence) if args.evidence else Path("evidence_inbox")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    case = load_case(answers)
    evidence = ingest_evidence(evidence_folder)
    review = review_case(case)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in case.title.lower()).strip("_") or "business_case"
    md_path = out_dir / f"{safe_name}.md"
    review_path = out_dir / f"{safe_name}_maturity_review.md"
    md_path.write_text(render_business_case_md(case, evidence, review), encoding="utf-8")
    review_path.write_text(review_to_markdown(review), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {review_path}")

    if args.docx:
        docx_path = out_dir / f"{safe_name}.docx"
        render_business_case_docx(case, evidence, review, docx_path)
        print(f"Wrote {docx_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interview, build, mature, and review business case documents.")
    sub = parser.add_subparsers(required=True)

    p_init = sub.add_parser("init", help="Create a workspace")
    p_init.add_argument("--workspace", required=True)
    p_init.set_defaults(func=cmd_init)

    p_interview = sub.add_parser("interview", help="Run the intake interview")
    p_interview.add_argument("--out", required=True)
    p_interview.set_defaults(func=cmd_interview)

    p_review = sub.add_parser("review", help="Review business case maturity")
    p_review.add_argument("--answers", required=True)
    p_review.add_argument("--out")
    p_review.set_defaults(func=cmd_review)

    p_build = sub.add_parser("build", help="Build Markdown and optionally DOCX outputs")
    p_build.add_argument("--answers", required=True)
    p_build.add_argument("--evidence")
    p_build.add_argument("--out", required=True)
    p_build.add_argument("--docx", action="store_true")
    p_build.set_defaults(func=cmd_build)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
