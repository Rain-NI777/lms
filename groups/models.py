from django.db import models
import uuid
import datetime


class Course(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(null=False, max_length=100)
    start_date = models.DateField(null=True, default=datetime.date.today())
    count_of_students = models.IntegerField(default=0)
    room = models.ForeignKey(
        "groups.Room", null=True, related_name="courses",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    color = models.ForeignKey("groups.Color", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.location}, {self.color}"


class Color(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"