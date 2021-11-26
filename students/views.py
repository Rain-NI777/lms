from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from webargs import fields

from students.forms import StudentCreateForm, RegistrationStudentForm
from students.models import *
from students.services.emails import send_registration_email
from students.token_generator import TokenGenerator
from django.core.exceptions import BadRequest
from webargs import djangoparser
from webargs.djangoparser import use_args
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    RedirectView,
)


parser = djangoparser.DjangoParser()


class IndexPage(TemplateView):
    template_name = "index.html"
    extra_context = {'name': 'Igor'}


class StudentSignIn(TemplateView):
    template_name = 'registration/sign_in.html'


class LoginStudent(LoginView):
    success_url = reverse_lazy('login')


class LogoutStudent(LogoutView):
    template_name = 'index.html'


class RegistrationStudent(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationStudentForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(request=self.request,
                                user_instance=self.object)
        return super().form_valid(form)


class ActivateUser(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, uidb64, token, *args, **kwargs):
        print(f"uidb64: {uidb64}")
        print(f"token: {token}")

        try:
            user_pk = force_bytes(urlsafe_base64_decode(uidb64))
            print(f"user_pk: {user_pk}")
            current_user = User.objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)
            return super().get(request, *args, **kwargs)
        return HttpResponse("Wrong data")


@parser.error_handler
def handle_error(error):
    raise BadRequest(error.messages)


class GetStudents(LoginRequiredMixin, ListView):
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


class CreateStudent(LoginRequiredMixin, CreateView):
    template_name = "students_create.html"
    fields = "__all__"
    model = Student
    success_url = reverse_lazy("students:list")

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = StudentCreateForm(request.POST, request.FILES)
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

        form = StudentCreateForm()

        return render(
            request=request,
            template_name='students_create.html',
            context={'create_form': form}
        )


class UpdateStudent(LoginRequiredMixin, UpdateView):
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


class DeleteStudent(LoginRequiredMixin, DeleteView):
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