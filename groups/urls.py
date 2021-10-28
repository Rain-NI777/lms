from django.urls import path
from groups.views import get_groups, create_group, update_group

app_name = 'groups'

urlpatterns = [
    path('', get_groups, name='list'),
    path('new/', create_group, name='create'),
    path('edit/<int:pk>/', update_group, name='update'),
]