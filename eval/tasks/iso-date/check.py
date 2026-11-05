import datetime
from dates import parse_day
assert parse_day("2026-03-07") == datetime.date(2026, 3, 7)
for bad in ["2026-13-01", "nope", "2026-02-30", ""]:
    try:
        parse_day(bad); raise SystemExit(f"accepted {bad!r}")
    except ValueError:
        pass
