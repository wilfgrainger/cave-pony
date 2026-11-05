from process import process
from report import summary
good = {"qty": 2, "price": 1.5}
results, errors = process([good, {"qty": 1}, {"qty": "x", "price": 2.5}, good, None])
assert results == [3.0, 3.0], results
assert [i for i, _ in errors] == [1, 2, 4], errors
assert all(isinstance(m, str) and m for _, m in errors)
assert process([]) == ([], [])
# The caller must survive the new return shape; extra detail such as a skipped count is fine.
line = summary([good, {"qty": 1}, good])
assert line.startswith("2 records, total 6.00"), line
