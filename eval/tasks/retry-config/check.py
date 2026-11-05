import inspect
import client
calls = []
def flaky(fails):
    def get(url):
        calls.append(url)
        if len(calls) <= fails:
            raise ConnectionError
        return "ok"
    return get
assert client.fetch(flaky(2), "u") == "ok"
calls.clear()
try:
    client.fetch(flaky(3), "u"); raise SystemExit("default should be 3 attempts")
except ConnectionError:
    pass
calls.clear()
params = inspect.signature(client.fetch).parameters
name = [p for p in params if p not in ("get", "url")]
assert name, "no retry parameter"
calls.clear()
assert client.fetch(flaky(4), "u", **{name[0]: 5}) == "ok"
