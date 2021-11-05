"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from teachers.views import create_teacher, get_teachers, delete_teacher

from students.views import (
    get_students,
    delete_student,
    test_view,
    search_view,
    CreateStudent, UpdateStudent, LoginStudent
)

app_name = "students"

urlpatterns = [
    path("", get_students, name="list"),
    path("teachers/", get_teachers, name="teachers"),
    path("create/", CreateStudent.as_view(), name="create"),
    path("update/<int:pk>/", UpdateStudent.as_view(), name="update"),
    path("create-teacher/", create_teacher, name="create-teacher"),
    path("delete/<int:pk>/", delete_student, name="delete"),
    #path("delete-teacher/<int:pk>/", delete_teacher, name="delete-teacher"),
    path("test/", test_view, name="test"),
    path("search/", search_view, name="search"),
    path("login/", LoginStudent.as_view(), name="login")
]