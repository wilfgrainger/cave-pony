from listutil import unique
assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]
assert unique([]) == []
assert unique(["a", "b", "a"]) == ["a", "b"]
