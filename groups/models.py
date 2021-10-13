from django.db import models
from faker import Faker


class Group(models.Model):
    name = models.CharField(max_length=80, null=True)
    number_of_students = models.IntegerField(null=True)                                # Кол-во студентов
    average_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)     # Средний балл


    @classmethod
    def generate_groups(cls, count):
        faker = Faker()
        for _ in range(count):
            gr = cls(
                name=faker.name(),
                number_of_students=faker.random_int(10, 30),
                average_score=faker.random_float(10, 100),
            )
            gr.save()