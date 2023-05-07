from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password(password):
    if len(password) < 6:
        raise ValidationError(
            _('%(password)s is too short'),
            params={'password': password},
        )


