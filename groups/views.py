from django.shortcuts import render
from django.http import HttpResponse
from groups.models import Group

def get_groups(request):
    return HttpResponse(Group)

