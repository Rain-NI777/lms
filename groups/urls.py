from django.urls import path
from groups.views import (
    GetGroups,
    CreateGroup,
    UpdateGroup,
)

app_name = 'groups'

urlpatterns = [
    path('', GetGroups.as_view(), name='list'),
    path('new/', CreateGroup.as_view(), name='create'),
    path('edit/<int:pk>/', UpdateGroup.as_view(), name='update'),
]