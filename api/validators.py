from rest_framework import serializers
from datetime import date


def validate_alpha_and_title(value, alpha_error, title_error, allowed_uppercase=[]):
    if not value.replace(' ', '').isalpha():
        raise serializers.ValidationError(alpha_error)

    if not value.istitle() and value.upper() not in allowed_uppercase:
        raise serializers.ValidationError(title_error)

    return value


def validate_future_date(value, error_message):
    if value > date.today():
        raise serializers.ValidationError(error_message)

    return value


def validate_over_eighteen(value, error_message):
    now = date.today()

    if (
        now.year - value.year < 18 or
        (now.year - value.year == 18 and (
                now.month < value.month or
                (now.month == value.month and now.day <= value.day)
        ))
    ):
        raise serializers.ValidationError(error_message)

    return value


def validate_positive(value, error_message):
    if value <= 0:
        raise serializers.ValidationError(error_message)

    return value


def validate_nonnegative(value, error_message):
    if value < 0:
        raise serializers.ValidationError(error_message)

    return value
