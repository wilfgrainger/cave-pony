from users import create_user, ValidationError
assert create_user({"email": " A@B.co ", "age": 20, "name": " Al "}) == {"email": "a@b.co", "age": 20, "name": "Al"}
assert create_user({"email": "x@y"}) == {"email": "x@y", "age": None, "name": ""}
assert create_user({"email": "x@y", "name": None})["name"] == ""
for bad in [None, {}, {"email": None}, {"email": 5}, {"email": "nope"}, {"email": "a@b", "age": 12},
            {"email": "a@b", "age": 151}, {"email": "a@b", "age": "20"}, {"email": "a@b", "age": True}, {"email": "a@b", "age": 1.5}]:
    try:
        create_user(bad); raise SystemExit(f"accepted {bad!r}")
    except ValidationError:
        pass
