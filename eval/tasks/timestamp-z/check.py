from datetime import datetime, timedelta, timezone
from events import event_time
from audit import audit_time
utc = timezone.utc
for f, key in ((event_time, "ts"), (audit_time, "at")):
    assert f({key: "2026-01-05T10:00:00.250Z"}) == datetime(2026, 1, 5, 10, 0, 0, 250000, tzinfo=utc), f.__name__
    assert f({key: "2026-01-05T10:00:00Z"}) == datetime(2026, 1, 5, 10, tzinfo=utc), f.__name__
    assert f({key: "2026-01-05T11:00:00+01:00"}) == datetime(2026, 1, 5, 10, tzinfo=utc), f.__name__
    assert f({key: "2026-01-05T11:00:00+01:00"}).utcoffset() == timedelta(hours=1)
