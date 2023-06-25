from django.core.exceptions import ValidationError
import re


def validate_email(email):
    email_regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    if not re.match(email_regex, email):
        raise ValidationError("Wrong email")


def validate_username(username):
    name_regex = r'[a-zA-Z0-9]+(\s[a-zA-Z0-9]+)*$'

    if not re.match(name_regex, username):
        raise ValidationError("Wrong username")


def validate_name(name):
    name_regex = r'[a-zA-Z0-9]+(\s[a-zA-Z0-9]+)*$'

    if not re.match(name_regex, name):
        raise ValidationError(f"Wrong {name}")


def validate_postcode(postcode):
    regex = r'^[0-9]{2}-[0-9]{3}$'

    if not re.match(regex, postcode):
        raise ValidationError("Wrong postcode")


def validate_password(password):
    regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    return re.match(regex, password)


