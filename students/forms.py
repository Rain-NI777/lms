from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput
from students.models import Student


class StudentBaseForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birthdate', 'email', 'phone_number', 'enroll_date', 'graduate_date']

        widgets = {'phone_number': TextInput(attrs={'pattern': '\d{10,14}'})}

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return self.normalize_name(last_name)


    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        enroll_date = cleaned_data['enroll_date']
        graduate_date = cleaned_data['graduate_date']

        if first_name == last_name:
            errors['first_name'] = ('First and last names can\'t be equal')

        if enroll_date > graduate_date:
            errors['enroll_date'] = ('Graduate date cannot be earlier than the enroll date!')

            raise ValidationError(errors)

        return cleaned_data


class StudentCreateForm(StudentBaseForm):
    pass


class StudentUpdateForm(StudentBaseForm):
    class Meta(StudentBaseForm.Meta):
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthdate']