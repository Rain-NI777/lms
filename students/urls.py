from django.urls import path
from students.views import get_students, create_student, update_student

app_name = 'students'

urlpatterns = [
    path('', get_students, name='list'),
    path('new/', create_student, name='create'),
    path('edit/<int:pk>/', update_student, name='update'),
]