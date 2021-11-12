# Generated by Django 3.2.7 on 2021-11-12 12:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20211112_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invite',
            name='id',
            field=models.UUIDField(default=uuid.UUID('03a0de07-8e8f-416f-9d16-d81a007cd9f3'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
