from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput
from groups.models import *


class GroupBaseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'start_date', 'count_of_students', 'room']

        widgets = {'phone_number': TextInput(attrs={'pattern': '\d{10,14}'})}

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()


class GroupCreateForm(GroupBaseForm):
    pass


class GroupUpdateForm(GroupBaseForm):
    class Meta(GroupBaseForm.Meta):
        fields = ['name', 'start_date', 'count_of_students', 'room']