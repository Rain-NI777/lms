from django.db import models
from faker import Faker

fake = Faker()

class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    subject_name = models.CharField(max_length=80, null=False)                    # Название предмета
    cabinet_number = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=120, null=True)

