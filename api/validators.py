from rest_framework import serializers
from datetime import date


def validate_alpha_and_title(value, alpha_error, title_error):
    if not value.replace(' ', '').isalpha():
        raise serializers.ValidationError(alpha_error)
    if not value.istitle():
        raise serializers.ValidationError(title_error)
    return value


def validate_future_date(value, error_message):
    if value > date.today():
        raise serializers.ValidationError(error_message)
    return value


def validate_positive(value, error_message):
    if value <= 0:
        raise serializers.ValidationError(error_message)
    return value
