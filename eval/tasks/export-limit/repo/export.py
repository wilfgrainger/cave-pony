def export(items):
    """Return export lines followed by a summary line."""
    lines = [f"{i['id']},{i['name']}" for i in items]
    lines.append(f"# exported {len(lines)}")
    return lines
