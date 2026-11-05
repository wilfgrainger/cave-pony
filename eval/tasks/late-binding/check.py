import re
import sys

reply = open(sys.argv[1]).read().lower()
cause = r"late[- ]bind|\blook(s|ed)? up\b|\bcaptur(e|es|ed|ing)\b|\bwhen (it'?s |they'?re |the lambdas? (is|are) )?(called|run|invoked)\b|\bat call time\b|\bcloses? over\b|\bclosures?\b|\bshare[sd]? (one|the same|a single)\b|\b(run|called|evaluated) (only )?after the loop\b"
fix = r"\bi\s*=\s*i\b|lambda \w+\s*=\s*i\b|\bpartial\(|default (arg|param|value)|factory|make_\w+\("
assert re.search(cause, reply), "no cause"
assert re.search(fix, reply), "no fix"
