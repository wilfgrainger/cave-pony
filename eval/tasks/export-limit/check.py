import re
from export import export
items = [{"id": n, "name": f"n{n}"} for n in range(5)]
assert export(items) == ["0,n0", "1,n1", "2,n2", "3,n3", "4,n4", "# exported 5"]
out = export(items, max_items=2)
assert out[:2] == ["0,n0", "1,n1"] and len(out) == 3, out
assert "exported 2" in out[-1] and re.search(r"\b3\b", out[-1]) and "skip" in out[-1].lower(), out[-1]
out = export(items, max_items=0)
assert len(out) == 1 and "exported 0" in out[0] and re.search(r"\b5\b", out[0]), out
assert export(items, max_items=10)[-1] == "# exported 5"
assert export([], max_items=3) == ["# exported 0"]
