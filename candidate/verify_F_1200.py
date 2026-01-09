import sys
from pathlib import Path
import importlib.util


def load_module():
    root = Path(__file__).parent
    path = root / 'eval_gates.py'
    spec = importlib.util.spec_from_file_location('candidate.eval_gates', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_tests():
    mod = load_module()
    eval_h = mod.evaluate_hard_gates

    tests = [
        # AI-core required but candidate missing -> fail
        ({'ai_core_required': True}, {'candidate': 'x'}, False, 'ai_core'),
        # Work-mode mismatch -> fail
        ({'work_mode': 'remote'}, {'work_mode': 'onsite'}, False, 'work_mode'),
        # Compensation no overlap -> fail
        ({'compensation': {'min': 100, 'max': 120}}, {'compensation': {'min': 130, 'max': 150}}, False, 'compensation'),
        # Successful pass
        ({'work_mode': ['remote'], 'compensation': {'min': 50, 'max': 150}}, {'work_mode': 'remote', 'compensation': {'min': 60, 'max': 80}}, True, None),
    ]

    for idx, (jp, kp, expect_pass, expect_gate) in enumerate(tests, 1):
        res = eval_h(jp, kp)
        passed = res.get('passed', False)
        if passed != expect_pass:
            print(f"Test {idx} FAILED: expected pass={expect_pass}, got {res}")
            return 2
        if not expect_pass and res.get('failed_gate') != expect_gate:
            print(f"Test {idx} FAILED: expected failed_gate={expect_gate}, got {res}")
            return 3
    print('All gate tests: PASS')
    return 0


if __name__ == '__main__':
    rc = run_tests()
    sys.exit(rc)
