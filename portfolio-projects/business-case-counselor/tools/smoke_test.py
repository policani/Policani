from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / "examples" / "sample_outputs"
cmd = [
    sys.executable, "-m", "business_case_counselor.cli", "build",
    "--answers", str(root / "examples" / "sample_business_case_input.json"),
    "--evidence", str(root / "examples" / "sample_evidence_inbox"),
    "--out", str(out),
    "--docx", "--html",
]
subprocess.check_call(cmd, cwd=root, env={**__import__('os').environ, "PYTHONPATH": str(root / "src")})
expected = [
    out / "field_service_dispatch_and_parts_readiness_modernization.md",
    out / "field_service_dispatch_and_parts_readiness_modernization.docx",
    out / "field_service_dispatch_and_parts_readiness_modernization.html",
    out / "field_service_dispatch_and_parts_readiness_modernization_maturity_review.md",
]
missing = [p for p in expected if not p.exists()]
if missing:
    raise SystemExit(f"Missing expected outputs: {missing}")
print("Smoke test passed.")
