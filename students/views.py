from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from students.forms import StudentCreateForm
from teachers.forms import TeacherCreateForm
from students.models import *
from students.utils import format_records
from django.core.exceptions import BadRequest, ValidationError
from webargs import djangoparser
from webargs.djangoparser import use_args
from django.contrib.auth.models import User

from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
)


class IndexPage(TemplateView):
    template_name = "index.html"
    extra_context = {'name': 'Igor'}


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


class GetStudents(ListView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")

    @use_args(
        {
            "first_name": fields.Str(required=False),
            "text": fields.Str(required=False),
            "course": fields.Str(required=False),
        },
        location="query",
    )
    def get(self, request, params, *args, **kwargs):
        students = Student.objects.all().order_by("id")
        courses = Course.objects.all()

        text_fields = ["first_name", "last_name", "email"]

        for param_name, param_value in params.items():
            if param_value:
                if param_name == "text":
                    or_filter = Q()
                    for field in text_fields:
                        or_filter |= Q(**{f"{field}__contains": param_value})
                    students = students.filter(or_filter)
                elif param_name == 'course':
                    students = students.filter(course__id__contains=params['course'])
                else:
                    students = students.filter(**{param_name: param_value})


        return render(
            request=request,
            template_name="students_table.html",
            context={"students_list": students,
                    "courses_list": courses}
        )

class CreateStudent(CreateView):
    template_name = "students_create.html"
    fields = "__all__"
    model = Student
    success_url = reverse_lazy("students:list")

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = StudentCreateForm(request.POST, request.FILES)
            #if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

        form = StudentCreateForm()

        return render(
            request=request,
            template_name='students_create.html',
            context={'create_form': form}
        )


class UpdateStudent(UpdateView):
    model = Student
    template_name = "students_update.html"
    fields = "__all__"
    success_url = reverse_lazy("students:list")

    @csrf_exempt
    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)

        if request.method == "POST":
            form = StudentCreateForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("students:list"))

        elif request.method == "GET":
            form = StudentCreateForm(instance=student)

        return render(
            request=request,
            template_name='students_update.html',
            context={'update_form': form}
        )


class DeleteStudent(DeleteView):
    fields = "__all__"
    model = Student

    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        student.delete()

        return HttpResponseRedirect(reverse("students:list"))


def test_view(request):
    data_to_save = []
    course = Course.objects.get(id="482fdb3c-3a7f-4750-913a-65a8b091a7ab")

    for i in range(1000):
        new_student = Student()
        new_student.first_name = "12"
        new_student.last_name = "12"
        new_student.email = "test"
        new_student.course = course
        data_to_save.append(new_student)

    Student.objects.bulk_create(data_to_save)

    student = Student.objects.filter(course__room__color__name__contains="red")

    return HttpResponse(student)


def search_view(request):
    search_text = request.GET.get('search')
    text_fields = ["first_name", "last_name", "email"]
    request.session["last_search_text"] = search_text
    print(request.GET)

    if search_text:
        or_filter = Q()
        for field in text_fields:
            or_filter |= Q(**{f"{field}__icontains": search_text})
        students = Student.objects.filter(or_filter)
    else:
        students = Student.objects.all().order_by("id")

    return render(
        request=request,
        template_name="students_table.html",
        context={"students_list": students},
    )

class LoginStudent(LoginView):
    pass