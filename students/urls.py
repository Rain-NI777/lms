from django.urls import path
from students.views import (
    get_students,
    create_student,
    edit_student,
    update_student,
    delete_student,
    create_teacher,
    test_view,
)

app_name = 'students'

urlpatterns = [
    path('', get_students, name='list'),
    path('create/', create_student, name='create'),
    path('edit/<int:pk>/', edit_student, name='edit'),
    path('update/<int:pk>/', update_student, name='update'),
    path('delete/<int:pk>/', delete_student, name='delete'),
    path('create-teacher/', create_teacher, name='create-teacher'),
    path('test/', test_view, name='test'),
]