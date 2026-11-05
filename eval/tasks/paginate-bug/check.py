from utils import page
from api import list_orders
from cli import show
xs = list(range(23))
assert page(xs, 0, 10) == list(range(10))
assert page(xs, 2, 10) == [20, 21, 22]
assert list_orders(xs, 1)["items"] == list(range(10, 20))
lines = [str(i) for i in range(12)]
assert show(lines, 0) == "0\n1\n2\n3\n4", show(lines, 0)
assert show(lines, 2) == "10\n11", show(lines, 2)
