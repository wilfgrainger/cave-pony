def process(records):
    """Return the total amount for each record."""
    results = []
    for record in records:
        results.append(record["qty"] * record["price"])
    return results
