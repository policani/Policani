from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validate_charter', ROOT / 'scripts' / 'validate_charter.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_sample_charter_passes_required_signals():
    charter = ROOT / 'examples' / 'fictional-customer-onboarding-control-tower' / 'generated_markdown' / 'project_charter.md'
    results = module.validate(charter.read_text(encoding='utf-8'))
    assert all(item['status'] == 'pass' for item in results)
