def page(items, n, size):
    """Return page n (0-based) of items."""
    start = n * size
    return items[start:start + size + 1]
