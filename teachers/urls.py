from django.urls import path
from teachers.views import (
    GetTeachers,
    CreateTeacher,
    UpdateTeacher,
    DeleteTeacher,
)

app_name = 'teachers'

urlpatterns = [
    path('', GetTeachers.as_view(), name='list'),
    path('new/', CreateTeacher.as_view(), name='create'),
    path('update/<int:pk>/', UpdateTeacher.as_view(), name='update'),
    path("delete/<int:pk>/", DeleteTeacher.as_view(), name="delete")
]