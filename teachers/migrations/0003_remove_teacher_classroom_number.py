# Generated by Django 3.2.7 on 2021-10-12 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_rename_cabinet_number_teacher_classroom_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classroom_number',
        ),
    ]
