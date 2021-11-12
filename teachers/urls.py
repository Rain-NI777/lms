from django.urls import path
from teachers.views import get_teachers, create_teacher, update_teacher

app_name = 'teachers'

urlpatterns = [
    path('', get_teachers, name='list'),
    path('new/', create_teacher, name='create'),
    path('edit/<int:pk>/', update_teacher, name='update'),
]