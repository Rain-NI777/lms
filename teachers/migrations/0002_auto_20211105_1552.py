# Generated by Django 3.2.7 on 2021-11-05 13:52

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields
import students.validators


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20211105_1552'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classroom_number',
        ),
        migrations.AddField(
            model_name='teacher',
            name='course',
            field=models.ManyToManyField(related_name='teachers', to='students.Course'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=120, null=True, validators=[students.validators.no_elon_validator]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]
