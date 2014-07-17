from django.core.exceptions import ValidationError

def validate_not_zero(value):
    if value <= 0:
        msg = u"This value cannot be less than 1"
        raise ValidationError(msg)

