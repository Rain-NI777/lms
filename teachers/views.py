from django.db.models import Q
from webargs import fields
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from teachers.models import Teacher
from teachers.utils import format_records



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