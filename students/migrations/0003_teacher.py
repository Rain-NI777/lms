# Generated by Django 3.2.7 on 2021-11-05 14:48

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields
import students.validators


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20211105_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(max_length=120, null=True, validators=[students.validators.no_elon_validator])),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('course', models.ManyToManyField(related_name='teachers', to='students.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
