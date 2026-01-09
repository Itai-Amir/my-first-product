import json
from pathlib import Path
from typing import Any


class FrozenList(list):
    def _immutable(self, *args, **kwargs):
        raise TypeError("FrozenList is immutable")

    __setitem__ = __delitem__ = append = extend = insert = pop = remove = clear = sort = reverse = _immutable


class FrozenDict(dict):
    def _immutable(self, *args, **kwargs):
        raise TypeError("FrozenDict is immutable")

    __setitem__ = __delitem__ = pop = popitem = clear = setdefault = update = _immutable


def _freeze(obj: Any) -> Any:
    """Recursively convert lists and dicts into immutable subclasses.

    Uses subclasses of builtins so JSON serialization (which checks for dict/list
    instances) continues to work and deterministic save/load round-trips.
    """
    if isinstance(obj, dict):
        return FrozenDict({k: _freeze(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return FrozenList([_freeze(v) for v in obj])
    return obj


def save_kp(path: str, data: object) -> None:
    """Save knowledge pack deterministically to `path`.

    Deterministic JSON: sort keys, separators without spaces, ensure ASCII false
    to preserve unicode, and UTF-8 encoding.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",",":"))
    p.write_text(text, encoding="utf-8")


def load_kp(path: str) -> object:
    """Load knowledge pack from `path` and return an immutable parsed object."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    obj = json.loads(text)
    return _freeze(obj)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: kp.py <path>")
        raise SystemExit(2)
    obj = load_kp(sys.argv[1])
    print(json.dumps(obj, indent=2, ensure_ascii=False))
