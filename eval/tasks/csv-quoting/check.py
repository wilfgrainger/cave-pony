from rows import parse_row
assert parse_row('a,"b,c",d') == ["a", "b,c", "d"]
assert parse_row('x,"say ""hi""",z') == ["x", 'say "hi"', "z"]
assert parse_row("a,,c") == ["a", "", "c"]
assert parse_row('"",1') == ["", "1"]
assert parse_row("plain,row") == ["plain", "row"]
