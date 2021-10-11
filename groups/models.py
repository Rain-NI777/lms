#

from django.db import models

class Group(models.Model):
    group_name = models.CharField(max_length=80, null=True)
    number_of_students = models.CharField(max_length=80, null=True)        # Кол-во студентов
    average_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)     # Средний балл
