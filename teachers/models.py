from django.db import models
from faker import Faker
#from students.models import Person
from teachers.validators import no_blacklist_email



class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    phone_number = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=120, null=True, unique=True, validators=[no_blacklist_email])


    def __str__(self):
        return f'{self.full_name()}, phone: {self.phone_number}, email: {self.email}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

@classmethod
def generate_teachers(cls, count):
    faker = Faker()
    for _ in range(count):
        tch = cls(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone_number=faker.phone_number(),
            email=faker.email(),
        )
        tch.save()