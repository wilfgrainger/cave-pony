class ValidationError(Exception):
    pass


def create_user(payload):
    result = None
    if payload is None:
        raise ValidationError("payload required")
    else:
        email = None
        if "email" in payload:
            email = payload["email"]
        else:
            email = None
        if email is None:
            raise ValidationError("email required")
        else:
            if isinstance(email, str) == True:
                if "@" in email:
                    pass
                else:
                    raise ValidationError("invalid email")
            else:
                raise ValidationError("invalid email")
        age = None
        if "age" in payload:
            age = payload["age"]
        if age is not None:
            if isinstance(age, int) == False or isinstance(age, bool) == True:
                raise ValidationError("invalid age")
            if age < 13:
                raise ValidationError("too young")
            if age > 150:
                raise ValidationError("invalid age")
        name = ""
        if "name" in payload:
            if payload["name"] is not None:
                name = str(payload["name"]).strip()
            else:
                name = ""
        else:
            name = ""
        result = {"email": email.strip().lower(), "age": age, "name": name}
    return result
