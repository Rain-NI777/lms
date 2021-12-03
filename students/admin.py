from django.utils.html import format_html
from django.contrib import admin
from students.models import Student, UserProfile, \
    CustomUser
from teachers.models import Teacher
from groups.models import Course, Color, Room


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'age', 'birthdate']
    search_fields = ['first_name__startswith', 'last_name__icontains']
    list_filter = ['first_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_of_students']
    ordering = ['count_of_students']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email',
                    'course_count', 'list_courses']
    fieldsets = (
        ("Personal info", {
            'fields': ('first_name', 'last_name',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('email', 'phone_number'),
        }),
    )


    def list_courses(self, obj):
        if obj.course:
            courses = obj.course.all()
            links = [
                f"<a href='http://127.0.0.1:8000/admin/students/course/{course.pk}/change/'>{course.name}</p>"
                for course in courses]

            return format_html(f"{''.join(links)}")
        else:
            return format_html("Empty courses")

    def course_count(self, obj):
        if obj.course:
            courses = obj.course.all().count()
            return format_html(f"<p>{courses}</p>")
        else:
            return format_html(f"<p>0</p>")


admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Color)
admin.site.register(CustomUser)