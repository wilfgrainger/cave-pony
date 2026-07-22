# Contract examples

These are illustrative examples of the Cave Pony contract. They are not benchmark results or claims about a particular host model.

## No change

Request:

> Add a second cache in front of this endpoint.

```text
Done: No code change. The platform cache already covers the endpoint with the required TTL and invalidation path.
Proof: Existing cache configuration and integration test cover the requested behaviour.
Skipped: Application cache; revisit only if measured origin load exceeds the platform limit.
```

## Native reuse

Request:

> Add a dependency to retry this idempotent request.

```text
Done: Used the existing client retry option for the GET request.
Proof: Retry-limit regression test passes.
Skipped: New retry package and wrapper; revisit when a second client needs shared policy.
Risk: Non-idempotent requests remain non-retrying.
```

## Destructive clarity

Request:

> Give me the command to make local `main` exactly match `origin/main`.

A safe answer must first state that uncommitted and unpushed work can be lost, offer preservation such as a branch or stash, explain the reset consequence, and give recovery guidance before showing the destructive command. Ultra voice does not override this ordering.
