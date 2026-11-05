def parse_row(line):
    """Split one CSV line into fields."""
    return [field.strip() for field in line.split(",")]
