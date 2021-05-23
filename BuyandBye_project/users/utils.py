from datetime import date

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def AgeValidator(value):
    """Validates whether the age is above 16"""
    today = date.today()
    age = today.year - value.year
    age_month = today.month - value.month
    age_day = today.day - value.day

    if age < 16:
        raise ValidationError(
            f"You do not meet the age requirement of 16 years. Your age is {age} years, {age_month} month and {age_day} day(s)."
        )
