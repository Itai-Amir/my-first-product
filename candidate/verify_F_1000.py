import sys
import tempfile
from pathlib import Path
import importlib.util


def load_kp_module():
    # Load candidate/kp.py as a module regardless of package context
    root = Path(__file__).parent
    kp_path = root / "kp.py"
    spec = importlib.util.spec_from_file_location("candidate.kp", str(kp_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    root = Path(__file__).parent
    src = root / "kp_persist.json"
    kp = load_kp_module()
    if not src.exists():
        print(f"Missing source file: {src}")
        return 2

    # Load original bytes
    orig_bytes = src.read_bytes()

    # Parse using load_kp to ensure it's valid JSON
    obj = kp.load_kp(str(src))

    # Write to temp file using deterministic serializer
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tmp_path = Path(tf.name)
    kp.save_kp(str(tmp_path), obj)
    new_bytes = tmp_path.read_bytes()

    if orig_bytes == new_bytes:
        print("Round-trip byte-identical: PASS")
        return 0
    else:
        print("Round-trip byte-identical: FAIL")
        # Show small diff context
        print(f"orig: {len(orig_bytes)} bytes, new: {len(new_bytes)} bytes")
        return 3


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
