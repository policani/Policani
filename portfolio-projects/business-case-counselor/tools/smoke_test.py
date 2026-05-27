from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    out = ROOT / "examples" / "sample_outputs"
    cmd = [
        sys.executable,
        "-m",
        "business_case_counselor.cli",
        "build",
        "--answers",
        "examples/sample_business_case_input.json",
        "--evidence",
        "examples/sample_evidence_inbox",
        "--out",
        str(out),
        "--docx",
    ]
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
        return result.returncode
    expected = [
        out / "customer_support_knowledge_base_modernization.md",
        out / "customer_support_knowledge_base_modernization_maturity_review.md",
        out / "customer_support_knowledge_base_modernization.docx",
    ]
    missing = [str(p) for p in expected if not p.exists()]
    if missing:
        print("Missing expected outputs:", missing)
        return 1
    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
