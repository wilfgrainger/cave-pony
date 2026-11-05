from process import process
from report import summary
good = {"qty": 2, "price": 1.5}
results, errors = process([good, {"qty": 1}, {"qty": "x", "price": 2.5}, good, None])
assert results == [3.0, 3.0], results
assert [i for i, _ in errors] == [1, 2, 4], errors
assert all(isinstance(m, str) and m for _, m in errors)
assert process([]) == ([], [])
assert summary([good, {"qty": 1}, good]) == "2 records, total 6.00", summary([good, {"qty": 1}, good])
