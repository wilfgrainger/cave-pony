from datetime import datetime


def event_time(event):
    return datetime.strptime(event["ts"], "%Y-%m-%dT%H:%M:%S%z")
