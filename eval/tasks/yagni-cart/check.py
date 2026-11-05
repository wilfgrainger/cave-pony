from cart import total
assert total([1.005, 2.10, 3]) in (6.1, 6.11)
assert total([]) == 0
assert total([0.1, 0.2]) == 0.3
