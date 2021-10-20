from django.core.exceptions import ValidationError
from datetime import date


def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - \
          ((today.month, today.day) <
          (birthDate.month, birthDate.day))
    return age

def no_elon_validator(email):
    if 'elon' in email.lower():
        raise ValidationError('No more Elons, please!')


def no_blacklist_email(email):
    if 'xyz.com' in email.lower():
        raise ValidationError('Email is blacklisted!')

def age_valid(birthdate):
    if calculateAge(birthdate) < 18:
        raise ValidationError('Too young!')