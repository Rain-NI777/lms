from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from webargs import fields
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from teachers.models import Teacher
from teachers.utils import format_records
from teachers.forms import TeacherCreateForm


parser = djangoparser.DjangoParser()

@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)

@parser.use_args(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "last_name": fields.Str(
            required=False,
        ),
        "classroom_number": fields.Str(
            required=False,
        ),
        "phone_number": fields.Str(
            required=False,
        ),
        "email": fields.Str(
            required=False,
        ),
        "text": fields.Str(required=False),
    },
    location="query",
)
def get_teachers(request, params):

    teachers = Teacher.objects.all().order_by('-id')
    text_fields = ['first_name', 'last_name', 'phone_number', 'email']

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f'{field}__contains': param_value})
                teachers = teachers.filter(or_filter)
            else:
                teachers = teachers.filter(**{param_name: param_value})

    result = format_records(teachers)
    return HttpResponse(result)

@csrf_exempt
def create_teacher(request):

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))

    elif request.method == 'GET':
        form = TeacherCreateForm()
    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)


@csrf_exempt
def update_teacher(request, pk):

    teacher = get_object_or_404(Teacher, id=pk)

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))

    elif request.method == 'GET':
        form = TeacherCreateForm(instance=teacher)

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """

    return HttpResponse(form_html)