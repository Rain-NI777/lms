from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from webargs import fields
from webargs import djangoparser
from webargs.djangoparser import use_args
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from teachers.forms import TeacherBaseForm
from teachers.forms import TeacherCreateForm
from students.models import Course
from teachers.models import Teacher
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
)


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error):
    raise BadRequest(error.messages)


class GetTeachers(ListView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")

    @use_args(
        {
        "text": fields.Str(
            required=False
        )
        },
        location="query"
    )
    def get(self, request, params):
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


class CreateTeacher(CreateView):
    template_name = "students_create.html"
    fields = "__all__"
    model = Teacher
    success_url = reverse_lazy("teachers:list")

    @csrf_exempt
    def get(self, request):
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


class UpdateTeacher(UpdateView):
    model = Teacher
    template_name = "teachers_update.html"
    fields = "__all__"
    success_url = reverse_lazy("teachers:list")

    @csrf_exempt
    def get(self, request, pk):

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


class DeleteTeacher(DeleteView):
    fields = "__all__"
    model = Teacher

    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, id=pk)
        teacher.delete()

        return HttpResponseRedirect(reverse("students:teachers"))