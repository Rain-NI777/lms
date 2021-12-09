from django.core.exceptions import ValidationError


def no_blacklist_email(email):
    if 'xyz.com' in email.lower():
        raise ValidationError('Email is blacklisted!')