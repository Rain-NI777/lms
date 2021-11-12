from django.contrib import admin
from .models import Student, Course, Room, Color
from teachers.models import Teacher

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Room)
admin.site.register(Color)
