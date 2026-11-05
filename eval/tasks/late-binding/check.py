import sys, re
reply = open(sys.argv[1]).read().lower()
assert re.search(r"late|when (it'?s|the lambda is) called|at call time|looked up|closes over|closure", reply), "no cause"
assert re.search(r"i\s*=\s*i|partial|default arg", reply), "no fix"
