from datetime import datetime


def audit_time(entry):
    return datetime.strptime(entry["at"], "%Y-%m-%dT%H:%M:%S%z")
