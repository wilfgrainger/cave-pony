import re
import sys

reply = open(sys.argv[1]).read().lower()
cause = r"late[- ]bind|\bwhen (it'?s|the lambdas? (is|are)) called\b|\bat call time\b|\bcloses? over\b|\bclosures?\b|looked up (when|at)"
fix = r"\bi\s*=\s*i\b|lambda \w+\s*=\s*i\b|\bpartial\(|default (arg|param|value)|factory|make_\w+\("
assert re.search(cause, reply), "no cause"
assert re.search(fix, reply), "no fix"
