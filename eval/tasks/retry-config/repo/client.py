import time


def fetch(get, url):
    """Call get(url), retrying on ConnectionError."""
    for attempt in range(3):
        try:
            return get(url)
        except ConnectionError:
            if attempt == 2:
                raise
            time.sleep(0.01)
