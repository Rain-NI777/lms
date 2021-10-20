from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput
from groups.models import Group


class GroupBaseForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'number_of_students', 'average_score']

        widgets = {'phone_number': TextInput(attrs={'pattern': '\d{10,14}'})}

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

   # def clean(self):
       # cleaned_data = super().clean()

      #  name = cleaned_data['first_name']
       # if first_name == last_name:
       #     raise ValidationError('First and last names can\'t be equal')

    #    return cleaned_data


class GroupCreateForm(GroupBaseForm):
    pass


class GroupUpdateForm(GroupBaseForm):
    class Meta(GroupBaseForm.Meta):
        fields = ['name', 'number_of_students', 'average_score']