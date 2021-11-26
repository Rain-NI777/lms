from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from groups.forms import GroupCreateForm
from groups.models import *
from groups.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser
from webargs.djangoparser import use_args
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
)


parser = djangoparser.DjangoParser()


class GetGroups(LoginRequiredMixin, ListView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")

    @use_args(
        {
            "name": fields.Str(
                required=False,
            ),
            "number_of_students": fields.Str(
                required=False,
            ),
            "average_score": fields.Float(
                required=False,
            ),
            "text": fields.Str(required=False),
        },
        location="query",
    )
    def get(self, request, params):
        groups = Group.objects.all().order_by('-id')
        text_fields = ['name', 'number_of_students', 'average_score']

        for param_name, param_value in params.items():
            if param_value:
                if param_name == 'text':
                    or_filter = Q()
                    for field in text_fields:
                        or_filter |= Q(**{f'{field}__contains': param_value})
                    groups = groups.filter(or_filter)
                else:
                    groups = groups.filter(**{param_name: param_value})

        result = format_records(groups)
        return HttpResponse(result)


class CreateGroup(LoginRequiredMixin, CreateView):
    template_name = "students_create.html"
    fields = "__all__"
    model = Group
    success_url = reverse_lazy("students:list")

    @csrf_exempt
    def get(self, request):

        if request.method == 'POST':
            form = GroupCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('groups:list'))

        elif request.method == 'GET':
            form = GroupCreateForm()

        form_html = f"""
        <form method="POST">
        {form.as_p()}
        <input type="submit" value="Create">
        </form>
        """

        return HttpResponse(form_html)


class UpdateGroup(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = "students_update.html"
    fields = "__all__"
    success_url = reverse_lazy("students:list")

    @csrf_exempt
    def get(self, request, pk):

        group = get_object_or_404(Group, id=pk)

        if request.method == 'POST':
            form = GroupCreateForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('groups:list'))

        elif request.method == 'GET':
            form = GroupCreateForm(instance=group)

        form_html = f"""
        <form method="POST">
        {form.as_p()}
        <input type="submit" value="Save">
        </form>
        """

        return HttpResponse(form_html)