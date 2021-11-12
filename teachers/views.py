from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from webargs import fields
from webargs import djangoparser
from webargs.djangoparser import use_args, use_kwargs
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from teachers.forms import TeacherBaseForm
from teachers.forms import TeacherCreateForm
from students.models import Course
from teachers.models import Teacher


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error):
    raise BadRequest(error.messages)

@use_args(
    {
    "text": fields.Str(
        required=False
    )
    },
    location="query"
)
def get_teachers(request, params):
    teachers = Teacher.objects.all().order_by('id')
    courses = Course.objects.all()
    text_fields = ['first_name', 'last_name', 'phone_number', 'email']

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f'{field}__contains': param_value})
                teachers = teachers.filter(or_filter)
            elif param_name == 'course':
                teachers = teachers.filter(course__id__contains=params['course'])
            else:
                teachers = teachers.filter(**{param_name: param_value})

    return render(
        request=request,
        template_name="teachers_table.html",
        context={"teachers_list": teachers,
                 "courses_list": courses}
    )


@csrf_exempt
def create_teacher(request):
    if request.method == "POST":
        form = TeacherBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:teachers"))

    elif request.method == "GET":
        form = TeacherBaseForm()

    return render(
        request=request, template_name="teachers_create.html",
        context={"form": form}
    )

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


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    teacher.delete()

    return HttpResponseRedirect(reverse("students:teachers"))