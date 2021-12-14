from django.core.exceptions import ValidationError
import datetime
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


def prohibited_domains(email):
    if any([email.endswith(mail) for mail in PROHIBITED]):
        raise ValidationError('Such domain is not accepted. Please use another email domain')


def older_than_18(birthdate):
    eighteen_years_ago = datetime.date.today() - datetime.timedelta(days=YEARS_18_IN_DAYS)  # 6570 days in 18 years
    if birthdate > eighteen_years_ago:
        raise ValidationError('A student cannot be younger than 18')