from django.core.exceptions import ValidationError
import re


def validate_email(email, account):
    email_regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    if not re.match(email_regex, email):
        raise ValidationError("Wrong email")

    if account.objects.get(email=email):
        raise ValidationError("Email already exist")


def validate_username(username, account):
    if account.objects.get(username=username):
        raise ValidationError("Username already exist")

    name_regex = r'[a-zA-Z0-9]+(\s[a-zA-Z0-9]+)*$'

    if not re.match(name_regex, username):
        raise ValidationError("Wrong username")


def validate_firstname(name):
    name_regex = r'[a-zA-Z0-9]+(\s[a-zA-Z0-9]+)*$'

    if not re.match(name_regex, name):
        raise ValidationError("Wrong name")


def validate_postcode(postcode):
    regex = r'^[0-9]{2}-[0-9]{3}$'

    if not re.match(regex, postcode):
        raise ValidationError("Wrong name")


def validate_password(password, repeated_password):
    pass
